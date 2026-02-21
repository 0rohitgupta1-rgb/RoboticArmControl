import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time

class GuptaArmController:
    def __init__(self, root):
        self.root = root
        self.root.title("Gupta's Precision Controller - 50° Gripper Mode")
        self.root.geometry("550x900")
        self.root.configure(bg="#1e272e")
        self.ser = None
        
        # Track positions locally
        self.angles = {"A1": 90, "A2": 90, "WA": 90, "GR": 0}

        # --- Connection ---
        conn_frame = tk.Frame(root, bg="#485460", pady=10)
        conn_frame.pack(fill="x")
        self.port_list = ttk.Combobox(conn_frame, values=self.find_ports(), state="readonly")
        self.port_list.set("Select Port")
        self.port_list.pack(side="left", padx=10)
        tk.Button(conn_frame, text="Connect", bg="#05c46b", fg="white", command=self.connect).pack(side="left")

        # --- Precision Controls Section ---
        prec_frame = tk.LabelFrame(root, text="Precision Controls", bg="#d2dae2", padx=15, pady=15)
        prec_frame.pack(padx=20, pady=10, fill="x")

        # Configuration for each joint
        # Format: (DisplayName, InternalKey, ArduinoCode, StepSize)
        joints = [
            ("Arm A1", "A1", "1", 10),
            ("Arm A2", "A2", "2", 10),
            ("Wrist A", "WA", "W", 10),
            ("Gripper", "GR", "G", 50)  # Changed Gripper step to 50
        ]

        self.label_vars = {}
        for i, (name, key, code, step_val) in enumerate(joints):
            tk.Label(prec_frame, text=f"{name} ({step_val}°):", bg="#d2dae2").grid(row=i, column=0, sticky="w")
            
            # Angle Display
            self.label_vars[key] = tk.StringVar(value=f"{self.angles[key]}°")
            tk.Label(prec_frame, textvariable=self.label_vars[key], bg="#d2dae2", font=("Arial", 10, "bold"), width=6).grid(row=i, column=1, padx=10)

            # Up/Open Button
            tk.Button(prec_frame, text=f"+{step_val}°", width=10, bg="#3c40c6", fg="white",
                      command=lambda k=key, c=code, s=step_val: self.step_motor(k, c, s)).grid(row=i, column=2, padx=5, pady=5)
            
            # Down/Close Button
            tk.Button(prec_frame, text=f"-{step_val}°", width=10, bg="#5758bb", fg="white",
                      command=lambda k=key, c=code, s=step_val: self.step_motor(k, c, -s)).grid(row=i, column=3, padx=5, pady=5)

        # --- Continuous Controls ---
        grid_frame = tk.LabelFrame(root, text="Continuous Rotation (360°)", bg="#d2dae2", padx=15, pady=15)
        grid_frame.pack(padx=20, pady=10, fill="both", expand=True)

        cont_controls = [
            ("Root Left", "R0"), ("Root Right", "R180"),
            ("Arm B Forward", "B0"), ("Arm B Back", "B180"),
            ("Wrist B CW", "V0"), ("Wrist B CCW", "V180")
        ]

        for i, (txt, cmd) in enumerate(cont_controls):
            btn = tk.Button(grid_frame, text=txt, width=15, height=2, command=lambda c=cmd: self.send(c))
            btn.grid(row=i//2, column=i%2, padx=25, pady=5)

        tk.Button(root, text="🏠 RESET ALL TO HOME", bg="#ff3f34", fg="white", font=("Arial", 10, "bold"),
                  height=2, command=self.reset_home).pack(fill="x", padx=40, pady=20)

    def find_ports(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def connect(self):
        try:
            self.ser = serial.Serial(self.port_list.get(), 9600, timeout=1)
            time.sleep(2)
            self.reset_home()
            messagebox.showinfo("Success", "Precision System Active")
        except:
            messagebox.showerror("Error", "Check Connection")

    def step_motor(self, key, code, step):
        new_angle = self.angles[key] + step
        # Constraint: Keep within 0-180
        if 0 <= new_angle <= 180:
            self.angles[key] = new_angle
            self.label_vars[key].set(f"{new_angle}°")
            self.send(f"{code}{new_angle}")
        else:
            messagebox.showwarning("Limit Reached", f"Motor cannot move beyond {new_angle}°")

    def reset_home(self):
        self.angles = {"A1": 90, "A2": 90, "WA": 90, "GR": 0}
        for key in self.label_vars:
            self.label_vars[key].set(f"{self.angles[key]}°")
        self.send("H1")

    def send(self, val):
        if self.ser and self.ser.is_open:
            self.ser.write((val + "\n").encode())

if __name__ == "__main__":
    root = tk.Tk()
    app = GuptaArmController(root)
    root.mainloop()
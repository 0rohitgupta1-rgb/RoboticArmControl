# Robotic Arm Control

A Python-based GUI controller for a precision robotic arm using Tkinter and serial communication.

## Features

- **Precision Controls**: Step-by-step angle control for:
  - Arm A1 (±10°)
  - Arm A2 (±10°)
  - Wrist Angle (±10°)
  - Gripper (±50°)

- **Continuous Rotation**: 360° control modes for:
  - Root (Left/Right)
  - Arm B (Forward/Back)
  - Wrist B (Clockwise/Counter-clockwise)

- **Home Reset**: Quick reset all joints to home position

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- pyserial

## Installation

```bash
pip install pyserial
```

## Usage

1. Connect your robotic arm via serial port
2. Run the application:
```bash
python main.py
```
3. Select the appropriate COM port and click "Connect"
4. Use the GUI buttons to control the arm

## Communication Protocol

The application sends single-character commands to the Arduino:
- `1`, `2`, `W`, `G`: Position-based commands with angle
- `R0`, `R180`: Root rotation
- `B0`, `B180`: Arm B movement
- `V0`, `V180`: Wrist B rotation
- `H1`: Home reset

## Author

Gupta's Precision Controller System

## License

MIT

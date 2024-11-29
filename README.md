# Luxafor Mini Controller

A simple tray application to control the Luxafor Flag USB LED light.

## Features
- System tray icon that matches current light color
- Quick color cycling (Green -> Yellow -> Red -> Off)
- Configurable hotkey (default: Ctrl + `)
- Color state persistence across restarts
- Left-click to cycle colors
- Right-click menu for direct color selection

## Setup
1. Install Python 3.8 or higher
2. Install requirements: `pip install -r requirements.txt`
3. To run the application: `run.bat`
4. To build an executable: `build.bat`

## Auto-start
Place a shortcut to the executable in:
`C:\Users\[YourUsername]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
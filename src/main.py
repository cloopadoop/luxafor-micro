import sys
from gui import LuxaforGUI
from tray import create_tray_icon
import threading

def main():
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Handle color command
        controller = LuxaforControl()
        if sys.argv[1] == "off":
            controller.turn_off()
        else:
            try:
                r, g, b = map(int, sys.argv[1].split(','))
                controller.set_color(r, g, b)
            except:
                print("Invalid color format. Use: r,g,b")
        sys.exit(0)

    # Start main application
    gui = LuxaforGUI()
    icon = create_tray_icon(gui)
    
    # Run tray icon in separate thread
    threading.Thread(target=icon.run, daemon=True).start()
    
    # Run main GUI
    gui.run()

if __name__ == "__main__":
    main()

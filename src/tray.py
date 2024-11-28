import pystray
from PIL import Image
import sys
from luxafor_control import LuxaforControl
from gui import LuxaforGUI
import threading

def create_tray_icon(gui):
    def show_window():
        gui.root.deiconify()

    def quit_app():
        gui.controller.turn_off()
        gui.root.quit()
        icon.stop()

    menu = pystray.Menu(
        pystray.MenuItem("Show", show_window),
        pystray.MenuItem("Turn Off", gui.controller.turn_off),
        pystray.MenuItem("Quit", quit_app)
    )

    image = Image.new('RGB', (64, 64), color = 'red')
    icon = pystray.Icon("Luxafor Control", image, "Luxafor Control", menu)
    return icon

import pystray
from PIL import Image
import keyboard
from luxafor_control import LuxaforControl
import json
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog

class LuxaforTray:
    def __init__(self):
        self.controller = LuxaforControl()
        self.config_file = Path("config.json")
        config = self.load_config()
        self.hotkey = config.get('hotkey', 'ctrl+`')
        
        # Restore last color state
        last_color = config.get('last_color')
        if last_color:
            self.controller.set_color(*last_color)
            
        self.setup_hotkey()
        self.create_tray_icon()
        self.update_icon_color()  # Update icon to match initial light state

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return {'hotkey': 'ctrl+`'}

    def save_config(self):
        config = {
            'hotkey': self.hotkey,
            'last_color': self.controller.current_color
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def setup_hotkey(self):
        try:
            keyboard.remove_hotkey(self.hotkey)
        except:
            pass
        keyboard.add_hotkey(self.hotkey, self.cycle_color)

    def cycle_color(self):
        if not self.controller.current_color or self.controller.current_color == [0, 0, 0]:
            self.controller.set_color(0, 255, 0)  # Green
        elif self.controller.current_color == [0, 255, 0]:
            self.controller.set_color(255, 255, 0)  # Yellow
        elif self.controller.current_color == [255, 255, 0]:
            self.controller.set_color(255, 0, 0)  # Red
        else:
            self.controller.turn_off()
        self.update_icon_color()
        self.save_config()

    def update_icon_color(self):
        color = (0, 0, 0) if not self.controller.current_color else tuple(self.controller.current_color)
        image = Image.new('RGB', (64, 64), color=color)
        self.icon.icon = image

    def change_hotkey(self):
        root = tk.Tk()
        root.withdraw()
        new_hotkey = simpledialog.askstring("Set Hotkey", 
                                          f"Current hotkey: {self.hotkey}\nEnter new hotkey:", 
                                          initialvalue=self.hotkey)
        if new_hotkey:
            self.hotkey = new_hotkey
            self.save_config()
            self.setup_hotkey()

    def create_menu(self):
        return pystray.Menu(
            pystray.MenuItem("Cycle Light", self.cycle_color, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Green", lambda: self.set_color_and_update(0, 255, 0)),
            pystray.MenuItem("Yellow", lambda: self.set_color_and_update(255, 255, 0)),
            pystray.MenuItem("Red", lambda: self.set_color_and_update(255, 0, 0)),
            pystray.MenuItem("Off", self.turn_off_and_update),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Set Hotkey", self.change_hotkey),
            pystray.MenuItem("Quit", self.quit_app)
        )

    def set_color_and_update(self, r, g, b):
        self.controller.set_color(r, g, b)
        self.update_icon_color()
        self.save_config()

    def turn_off_and_update(self):
        self.controller.turn_off()
        self.update_icon_color()
        self.save_config()

    def quit_app(self):
        self.save_config()
        self.controller.turn_off()
        self.icon.stop()

    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), color='black')
        self.icon = pystray.Icon("Luxafor Micro", image, "Luxafor Micro", self.create_menu())

    def run(self):
        self.icon.run()

if __name__ == "__main__":
    app = LuxaforTray()
    app.run()

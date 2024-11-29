import json
import hid
import time
import threading
from pathlib import Path

class LuxaforControl:
    def __init__(self):
        self.VENDOR_ID = 0x04d8
        self.PRODUCT_ID = 0xf372
        self.device = None
        self.config_file = Path("config.json")
        self.default_colors = {
            "Red": [255, 0, 0],
            "Green": [0, 255, 0],
            "Blue": [0, 0, 255],
            "Yellow": [255, 255, 0],
            "Purple": [255, 0, 255],
            "White": [255, 255, 255]
        }
        self.saved_colors = self.load_config()
        self.current_color = None
        self.party_mode_active = False
        self.connect_device()

    def connect_device(self):
        try:
            self.device = hid.device()
            self.device.open(self.VENDOR_ID, self.PRODUCT_ID)
            return True
        except Exception:
            return False

    def write_command(self, command):
        if not self.device and not self.connect_device():
            return False
        try:
            self.device.write(command)
            return True
        except Exception:
            return False

    def set_color(self, r, g, b, led=255):
        return self.write_command([0x00, 0x01, led, r, g, b, 0x00, 0x00, 0x00])

    def fade_color(self, r, g, b, duration=20, led=255):
        return self.write_command([0x00, 0x02, led, r, g, b, duration, 0x00, 0x00])

    def strobe_effect(self, r=255, g=0, b=0, speed=20, repeat=5, led=255):
        return self.write_command([0x00, 0x03, led, r, g, b, speed, repeat, 0x00])

    def wave_effect(self, wave_type=4, r=0, g=0, b=255, repeat=3, speed=20):
        return self.write_command([0x00, 0x04, wave_type, r, g, b, 0x00, repeat, speed])

    def pattern_effect(self, pattern=1, repeat=3):
        return self.write_command([0x00, 0x06, pattern, repeat, 0x00, 0x00, 0x00, 0x00, 0x00])

    def turn_off(self):
        return self.set_color(0, 0, 0)

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return self.default_colors.copy()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.saved_colors, f)

    def reset_to_defaults(self):
        self.saved_colors = self.default_colors.copy()
        self.save_config()

    def start_party_mode(self):
        import random
        while self.party_mode_active:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.fade_color(r, g, b, duration=10)
            time.sleep(0.5)

    def toggle_party_mode(self):
        self.party_mode_active = not self.party_mode_active
        if self.party_mode_active:
            threading.Thread(target=self.start_party_mode, daemon=True).start()

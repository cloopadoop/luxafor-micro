import json
import sys
import hid
import pystray
from PIL import Image
import keyboard
import customtkinter as ctk
import threading
import sounddevice as sd
import numpy as np
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

    def set_color(self, r, g, b):
        if not self.device:
            if not self.connect_device():
                return False
        try:
            self.device.write([0x00, 0x01, r, g, b, 0x00, 0x00, 0x00])
            self.current_color = [r, g, b]
            return True
        except Exception:
            return False

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

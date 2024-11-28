import customtkinter as ctk
import keyboard
from luxafor_control import LuxaforControl
import threading

class LuxaforGUI:
    def __init__(self):
        self.controller = LuxaforControl()
        self.root = ctk.CTk()
        self.root.title("Luxafor Control")
        self.root.geometry("400x600")
        
        # Create color buttons
        self.color_frame = ctk.CTkFrame(self.root)
        self.color_frame.pack(pady=10, padx=10, fill="x")
        
        row = 0
        col = 0
        for color_name, rgb in self.controller.saved_colors.items():
            btn = ctk.CTkButton(
                self.color_frame,
                text=color_name,
                command=lambda c=rgb: self.controller.set_color(*c),
                fg_color=f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Add color picker
        self.add_color_frame = ctk.CTkFrame(self.root)
        self.add_color_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkButton(
            self.add_color_frame,
            text="Add New Color",
            command=self.show_color_picker
        ).pack(pady=5)

        # Party mode toggle
        self.party_btn = ctk.CTkButton(
            self.root,
            text="Start Party Mode",
            command=self.toggle_party_mode
        )
        self.party_btn.pack(pady=10)

        # Register global hotkeys
        self.setup_hotkeys()

    def setup_hotkeys(self):
        keyboard.add_hotkey('ctrl+alt+r', lambda: self.controller.set_color(255, 0, 0))
        keyboard.add_hotkey('ctrl+alt+g', lambda: self.controller.set_color(0, 255, 0))
        keyboard.add_hotkey('ctrl+alt+o', self.controller.turn_off)

    def show_color_picker(self):
        color_picker = ctk.CTkInputDialog(
            text="Enter color name and RGB values (name,r,g,b):",
            title="Add Color"
        )
        result = color_picker.get_input()
        if result:
            try:
                name, r, g, b = result.split(',')
                rgb = [int(r), int(g), int(b)]
                self.controller.saved_colors[name] = rgb
                self.controller.save_config()
                self.refresh_gui()
            except:
                pass

    def toggle_party_mode(self):
        self.controller.party_mode_active = not self.controller.party_mode_active
        if self.controller.party_mode_active:
            self.party_btn.configure(text="Stop Party Mode")
            threading.Thread(target=self.party_mode, daemon=True).start()
        else:
            self.party_btn.configure(text="Start Party Mode")

    def party_mode(self):
        import time
        import random
        while self.controller.party_mode_active:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.controller.set_color(r, g, b)
            time.sleep(0.5)

    def run(self):
        self.root.mainloop()

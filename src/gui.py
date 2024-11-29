import customtkinter as ctk
from luxafor_control import LuxaforControl
from CTkColorPicker import *

class LuxaforGUI:
    def __init__(self):
        self.controller = LuxaforControl()
        self.root = ctk.CTk()
        self.root.title("Luxafor Control")
        self.root.geometry("500x400")
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Menu bar
        self.menu_frame = ctk.CTkFrame(self.main_frame)
        self.menu_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            self.menu_frame,
            text="Reset to Defaults",
            width=120,
            command=self.reset_colors
        ).pack(side="right", padx=5)
        
        # Colors container
        self.colors_frame = ctk.CTkFrame(self.main_frame)
        self.colors_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_color_grid()
        
        # Effects frame
        self.effects_frame = ctk.CTkFrame(self.main_frame)
        self.effects_frame.pack(fill="x", padx=10, pady=10)
        
        self.create_effects_controls()

    def create_color_grid(self):
        # Clear existing widgets
        for widget in self.colors_frame.winfo_children():
            widget.destroy()
            
        # Add "Off" button first
        off_btn = ctk.CTkButton(
            self.colors_frame,
            text="OFF",
            width=60,
            height=60,
            fg_color="#333333",
            hover_color="#444444",
            command=self.controller.turn_off
        )
        off_btn.grid(row=0, column=0, padx=5, pady=5)
        
        row = 0
        col = 1
        for color_name, rgb in self.controller.saved_colors.items():
            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            
            # Container for color button and controls
            container = ctk.CTkFrame(self.colors_frame, fg_color="transparent")
            container.grid(row=row, column=col, padx=5, pady=5)
            
            # Color button
            btn = ctk.CTkButton(
                container,
                text="",
                width=60,
                height=60,
                fg_color=hex_color,
                hover_color=hex_color,
                command=lambda c=rgb: self.controller.set_color(*c)
            )
            btn.pack(side="left")
            
            # Controls container
            controls = ctk.CTkFrame(container, fg_color="transparent")
            controls.pack(side="left", padx=2)
            
            # Edit button
            ctk.CTkButton(
                controls,
                text="✏️",
                width=25,
                height=25,
                command=lambda name=color_name: self.edit_color(name)
            ).pack(pady=1)
            
            # Delete button
            ctk.CTkButton(
                controls,
                text="🗑️",
                width=25,
                height=25,
                fg_color="darkred",
                hover_color="red",
                command=lambda name=color_name: self.delete_color(name)
            ).pack(pady=1)
            
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        # Add new color button
        add_btn = ctk.CTkButton(
            self.colors_frame,
            text="+",
            width=60,
            height=60,
            command=self.add_new_color
        )
        add_btn.grid(row=row if col == 0 else row + 1, column=0, padx=5, pady=5)

    def create_effects_controls(self):
        effects = ctk.CTkFrame(self.effects_frame)
        effects.pack(fill="x", pady=5)
        
        ctk.CTkButton(
            effects,
            text="🌊 Wave",
            width=80,
            command=lambda: self.controller.wave_effect()
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            effects,
            text="⚡ Strobe",
            width=80,
            command=lambda: self.controller.strobe_effect()
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            effects,
            text="🎉 Party",
            width=80,
            command=self.toggle_party_mode
        ).pack(side="left", padx=5)

    def reset_colors(self):
        self.controller.reset_to_defaults()
        self.create_color_grid()

    def delete_color(self, color_name):
        del self.controller.saved_colors[color_name]
        self.controller.save_config()
        self.create_color_grid()

    def edit_color(self, color_name):
        picker = AskColor()
        new_color = picker.get()
        if new_color:
            rgb = [int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)]
            self.controller.saved_colors[color_name] = rgb
            self.controller.save_config()
            self.create_color_grid()

    def add_new_color(self):
        picker = AskColor()
        new_color = picker.get()
        if new_color:
            rgb = [int(new_color[1:3], 16), int(new_color[3:5], 16), int(new_color[5:7], 16)]
            color_name = f"Color {len(self.controller.saved_colors) + 1}"
            self.controller.saved_colors[color_name] = rgb
            self.controller.save_config()
            self.create_color_grid()

    def toggle_party_mode(self):
        self.controller.toggle_party_mode()

    def run(self):
        self.root.mainloop()

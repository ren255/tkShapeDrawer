import tkinter as tk
from interface import page_interface

class canvas(page_interface):
    def __init__(self,parent_frame,model):
        super().__init__(parent_frame,model)
        
    def create_content(self):
        super().create_content()
        
        self.canvas_main = tk.Canvas(
            self.frame_content,
            bg="green",
        )
        self.canvas_main.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5,
        )
        self.frame_buttons = tk.Frame(
            self.frame_content,
            bg = "blue",
            width=150,
        )
        self.frame_buttons.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=5,
            pady=5,
        )
        
        for i in range(10):
            tk.Button(
                self.frame_buttons,
                text=f"button {i}",
            ).pack(
                fill=tk.X,
                padx=15,
                pady=10,
            )
        
        self.canvas_main.create_rectangle(
            50,50,
            100,250,
        )

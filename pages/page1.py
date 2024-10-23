import tkinter as tk
from interface import page_interface

class page1(page_interface):
    def __init__(self,parent_frame,model):
        super().__init__(parent_frame,model)
        
    def create_content(self):
        super().create_content()
        tk.Label(
            self.frame_content,
            text="frame_content page 1",
        ).pack()

    def text(self):
        self.frame_text = tk.Frame(
            self.frame_body,
        )
        self.frame_text.pack(expand=True)
        
        for i in range(10):
            tk.Label(
                text=f"label {i}",
                bg="green"
            ).pack(anchor="w")
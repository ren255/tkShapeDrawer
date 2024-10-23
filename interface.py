from abc import ABC, abstractmethod
import tkinter as tk

class page_interface(ABC):
    def __init__(self, parent_frame, model):
        self.parent_frame = parent_frame
        self.model = model
        self.frame_content = None  

    @abstractmethod
    def create_content(self):
        self.destroy()
        self.frame_content = tk.Frame(
            self.parent_frame,
            bg="brown"
        )
        self.frame_content.place(
            relheight=1,
            relwidth=1,
        )


    def update(self):
        self.destroy()
        self.create_content()

    def destroy(self):
        if self.frame_content:
            self.frame_content.destroy()
        self.frame_content = None
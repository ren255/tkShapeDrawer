import tkinter as tk
from interface import page_interface

class blank(page_interface):
    def __init__(self,parent_frame,model):
        super().__init__(parent_frame,model)
        self.callback = callback()
        
    def create_content(self):
        super().create_content()

class callback(blank):
    def __init__(self):
        pass
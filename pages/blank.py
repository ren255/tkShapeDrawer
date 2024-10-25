import tkinter as tk
from interface import page_interface

class blank(page_interface):
    def __init__(self,parent_frame,model):
        super().__init__(parent_frame,model)
        
    def create_content(self):
        super().create_content()
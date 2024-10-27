import tkinter as tk
import customtkinter as ctk
from interface import page_interface


class canvas(page_interface):
    def __init__(self, parent_frame, model):
        super().__init__(parent_frame, model)
        self.pad = 10
        

    def create_content(self):
        super().create_content(5)
        self.body()
        self.canvaswidgets()
        
        self.toolbox = toolbox(self)

    def body(self):
        height = 100
        # canvas
        self.canvas_main = tk.Canvas(
            self.frame_content,
            bg="light green",
        )
        self.canvas_main.pack(
            fill=tk.BOTH,
            expand=True,
        )
        # label
        self.frame_labels = tk.Frame(
            self.frame_content,
            height=20,
            bg="light yellow",
        )
        self.frame_labels.pack(
            fill=tk.X,
        )
        self.mouseposLabel = tk.Label(self.frame_labels,text="")
        self.mouseposLabel.pack(side=tk.LEFT)
        self.canvas_main.bind(
            "<Motion>", 
            lambda event:
                self.toolbox.motion(event),
        )
        

        
        # toolbox
        self.frame_toolbar = tk.Frame(
            self.frame_content,
            bg="light blue",
            height=height,
        )
        self.frame_toolbar.pack(
            side=tk.BOTTOM,
            fill=tk.X,
        )
        self.frame_toolbar.pack_propagate(False)

        self.toolbar(height)

    def toolbar(self, height):
        for i in range(10):
            ctk.CTkButton(
                self.frame_toolbar,
                text=f"{i}",
                height=height - self.pad,
                width=height - self.pad,
            ).pack(
                side=tk.LEFT,
                fill=tk.Y,
                padx=self.pad // 2,
                pady=self.pad // 2,
            )

    def canvaswidgets(self):
        rec_list = [
            (50, 0, 100, 100),
            (50, 50, 100, 250),
            (300, 50, 250, 250),
            (250, 100, 100, 250),
        ]
        for i in rec_list:
            self.canvas_main.create_rectangle(*i)

class toolbox():
    def __init__(self,page):
        self.page = page
        self.canvas = self.page.canvas_main
        self.mpos = mouse()

    def motion(self,event):
        """Get mouse position"""
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.page.mouseposLabel.config(text="{}|{}".format(x, y))

    def create_rectangle(*args):
        pass

def mouse():
    def __init__(self):
        pass
    
    def setShape(self):
        pass
    
    def setpos(self,pos):
        self.pos1 = pos
    
    def endpos(self,pos):
        self.pos2 = pos
    
    def getrec(self):
        return (self.pos1,self.pos2)
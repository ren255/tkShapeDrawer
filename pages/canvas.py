import tkinter as tk
import customtkinter as ctk

from interface import page_interface
from modules.mouse import mouse


class canvas(page_interface):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        self.pad = 10
        self.mouse = mouse()

    def create_content(self):
        super().create_content(5)
        self.body()
        self.labels()

        self.set_handlers()

    def set_handlers(self):
        labels = {"Mpos": self.mouseposLabel, "mode": self.modeLabel}

        self.labMgr = toolboxM(self.canvas, labels, self.mouse)
        self.CnvMgr = canvasM(self.canvas, self.mouse)

        # 範囲選択
        self.canvas.bind("<ButtonPress-1>", self.CnvMgr.click_selecBox)
        self.canvas.bind("<Button1-Motion>", self.CnvMgr.motion_selecBox)

    def body(self):
        height = 75
        # canvas
        self.canvas = tk.Canvas(
            self.frame_content,
            bg="light green",
        )
        self.canvas.pack(
            fill=tk.BOTH,
            expand=True,
        )
        self.canvas.bind(
            "<Motion>",
            lambda event: self.labMgr.motion(event),
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

    def labels(self):
        self.frame_labels = tk.Frame(
            self.frame_content,
            height=20,
            bg="light yellow",
        )
        self.frame_labels.pack(
            fill=tk.X,
        )

        self.mouseposLabel = tk.Label(self.frame_labels, text="0:0")
        self.mouseposLabel.pack(side=tk.LEFT)

        self.modeLabel = tk.Label(self.frame_labels, text="mode:select")
        self.modeLabel.pack(side=tk.LEFT)

    def toolbar(self, height):
        heabytools = [
            "select",  # 選択
            "move",  # 移動
            "delete",  # 削除
        ]
        tools = [
            "text",  # テキスト
            "line",  # 直線
            "rectangle",  # 四角
            "circle",  # 丸
            "ellipse",  # 楕円
            "triangle",  # 三角
            "polyline",  # 折れ線
        ]

        for i in heabytools:
            self.make_toolbutton(i, height, heaby=True)

        for i in tools:
            self.make_toolbutton(i, height)

    def make_toolbutton(self, text, height, heaby=False):
        button = ctk.CTkButton(
            self.frame_toolbar,
            text=text,
            height=height - self.pad,
            width=height - self.pad,
            command=lambda mode=text: [
                self.labMgr.setmode(mode),
                self.CnvMgr.setmode(mode),
            ],
        )
        if heaby:
            button.configure(fg_color="blue", hover_color="darkblue")
        button.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=self.pad // 2,
            pady=self.pad // 2,
        )

class canvasM:
    def __init__(self, canvas, mouse):
        self.mouse = mouse
        self.canvas = canvas
        self.mode = "selection"
    
    def setmode(self,mode):
        self.mode = mode
        print(self.mode)

    # bind with canvas
    def click_select(self, event):
        self.selected = self.canvas.find_closest(
            *self.mouse.setpos(event),
        )

    def motion_selected(self, event):
        self.canvas.move(
            self.selected,
            *self.mouse.getdiff(event),
        )
        self.mouse.setpos(event)

    def click_selecBox(self, event):
        self.canvas.delete("selecBox")
        self.mouse.setpos(event)

    def motion_selecBox(self, event):
        if self.canvas.find_withtag("selecBox"):
            self.canvas.coords(
                "selecBox",
                *self.mouse.getPpos(),
                *self.mouse.getpos(event),
            )
        else:
            self.canvas.create_rectangle(
                *self.mouse.getPpos(),
                *self.mouse.getpos(event),
                outline="blue",
                tag="selecBox",
            )
    # create things
    def create_circle():
        pass

class toolboxM:
    """
    tool box + text under canvas
    """

    def __init__(self, canvas, labels: dict, mouse):
        self.mouse = mouse
        self.canvas = canvas
        self.labels = labels

    def setmode(self, mode):
        self.labels["mode"].config(text="mode:" + mode)

    def motion(self, event):
        """Get mouse position"""
        # x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.labels["Mpos"].config(text=f"pos:{self.mouse.getpos(event)}")

    def create_rectangle(*args):
        pass

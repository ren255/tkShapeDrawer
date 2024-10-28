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
        labels = {
            "Mpos": self.mouseposLabel,
            "mode": self.modeLabel,
            "createID": self.createIDLebel,
            "selecnum": self.selecnumLabel,
        }

        self.labMgr = toolboxM(self.canvas, self.mouse, labels)
        self.CnvMgr = canvasM(self.canvas, self.mouse, self.labMgr)

        # bind
        self.canvas.bind("<ButtonPress-1>", self.CnvMgr.click_bind)
        self.canvas.bind("<Button1-Motion>", self.CnvMgr.motion_bind)
        self.canvas.bind("<ButtonRelease-1>", self.CnvMgr.release_bind)

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
        )
        self.frame_labels.pack(
            fill=tk.X,
        )

        self.mouseposLabel = tk.Label(self.frame_labels, text="0:0")
        self.mouseposLabel.pack(side=tk.RIGHT, padx=5)

        self.modeLabel = tk.Label(self.frame_labels, text="mode:select")
        self.modeLabel.pack(side=tk.LEFT, padx=5)

        self.createIDLebel = tk.Label(self.frame_labels, text="id:0")
        self.createIDLebel.pack(side=tk.LEFT, padx=5)

        self.selecnumLabel = tk.Label(self.frame_labels, text="selecnum:0")
        self.selecnumLabel.pack(side=tk.LEFT, padx=5)

    def toolbar(self, height):
        heabytools = [
            "select",  # 選択
            # "move",    # 移動
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
    def __init__(self, canvas, mouse, labelM):
        self.mouse = mouse
        self.labMgr = labelM
        self.canvas = canvas
        self.mode = "select"
        self.createID = 0

    def setmode(self, mode):
        self.mode = mode
        print(self.mode)

    ## bind with canvas
    # click_bind -------------------------------------------------------------------------------------
    def click_bind(self, event):
        self.click_selecBox(event)

    def click_selecBox(self, event):
        self.canvas.delete("selecBox")
        self.mouse.setpos(event)

    # rerease -------------------------------------------------------------------------------------
    def release_bind(self, event):
        isblank, seleRec = self.getVs(event)
        match self.mode:
            case "select":
                self.objects = self.canvas.find_overlapping(
                    *self.mouse.getpos(event),
                    *self.mouse.getpos(event),
                )
            case "delete":
                if isblank:
                    self.canvas.delete("all")
                    self.makeID(0)
                self.mode = "select"

            case "text":
                self.create_text(seleRec)
            case "line":
                self.create_line(seleRec)
            case "rectangle":
                self.create_rectangle(seleRec)
            case "circle":
                self.create_circle(seleRec)
            case "ellipse":
                self.create_ellipse(seleRec)
            case "triangle":
                self.create_triangle(seleRec)
            case "polyline":
                self.create_polyline(seleRec)
        
        self.labMgr.setmode(self.mode)

    # motion_bind  -------------------------------------------------------------------------------------
    def getVs(self, event):
        isblank = self.canvas.find_overlapping(
            *self.mouse.getpos(event),
            *self.mouse.getpos(event),
        )
        if not isblank:
            isblank = True
        else:
            isblank = False
        seleRec = (
            *self.mouse.getPpos(),
            *self.mouse.getpos(event),
        )
        return isblank, seleRec

    def motion_bind(self, event):
        isblank, seleRec = self.getVs(event)
        if isblank:
            self.displayBox(seleRec)

    def displayBox(self, seleRec):
        if self.canvas.find_withtag("selecBox"):
            self.canvas.coords(
                "selecBox",
                *seleRec,
            )
        else:
            self.canvas.create_rectangle(
                *seleRec,
                outline="blue",
                dash=(4, 4),  # 点線のパターン
                fill="light blue",
                stipple="gray25",  # 透明度を高くする
                tag="selecBox",
            )

    # create things
    def create_text(self, rec):
        self.makeID()
        return self.canvas.create_text(*rec[:2], text="テキスト", tags=str(self.createID))

    def create_line(self, rec):
        self.makeID()
        return self.canvas.create_line(*rec, tags=str(self.createID))

    def create_rectangle(self, rec):
        self.makeID()
        return self.canvas.create_rectangle(*rec, tags=str(self.createID))

    def create_circle(self, rec):
        self.makeID()
        x, y, x2, y2 = rec
        if x > x2:
            x,x2 = x2,x
        if y > y2:
            y,y2 = y2,y
            
        width, height = x2-x, y2-y
        size = min(width, height)
        print(f"rec is {rec},and making circle with {x, y, x + size, y + size,},size is {size}")
        return self.canvas.create_oval(x, y, x + size, y + size, tags=str(self.createID))

    def create_ellipse(self, rec):
        self.makeID()
        return self.canvas.create_oval(*rec, tags=str(self.createID))

    def create_triangle(self, rec):
        self.makeID()
        x1, y1, x2, y2 = rec
        x3 = (x1 + x2) / 2
        y3 = y1
        return self.canvas.create_polygon(x1, y2, x2, y2, x3, y3, tags=str(self.createID))

    def create_polyline(self, rec):
        self.makeID()
        return self.canvas.create_line(*rec, tags=str(self.createID))
    
    def makeID(self,id=False):
        if id is False:
            self.createID += 1
        else:
            self.createID = id
        self.labMgr.setcreateID(self.createID)

class toolboxM:
    """
    tool box + text under canvas
    """

    def __init__(self, canvas, mouse, labels: dict):
        self.mouse = mouse
        self.canvas = canvas
        self.labels = labels

    def setmode(self, mode):
        self.labels["mode"].config(text="mode:" + mode)
    
    def setcreateID(self,idnum):
        self.labels["createID"].config(text="createID:" + str(idnum))

    def motion(self, event):
        """Get mouse position"""
        # x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.labels["Mpos"].config(text=f"pos:{self.mouse.getpos(event)}")

    def create_rectangle(*args):
        pass

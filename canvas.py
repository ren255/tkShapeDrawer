import tkinter as tk
import customtkinter as ctk

from modules.mouse import mouse


class canvas():
    def __init__(self, root):
        self.frame_content = tk.Frame(root)
        self.frame_content.pack(
            expand=True,
            fill=tk.BOTH,
        )
        self.pad = 10
        self.mouse = mouse()

    def create_content(self):
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

        self.CnvMgr = canvasM(self.canvas, self.mouse,labels)

        # bind
        self.canvas.bind("<ButtonPress-1>", self.CnvMgr.click_bind)
        self.canvas.bind("<Motion>", self.CnvMgr.motion_bind)
        self.canvas.bind("<Button1-Motion>", self.CnvMgr.motion_bindB1)
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
    def __init__(self, canvas, mouse,labels):
        self.mouse = mouse
        self.canvas = canvas
        self.labels = labels
        
        self.mode = "select"
        self.createID = 0
        self.selected_objects = []

    def setmode(self, mode):
        self.mode = mode
        print(self.mode)

    ## bind with canvas
    # continuas
    def updateLabel(self,event):
        self.labels["selecnum"].config(
            text="selecnum:" + str(len(self.selected_objects)),
        )
        self.labels["mode"].config(
            text="mode:" + self.mode,
        )
        self.labels["createID"].config(
            text="createID:" + str(self.createID),
        )
        self.labels["Mpos"].config(
            text=f"pos:{self.mouse.getpos(event)}",
        )


    # click_bind -------------------------------------------------------------------------------------
    def click_bind(self, event):
        self.mouse.setpos(event)
        object, seleRec = self.getVs(event, object=True)

        if not object:
            self.boxon = True
            self.selected_objects = []
        else:
            self.boxon = []
            self.selected_objects = [object]

    # rerease -------------------------------------------------------------------------------------
    def release_bind(self, event):
        isblank, seleRec = self.getVs(event)
        match self.mode:
            case "select":
                self.selected_objects = self.canvas.find_overlapping(
                    *self.mouse.getpos(event),
                    *self.mouse.getpos(event),
                )
                self.canvas.delete("selecBox")

            case "delete":
                if isblank:
                    self.canvas.delete("all")
                    self.makeID(0)
                else:
                    self.canvas.delete(self.selected_objects)
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

    # motion_bind  -------------------------------------------------------------------------------------
    def motion_bind(self,event):
        self.updateLabel(event)

    def motion_bindB1(self, event):
        self.updateLabel(event)
        
        isblank, seleRec = self.getVs(event)
        if self.boxon:
            self.displayBox(seleRec)
        else:
            self.canvas.move(self.selected_objects, *self.mouse.getdiff(event))
            self.mouse.setpos(event)

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

    def getVs(self, event, object=False):
        # get object_clicked
        seleRec = (
            *self.mouse.getPpos(),
            *self.mouse.getpos(event),
        )
        isblank = self.canvas.find_overlapping(
            *self.mouse.getpos(event),
            *self.mouse.getpos(event),
        )

        if object == True:
            return isblank, seleRec

        if not isblank:
            isblank = True
        else:
            isblank = False

        return isblank, seleRec

    # create things
    def create_text(self, rec):
        self.makeID()
        return self.canvas.create_text(
            *rec[:2], text="テキスト", tags=str(self.createID)
        )

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
            x, x2 = x2, x
        if y > y2:
            y, y2 = y2, y

        width, height = x2 - x, y2 - y
        size = min(width, height)
        return self.canvas.create_oval(
            x, y, x + size, y + size, tags=str(self.createID)
        )

    def create_ellipse(self, rec):
        self.makeID()
        return self.canvas.create_oval(*rec, tags=str(self.createID))

    def create_triangle(self, rec):
        self.makeID()
        x1, y1, x2, y2 = rec
        x3 = (x1 + x2) / 2
        y3 = y1
        return self.canvas.create_polygon(
            x1, y2, x2, y2, x3, y3, tags=str(self.createID)
        )

    def create_polyline(self, rec):
        self.makeID()
        return self.canvas.create_line(*rec, tags=str(self.createID))

    def makeID(self, id=False):
        if id is False:
            self.createID += 1
        else:
            self.createID = id

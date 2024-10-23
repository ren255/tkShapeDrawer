import tkinter as tk
import importlib

class View:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        
        self.window()

        self.page_list = ["Frame_textlist", "grid_buttons","blank"]
        self.make_frame()
        self.initialize_pages()
        
        self.current_page_name = "Frame_textlist"
        self.page_change(self.current_page_name)
        
    def window(self):
        self.root.minsize(300, 300)  # 最小サイズ
        self.root.geometry("600x600+200+0")

    def initialize_pages(self):
        self.pageClasses = {}
        self.pageObjects = {}
        for page_name in self.page_list:
            module = importlib.import_module(f"pages.{page_name}")
            page_class = getattr(module, page_name)
            self.pageClasses[page_name] = page_class
            self.pageObjects[page_name] = page_class(self.frame_body, self.model)

    def make_frame(self):
        self.top_frame()
        self.body_frame()
        
    def page_change(self, page_name):
        print(f"page changing to {page_name}")
        self.pageObjects[self.current_page_name].destroyView()
        self.current_page_name = page_name
        self.pageObjects[self.current_page_name].createView()

    # Frames
    def top_frame(self):
        frame_top = tk.Frame(self.root, bg="light blue", padx=25, pady=5)
        frame_top.place(relheight=0.1, relwidth=1)

        tk.Label(
            frame_top, text="top flame", font=(20), bg="light blue"
        ).pack(side=tk.LEFT, padx=10)

        for page_name in self.page_list:
            tk.Button(
                frame_top,
                text=page_name,
                padx=5,
                command=lambda name=page_name: self.page_change(name),
            ).pack(side=tk.LEFT, padx=10)

    def body_frame(self):
        self.frame_body = tk.Frame(self.root)
        self.frame_body.place(
            relx=0,
            rely=0.1,
            relheight=0.9,
            relwidth=1,
        )
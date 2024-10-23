import tkinter as tk
import importlib

page_list = ["Frame_textlist", "page1"]

def import_pages(page_list):
    pages = {}
    for page_name in page_list:
        module = importlib.import_module(f"pages.{page_name}")
        page_class = getattr(module, page_name)
        pages[page_name] = page_class
    return pages



class View:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        
        self.window()
        self.initialize_pages()

        self.setup()
        
        



    def window(self):
        self.root.minsize(300, 300)  # 最小サイズ
        self.root.geometry("600x600+200+100")

    def initialize_pages(self):
        self.pages = import_pages(page_list)

    def setup(self):
        self.top_frame()
        self.body_frame()
        
        page_class = self.pages["Frame_textlist"]
        self.current_page = page_class(self.frame_body, self.model)
        self.page_change("Frame_textlist")

        
        
    def page_change(self, page_name):
        print(f"page changing to {page_name}")
        self.current_page.destroy()
            
        page_class = self.pages[page_name]
        self.current_page = page_class(self.frame_body, self.model)
        self.current_page.update()

    def top_frame(self):
        frame_top = tk.Frame(self.root, bg="light blue", padx=25, pady=5)
        frame_top.place(relheight=0.1, relwidth=1)

        tk.Label(
            frame_top, text="top flame", font=(20), bg="light blue"
        ).pack(side=tk.LEFT, padx=10)

        for page_name in self.pages:
            tk.Button(
                frame_top,
                text=page_name,
                padx=5,
                command=lambda name=page_name: self.page_change(name),
            ).pack(side=tk.LEFT, padx=10)

    def body_frame(self):
        self.frame_body = tk.Frame(self.root,bg="green")
        self.frame_body.place(
            relx=0,
            rely=0.1,
            relheight=0.9,
            relwidth=1,
        )
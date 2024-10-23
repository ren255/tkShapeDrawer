from abc import ABC, abstractmethod
import tkinter as tk


class page_interface(ABC):
    def __init__(self, parent_frame, model, model_page=None):
        self.parent_frame = parent_frame
        self.model = model  # すべてページで同じ
        self.model_page = model_page  # 各ページごとに異なる

    @abstractmethod
    def create_content(self):
        self.frame_content = tk.Frame(self.parent_frame)
        self.frame_content.place(
            relheight=1,
            relwidth=1,
        )

    # Todo
    def built(self):
        self.destroyView()
        self.createView()
        return

    def createView(self):
        # frameを消し、作成する。
        self.destroyView()
        self.create_content()

    def destroyView(self):
        # frameを消す
        if hasattr(self, "frame_content"):
            self.frame_content.destroy()

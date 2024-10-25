import tkinter as tk
from view import View

class Model:
    def __init__(self, root):
        self.app_gui = View(root, self)


if __name__ == "__main__":
    root = tk.Tk()

    model = Model(root)

    root.mainloop()

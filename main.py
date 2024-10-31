import tkinter as tk
from view import View
from canvas import canvas

if __name__ == "__main__":
    root = tk.Tk()
    Canvas = canvas(root)
    Canvas.create_content()

    root.mainloop()

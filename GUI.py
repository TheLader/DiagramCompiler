import tkinter as tk
import Block

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Стрілки переміщуються разом із фігурами")
        self.arrow_source = None

        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)
        Block.Block(self.canvas, 70, 70, "start")
        sidebar = tk.Frame(self.root)
        sidebar.pack(side="right", fill="y")
        button_holder = tk.Frame(sidebar)
        button_holder.pack(expand=True)

        tk.Button(button_holder, text="Додати змінну", command=self.addVariable).pack(pady=5)

    def addStart(self):
        Block.Block(self.canvas, 70, 70, "start")

    def addVariable(self):
        Block.Block(self.canvas, 70, 70, "variable")
import tkinter as tk
import math
class Arrow:
    def __init__(self, canvas, source, target):
        self.canvas = canvas
        self.source = source
        self.target = target
        self.line = canvas.create_line(
            source.get_center(), target.get_center(),
            arrow=tk.LAST, fill="red", width=2
        )
        self.update()

    def update(self):
        start = self.source.get_border_point(self.target.get_center())
        end = self.target.get_border_point(self.source.get_center())
        self.canvas.coords(self.line, *start, *end)

    def delete(self):
        self.canvas.delete(self.line)
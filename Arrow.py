import tkinter as tk
import math
class Arrow:
    def __init__(self, canvas, source, target, text = ""):
        self.canvas = canvas
        self.source = source
        self.target = target
        self.text = text
        self.line = canvas.create_line(
            source.get_center(), target.get_center(),
            arrow=tk.LAST, fill="red", width=2
        )
        if text != "":
            self.labelbox,  self.label = self.draw_text_with_box(0, 0, text)

        self.update()

    def update(self):
        start = self.source.get_border_point(self.target.get_center())
        end = self.target.get_border_point(self.source.get_center())
        self.canvas.coords(self.line, *start, *end)

        # Центр стрілки
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        if self.text != "":
            bbox = self.canvas.bbox(self.label)
            if bbox:
                x1, y1, x2, y2 = bbox
                padding = 4
                x1 -= padding
                y1 -= padding
                x2 += padding
                y2 += padding
                self.canvas.coords(self.labelbox, x1, y1, x2, y2)
            self.canvas.coords(self.label, mid_x, mid_y)

    def draw_text_with_box(self, x, y, text, padding=4):
        temp = self.canvas.create_text(x, y, text=text)
        bbox = self.canvas.bbox(temp)
        self.canvas.delete(temp)

        x1, y1, x2, y2 = bbox
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding

        return self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black"), self.canvas.create_text(x, y, text=text, fill="black")



    def delete(self):
        self.canvas.delete(self.line)
        if self.text != "":
            self.canvas.delete(self.labelbox)
            self.canvas.delete(self.label)
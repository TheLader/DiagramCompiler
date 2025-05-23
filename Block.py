import tkinter as tk
from tkinter import simpledialog
from venv import create
import Arrow

class Block:
    arrow = None
    def __init__(self, canvas, x, y, type):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.type = type
        self.size = 50
        self.item = None
        self.text = None
        self.variableName = None
        self.variableValue = None
        self._drag_data = {"x": 0, "y": 0}
        self.connectedToBlocks = []
        self.connectedFromBlocks = []
        self.arrows = []

        match type:
            case "start":
                self.createStart()
            case "variable":
                self.createVariable()

    def createStart(self):
        self.item = self.canvas.create_rectangle(self.x, self.y, self.x + self.size*2, self.y + self.size, fill="white")
        self.text = self.canvas.create_text(self.x+self.size, self.y+self.size/2, text="Start")
        self.canvas.tag_bind(self.item, "<ButtonPress-1>", self.onLeftClick)
        self.canvas.tag_bind(self.item, "<B1-Motion>", self.onDrag)
        self.canvas.tag_bind(self.item, "<Button-3>", self.onRightClick)

    def createVariable(self):
        self.item = self.canvas.create_rectangle(self.x, self.y, self.x + self.size * 2, self.y + self.size,
                                                 fill="white")
        self.text = self.canvas.create_text(self.x + self.size, self.y + self.size / 2, text="")
        self.canvas.tag_bind(self.item, "<ButtonPress-1>", self.onLeftClick)
        self.canvas.tag_bind(self.item, "<B1-Motion>", self.onDrag)
        self.canvas.tag_bind(self.item, "<Button-3>", self.onRightClick)

    def onLeftClick(self, event):
        if Block.arrow is not None:
            source = Block.arrow
            if source is not self:
                self.createArrow(source)
                self.connectedFromBlocks.append(source)
                source.connectedToBlocks.append(self)
                Block.arrow = None
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def onDrag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.canvas.move(self.item, dx, dy)
        self.canvas.move(self.text, dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        for arrow in self.arrows:
            arrow.update()
        for connectedToBlock in self.connectedToBlocks:
            for connectedArrow in connectedToBlock.arrows:
                connectedArrow.update()

    def onRightClick(self, event):
        self.menu = tk.Menu(self.canvas, tearoff=0)
        if(self.type == "start"):
            self.menu.add_command(label="Додати стрілку", command=self.startArrow)
        if(self.type == "variable"):
            self.menu.add_command(label="Додати стрілку", command=self.startArrow)
            self.menu.add_command(label="Задати імя змінної", command=self.setVariableName)
            self.menu.add_command(label="Задати значення змінної", command=self.setVariableValue)
            self.menu.add_command(label="Видалити", command=self.delete)
        self.menu.post(event.x_root, event.y_root)

    def startArrow(self):
        Block.arrow = self

    def createArrow(self, block):
        self.arrows.append(Arrow.Arrow(self.canvas, block, self))

    def setVariableName(self):
        text = simpledialog.askstring("Вписати текст", "Назва змінної")
        self.canvas.delete(self.text)
        self.variableName = text
        x, y =self.get_center()
        self.text = self.canvas.create_text(x, y, text=f"{self.variableName}={self.variableValue}")

    def setVariableValue(self):
        text = simpledialog.askstring("Вписати текст", "Значення змінної")
        self.canvas.delete(self.text)
        self.variableValue = text
        x, y =self.get_center()
        self.text = self.canvas.create_text(x, y, text=f"{self.variableName}={self.variableValue}")

    def delete(self):
        self.canvas.delete(self.item)
        self.canvas.delete(self.text)
        self.arrows.clear()

    def get_center(self):
        coords = self.canvas.coords(self.item)
        x1, y1, x2, y2 = coords
        return (x1 + x2) // 2, (y1 + y2) // 2

    def get_border_point(self, other_center):
        x0, y0 = self.get_center()
        x1, y1 = other_center

        coords = self.canvas.coords(self.item)
        x_left, y_top, x_right, y_bottom = coords
        w = (x_right - x_left) / 2
        h = (y_bottom - y_top) / 2

        dx = x1 - x0
        dy = y1 - y0

        if dx == 0:
            return (x0, y0 + h * (1 if dy > 0 else -1))

        slope = dy / dx
        if abs(slope) < h / w:
            # перетин із вертикальними сторонами
            x = x0 + w * (1 if dx > 0 else -1)
            y = y0 + slope * (x - x0)
        else:
            # перетин із горизонтальними сторонами
            y = y0 + h * (1 if dy > 0 else -1)
            x = x0 + (y - y0) / slope

        return (x, y)
import tkinter as tk
from tkinter import simpledialog
from venv import create
import Arrow

class Block:
    _arrow = None
    _condition = None
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
        self.condition = None
        self._drag_data = {"x": 0, "y": 0}
        self.connectedToBlock = None
        self.connectedFromBlocks = []
        self.arrow = []
        self.conditionTrueBlock = None
        self.conditionFalseBlock = None

        match type:
            case "start":
                self.createStart()
            case "variable":
                self.createVariable()
            case "condition":
                self.createCondition()
            case "end":
                self.createEnd()

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

    def createCondition(self):
        half = self.size
        points = [self.x, self.y - half, self.x + half, self.y, self.x, self.y + half, self.x - half, self.y]
        self.item = self.canvas.create_polygon(points, fill="white", outline="black")
        self.text = self.canvas.create_text(self.x , self.y , text="")
        self.canvas.tag_bind(self.item, "<ButtonPress-1>", self.onLeftClick)
        self.canvas.tag_bind(self.item, "<B1-Motion>", self.onDrag)
        self.canvas.tag_bind(self.item, "<Button-3>", self.onRightClick)

    def createEnd(self):
        self.item = self.canvas.create_rectangle(self.x, self.y, self.x + self.size * 2, self.y + self.size,
                                                 fill="white")
        self.text = self.canvas.create_text(self.x + self.size, self.y + self.size / 2, text="End")
        self.canvas.tag_bind(self.item, "<ButtonPress-1>", self.onLeftClick)
        self.canvas.tag_bind(self.item, "<B1-Motion>", self.onDrag)
        self.canvas.tag_bind(self.item, "<Button-3>", self.onRightClick)

    def onLeftClick(self, event):
        if Block._arrow is not None:
            source = Block._arrow
            if source is not self:
                if Block._condition is not None:
                    source.createArrow(self, f"{Block._condition}")
                    self.connectedFromBlocks.append(source)
                    if Block._condition:
                        source.conditionTrueBlock = self
                    else:
                        source.conditionFalseBlock = self
                    Block._arrow = None
                    Block._condition = None
                else:
                    source.createArrow(self)
                    self.connectedFromBlocks.append(source)
                    source.connectedToBlock = self
                    Block._arrow = None
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def onDrag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.canvas.move(self.item, dx, dy)
        self.canvas.move(self.text, dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        for arrow in self.arrow:
            arrow.update()
        for connectedFromBlock in self.connectedFromBlocks:
            for arrow in connectedFromBlock.arrow:
                arrow.update()

    def onRightClick(self, event):
        self.menu = tk.Menu(self.canvas, tearoff=0)
        if(self.type == "start"):
            if not self.arrow:
                self.menu.add_command(label="Додати стрілку", command=self.startArrow)
            else:
                self.menu.add_command(label="Видалити стрілку", command=self.deleteArrow)
        if(self.type == "variable"):
            if not self.arrow:
                self.menu.add_command(label="Додати стрілку", command=self.startArrow)
            else:
                self.menu.add_command(label="Видалити стрілку", command=self.deleteArrow)
            self.menu.add_command(label="Задати імя змінної", command=self.setVariableName)
            self.menu.add_command(label="Задати значення змінної", command=self.setVariableValue)
            self.menu.add_command(label="Видалити", command=self.delete)
        if(self.type == "condition"):
            self.menu.add_command(label="Задати умову", command=self.setCondition)
            if self.conditionTrueBlock is None:
                self.menu.add_command(label="Виконання умови", command=self.startTrueArrow)
            else:
                self.menu.add_command(label="Видалити виконання умови", command=self.deleteTrueArrow)
            if self.conditionFalseBlock is None:
                self.menu.add_command(label="Невиконання умови", command=self.startFalseArrow)
            else:
                self.menu.add_command(label="Видалити невиконання умови", command=self.deleteFalseArrow)
            self.menu.add_command(label="Видалити", command=self.delete)

        self.menu.post(event.x_root, event.y_root)

    def startTrueArrow(self):
        self.startArrow(True)

    def startFalseArrow(self):
        self.startArrow(False)

    def startArrow(self, condition = None):
        Block._arrow = self
        Block._condition = condition

    def createArrow(self, block, text = ""):
        self.arrow.append(Arrow.Arrow(self.canvas, self, block, text))

    def deleteArrow(self):
        arrowForDelete = []
        for arrow in self.arrow:
            arrow.delete()
            arrowForDelete.append(arrow)
        for arrow in arrowForDelete:
            self.arrow.remove(arrow)

    def deleteTrueArrow(self):
        deleteArrow = None
        for arrow in self.arrow:
            if self.conditionTrueBlock is arrow.target:
                deleteArrow = arrow
        deleteArrow.delete()
        self.arrow.remove(deleteArrow)
        self.conditionTrueBlock = None

    def deleteFalseArrow(self):
        deleteArrow = None
        for arrow in self.arrow:
            if self.conditionFalseBlock is arrow.target:
                deleteArrow = arrow
        deleteArrow.delete()
        self.arrow.remove(deleteArrow)
        self.conditionFalseBlock = None

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

    def setCondition(self):
        text = simpledialog.askstring("Вписати текст", "Умова")
        self.canvas.delete(self.text)
        self.condition = text
        x, y =self.get_center()
        self.text = self.canvas.create_text(x, y, text=f"{self.condition}")

    def delete(self):
        for connectedFromBlock in self.connectedFromBlocks:
            for arrow in connectedFromBlock.arrow:
                if arrow.target == self:
                    arrow.delete()
                    connectedFromBlock.arrow.remove(arrow)
            connectedFromBlock.conditionTrueBlock = None
            connectedFromBlock.conditionFalseBlock = None
            connectedFromBlock.connectedToBlock = None
        if self.connectedToBlock is not None:
            self.connectedToBlock.connectedFromBlocks.remove(self)
        self.canvas.delete(self.item)
        self.canvas.delete(self.text)
        arrowForDelete = []
        for arrow in self.arrow:
            arrow.delete()
            arrowForDelete.append(arrow)
        for arrow in arrowForDelete:
            self.arrow.remove(arrow)



    def get_center(self):
        coords = self.canvas.coords(self.item)
        if len(coords) == 4:  # прямокутник
            x1, y1, x2, y2 = coords
            return (x1 + x2) // 2, (y1 + y2) // 2
        elif len(coords) == 8:  # ромб
            xs = coords[::2]
            ys = coords[1::2]
            return sum(xs) // 4, sum(ys) // 4

    def get_border_point(self, other_center):
        x0, y0 = self.get_center()
        x1, y1 = other_center

        coords = self.canvas.coords(self.item)

        if len(coords) == 4:  # Прямокутник
            x_left, y_top, x_right, y_bottom = coords
            w = (x_right - x_left) / 2
            h = (y_bottom - y_top) / 2

            dx = x1 - x0
            dy = y1 - y0

            if dx == 0:
                return (x0, y0 + h * (1 if dy > 0 else -1))

            slope = dy / dx
            if abs(slope) < h / w:
                x = x0 + w * (1 if dx > 0 else -1)
                y = y0 + slope * (x - x0)
            else:
                y = y0 + h * (1 if dy > 0 else -1)
                x = x0 + (y - y0) / slope

            return (x, y)

        elif len(coords) == 8:  # Ромб
            # Точки: [top, right, bottom, left]
            points = [(coords[i], coords[i + 1]) for i in range(0, 8, 2)]

            def line_intersection(p1, p2, p3, p4):
                """Перетин відрізків p1-p2 і p3-p4"""
                x1, y1 = p1
                x2, y2 = p2
                x3, y3 = p3
                x4, y4 = p4

                denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if denom == 0:
                    return None  # паралельні

                px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
                py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

                # перевірка, чи точка перетину належить обом відрізкам
                def between(a, b, c):
                    return min(a, b) <= c <= max(a, b)

                if (between(x1, x2, px) and between(y1, y2, py) and
                        between(x3, x4, px) and between(y3, y4, py)):
                    return (px, py)
                return None

            # Сторони ромба: [top->right, right->bottom, bottom->left, left->top]
            sides = [
                (points[0], points[1]),
                (points[1], points[2]),
                (points[2], points[3]),
                (points[3], points[0])
            ]

            for side_start, side_end in sides:
                intersection = line_intersection((x0, y0), (x1, y1), side_start, side_end)
                if intersection:
                    return intersection

            return (x0, y0)  # fallback

        else:
            return self.get_center()

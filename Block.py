import tkinter as tk
from tkinter import simpledialog

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
        self.inputVariable = None
        self.operationText = None
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
            case "input":
                self.createInput()
            case "operation":
                self.createOperation()

    def createStart(self):
        self.item = self.canvas.create_rectangle(self.x, self.y, self.x + self.size*2, self.y + self.size, fill="white")
        self.text = self.canvas.create_text(self.x + self.size, self.y + self.size / 2, text="Start")
        self.bindEvents()

    def createVariable(self):
        self.item = self.canvas.create_rectangle(self.x, self.y, self.x + self.size * 2, self.y + self.size, fill="white")
        self.text = self.canvas.create_text(self.x + self.size, self.y + self.size / 2, text="")
        self.bindEvents()

    def createCondition(self):
        half = self.size
        points = [self.x, self.y - half, self.x + half, self.y, self.x, self.y + half, self.x - half, self.y]
        self.item = self.canvas.create_polygon(points, fill="white", outline="black")
        self.text = self.canvas.create_text(self.x, self.y, text="Condition")
        self.bindEvents()

    def createInput(self):
        # Draw parallelogram
        offset = 20
        x1, y1 = self.x + offset, self.y
        x2, y2 = self.x + self.size * 2 + offset, self.y
        x3, y3 = self.x + self.size * 2, self.y + self.size
        x4, y4 = self.x, self.y + self.size

        self.item = self.canvas.create_polygon(
            [x1, y1, x2, y2, x3, y3, x4, y4],
            fill="white",
            outline="black"
        )
        center_x = (x1 + x3) // 2
        center_y = (y1 + y3) // 2
        self.text = self.canvas.create_text(center_x, center_y, text="Input")
        self.bindEvents()

    def createOperation(self):
        self.item = self.canvas.create_rectangle(self.x, self.y, self.x + self.size * 2, self.y + self.size, fill="white")
        self.text = self.canvas.create_text(self.x + self.size, self.y + self.size / 2, text="Operation")
        self.bindEvents()

    def bindEvents(self):
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
        if self.type in {"start", "variable", "input"}:
            if not self.arrow:
                self.menu.add_command(label="Додати стрілку", command=self.startArrow)
            else:
                self.menu.add_command(label="Видалити стрілку", command=self.deleteArrow)
        if self.type == "variable":
            self.menu.add_command(label="Задати ім’я змінної", command=self.setVariableName)
            self.menu.add_command(label="Задати значення змінної", command=self.setVariableValue)
            self.menu.add_command(label="Видалити", command=self.delete)
        if self.type == "condition":
            if self.conditionTrueBlock is None:
                self.menu.add_command(label="Виконання умови", command=self.startTrueArrow)
            else:
                self.menu.add_command(label="Видалити виконання умови", command=self.deleteTrueArrow)
            if self.conditionFalseBlock is None:
                self.menu.add_command(label="Невиконання умови", command=self.startFalseArrow)
            else:
                self.menu.add_command(label="Видалити невиконання умови", command=self.deleteFalseArrow)
            self.menu.add_command(label="Видалити", command=self.delete)
        if self.type == "input":
            self.menu.add_command(label="Ввести змінну", command=self.setInputVariable)
            self.menu.add_command(label="Видалити", command=self.delete)
        if self.type == "operation":
            self.menu.add_command(label="Встановити операцію", command=self.setOperationText)
            self.menu.add_command(label="Видалити", command=self.delete)
        self.menu.post(event.x_root, event.y_root)

    def startTrueArrow(self):
        self.startArrow(True)

    def startFalseArrow(self):
        self.startArrow(False)

    def startArrow(self, condition=None):
        Block._arrow = self
        Block._condition = condition

    def createArrow(self, block, text=""):
        import Arrow  # avoid cyclic import
        self.arrow.append(Arrow.Arrow(self.canvas, self, block, text))

    def deleteArrow(self):
        for arrow in list(self.arrow):
            arrow.delete()
            self.arrow.remove(arrow)

    def deleteTrueArrow(self):
        for arrow in list(self.arrow):
            if self.conditionTrueBlock is arrow.target:
                arrow.delete()
                self.arrow.remove(arrow)
        self.conditionTrueBlock = None

    def deleteFalseArrow(self):
        for arrow in list(self.arrow):
            if self.conditionFalseBlock is arrow.target:
                arrow.delete()
                self.arrow.remove(arrow)
        self.conditionFalseBlock = None

    def setVariableName(self):
        text = simpledialog.askstring("Вписати текст", "Назва змінної")
        self.variableName = text
        self.updateText()

    def setVariableValue(self):
        text = simpledialog.askstring("Вписати текст", "Значення змінної")
        self.variableValue = text
        self.updateText()

    def setInputVariable(self):
        text = simpledialog.askstring("Введення", "Назва змінної для введення")
        self.inputVariable = text
        self.updateText()

    def setOperationText(self):
        text = simpledialog.askstring("Операція", "Введіть текст операції")
        if text:
            self.operationText = text
            self.updateText()

    def updateText(self):
        self.canvas.delete(self.text)
        x, y = self.get_center()
        if self.type == "variable":
            display = f"{self.variableName}={self.variableValue}" if self.variableName else ""
        elif self.type == "input":
            display = f"input({self.inputVariable})" if self.inputVariable else ""
        elif self.type == "operation":
            display = self.operationText if self.operationText else "Operation"
        else:
            display = self.type
        self.text = self.canvas.create_text(x, y, text=display)

    def delete(self):
        for connectedFromBlock in self.connectedFromBlocks:
            for arrow in list(connectedFromBlock.arrow):
                if arrow.target == self:
                    arrow.delete()
                    connectedFromBlock.arrow.remove(arrow)
            connectedFromBlock.conditionTrueBlock = None
            connectedFromBlock.conditionFalseBlock = None
            connectedFromBlock.connectedToBlock = None
        if self.connectedToBlock:
            self.connectedToBlock.connectedFromBlocks.remove(self)
        self.canvas.delete(self.item)
        self.canvas.delete(self.text)
        for arrow in list(self.arrow):
            arrow.delete()
            self.arrow.remove(arrow)

    def get_center(self):
        coords = self.canvas.coords(self.item)
        if len(coords) == 4:
            x1, y1, x2, y2 = coords
            return (x1 + x2) // 2, (y1 + y2) // 2
        elif len(coords) == 8:
            xs = coords[::2]
            ys = coords[1::2]
            return sum(xs) // 4, sum(ys) // 4

    def get_border_point(self, other_center):
        x0, y0 = self.get_center()
        x1, y1 = other_center
        coords = self.canvas.coords(self.item)

        if len(coords) == 4:
            x_left, y_top, x_right, y_bottom = coords
            w, h = (x_right - x_left) / 2, (y_bottom - y_top) / 2
            dx, dy = x1 - x0, y1 - y0

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

        elif len(coords) == 8:
            points = [(coords[i], coords[i + 1]) for i in range(0, 8, 2)]
            def line_intersection(p1, p2, p3, p4):
                x1, y1 = p1
                x2, y2 = p2
                x3, y3 = p3
                x4, y4 = p4
                denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if denom == 0:
                    return None
                px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
                py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom
                def between(a, b, c): return min(a, b) <= c <= max(a, b)
                if all([between(*p, q) for p, q in zip([(x1, x2), (y1, y2), (x3, x4), (y3, y4)], [px, py, px, py])]):
                    return (px, py)
                return None

            sides = [(points[i], points[(i + 1) % 4]) for i in range(4)]
            for a, b in sides:
                inter = line_intersection((x0, y0), (x1, y1), a, b)
                if inter:
                    return inter
        return self.get_center()
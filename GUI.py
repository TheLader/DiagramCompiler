import tkinter as tk
from tkinter import simpledialog
class Arrow:
    def __init__(self, canvas, source, target):
        self.canvas = canvas
        self.source = source
        self.target = target
        self.line = canvas.create_line(
            *source.get_center(), *target.get_center(),
            arrow=tk.LAST, fill="red", width=2
        )
        source.out_arrows.append(self)
        target.in_arrows.append(self)

    def update(self):
        x1, y1 = self.source.get_center()
        x2, y2 = self.target.get_center()
        self.canvas.coords(self.line, x1, y1, x2, y2)

    def delete(self):
        self.canvas.delete(self.line)


class DraggableObject:
    all_objects = []

    def __init__(self, canvas, x, y, shape="square", size=50):
        self.canvas = canvas
        self.shape_type = shape
        self.size = size
        self.menu = None
        self.arrow_start = None
        self.out_arrows = []
        self.in_arrows = []

        half = size // 2
        if shape == "diamond":
            points = [x, y - half, x + half, y, x, y + half, x - half, y]
            self.item = canvas.create_polygon(points, fill="orange", outline="black")
        else:
            self.item = canvas.create_rectangle(x, y, x + size, y + size, fill="skyblue")

        canvas.tag_bind(self.item, "<ButtonPress-1>", self.on_left_click)
        canvas.tag_bind(self.item, "<B1-Motion>", self.on_drag)
        canvas.tag_bind(self.item, "<Button-3>", self.on_right_click)

        self._drag_data = {"x": 0, "y": 0}
        DraggableObject.all_objects.append(self)

    def on_left_click(self, event):
        if self.canvas.master.arrow_source:
            source = self.canvas.master.arrow_source
            if source != self:
                Arrow(self.canvas, source, self)
            self.canvas.master.arrow_source = None
        else:
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y

    def on_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.canvas.move(self.item, dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        # Update arrows
        for arrow in self.out_arrows + self.in_arrows:
            arrow.update()

    def on_right_click(self, event):
        self.menu = tk.Menu(self.canvas, tearoff=0)
        self.menu.add_command(label="Прикріпити стрілку", command=self.start_arrow)
        self.menu.add_command(label="Вписати текст", command=self.add_text)
        self.menu.add_command(label="Видалити", command=self.delete)
        self.menu.post(event.x_root, event.y_root)

    def add_text(self):
        text = simpledialog.askstring("Вписати текст", "Введіть текст:")
        if text:
            if self.text_id:
                self.canvas.delete(self.text_id)
            x, y = self.get_center()
            self.text_id = self.canvas.create_text(x, y, text=text, font=("Arial", 12))

    def start_arrow(self):
        self.canvas.master.arrow_source = self

    def delete(self):
        for arrow in self.out_arrows[:]:
            arrow.delete()
            arrow.target.in_arrows.remove(arrow)
        for arrow in self.in_arrows[:]:
            arrow.delete()
            arrow.source.out_arrows.remove(arrow)
        self.canvas.delete(self.item)
        DraggableObject.all_objects.remove(self)

    def get_center(self):
        coords = self.canvas.coords(self.item)
        if self.shape_type == "diamond":
            xs = coords[::2]
            ys = coords[1::2]
            return sum(xs) // len(xs), sum(ys) // len(ys)
        else:
            x1, y1, x2, y2 = coords
            return (x1 + x2) // 2, (y1 + y2) // 2


class App:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Стрілки переміщуються разом із фігурами")
        self.arrow_source = None

        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        sidebar = tk.Frame(self.root)
        sidebar.pack(side="right", fill="y")
        button_holder = tk.Frame(sidebar)
        button_holder.pack(expand=True)

        tk.Button(button_holder, text="Додати квадрат", command=self.add_square).pack(pady=5)
        tk.Button(button_holder, text="Додати ромбик", command=self.add_diamond).pack(pady=5)

    def add_square(self):
        DraggableObject(self.canvas, 70, 70, "square")

    def add_diamond(self):
        DraggableObject(self.canvas, 120, 120, "diamond")
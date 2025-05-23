import tkinter as tk

class DraggableObject:
    def __init__(self, canvas, x, y, size=50):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x, y, x + size, y + size, fill="skyblue")
        self._drag_data = {"x": 0, "y": 0}

        canvas.tag_bind(self.rect, "<ButtonPress-1>", self.on_start_drag)
        canvas.tag_bind(self.rect, "<B1-Motion>", self.on_drag)

    def on_start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.canvas.move(self.rect, dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Drag & Drop об'єкти")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.button = tk.Button(root, text="Додати об'єкт", command=self.add_object)
        self.button.pack(pady=10)

    def add_object(self):
        x, y = 50, 50
        DraggableObject(self.canvas, x, y)
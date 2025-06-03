import tkinter as tk
from tkinter import messagebox, scrolledtext
import Block
from code_generator import generate_code_from_blocks

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("DC V_Aplha")
        self.arrow_source = None

        # Полотно для блоків
        self.canvas = tk.Canvas(self.root, width=700, height=500, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Початкові блоки
        Block.Block(self.canvas, 70, 70, "start")
        Block.Block(self.canvas, 70, 70, "end")

        # Бокова панель із кнопками
        sidebar = tk.Frame(self.root)
        sidebar.pack(side="right", fill="y")
        button_holder = tk.Frame(sidebar)
        button_holder.pack(expand=True)

        tk.Button(button_holder, text="Додати змінну",   command=self.addVariable).pack(pady=5)
        tk.Button(button_holder, text="Додати умову",    command=self.addCondition).pack(pady=5)
        tk.Button(button_holder, text="Додати введення", command=self.addInput).pack(pady=5)
        tk.Button(button_holder, text="Додати операцію", command=self.addOperation).pack(pady=5)
        tk.Button(button_holder, text="Додати виведення", command=self.addOutput).pack(pady=5)

        # Вибір мови програмування
        tk.Label(button_holder, text="Оберіть мову:").pack(pady=(20, 0))
        self.lang_var = tk.StringVar(value="Python")
        langs = ["Python", "C++", "C#", "JavaScript"]
        tk.OptionMenu(button_holder, self.lang_var, *langs).pack(pady=5)

        # Кнопка "Згенерувати код"
        tk.Button(button_holder, text="Згенерувати код", command=self.generate_code).pack(pady=(20, 5))

    def addStart(self):
        Block.Block(self.canvas, 70, 70, "start")

    def addVariable(self):
        Block.Block(self.canvas, 70, 70, "variable")

    def addCondition(self):
        Block.Block(self.canvas, 70, 70, "condition")

    def addInput(self):
        Block.Block(self.canvas, 70, 70, "input")

    def addOperation(self):
        Block.Block(self.canvas, 70, 70, "operation")

    def addOutput(self):
        Block.Block(self.canvas, 70, 70, "output")

    def generate_code(self):
        """
        Збирає всі блоки, визначає вибрану мову і викликає генератор.
        """
        blocks = Block.Block.all_blocks
        language = self.lang_var.get()
        lines = generate_code_from_blocks(blocks, language)
        if not lines:
            messagebox.showerror("Помилка", "Не знайдено блок 'start' або блоки відсутні.")
            return

        # Відкриваємо нове вікно з ним
        code_window = tk.Toplevel(self.root)
        code_window.title(f"Згенерований код ({language})")
        txt = scrolledtext.ScrolledText(code_window, width=80, height=30, wrap=tk.WORD)
        txt.pack(expand=True, fill="both")
        txt.insert("1.0", "\n".join(lines))
        txt.configure(state="disabled")

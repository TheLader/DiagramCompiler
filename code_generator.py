import tkinter as tk
import Block
from typing import List


def generate_code_from_blocks(blocks: List[Block.Block], language: str) -> List[str]:
    """
    Генерує список рядків коду залежно від обраної мови.
    Підтримуються: "Python", "C++", "C#", "JavaScript".
    """

    # Спочатку знайдемо блок "start"
    start_block = None
    for b in blocks:
        if b.type == "start":
            start_block = b
            break

    if not start_block:
        return []

    # Викликаємо відповідний генератор
    match language:
        case "Python":
            return _generate_python(blocks, start_block)
        case "C++":
            return _generate_cpp(blocks, start_block)
        case "C#":
            return _generate_csharp(blocks, start_block)
        case "JavaScript":
            return _generate_js(blocks, start_block)
        case _:
            return ["# Unsupported language"]

# ======================== PYTHON ========================
def _generate_python(blocks: List[Block.Block], start_block: Block.Block) -> List[str]:
    code_lines: List[str] = []
    visited = set()

    def dfs(block: Block.Block, indent: int = 0):
        if block in visited:
            return
        visited.add(block)
        prefix = "    " * indent

        if block.type == "start":
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "variable":
            name = block.variableName or ""
            val = block.variableValue or ""
            if name and val:
                code_lines.append(f"{prefix}{name} = {val}")
            else:
                code_lines.append(f"{prefix}# TODO: variable or value missing")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "input":
            var = block.inputVariable or "var"
            code_lines.append(f'{prefix}{var} = input("Введіть {var}: ")')
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "operation":
            op = block.operationText or ""
            if op:
                code_lines.append(f"{prefix}{op}")
            else:
                code_lines.append(f"{prefix}# TODO: operation not set")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "output":
            out = block.outputVariable or ""
            if out:
                code_lines.append(f"{prefix}print({out})")
            else:
                code_lines.append(f"{prefix}# TODO: output not set")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "condition":
            cond = block.condition or "True"
            code_lines.append(f"{prefix}if {cond}:")
            # True branch
            if block.conditionTrueBlock:
                dfs(block.conditionTrueBlock, indent + 1)
            else:
                code_lines.append(f"{prefix}    pass  # TODO: true branch")
            # False branch
            code_lines.append(f"{prefix}else:")
            if block.conditionFalseBlock:
                dfs(block.conditionFalseBlock, indent + 1)
            else:
                code_lines.append(f"{prefix}    pass  # TODO: false branch")

            # Об’єднаємо гілки, якщо вони сходяться
            next_blocks = []
            if block.conditionTrueBlock and block.conditionTrueBlock.connectedToBlock:
                next_blocks.append(block.conditionTrueBlock.connectedToBlock)
            if block.conditionFalseBlock and block.conditionFalseBlock.connectedToBlock:
                next_blocks.append(block.conditionFalseBlock.connectedToBlock)
            if next_blocks:
                dfs(next_blocks[0], indent)

        elif block.type == "end":
            code_lines.append(f"{prefix}# Кінець програми")
            return

        else:
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

    dfs(start_block, 0)
    return code_lines


# ======================== C++ ========================
def _generate_cpp(blocks: List[Block.Block], start_block: Block.Block) -> List[str]:
    code_lines: List[str] = []
    visited = set()

    # Додаємо базовий заголовок
    code_lines.append("#include <iostream>")
    code_lines.append("using namespace std;")
    code_lines.append("")
    code_lines.append("int main() {")

    def dfs(block: Block.Block, indent: int = 1):
        if block in visited:
            return
        visited.add(block)
        prefix = "    " * indent

        if block.type == "start":
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "variable":
            name = block.variableName or ""
            val = block.variableValue or ""
            if name and val:
                code_lines.append(f"{prefix}int {name} = {val};")
            else:
                code_lines.append(f"{prefix}// TODO: variable or value missing for C++")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "input":
            var = block.inputVariable or "var"
            code_lines.append(f"{prefix}int {var};")
            code_lines.append(f"{prefix}cin >> {var};")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "operation":
            op = block.operationText or ""
            if op:
                # Переконаємося, що є крапка-з комою
                line = op if op.strip().endswith(";") else op.strip() + ";"
                code_lines.append(f"{prefix}{line}")
            else:
                code_lines.append(f"{prefix}// TODO: operation not set")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "output":
            out = block.outputVariable or ""
            if out:
                code_lines.append(f"{prefix}cout << {out} << endl;")
            else:
                code_lines.append(f"{prefix}// TODO: output not set")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "condition":
            cond = block.condition or "true"
            code_lines.append(f"{prefix}if ({cond}) {{")
            # True branch
            if block.conditionTrueBlock:
                dfs(block.conditionTrueBlock, indent + 1)
            else:
                code_lines.append(f"{prefix}    // TODO: true branch")
            code_lines.append(f"{prefix}}} else {{")
            # False branch
            if block.conditionFalseBlock:
                dfs(block.conditionFalseBlock, indent + 1)
            else:
                code_lines.append(f"{prefix}    // TODO: false branch")
            code_lines.append(f"{prefix}}}")

            # Об’єднання гілок
            next_blocks = []
            if block.conditionTrueBlock and block.conditionTrueBlock.connectedToBlock:
                next_blocks.append(block.conditionTrueBlock.connectedToBlock)
            if block.conditionFalseBlock and block.conditionFalseBlock.connectedToBlock:
                next_blocks.append(block.conditionFalseBlock.connectedToBlock)
            if next_blocks:
                dfs(next_blocks[0], indent)

        elif block.type == "end":
            # Завершення main
            code_lines.append(f"{prefix}return 0;")
            return

        else:
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

    dfs(start_block, 1)
    code_lines.append("}")
    return code_lines


# ======================== C# ========================
def _generate_csharp(blocks: List[Block.Block], start_block: Block.Block) -> List[str]:
    code_lines: List[str] = []
    visited = set()

    # Додаємо базовий заголовок
    code_lines.append("using System;")
    code_lines.append("")
    code_lines.append("class Program {")
    code_lines.append("    static void Main(string[] args) {")

    def dfs(block: Block.Block, indent: int = 2):
        if block in visited:
            return
        visited.add(block)
        prefix = "    " * indent

        if block.type == "start":
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "variable":
            name = block.variableName or ""
            val = block.variableValue or ""
            if name and val:
                code_lines.append(f"{prefix}int {name} = {val};")
            else:
                code_lines.append(f"{prefix}// TODO: variable or value missing for C#")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "input":
            var = block.inputVariable or "var"
            code_lines.append(f"{prefix}int {var} = int.Parse(Console.ReadLine());")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "operation":
            op = block.operationText or ""
            if op:
                line = op if op.strip().endswith(";") else op.strip() + ";"
                code_lines.append(f"{prefix}{line}")
            else:
                code_lines.append(f"{prefix}// TODO: operation not set")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "output":
            out = block.outputVariable or ""
            if out:
                code_lines.append(f"{prefix}Console.WriteLine({out});")
            else:
                code_lines.append(f"{prefix}// TODO: output not set")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "condition":
            cond = block.condition or "true"
            code_lines.append(f"{prefix}if ({cond}) {{")
            # True branch
            if block.conditionTrueBlock:
                dfs(block.conditionTrueBlock, indent + 1)
            else:
                code_lines.append(f"{prefix}    // TODO: true branch")
            code_lines.append(f"{prefix}}} else {{")
            # False branch
            if block.conditionFalseBlock:
                dfs(block.conditionFalseBlock, indent + 1)
            else:
                code_lines.append(f"{prefix}    // TODO: false branch")
            code_lines.append(f"{prefix}}}")

            # Об’єднання гілок
            next_blocks = []
            if block.conditionTrueBlock and block.conditionTrueBlock.connectedToBlock:
                next_blocks.append(block.conditionTrueBlock.connectedToBlock)
            if block.conditionFalseBlock and block.conditionFalseBlock.connectedToBlock:
                next_blocks.append(block.conditionFalseBlock.connectedToBlock)
            if next_blocks:
                dfs(next_blocks[0], indent)

        elif block.type == "end":
            # Завершуємо Main
            return

        else:
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

    dfs(start_block, 2)
    code_lines.append("    }")
    code_lines.append("}")
    return code_lines


# ======================== JavaScript ========================
def _generate_js(blocks: List[Block.Block], start_block: Block.Block) -> List[str]:
    code_lines: List[str] = []
    visited = set()

    # У JS не треба заголовків—одразу скрипт
    def dfs(block: Block.Block, indent: int = 0):
        if block in visited:
            return
        visited.add(block)
        prefix = "    " * indent

        if block.type == "start":
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "variable":
            name = block.variableName or ""
            val = block.variableValue or ""
            if name and val:
                code_lines.append(f"{prefix}let {name} = {val};")
            else:
                code_lines.append(f"{prefix}// TODO: variable or value missing for JS")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "input":
            var = block.inputVariable or "var"
            code_lines.append(f'{prefix}let {var} = prompt("Введіть {var}:");')
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "operation":
            op = block.operationText or ""
            if op:
                line = op if op.strip().endswith(";") else op.strip() + ";"
                code_lines.append(f"{prefix}{line}")
            else:
                code_lines.append(f"{prefix}// TODO: operation not set")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "output":
            out = block.outputVariable or ""
            if out:
                code_lines.append(f"{prefix}console.log({out});")
            else:
                code_lines.append(f"{prefix}// TODO: output not set")
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

        elif block.type == "condition":
            cond = block.condition or "true"
            code_lines.append(f"{prefix}if ({cond}) {{")
            # True branch
            if block.conditionTrueBlock:
                dfs(block.conditionTrueBlock, indent + 1)
            else:
                code_lines.append(f"{prefix}    // TODO: true branch")
            code_lines.append(f"{prefix}}} else {{")
            # False branch
            if block.conditionFalseBlock:
                dfs(block.conditionFalseBlock, indent + 1)
            else:
                code_lines.append(f"{prefix}    // TODO: false branch")
            code_lines.append(f"{prefix}}}")

            # Об’єднання гілок
            next_blocks = []
            if block.conditionTrueBlock and block.conditionTrueBlock.connectedToBlock:
                next_blocks.append(block.conditionTrueBlock.connectedToBlock)
            if block.conditionFalseBlock and block.conditionFalseBlock.connectedToBlock:
                next_blocks.append(block.conditionFalseBlock.connectedToBlock)
            if next_blocks:
                dfs(next_blocks[0], indent)

        elif block.type == "end":
            return

        else:
            if block.connectedToBlock:
                dfs(block.connectedToBlock, indent)

    dfs(start_block, 0)
    return code_lines
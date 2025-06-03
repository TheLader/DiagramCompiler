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


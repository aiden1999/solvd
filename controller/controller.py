import random
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

import backend.sudoku_solving
import controller.data_structs
import ui.sudoku.puzzle


def show_page(frame_choice: ttk.Frame, previous_frame: ttk.Frame | str):
    if not isinstance(previous_frame, str):
        hide_widget(previous_frame)
    frame_choice.grid(row=0, column=0)


def change_title(app: tk.Tk | tk.Toplevel, app_title: str):
    app.title(app_title)


def enable_button(button: ttk.Button):
    button["state"] = "normal"


def disable_button(button: ttk.Button):
    button["state"] = "disabled"


def clear_combobox(combobox: ttk.Combobox):
    combobox.set("")


def show_example_image(choice: str, image_label: ttk.Label):
    choice = choice.lower()
    choice = choice.replace(" ", "_")
    choice = choice.replace("(", "")
    choice = choice.replace(")", "")
    img = ImageTk.PhotoImage(Image.open("images/" + choice + ".png"))
    image_label["image"] = img
    image_label.image = img


def solve_sudoku(puzzle: ui.sudoku.puzzle.PuzzlePage):
    known_vars = []
    all_vars = []
    empty_cells = []
    for cell in puzzle.puzzle_grid.cells:
        value = cell.get_text()
        if value == "":
            value = 0
            empty_cells.append(cell)
        else:
            known_vars.append(
                controller.data_structs.SudokuVar(int(value), cell.row, cell.col, cell.box)
            )
        all_vars.append(controller.data_structs.SudokuVar(int(value), cell.row, cell.col, cell.box))
    solution = backend.sudoku_solving.get_solution(known_vars, all_vars, puzzle)
    if solution == 0:
        pass
        # TODO: return error
    else:
        for cell in empty_cells:
            for var in solution:
                if (cell.row == var.row) and (cell.col == var.col):
                    cell.true_value = var.value
                    solution.remove(var)
                    break


def hide_widget(widget: tk.Widget):
    widget.grid_remove()


def reveal_random_cell(puzzle: ui.sudoku.puzzle.PuzzlePage):
    empty_cells = []
    for cell in puzzle.puzzle_grid.cells:
        if cell.is_empty():
            empty_cells.append(cell)
    empty_cells_total = len(empty_cells)
    chosen_cell_index = random.randrange(empty_cells_total)
    chosen_cell = empty_cells[chosen_cell_index]
    chosen_cell.show_true_value()
    if empty_cells_total == 1:
        hide_widget(puzzle.random_button)


def reveal_specific_cells(puzzle: ui.sudoku.puzzle.PuzzlePage):
    for chosen_cell in puzzle.chosen_cells:
        for cell in puzzle.puzzle_grid.cells:
            if (chosen_cell.row == cell.row) and (chosen_cell.col == cell.col):
                cell.show_true_value()
                break

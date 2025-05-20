import tkinter as tk
from random import randrange
from tkinter import ttk

from PIL import Image, ImageTk

from backend.sudoku_solving import get_solution
from controller.data_structs import SudokuVar


def show_page(frame_choice: ttk.Frame, previous_frame: ttk.Frame | str):
    if not isinstance(previous_frame, str):
        hide_widget(previous_frame)
    frame_choice.grid(row=0, column=0)


def change_title(app: tk.Tk | tk.Toplevel, app_title: str):
    app.title(app_title)


def goto_main_menu(app, current_page: ttk.Frame):
    show_page(app.choose_puzzle_page, current_page)
    change_title(app, "Solvd - Select your puzzle")


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


def solve_sudoku(cells, dim: int, ratio: str):
    known_vars = []
    all_vars = []
    empty_cells = []
    for cell in cells:
        value = cell.get_text()
        if value == "":
            value = 0
            empty_cells.append(cell)
        else:
            known_vars.append(SudokuVar(int(value), cell.row, cell.col, cell.box))
        all_vars.append(SudokuVar(int(value), cell.row, cell.col, cell.box))
    solution = get_solution(known_vars, all_vars, dim, ratio)
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


def hide_widget(widget):
    widget.grid_remove()


def reveal_random_cell(sudoku_frame):
    empty_cells = []
    for cell in sudoku_frame.puzzle_grid.cells:
        if cell.is_empty():
            empty_cells.append(cell)
    empty_cells_total = len(empty_cells)
    chosen_cell_index = randrange(empty_cells_total)
    chosen_cell = empty_cells[chosen_cell_index]
    chosen_cell.show_true_value()
    if empty_cells_total == 1:
        hide_widget(sudoku_frame.random_button)


def reveal_specific_cells(sudoku_frame):
    for chosen_cell in sudoku_frame.chosen_cells:
        for cell in sudoku_frame.puzzle_grid.cells:
            if (chosen_cell.row == cell.row) and (chosen_cell.col == cell.col):
                cell.show_true_value()
                break

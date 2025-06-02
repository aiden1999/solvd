"""Bridging between the backend and UI.

Abstractify functions on UI elements also.
"""

import random
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

import backend.sudoku_solving
import controller.data_structs
import ui.sudoku.puzzle


def show_page(frame_choice: ttk.Frame, previous_frame: ttk.Frame | str):
    """Change which frame is currently visible.

    Args:
        frame_choice: the frame to be shown.
        previous_frame: the current frame, which will be hidden.
    """
    if not isinstance(previous_frame, str):
        hide_widget(previous_frame)
    frame_choice.grid(row=0, column=0)


def change_title(app: tk.Tk | tk.Toplevel, app_title: str):
    """Change the title of a window.

    Args:
        app: the window in question.
        app_title: text for the title to be changed to.
    """
    app.title(app_title)


def enable_button(button: ttk.Button):
    """Enable a button so it can be clicked.

    Args:
        button: the button to be enabled.
    """
    button["state"] = "normal"


def disable_button(button: ttk.Button):
    """Disable a button so it cannot be clicked.

    Args:
        button: the button to be disabled.
    """
    button["state"] = "disabled"


def clear_combobox(combobox: ttk.Combobox):
    """Clear a selection from a combobox.

    Args:
        combobox: the combobox to be cleared.
    """
    combobox.set("")


def show_example_image(choice: str, image_label: ttk.Label):
    """Display an image showing an example of the chosen puzzle type.

    Args:
        choice: chosen puzzle type.
        image_label: image container.
    """
    choice = choice.lower()
    choice = choice.replace(" ", "_")
    choice = choice.replace("(", "")
    choice = choice.replace(")", "")
    img = ImageTk.PhotoImage(Image.open("images/" + choice + ".png"))
    image_label.configure(image=img)
    image_label.image = img


def solve_sudoku(puzzle: ui.sudoku.puzzle.PuzzlePage):
    """Solve a standard sudoku puzzle.

    Args:
        puzzle: the puzzle to be solved.
    """
    known_vars = []
    all_vars = []
    for cell in puzzle.puzzle_grid.cells:
        value = cell.get_text()
        if value == "":
            value = 0
        elif cell.is_guess:
            value = 0
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
        for cell in puzzle.puzzle_grid.cells:
            for var in solution:
                if (cell.row == var.row) and (cell.col == var.col):
                    cell.true_value = var.value
                    solution.remove(var)
                    break


def hide_widget(widget: tk.Widget):
    """Remove a widget.

    Args:
        widget: widget to be removed.
    """
    widget.grid_remove()


def reveal_random_cell(puzzle: ui.sudoku.puzzle.PuzzlePage):
    """Reveal the solved value of a random cell.

    Args:
        puzzle: the puzzle.
    """
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
    """Reveal the solved values of a set of chosen cells.

    Args:
        puzzle: the puzzle.
    """
    for chosen_cell in puzzle.chosen_cells:
        for cell in puzzle.puzzle_grid.cells:
            if (chosen_cell.row == cell.row) and (chosen_cell.col == cell.col):
                cell.show_true_value()
                break

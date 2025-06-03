"""Bridging between the backend and UI."""

import random

import backend.sudoku_solving
import controller.data_structs
import controller.ui_ctrl
import ui.sudoku.puzzle


def solve_sudoku(puzzle: "ui.sudoku.puzzle.PuzzlePage"):
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


def reveal_random_cell(puzzle: "ui.sudoku.puzzle.PuzzlePage"):
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
        controller.ui_ctrl.hide_widget(puzzle.random_button)


def reveal_specific_cells(puzzle: "ui.sudoku.puzzle.PuzzlePage"):
    """Reveal the solved values of a set of chosen cells.

    Args:
        puzzle: the puzzle.
    """
    for chosen_cell in puzzle.chosen_cells:
        for cell in puzzle.puzzle_grid.cells:
            if (chosen_cell.row == cell.row) and (chosen_cell.col == cell.col):
                cell.show_true_value()
                break

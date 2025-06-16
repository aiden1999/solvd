"""Miscellaneous functions that have a more general purpose.

These typically are related to the backend, i.e. solving, rather than anything relating to the UI.
"""

import math

import ui.sudoku.puzzle


def calculate_box_index(puzzle: "ui.sudoku.puzzle.PuzzlePage", col: int, row: int) -> int:
    """Calculate the box value for a Sudoku cell based on its column and row values.

    Args:
        puzzle: contains information on the dimension of the puzzle.
        col: column value of the cell.
        row: row value of the cell.

    Returns:
        box value of the cell.
    """
    if puzzle.ratio == "square":
        box_size = calculate_square_box_size(puzzle.dimension)
        x = col // box_size
        y = (row // box_size) * box_size
    else:
        box_size_short, box_size_long = calculate_box_sizes(puzzle.dimension)
        if puzzle.ratio == "wide":
            x = col // box_size_long
            y = (row // box_size_short) * box_size_short
        if puzzle.ratio == "tall":
            x = col // box_size_short
            y = (row // box_size_long) * box_size_long
    box_index = int(x) + int(y)
    return box_index


def calculate_square_box_size(dimension: int) -> int:
    """Calculate the box size of a square Sudoku (e.g. 9 x 9) puzzle.

    Args:
        dimension: the side length of the puzzle.

    Returns:
        the box length of the puzzle.
    """
    return int(math.sqrt(dimension))


def calculate_box_sizes(dimension: int) -> tuple[int, int]:
    """Calculate the box sizes of a non-square Sudoku puzzle.

    Args:
        dimension: the side length of the puzzle.

    Returns:
        the box length and width of the puzzle
    """
    if dimension == 12:
        box_size_short = 3
    else:
        box_size_short = 2
    box_size_long = dimension // box_size_short
    return box_size_short, box_size_long


def calculate_butterfly_box_index(row: int, col: int) -> int:
    """[TODO:description]

    Args:
        row: [TODO:description]
        col: [TODO:description]

    Returns:
        [TODO:return]
    """
    x = col // 3
    y = (row // 3) * 4
    return x + y


def calculate_cross_box_index(row: int, col: int) -> int:
    """[TODO:description]

    Args:
        row: [TODO:description]
        col: [TODO:description]

    Returns:
        [TODO:return]
    """
    match row:
        case num if 0 <= num <= 5:
            if 6 <= col <= 14:
                x = (col - 6) // 3
                y = (row // 3) * 3
        case num if 6 <= num <= 14:
            x = col // 3
            y = (7 * (row // 3)) - 8
        case num if 15 <= num <= 20:
            if 6 <= col <= 14:
                x = (col - 6) // 3
                y = ((row // 3) * 3) + 12
    box = int(x) + int(y)
    return box

import math

import ui.sudoku.puzzle


def calculate_box_index(puzzle: ui.sudoku.puzzle.PuzzlePage, col: int, row: int) -> int:
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
    return int(math.sqrt(dimension))


def calculate_box_sizes(dimension: int) -> tuple[int, int]:
    if dimension == 12:
        box_size_short = 3
    else:
        box_size_short = 2
    box_size_long = dimension // box_size_short
    return box_size_short, box_size_long

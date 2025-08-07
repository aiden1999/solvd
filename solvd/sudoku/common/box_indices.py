"""Functions to do with calculating box indices for sudoku solving."""

import math

import solvd.sudoku.ui.puzzle_page as ui_pp
import solvd.sudoku.common.box_lookup_tables as box_lookup


def calculate_standard(puzzle: "ui_pp.PuzzlePage", col: int, row: int) -> int:
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


def calculate_butterfly(row: int, col: int) -> int:
    """Calculate the box value for cells in a butterfly sudoku puzzle.

    Args:
        row: row value of the cell.
        col: column value of the cell.

    Returns:
        box value of the cell.
    """
    return box_lookup.BUTTERFLY_LOOKUP[(row, col)]


def calculate_cross(row: int, col: int) -> int:
    """Calculate the box value for cells in a cross sudoku puzzle.

    Args:
        row: row value of the cell.
        col: column value of the cell.

    Returns:
        box value of the cell.
    """
    return box_lookup.CROSS_LOOKUP[(row, col)]


def calculate_flower(row: int, col: int) -> int:
    """Calculate the box value for cells in a flower sudoku puzzle.

    Args:
        row: row value of the cell.
        col: column value of the cell.

    Returns:
        box value of the cell.
    """
    return box_lookup.FLOWER_LOOKUP[(row, col)]


def calculate_gattai(row: int, col: int) -> int:
    """Calculate the box value for cells in a gattai-3 sudoku puzzle.

    Args:
        row: row value of the cell.
        col: column value of the cell.

    Returns:
        box value of the cell.
    """
    return box_lookup.GATTAI_LOOKUP[(row, col)]


def calculate_kazaguruma(row: int, col: int) -> int:
    """Calculate the box value for cells in a kazaguruma sudoku puzzle.

    Args:
        row: row value of the cell.
        col: column value of the cell.

    Returns:
        box value of the cell.
    """
    return box_lookup.KAZAGURUMA_LOOKUP[(row, col)]


def calculate_samurai(row: int, col: int) -> int:
    """[TODO:description]

    Args:
        row: [TODO:description]
        col: [TODO:description]

    Returns:
        [TODO:return]
    """
    return box_lookup.SAMURAI_LOOKUP[(row, col)]


def calculate_sohei(row: int, col: int) -> int:
    """[TODO:description]

    Args:
        row: [TODO:description]
        col: [TODO:description]

    Returns:
        [TODO:return]
    """
    return box_lookup.SOHEI_LOOKUP[(row, col)]


def calculate_tripledoku(): ...


def calculate_twodoku(): ...

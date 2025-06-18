"""Backend of solving standard sudoku."""

import pysat.solvers

import backend.misc_funcs
import controller.data_structs
import ui.sudoku.puzzle


def get_solution(
    known_vars: list[controller.data_structs.SudokuVar],
    all_vars: list[controller.data_structs.SudokuVar],
    puzzle: "ui.sudoku.puzzle.PuzzlePage",
):
    """Works out solution to sudoku.

    Args:
        known_vars: list of known true variables.
        all_vars: list of all possible variables.
        puzzle: the sudoku puzzle.

    Returns:
        the solution, or 0 if no solution is found.
    """
    match puzzle.type:
        case "standard":
            puzzle_clauses = make_standard_clauses(all_vars, puzzle)
        case "multidoku":
            match puzzle.subtype:
                case "Butterfly Sudoku":
                    puzzle_clauses = make_butterfly_clauses(all_vars)
                case "Cross Sudoku":
                    puzzle_clauses = make_cross_clauses(all_vars)
                case _:
                    pass
        case "variants":
            pass
    known_value_clauses = make_known_value_clauses(known_vars, puzzle.dimension)
    all_clauses = known_value_clauses + puzzle_clauses
    sat_solver = pysat.solvers.Glucose3()
    for clause in all_clauses:
        sat_solver.add_clause(clause)
    if sat_solver.solve():
        solution = sat_solver.get_model()
        return model_to_sudokuvar(solution, puzzle)
    else:
        return 0


def make_standard_clauses(
    all_vars: list[controller.data_structs.SudokuVar], puzzle: "ui.sudoku.puzzle.PuzzlePage"
) -> list[int]:
    """Creates CNF clauses for a standard sudoku puzzle.

    Args:
        all_vars: list of all possible variables.
        puzzle: the sudoku puzzle.

    Returns:
        list of CNF clauses.
    """
    dim = puzzle.dimension
    cell_clauses = make_cell_clauses(all_vars, dim, dim)
    row_clauses = make_row_clauses(all_vars, dim, dim, dim)
    col_clauses = make_column_clauses(all_vars, dim, dim, dim)
    box_clauses = make_box_clauses(all_vars, dim, dim, dim)
    standard_clauses = cell_clauses + row_clauses + col_clauses + box_clauses
    return standard_clauses


def make_butterfly_clauses(all_vars: list[controller.data_structs.SudokuVar]) -> list[int]:
    """Creates CNF clauses for a butterfly sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    cell_clauses = make_cell_clauses(all_vars, 12, 9)
    tl = []
    tr = []
    bl = []
    br = []
    for var in all_vars:
        match var.box:
            case 0:
                tl.append(var)
            case 1 | 2:
                tl.append(var)
                tr.append(var)
            case 3:
                tr.append(var)
            case 4 | 8:
                tl.append(var)
                bl.append(var)
            case 5 | 6 | 9 | 10:
                tl.append(var)
                tr.append(var)
                bl.append(var)
                br.append(var)
            case 7 | 11:
                tr.append(var)
                br.append(var)
            case 12:
                bl.append(var)
            case 13 | 14:
                bl.append(var)
                br.append(var)
            case 15:
                br.append(var)
    row_clauses = (
        make_row_clauses(tl, 12, 9, 8)
        + make_row_clauses(tr, 12, 9, 11)
        + make_row_clauses(bl, 12, 9, 8)
        + make_row_clauses(br, 12, 9, 11)
    )
    col_clauses = (
        make_column_clauses(tl, 12, 9, 8)
        + make_column_clauses(tr, 12, 9, 8)
        + make_column_clauses(bl, 12, 9, 11)
        + make_column_clauses(br, 12, 9, 11)
    )
    box_clauses = (
        make_box_clauses(tl, 12, 9, 16)
        + make_box_clauses(tr, 12, 9, 16)
        + make_box_clauses(bl, 12, 9, 16)
        + make_box_clauses(br, 12, 9, 16)
    )
    butterfly_clauses = cell_clauses + row_clauses + col_clauses + box_clauses
    return butterfly_clauses


def make_cross_clauses(all_vars: list[controller.data_structs.SudokuVar]) -> list[int]:
    """Create CNF clauses for a cross sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    cell_clauses = make_cell_clauses(all_vars, 21, 9)
    top_puzzle = []
    left_puzzle = []
    center_puzzle = []
    right_puzzle = []
    bottom_puzzle = []
    for var in all_vars:
        match var.box:
            case 0 | 1 | 2 | 3 | 4 | 5:
                top_puzzle.append(var)
            case 6 | 7 | 13 | 14 | 20 | 21:
                left_puzzle.append(var)
            case 8:
                top_puzzle.append(var)
                left_puzzle.append(var)
                center_puzzle.append(var)
            case 9:
                top_puzzle.append(var)
                center_puzzle.append(var)
            case 10:
                top_puzzle.append(var)
                center_puzzle.append(var)
                right_puzzle.append(var)
            case 11 | 12 | 18 | 19 | 25 | 26:
                right_puzzle.append(var)
            case 15:
                left_puzzle.append(var)
                center_puzzle.append(var)
            case 16:
                center_puzzle.append(var)
            case 17:
                center_puzzle.append(var)
            case 22:
                left_puzzle.append(var)
                center_puzzle.append(var)
                bottom_puzzle.append(var)
            case 23:
                center_puzzle.append(var)
                bottom_puzzle.append(var)
            case 24:
                center_puzzle.append(var)
                right_puzzle.append(var)
                bottom_puzzle.append(var)
            case 27 | 28 | 29 | 30 | 31 | 32:
                right_puzzle.append(var)
    row_clauses = (
        make_row_clauses(top_puzzle, 21, 9, 14)
        + make_row_clauses(left_puzzle, 21, 9, 8)
        + make_row_clauses(center_puzzle, 21, 9, 14)
        + make_row_clauses(right_puzzle, 21, 9, 20)
        + make_row_clauses(bottom_puzzle, 21, 9, 14)
    )
    column_clauses = (
        make_column_clauses(top_puzzle, 21, 9, 8)
        + make_column_clauses(left_puzzle, 21, 9, 14)
        + make_column_clauses(center_puzzle, 21, 9, 14)
        + make_column_clauses(right_puzzle, 21, 9, 14)
        + make_column_clauses(bottom_puzzle, 21, 9, 20)
    )
    box_clauses = (
        make_box_clauses(top_puzzle, 21, 9, 33)
        + make_box_clauses(left_puzzle, 21, 9, 33)
        + make_box_clauses(center_puzzle, 21, 9, 33)
        + make_box_clauses(right_puzzle, 21, 9, 33)
        + make_box_clauses(bottom_puzzle, 21, 9, 33)
    )
    cross_clauses = cell_clauses + row_clauses + column_clauses + box_clauses
    return cross_clauses


def make_known_value_clauses(
    vars: list[controller.data_structs.SudokuVar], dimension: int
) -> list[int]:
    """Make CNF clauses for the known values from clues.

    Args:
        vars: list of variables.
        dimension: size of sudoku.

    Returns:
        list of CNF clauses.
    """
    clauses = []
    for var in vars:
        var_coords = var_coords_to_str(var, dimension)
        clause = str(var.value) + var_coords
        clauses.append([int(clause)])
    return clauses


def make_cell_clauses(
    vars: list[controller.data_structs.SudokuVar], dimension: int, max_num: int
) -> list[int]:
    """Make clauses for where every cell contains at least one number.

    Args:
        vars: list of variables.
        dimension: size of sudoku.
        max_num: highest number a cell can take.

    Returns:
        list of CNF clauses.
    """
    clauses = []
    for var in vars:
        temp_clause = []
        var_coords = var_coords_to_str(var, dimension)
        for value in range(1, max_num + 1):
            new_var = str(value) + var_coords
            temp_clause.append(int(new_var))
        clauses.append(temp_clause)
    return clauses


def make_row_clauses(
    vars: list[controller.data_structs.SudokuVar], dimension: int, max_num: int, max_col: int
) -> list[int]:
    """Make clauses for where every number occurs at most once per row.

    Args:
        vars: list of variables.
        dimension: size of sudoku.
        max_num: highest number a cell can take.
        max_col: highest index of a column.

    Returns:
        list of CNF clauses.
    """
    clauses = []
    for var in vars:
        row = attr_to_str(var.row, dimension)
        col_1 = attr_to_str(var.col, dimension)
        for i in range(var.col + 1, max_col + 1):
            col_2 = attr_to_str(i, dimension)
            for value in range(1, max_num + 1):
                lit_1 = str(value) + row + col_1
                lit_2 = str(value) + row + col_2
                clause = [-int(lit_1), -int(lit_2)]
                clauses.append(clause)
    return clauses


def make_column_clauses(
    vars: list[controller.data_structs.SudokuVar], dimension: int, max_num: int, max_row: int
) -> list[int]:
    """Make clauses for where every number occurs at most once column.

    Args:
        vars: list of variables.
        dimension: size of sudoku.
        max_num: the highest number a cell can take.
        max_row: highest index of a row.

    Returns:
        list of CNF clauses.
    """
    clauses = []
    for var in vars:
        col = attr_to_str(var.col, dimension)
        row_1 = attr_to_str(var.row, dimension)
        for i in range(var.row + 1, max_row + 1):
            row_2 = attr_to_str(i, dimension)
            for value in range(1, max_num + 1):
                lit_1 = str(value) + row_1 + col
                lit_2 = str(value) + row_2 + col
                clause = [-int(lit_1), -int(lit_2)]
                clauses.append(clause)
    return clauses


def make_box_clauses(
    vars: list[controller.data_structs.SudokuVar], dimension: int, max_num: int, total_boxes: int
) -> list[int]:
    """Make clauses for where every number occurs at most once per box.

    Args:
        vars: list of variables.
        dimension: size of sudoku.
        max_num: the highest number a cell can take.
        total_boxes: number of boxes in the puzzle.

    Returns:
        list of CNF clauses.
    """
    clauses = []
    boxes = [[] for _ in range(total_boxes)]
    for var in vars:
        if len(boxes[var.box]) != 0:
            for box_var in boxes[var.box]:
                for value in range(1, max_num + 1):
                    lit_1 = str(value) + var_coords_to_str(box_var, dimension)
                    lit_2 = str(value) + var_coords_to_str(var, dimension)
                    clause = [-int(lit_1), -int(lit_2)]
                    clauses.append(clause)
        boxes[var.box].append(var)
    return clauses


def var_coords_to_str(var: controller.data_structs.SudokuVar, dimension: int) -> str:
    """Convert 'co-ordinates' of SudokuVar to string.

    Args:
        var: the SudokuVar to be converted.
        dimension: size of sudoku.

    Returns:
        converted co-ordinates as a string.
    """
    row = attr_to_str(var.row, dimension)
    col = attr_to_str(var.col, dimension)
    new_var_coords = row + col
    return new_var_coords


def attr_to_str(attr: int, dimension: int) -> str:
    """Convert SudokuVar attribute to a string.

    Args:
        attr: the attribute.
        dimension: size of sudoku.

    Returns:
        attribute as a string.
    """
    new_attr = str(attr)
    if dimension >= 10:
        if attr <= 9:
            new_attr = "0" + new_attr
    return new_attr


def model_to_sudokuvar(
    solution, puzzle: "ui.sudoku.puzzle.PuzzlePage"
) -> list[controller.data_structs.SudokuVar]:
    """Converts solution model to a list of SudokuVars.

    Args:
        solution (list[int]): solution returned by the SAT solver.
        puzzle: the sudoku puzzle.

    Returns:
        solution as a list of SudokuVars.
    """
    # remove negated clauses
    i = 0
    while i < len(solution):
        if solution[i] < 0:
            solution.pop(i)
        else:
            i += 1
    # convert to SudokuVar
    converted_solution = []
    for item in solution:
        item = str(item)
        if puzzle.dimension < 10:
            value = int(item[0])
            row = int(item[1])
            column = int(item[2])
        else:
            if len(item) == 6:
                value = int(item[0:2])
            if len(item) == 5:
                value = int(item[0])
            row = int(item[-2:])
            column = int(item[-4:-2])
        match puzzle.type:
            case "standard":
                box = backend.misc_funcs.calculate_box_index(puzzle, column, row)
            case "multidoku":
                match puzzle.subtype:
                    case "Butterfly Sudoku":
                        box = backend.misc_funcs.calculate_butterfly_box_index(row, column)
                    case "Cross Sudoku":
                        box = backend.misc_funcs.calculate_cross_box_index(row, column)
                    case _:
                        pass
            case _:
                pass
        converted_item = controller.data_structs.SudokuVar(value, row, column, box)
        converted_solution.append(converted_item)
    return converted_solution

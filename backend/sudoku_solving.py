"""Backend of solving standard sudoku."""

import pysat.solvers

import backend.box_indices
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
                case "Flower Sudoku":
                    puzzle_clauses = make_flower_clauses(all_vars)
                case "Gattai-3":
                    puzzle_clauses = make_gattai_clauses(all_vars)
                case "Kazaguruma":
                    puzzle_clauses = make_kazaguruma_clauses(all_vars)
                case "Samurai Sudoku":
                    pass
                case "Sohei Sudoku":
                    pass
                case "Tripledoku":
                    pass
                case "Twodoku":
                    pass
        case "variants":
            match puzzle.subtype:
                case "Argyle Sudoku":
                    pass
                case "Asterisk Sudoku":
                    pass
                case "Center Dot Sudoku":
                    pass
                case "Chain Sudoku":
                    pass
                case "Chain Sudoku 6 x 6":
                    pass
                case "Consecutive Sudoku":
                    pass
                case "Even-Odd Sudoku":
                    pass
                case "Girandola Sudoku":
                    pass
                case "Greater Than Sudoku":
                    pass
                case "Jigsaw Sudoku":
                    pass
                case "Killer Sudoku":
                    pass
                case "Little Killer Sudoku":
                    pass
                case "Rossini Sudoku":
                    pass
                case "Skyscraper Sudoku":
                    pass
                case "Sudoku DG":
                    pass
                case "Sudoku Mine":
                    pass
                case "Sudoku X":
                    pass
                case "Sudoku XV":
                    pass
                case "Sujiken":
                    pass
                case "Vudoku":
                    pass
                case "Windoku":
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
    all_vars: list[controller.data_structs.SudokuVar],
    puzzle: "ui.sudoku.puzzle.PuzzlePage",
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


def make_butterfly_clauses(
    all_vars: list[controller.data_structs.SudokuVar],
) -> list[int]:
    """Creates CNF clauses for a butterfly sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    cell_clauses = make_cell_clauses(all_vars, 12, 9)
    tl, tr, bl, br = [], [], [], []
    for var in all_vars:
        if var.box in [0, 1, 2, 4, 5, 6, 8, 9, 10]:
            tl.append(var)
        if var.box in [1, 2, 3, 5, 6, 7, 9, 10, 11]:
            tr.append(var)
        if var.box in [4, 5, 6, 8, 9, 10, 12, 13, 14]:
            bl.append(var)
        if var.box in [5, 6, 7, 9, 10, 11, 13, 14, 15]:
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


def make_cross_clauses(
    all_vars: list[controller.data_structs.SudokuVar],
) -> list[int]:
    """Create CNF clauses for a cross sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    cell_clauses = make_cell_clauses(all_vars, 21, 9)
    top, left, center, right, bottom = [], [], [], [], []
    for var in all_vars:
        if var.box in [0, 1, 2, 3, 4, 5, 8, 9, 10]:
            top.append(var)
        if var.box in [6, 7, 8, 13, 14, 15, 20, 21, 22]:
            left.append(var)
        if var.box in [8, 9, 10, 15, 16, 17, 22, 23, 24]:
            center.append(var)
        if var.box in [10, 11, 12, 17, 18, 19, 24, 25, 26]:
            right.append(var)
        if var.box in [22, 23, 24, 27, 28, 29, 30, 31, 32]:
            bottom.append(var)
    row_clauses = (
        make_row_clauses(top, 21, 9, 14)
        + make_row_clauses(left, 21, 9, 8)
        + make_row_clauses(center, 21, 9, 14)
        + make_row_clauses(right, 21, 9, 20)
        + make_row_clauses(bottom, 21, 9, 14)
    )
    column_clauses = (
        make_column_clauses(top, 21, 9, 8)
        + make_column_clauses(left, 21, 9, 14)
        + make_column_clauses(center, 21, 9, 14)
        + make_column_clauses(right, 21, 9, 14)
        + make_column_clauses(bottom, 21, 9, 20)
    )
    box_clauses = (
        make_box_clauses(top, 21, 9, 33)
        + make_box_clauses(left, 21, 9, 33)
        + make_box_clauses(center, 21, 9, 33)
        + make_box_clauses(right, 21, 9, 33)
        + make_box_clauses(bottom, 21, 9, 33)
    )
    cross_clauses = cell_clauses + row_clauses + column_clauses + box_clauses
    return cross_clauses


def make_flower_clauses(
    all_vars: list[controller.data_structs.SudokuVar],
) -> list[int]:
    """Create CNF clauses for a flower sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    cell_clauses = make_cell_clauses(all_vars, 15, 9)
    top, left, center, right, bottom = [], [], [], [], []
    for var in all_vars:
        if var.box in [0, 1, 2, 4, 5, 6, 9, 10, 11]:
            top.append(var)
        if var.box in [3, 4, 5, 8, 9, 10, 13, 14, 15]:
            left.append(var)
        if var.box in [4, 5, 6, 9, 10, 11, 14, 15, 16]:
            center.append(var)
        if var.box in [5, 6, 7, 10, 11, 12, 15, 16, 17]:
            right.append(var)
        if var.box in [9, 10, 11, 14, 15, 16, 18, 19, 20]:
            bottom.append(var)
    row_clauses = (
        make_row_clauses(top, 15, 9, 11)
        + make_row_clauses(left, 15, 9, 8)
        + make_row_clauses(center, 15, 9, 11)
        + make_row_clauses(right, 15, 9, 14)
        + make_row_clauses(bottom, 15, 9, 11)
    )
    column_clauses = (
        make_column_clauses(top, 15, 9, 8)
        + make_column_clauses(left, 15, 9, 11)
        + make_column_clauses(center, 15, 9, 11)
        + make_column_clauses(right, 15, 9, 11)
        + make_column_clauses(bottom, 15, 9, 14)
    )
    box_clauses = (
        make_box_clauses(top, 15, 9, 21)
        + make_box_clauses(left, 15, 9, 21)
        + make_box_clauses(center, 15, 9, 21)
        + make_box_clauses(right, 15, 9, 21)
        + make_box_clauses(bottom, 15, 9, 21)
    )
    flower_clauses = cell_clauses + row_clauses + column_clauses + box_clauses
    return flower_clauses


def make_gattai_clauses(
    all_vars: list[controller.data_structs.SudokuVar],
) -> list[int]:
    """Create CNF clauses for a Gattai-3 sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    cell_clauses = make_cell_clauses(all_vars, 15, 9)
    north, east, south_west = [], [], []
    for var in all_vars:
        if var.box in [0, 1, 2, 3, 4, 5, 8, 9, 10]:
            north.append(var)
        if var.box in [4, 5, 6, 9, 10, 11, 14, 15, 16]:
            east.append(var)
        if var.box in [7, 8, 9, 12, 13, 14, 17, 18, 19]:
            south_west.append(var)
    row_clauses = (
        make_row_clauses(north, 15, 9, 11)
        + make_row_clauses(east, 15, 9, 14)
        + make_row_clauses(south_west, 15, 9, 8)
    )
    col_clauses = (
        make_column_clauses(north, 15, 9, 8)
        + make_column_clauses(east, 15, 9, 11)
        + make_column_clauses(south_west, 15, 9, 14)
    )
    box_clauses = (
        make_box_clauses(north, 15, 9, 20)
        + make_box_clauses(east, 15, 9, 20)
        + make_box_clauses(south_west, 15, 9, 20)
    )
    gattai_clauses = cell_clauses + row_clauses + col_clauses + box_clauses
    return gattai_clauses


def make_kazaguruma_clauses(
    all_vars: list[controller.data_structs.SudokuVar],
) -> list[int]:
    cell_clauses = make_cell_clauses(all_vars, 21, 9)
    top, right, center, left, bottom = [], [], [], [], []
    for var in all_vars:
        if var.box in [0, 1, 2, 3, 4, 5, 9, 10, 11]:
            top.append(var)
        if var.box in [6, 7, 8, 12, 13, 14, 19, 20, 21]:
            right.append(var)
        if var.box in [10, 11, 12, 17, 18, 19, 24, 25, 26]:
            center.append(var)
        if var.box in [15, 16, 17, 22, 23, 24, 28, 29, 30]:
            left.append(var)
        if var.box in [25, 26, 27, 31, 32, 33, 34, 35, 36]:
            bottom.append(var)
    row_clauses = (
        make_row_clauses(top, 21, 9, 11)
        + make_row_clauses(right, 21, 9, 20)
        + make_row_clauses(center, 21, 9, 14)
        + make_row_clauses(left, 21, 9, 8)
        + make_row_clauses(bottom, 21, 9, 17)
    )

    col_clauses = (
        make_column_clauses(top, 21, 9, 8)
        + make_column_clauses(right, 21, 9, 11)
        + make_column_clauses(center, 21, 9, 14)
        + make_column_clauses(left, 21, 9, 17)
        + make_column_clauses(bottom, 21, 9, 20)
    )
    box_clauses = (
        make_box_clauses(top, 21, 9, 37)
        + make_box_clauses(right, 21, 9, 37)
        + make_box_clauses(center, 21, 9, 37)
        + make_box_clauses(left, 21, 9, 37)
        + make_box_clauses(bottom, 21, 9, 37)
    )
    kazaguruma_clauses = cell_clauses + row_clauses + col_clauses + box_clauses
    return kazaguruma_clauses


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
    vars: list[controller.data_structs.SudokuVar],
    dimension: int,
    max_num: int,
    max_col: int,
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
    vars: list[controller.data_structs.SudokuVar],
    dimension: int,
    max_num: int,
    max_row: int,
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
    vars: list[controller.data_structs.SudokuVar],
    dimension: int,
    max_num: int,
    total_boxes: int,
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


def var_coords_to_str(
    var: controller.data_structs.SudokuVar, dimension: int
) -> str:
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
            column = int(item[-2:])
            row = int(item[-4:-2])
        match puzzle.type:
            case "standard":
                box = backend.box_indices.calculate_standard(
                    puzzle, column, row
                )
            case "multidoku":
                match puzzle.subtype:
                    case "Butterfly Sudoku":
                        box = backend.box_indices.calculate_butterfly(
                            row, column
                        )
                    case "Cross Sudoku":
                        box = backend.box_indices.calculate_cross(row, column)
                    case "Flower Sudoku":
                        box = backend.box_indices.calculate_flower(row, column)
                    case "Gattai-3":
                        box = backend.box_indices.calculate_gattai(row, column)
                    case "Kazaguruma":
                        box = backend.box_indices.calculate_kazaguruma(
                            row, column
                        )
                    case "Samurai Sudoku":
                        pass
                    case "Sohei Sudoku":
                        pass
                    case "Tripledoku":
                        pass
                    case "Twodoku":
                        pass
            case "variants":
                match puzzle.subtype:
                    case "Argyle Sudoku":
                        pass
                    case "Asterisk Sudoku":
                        pass
                    case "Center Dot Sudoku":
                        pass
                    case "Chain Sudoku":
                        pass
                    case "Chain Sudoku 6 x 6":
                        pass
                    case "Consecutive Sudoku":
                        pass
                    case "Even-Odd Sudoku":
                        pass
                    case "Girandola Sudoku":
                        pass
                    case "Greater Than Sudoku":
                        pass
                    case "Jigsaw Sudoku":
                        pass
                    case "Killer Sudoku":
                        pass
                    case "Little Killer Sudoku":
                        pass
                    case "Rossini Sudoku":
                        pass
                    case "Skyscraper Sudoku":
                        pass
                    case "Sudoku DG":
                        pass
                    case "Sudoku Mine":
                        pass
                    case "Sudoku X":
                        pass
                    case "Sudoku XV":
                        pass
                    case "Sujiken":
                        pass
                    case "Vudoku":
                        pass
                    case "Windoku":
                        pass
        converted_item = controller.data_structs.SudokuVar(
            value, row, column, box
        )
        converted_solution.append(converted_item)
    return converted_solution

"""Backend of solving standard sudoku."""

import pysat.solvers

import solvd.sudoku.common.box_indices as common_bi
import solvd.sudoku.common.sudoku_var as common_sv
import solvd.sudoku.ui.puzzle_page as ui_pp


def get_solution(
    known_vars: list[common_sv.SudokuVar],
    all_vars: list[common_sv.SudokuVar],
    puzzle: "ui_pp.PuzzlePage",
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
                    puzzle_clauses = make_samurai_clauses(all_vars)
                case "Sohei Sudoku":
                    puzzle_clauses = make_sohei_clauses(all_vars)
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


class SubPuzzle:
    """3 x 3 sub sudoku puzzle in variants.

    Attributes:
        dim: size of sudoku.
        max_num: highest number a cell can take.
        max_col: highest index of a column.
        max_row: highest index of a row.
        total_boxes: number of boxes in the puzzle.
        vars: list of variables.
    """

    def __init__(
        self,
        dim: int,
        max_num: int,
        max_col: int,
        max_row: int,
        total_boxes: int,
    ):
        self.dim = dim
        self.max_num = max_num
        self.max_col = max_col
        self.max_row = max_row
        self.total_boxes = total_boxes
        self.vars = []

    def make_row_clauses(self) -> list[int]:
        """Make clauses for where every number occurs at most once per row.

        Returns:
            list of CNF clauses.
        """
        clauses = []
        for var in self.vars:
            row = attr_to_str(var.row, self.dim)
            col_1 = attr_to_str(var.col, self.dim)
            for i in range(var.col + 1, self.max_col + 1):
                col_2 = attr_to_str(i, self.dim)
                for value in range(1, self.max_num + 1):
                    lit_1 = str(value) + row + col_1
                    lit_2 = str(value) + row + col_2
                    clause = [-int(lit_1), -int(lit_2)]
                    clauses.append(clause)
        return clauses

    def make_column_clauses(self) -> list[int]:
        """Make clauses for where every number occurs at most once per column.

        Returns:
            list of CNF clauses.
        """
        clauses = []
        for var in self.vars:
            col = attr_to_str(var.col, self.dim)
            row_1 = attr_to_str(var.row, self.dim)
            for i in range(var.row + 1, self.max_row + 1):
                row_2 = attr_to_str(i, self.dim)
                for value in range(1, self.max_num + 1):
                    lit_1 = str(value) + row_1 + col
                    lit_2 = str(value) + row_2 + col
                    clause = [-int(lit_1), -int(lit_2)]
                    clauses.append(clause)
        return clauses

    def make_box_clauses(self) -> list[int]:
        """Make clauses for where every number occurs at most once per box.

        Returns:
            list of CNF clauses.
        """
        clauses = []
        boxes = [[] for _ in range(self.total_boxes)]
        for var in self.vars:
            if len(boxes[var.box]) != 0:
                for box_var in boxes[var.box]:
                    for value in range(1, self.max_num + 1):
                        lit_1 = str(value) + var_coords_to_str(
                            box_var, self.dim
                        )
                        lit_2 = str(value) + var_coords_to_str(var, self.dim)
                        clause = [-int(lit_1), -int(lit_2)]
                        clauses.append(clause)
            boxes[var.box].append(var)
        return clauses

    def get_clauses(self) -> list[int]:
        """Make row, column and box clauses.

        Returns:
            list of CNF clauses.
        """
        return (
            self.make_row_clauses()
            + self.make_column_clauses()
            + self.make_box_clauses()
        )


def make_standard_clauses(
    all_vars: list[common_sv.SudokuVar], puzzle: "ui_pp.PuzzlePage"
) -> list[int]:
    """Creates CNF clauses for a standard sudoku puzzle.

    Args:
        all_vars: list of all possible variables.
        puzzle: the sudoku puzzle.

    Returns:
        list of CNF clauses.
    """
    dim = puzzle.dimension
    whole_puzzle = SubPuzzle(dim, dim, dim, dim, dim)
    whole_puzzle.vars = all_vars
    return make_cell_clauses(all_vars, dim, dim) + whole_puzzle.get_clauses()


def make_butterfly_clauses(all_vars: list[common_sv.SudokuVar]) -> list[int]:
    """Creates CNF clauses for a butterfly sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    dim, max_num, total_boxes = 12, 9, 16
    tl = SubPuzzle(dim, max_num, 8, 8, total_boxes)
    tr = SubPuzzle(dim, max_num, 11, 8, total_boxes)
    bl = SubPuzzle(dim, max_num, 8, 11, total_boxes)
    br = SubPuzzle(dim, max_num, 11, 11, total_boxes)
    for var in all_vars:
        if var.box in [0, 1, 2, 4, 5, 6, 8, 9, 10]:
            tl.vars.append(var)
        if var.box in [1, 2, 3, 5, 6, 7, 9, 10, 11]:
            tr.vars.append(var)
        if var.box in [4, 5, 6, 8, 9, 10, 12, 13, 14]:
            bl.vars.append(var)
        if var.box in [5, 6, 7, 9, 10, 11, 13, 14, 15]:
            br.vars.append(var)
    return (
        make_cell_clauses(all_vars, dim, max_num)
        + tl.get_clauses()
        + tr.get_clauses()
        + bl.get_clauses()
        + br.get_clauses()
    )


def make_cross_clauses(all_vars: list[common_sv.SudokuVar]) -> list[int]:
    """Create CNF clauses for a cross sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    dim, max_num, total_boxes = 21, 9, 33
    top = SubPuzzle(dim, max_num, 14, 8, total_boxes)
    left = SubPuzzle(dim, max_num, 8, 14, total_boxes)
    center = SubPuzzle(dim, max_num, 14, 14, total_boxes)
    right = SubPuzzle(dim, max_num, 20, 14, total_boxes)
    bottom = SubPuzzle(dim, max_num, 14, 20, total_boxes)
    for var in all_vars:
        if var.box in [0, 1, 2, 3, 4, 5, 8, 9, 10]:
            top.vars.append(var)
        if var.box in [6, 7, 8, 13, 14, 15, 20, 21, 22]:
            left.vars.append(var)
        if var.box in [8, 9, 10, 15, 16, 17, 22, 23, 24]:
            center.vars.append(var)
        if var.box in [10, 11, 12, 17, 18, 19, 24, 25, 26]:
            right.vars.append(var)
        if var.box in [22, 23, 24, 27, 28, 29, 30, 31, 32]:
            bottom.vars.append(var)
    return (
        make_cell_clauses(all_vars, dim, max_num)
        + top.get_clauses()
        + left.get_clauses()
        + center.get_clauses()
        + right.get_clauses()
        + bottom.get_clauses()
    )


def make_flower_clauses(all_vars: list[common_sv.SudokuVar]) -> list[int]:
    """Create CNF clauses for a flower sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    dim, max_num, total_boxes = 15, 9, 21
    top = SubPuzzle(dim, max_num, 11, 8, total_boxes)
    left = SubPuzzle(dim, max_num, 8, 11, total_boxes)
    center = SubPuzzle(dim, max_num, 11, 11, total_boxes)
    right = SubPuzzle(dim, max_num, 14, 11, total_boxes)
    bottom = SubPuzzle(dim, max_num, 11, 14, total_boxes)
    for var in all_vars:
        if var.box in [0, 1, 2, 4, 5, 6, 9, 10, 11]:
            top.vars.append(var)
        if var.box in [3, 4, 5, 8, 9, 10, 13, 14, 15]:
            left.vars.append(var)
        if var.box in [4, 5, 6, 9, 10, 11, 14, 15, 16]:
            center.vars.append(var)
        if var.box in [5, 6, 7, 10, 11, 12, 15, 16, 17]:
            right.vars.append(var)
        if var.box in [9, 10, 11, 14, 15, 16, 18, 19, 20]:
            bottom.vars.append(var)
    return (
        make_cell_clauses(all_vars, dim, max_num)
        + top.get_clauses()
        + left.get_clauses()
        + center.get_clauses()
        + right.get_clauses()
        + bottom.get_clauses()
    )


def make_gattai_clauses(all_vars: list[common_sv.SudokuVar]) -> list[int]:
    """Create CNF clauses for a Gattai-3 sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    dim, max_num, total_boxes = 15, 9, 20
    north = SubPuzzle(dim, max_num, 11, 8, total_boxes)
    east = SubPuzzle(dim, max_num, 14, 11, total_boxes)
    south_west = SubPuzzle(dim, max_num, 8, 14, total_boxes)
    for var in all_vars:
        if var.box in [0, 1, 2, 3, 4, 5, 8, 9, 10]:
            north.vars.append(var)
        if var.box in [4, 5, 6, 9, 10, 11, 14, 15, 16]:
            east.vars.append(var)
        if var.box in [7, 8, 9, 12, 13, 14, 17, 18, 19]:
            south_west.vars.append(var)
    return (
        make_cell_clauses(all_vars, dim, max_num)
        + north.get_clauses()
        + east.get_clauses()
        + south_west.get_clauses()
    )


def make_kazaguruma_clauses(all_vars: list[common_sv.SudokuVar]) -> list[int]:
    """Create CNF clauses for a Kazaguruma sudoku puzzle.

    Args:
        all_vars: list of all possible variables.

    Returns:
        list of CNF clauses.
    """
    dim, max_num, total_boxes = 21, 9, 37
    top = SubPuzzle(dim, max_num, 11, 8, total_boxes)
    right = SubPuzzle(dim, max_num, 20, 11, total_boxes)
    center = SubPuzzle(dim, max_num, 14, 14, total_boxes)
    left = SubPuzzle(dim, max_num, 8, 17, total_boxes)
    bottom = SubPuzzle(dim, max_num, 17, 20, total_boxes)
    for var in all_vars:
        if var.box in [0, 1, 2, 3, 4, 5, 9, 10, 11]:
            top.vars.append(var)
        if var.box in [6, 7, 8, 12, 13, 14, 19, 20, 21]:
            right.vars.append(var)
        if var.box in [10, 11, 12, 17, 18, 19, 24, 25, 26]:
            center.vars.append(var)
        if var.box in [15, 16, 17, 22, 23, 24, 28, 29, 30]:
            left.vars.append(var)
        if var.box in [25, 26, 27, 31, 32, 33, 34, 35, 36]:
            bottom.vars.append(var)
    return (
        make_cell_clauses(all_vars, dim, max_num)
        + top.get_clauses()
        + right.get_clauses()
        + center.get_clauses()
        + left.get_clauses()
        + bottom.get_clauses()
    )


def make_samurai_clauses(all_vars: list[common_sv.SudokuVar]) -> list[int]:
    """[TODO:description]

    Args:
        all_vars: [TODO:description]

    Returns:
        [TODO:return]
    """
    dim, max_num, total_boxes = 21, 9, 41
    top_left = SubPuzzle(dim, max_num, 8, 8, total_boxes)
    top_right = SubPuzzle(dim, max_num, 20, 8, total_boxes)
    center = SubPuzzle(dim, max_num, 14, 14, total_boxes)
    bottom_left = SubPuzzle(dim, max_num, 8, 20, total_boxes)
    bottom_right = SubPuzzle(dim, max_num, 20, 20, total_boxes)
    for var in all_vars:
        if var.box in [0, 1, 2, 6, 7, 8, 12, 13, 14]:
            top_left.vars.append(var)
        if var.box in [3, 4, 5, 9, 10, 11, 16, 17, 18]:
            top_right.vars.append(var)
        if var.box in [14, 15, 16, 19, 20, 21, 24, 25, 26]:
            center.vars.append(var)
        if var.box in [22, 23, 24, 29, 30, 31, 35, 36, 37]:
            bottom_left.vars.append(var)
        if var.box in [26, 27, 28, 32, 33, 34, 38, 39, 40]:
            bottom_right.vars.append(var)
    return (
        make_cell_clauses(all_vars, dim, max_num)
        + top_left.get_clauses()
        + top_right.get_clauses()
        + center.get_clauses()
        + bottom_left.get_clauses()
        + bottom_right.get_clauses()
    )


def make_sohei_clauses(all_vars: list[common_sv.SudokuVar]) -> list[int]:
    """[TODO:description]

    Args:
        all_vars: [TODO:description]

    Returns:
        [TODO:return]
    """
    dim, max_num, total_boxes = 21, 9, 32
    top = SubPuzzle(dim, max_num, 14, 8, total_boxes)
    left = SubPuzzle(dim, max_num, 8, 14, total_boxes)
    right = SubPuzzle(dim, max_num, 20, 14, total_boxes)
    bottom = SubPuzzle(dim, max_num, 14, 20, total_boxes)
    for var in all_vars:
        if var.box in [0, 1, 2, 3, 4, 5, 8, 9, 10]:
            top.vars.append(var)
        if var.box in [6, 7, 8, 13, 14, 15, 19, 20, 21]:
            left.vars.append(var)
        if var.box in [10, 11, 12, 16, 17, 18, 23, 24, 25]:
            right.vars.append(var)
        if var.box in [21, 22, 23, 26, 27, 28, 29, 30, 31]:
            bottom.vars.append(var)
    return (
        make_cell_clauses(all_vars, dim, max_num)
        + top.get_clauses()
        + left.get_clauses()
        + right.get_clauses()
        + bottom.get_clauses()
    )


def make_known_value_clauses(
    vars: list[common_sv.SudokuVar], dimension: int
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
    vars: list[common_sv.SudokuVar], dimension: int, max_num: int
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


def var_coords_to_str(var: common_sv.SudokuVar, dimension: int) -> str:
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
    solution, puzzle: "ui_pp.PuzzlePage"
) -> list[common_sv.SudokuVar]:
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
            col = int(item[2])
        else:
            if len(item) == 6:
                value = int(item[0:2])
            if len(item) == 5:
                value = int(item[0])
            col = int(item[-2:])
            row = int(item[-4:-2])
        match puzzle.type:
            case "standard":
                box = common_bi.calculate_standard(puzzle, col, row)
            case "multidoku":
                match puzzle.subtype:
                    case "Butterfly Sudoku":
                        box = common_bi.calculate_butterfly(row, col)
                    case "Cross Sudoku":
                        box = common_bi.calculate_cross(row, col)
                    case "Flower Sudoku":
                        box = common_bi.calculate_flower(row, col)
                    case "Gattai-3":
                        box = common_bi.calculate_gattai(row, col)
                    case "Kazaguruma":
                        box = common_bi.calculate_kazaguruma(row, col)
                    case "Samurai Sudoku":
                        box = common_bi.calculate_samurai(row, col)
                    case "Sohei Sudoku":
                        box = common_bi.calculate_sohei(row, col)
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
        converted_item = common_sv.SudokuVar(value, row, col, box)
        converted_solution.append(converted_item)
    return converted_solution

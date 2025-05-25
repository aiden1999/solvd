import pysat.solvers

import backend.misc_funcs
import controller.data_structs
import ui.sudoku.puzzle


def get_solution(
    known_vars: list[controller.data_structs.SudokuVar],
    all_vars: list[controller.data_structs.SudokuVar],
    puzzle: ui.sudoku.puzzle.PuzzlePage,
):
    known_value_clauses = make_known_value_clauses(known_vars, puzzle.dimension)
    cell_clauses = make_cell_clauses(all_vars, puzzle.dimension)
    row_clauses = make_row_clauses(all_vars, puzzle.dimension)
    col_clauses = make_column_clauses(all_vars, puzzle.dimension)
    box_clauses = make_box_clauses(all_vars, puzzle.dimension)
    all_clauses = known_value_clauses + cell_clauses + row_clauses + col_clauses + box_clauses
    sat_solver = pysat.solvers.Glucose3()
    for clause in all_clauses:
        sat_solver.add_clause(clause)
    if sat_solver.solve():
        solution = sat_solver.get_model()
        return model_to_sudokuvar(solution, puzzle)
    else:
        return 0


def make_known_value_clauses(
    vars: list[controller.data_structs.SudokuVar], dimension: int
) -> list[int]:
    clauses = []
    for var in vars:
        var_coords = var_coords_to_str(var, dimension)
        clause = str(var.value) + var_coords
        clauses.append([int(clause)])
    return clauses


def make_cell_clauses(vars: list[controller.data_structs.SudokuVar], dimension: int) -> list[int]:
    clauses = []
    for var in vars:
        temp_clause = []
        var_coords = var_coords_to_str(var, dimension)
        for value in range(1, dimension + 1):
            new_var = str(value) + var_coords
            temp_clause.append(int(new_var))
        clauses.append(temp_clause)
    return clauses


def make_row_clauses(vars: list[controller.data_structs.SudokuVar], dimension: int) -> list[int]:
    clauses = []
    for var in vars:
        row = attr_to_str(var.row, dimension)
        col_1 = attr_to_str(var.col, dimension)
        for i in range(var.col + 1, dimension):
            col_2 = attr_to_str(i, dimension)
            for value in range(1, dimension + 1):
                lit_1 = str(value) + row + col_1
                lit_2 = str(value) + row + col_2
                clause = [-int(lit_1), -int(lit_2)]
                clauses.append(clause)
    return clauses


def make_column_clauses(vars: list[controller.data_structs.SudokuVar], dimension: int) -> list[int]:
    clauses = []
    for var in vars:
        col = attr_to_str(var.col, dimension)
        row_1 = attr_to_str(var.row, dimension)
        for i in range(var.row + 1, dimension):
            row_2 = attr_to_str(i, dimension)
            for value in range(1, dimension + 1):
                lit_1 = str(value) + row_1 + col
                lit_2 = str(value) + row_2 + col
                clause = [-int(lit_1), -int(lit_2)]
                clauses.append(clause)
    return clauses


def make_box_clauses(vars: list[controller.data_structs.SudokuVar], dimension: int) -> list[int]:
    clauses = []
    boxes = [[] for _ in range(dimension)]
    for var in vars:
        if len(boxes[var.box]) != 0:
            for box_var in boxes[var.box]:
                for value in range(1, dimension + 1):
                    lit_1 = str(value) + var_coords_to_str(box_var, dimension)
                    lit_2 = str(value) + var_coords_to_str(var, dimension)
                    clause = [-int(lit_1), -int(lit_2)]
                    clauses.append(clause)
        boxes[var.box].append(var)
    return clauses


def var_coords_to_str(var: controller.data_structs.SudokuVar, dimension: int) -> str:
    row = attr_to_str(var.row, dimension)
    col = attr_to_str(var.col, dimension)
    new_var_coords = row + col
    return new_var_coords


def attr_to_str(attr: int, dimension: int) -> str:
    new_attr = str(attr)
    if dimension >= 10:
        if attr <= 9:
            new_attr = "0" + new_attr
    return new_attr


def model_to_sudokuvar(solution, puzzle) -> list[controller.data_structs.SudokuVar]:
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
        box = backend.misc_funcs.calculate_box_index(puzzle, column, row)
        converted_item = controller.data_structs.SudokuVar(value, row, column, box)
        converted_solution.append(converted_item)
    return converted_solution

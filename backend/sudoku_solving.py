from pysat.solvers import Glucose3

from controller.data_structs import SudokuVar


def get_solution(
    known_vars: list[SudokuVar], all_vars: list[SudokuVar], dimension: int
):
    known_value_clauses = make_known_value_clauses(known_vars, dimension)
    cell_clauses = make_cell_clauses(all_vars, dimension)
    row_clauses = make_row_clauses(all_vars, dimension)
    col_clauses = make_column_clauses(all_vars, dimension)
    box_clauses = make_box_clauses(all_vars, dimension)
    all_clauses = (
        known_value_clauses
        + cell_clauses
        + row_clauses
        + col_clauses
        + box_clauses
    )
    sat_solver = Glucose3()
    for clause in all_clauses:
        sat_solver.add_clause(clause)


def make_known_value_clauses(
    vars: list[SudokuVar], dimension: int
) -> list[int]:
    clauses = []
    for var in vars:
        var_coords = var_coords_to_str(var, dimension)
        clause = str(var.value) + var_coords
        clauses.append(int(clause))
    return clauses


def make_cell_clauses(vars: list[SudokuVar], dimension: int) -> list[int]:
    clauses = []
    for var in vars:
        temp_clause = []
        var_coords = var_coords_to_str(var, dimension)
        for value in range(1, dimension + 1):
            new_var = str(value) + var_coords
            temp_clause.append(int(new_var))
        clauses.append(temp_clause)
    return clauses


def make_row_clauses(vars: list[SudokuVar], dimension: int) -> list[int]:
    clauses = []
    for var in vars:
        row = attr_to_str(var.row, dimension)
        col_1 = attr_to_str(var.col, dimension)
        for i in range(var.col + 1, dimension + 1):
            col_2 = attr_to_str(i, dimension)
            for value in range(1, dimension + 1):
                lit_1 = str(value) + row + col_1
                lit_2 = str(value) + row + col_2
                clause = [-int(lit_1), -int(lit_2)]
                clauses.append(clause)
    return clauses


def make_column_clauses(vars: list[SudokuVar], dimension: int) -> list[int]:
    clauses = []
    for var in vars:
        col = attr_to_str(var.row, dimension)
        row_1 = attr_to_str(var.row, dimension)
        for i in range(var.row + 1, dimension + 1):
            row_2 = attr_to_str(i, dimension)
            for value in range(1, dimension + 1):
                lit_1 = str(value) + row_1 + col
                lit_2 = str(value) + row_2 + col
                clause = [-int(lit_1), -int(lit_2)]
                clauses.append(clause)
    return clauses


def make_box_clauses(vars: list[SudokuVar], dimension: int) -> list[int]:
    clauses = []
    boxes = [[]] * dimension
    for var in vars:
        if boxes[var.box]:  # sublist is not empty
            for box_var in boxes[var.box]:
                lit_1 = str(box_var.value) + var_coords_to_str(
                    box_var, dimension
                )
                lit_2 = str(var.value) + var_coords_to_str(var, dimension)
                clause = [-int(lit_1), -int(lit_2)]
                clauses.append(clause)
        boxes[var.box].append(var)
    return clauses


def var_coords_to_str(var: SudokuVar, dimension: int) -> str:
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

"""Miscellaneous data structures/classes"""


class SudokuVar:
    """Represents a Sudoku cell in an abstract way.

    Attributes:
        value: the cell's value.
        row: the cell's row (indexes from 0).
        col: the cell's column (indexes from 0).
        box: the cell's box (indexes from 0).
    """

    def __init__(self, value: int, row: int, col: int, box: int):
        """Create the SudokuVar.

        Args:
            value: the cell's value.
            row: the cell's row (indexes from 0).
            col: the cell's column (indexes from 0).
            box: the cell's box (indexes from 0).
        """
        self.value = value
        self.row = row
        self.col = col
        self.box = box

    def __str__(self) -> str:
        return (
            "v "
            + str(self.value)
            + ", r "
            + str(self.row)
            + ", c "
            + str(self.col)
            + ", b "
            + str(self.box)
        )

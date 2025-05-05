class SudokuVar:
    def __init__(self, value: int, row: int, col: int, box: int):
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

class SudokuVar:
    def __init__(self, value: int, row: int, col: int, box: int):
        self.value = value
        self.row = row
        self.col = col
        self.box = box

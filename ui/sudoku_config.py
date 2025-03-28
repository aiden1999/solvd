import tkinter as tk


class StandardSudokuGrid(tk.Canvas):
    def __init__(self, container, dimension, ratio):
        tk.Canvas.__init__(self, container)

        c1 = 25
        c2 = (25 * 50) + 25
        self.create_polygon(
            c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="white", outline="black"
        )

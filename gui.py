import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Solvd - Select your puzzle")
        puzzle_select_frame = tk.Frame(self)
        solve_sudoku_button = tk.Button(puzzle_select_frame, text="Solve Sudoku")
        solve_water_sort_button = tk.Button(
            puzzle_select_frame, text="Solve Water Sort"
        )
        solve_nonogram_button = tk.Button(puzzle_select_frame, text="Solve Nonogram")
        solve_rubiks_cube_button = tk.Button(
            puzzle_select_frame, text="Solve Rubik's Cube"
        )

        puzzle_select_frame.grid(column=0, row=0)
        solve_sudoku_button.grid(column=0, row=0)
        solve_water_sort_button.grid(column=0, row=1)
        solve_nonogram_button.grid(column=0, row=2)
        solve_rubiks_cube_button.grid(column=0, row=3)

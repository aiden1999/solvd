import tkinter as tk
from tkinter import ttk

import controller.controller
import ui.sudoku.config
import ui.theming


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        colours = ui.theming.load_colours()
        self.configure(background=colours["background0"])
        style = ttk.Style(self)
        ui.theming.configure_style(style)

        self.containing_frame = ttk.Frame(self, style="Background.TFrame")
        self.containing_frame.pack(anchor="center", expand=True)

        # create different frames
        self.choose_puzzle_page = ChoosePuzzleFrame(self)
        self.configure_sudoku_page = ui.sudoku.config.ConfigureSudokuFrame(self)
        self.configure_water_sort_page = ConfigureWaterSortFrame(self.containing_frame)
        self.configure_nonogram_page = ConfigureNonogramFrame(self.containing_frame)
        self.configure_rubiks_cube_page = ConfigureRubiksCubeFrame(self.containing_frame)

        controller.controller.show_page(self.choose_puzzle_page, "none")
        controller.controller.change_title(self, "Solvd - Select your puzzle")


class ChoosePuzzleFrame(ttk.Frame):
    def __init__(self, app_window: App):
        ttk.Frame.__init__(self, app_window.containing_frame)

        self.containing_frame = app_window.containing_frame
        self.app_window = app_window

        self.style = ui.theming.configure_style(self)
        self["style"] = "Background.TFrame"

        solve_sudoku_button = ttk.Button(
            self,
            text="Solve Sudoku",
            command=lambda: self.selected_puzzle("Sudoku", self.app_window.configure_sudoku_page),
            style="Standard.TButton",
        )
        solve_sudoku_button.grid(column=0, row=0, pady=10)

        solve_water_sort_button = ttk.Button(
            self,
            text="Solve Water Sort",
            command=lambda: self.selected_puzzle(
                "Water Sort", self.app_window.configure_water_sort_page
            ),
            style="Standard.TButton",
        )
        solve_water_sort_button.grid(column=0, row=1, pady=10)

        solve_nonogram_button = ttk.Button(
            self,
            text="Solve Nonogram",
            command=lambda: self.selected_puzzle(
                "Nonogram", self.app_window.configure_nonogram_page
            ),
            style="Standard.TButton",
        )
        solve_nonogram_button.grid(column=0, row=2, pady=10)

        solve_rubiks_cube_button = ttk.Button(
            self,
            text="Solve Rubik's Cube",
            command=lambda: self.selected_puzzle(
                "Rubik's Cube",
                self.app_window.configure_rubiks_cube_page,
            ),
            style="Standard.TButton",
        )
        solve_rubiks_cube_button.grid(column=0, row=3, pady=10)

    def selected_puzzle(self, puzzle_type: str, config_page: ttk.Frame):
        controller.controller.show_page(config_page, self.app_window.choose_puzzle_page)
        controller.controller.change_title(self.app_window, "Solvd - Configure " + puzzle_type)


class ConfigureWaterSortFrame(ttk.Frame):
    def __init__(self, containing_frame):
        ttk.Frame.__init__(self, containing_frame)

        label = ttk.Label(self, text="water sort config")
        label.grid(row=0, column=0)


class ConfigureNonogramFrame(ttk.Frame):
    def __init__(self, containing_frame):
        ttk.Frame.__init__(self, containing_frame)

        label = ttk.Label(self, text="nonogram config")
        label.grid(row=0, column=0)


class ConfigureRubiksCubeFrame(ttk.Frame):
    def __init__(self, containing_frame):
        ttk.Frame.__init__(self, containing_frame)

        label = tk.Label(self, text="rubik's cube config")
        label.grid(row=0, column=0)

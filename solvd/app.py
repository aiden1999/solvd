"""GUI for the landing page."""

import tkinter as tk
from tkinter import ttk

import solvd.common.theming as solvd_theming
import solvd.common.ui_ctrl as solvd_ui_ctrl
import solvd.sudoku.ui.configure_sudoku as sudoku_cfg


class App(tk.Tk):
    """Main app, contains everything.

    Attributes:
        containing_frame: frame that is a container for everything.
        choose_puzzle_page: page where a puzzle is chosen.
        configure_sudoku_page: page where sudoku is configured.
        configure_water_sort_page: page where water sort puzzle is configured.
        configure_nonogram_page: page where nonograms are configured.
        configure_rubiks_cube_page: page where Rubik's cube is configured.
    """

    def __init__(self):
        """Initiates the app."""
        tk.Tk.__init__(self)

        colours = solvd_theming.load_colours()
        self.configure(background=colours["bg0"])
        solvd_theming.configure_style()

        self.containing_frame = ttk.Frame(self, style="Background.TFrame")
        self.containing_frame.pack(anchor="center", expand=True)

        # create different frames
        self.choose_puzzle_page = ChoosePuzzleFrame(self)
        self.configure_sudoku_page = sudoku_cfg.ConfigureSudokuFrame(self)
        self.configure_water_sort_page = ConfigureWaterSortFrame(
            self.containing_frame
        )
        self.configure_nonogram_page = ConfigureNonogramFrame(
            self.containing_frame
        )
        self.configure_rubiks_cube_page = ConfigureRubiksCubeFrame(
            self.containing_frame
        )

        solvd_ui_ctrl.show_page(self.choose_puzzle_page, "none")
        solvd_ui_ctrl.change_title(self, "Select your puzzle")


class ChoosePuzzleFrame(ttk.Frame):
    """Page where a puzzle is chosen.

    Attributes:
        containing_frame: frame which contains this frame.
        app_window: parent App.
    """

    def __init__(self, app_window: App):
        """Initiates frame.

        Args:
            app_window: parent App.
        """
        ttk.Frame.__init__(self, app_window.containing_frame)

        self.containing_frame = app_window.containing_frame
        self.app_window = app_window

        self["style"] = "Background.TFrame"

        solve_sudoku_button = ttk.Button(
            self,
            text="Solve Sudoku",
            command=lambda: self.selected_puzzle(
                "Sudoku", self.app_window.configure_sudoku_page
            ),
            style="P1.Std.TButton",
        )
        solve_sudoku_button.grid(column=0, row=0, pady=10)

        solve_water_sort_button = ttk.Button(
            self,
            text="Solve Water Sort",
            command=lambda: self.selected_puzzle(
                "Water Sort", self.app_window.configure_water_sort_page
            ),
            style="P1.Std.TButton",
        )
        solve_water_sort_button.grid(column=0, row=1, pady=10)

        solve_nonogram_button = ttk.Button(
            self,
            text="Solve Nonogram",
            command=lambda: self.selected_puzzle(
                "Nonogram", self.app_window.configure_nonogram_page
            ),
            style="P1.Std.TButton",
        )
        solve_nonogram_button.grid(column=0, row=2, pady=10)

        solve_rubiks_cube_button = ttk.Button(
            self,
            text="Solve Rubik's Cube",
            command=lambda: self.selected_puzzle(
                "Rubik's Cube",
                self.app_window.configure_rubiks_cube_page,
            ),
            style="P1.Std.TButton",
        )
        solve_rubiks_cube_button.grid(column=0, row=3, pady=10)

    def selected_puzzle(self, puzzle_type: str, config_page: ttk.Frame):
        """Go to page of chosen puzzle.

        Args:
            puzzle_type: the chosen puzzle.
            config_page: the configuration page for the chosen puzzle.
        """
        solvd_ui_ctrl.show_page(config_page, self.app_window.choose_puzzle_page)
        solvd_ui_ctrl.change_title(self.app_window, f"Configure {puzzle_type}")


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

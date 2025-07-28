"""The UI for solving a Sudoku puzzle."""

import math
import tkinter as tk
from tkinter import ttk

import solvd.common.theming as solvd_theming
import solvd.common.ui_ctrl as solvd_ui_ctrl
import solvd.common.ui_elements as solvd_ui_elements
import solvd.sudoku.solving.controller as solving_ctrl
import solvd.sudoku.ui.cell as ui_cell
import solvd.sudoku.ui.configure_sudoku as ui_cfg
import solvd.sudoku.ui.grids as ui_grids


class PuzzlePage(ttk.Frame):
    """Frame that acts as a parent for all of the UI.

    Attributes:
        app_window: parent App.
        chosen_cells: cells that are being solved for with specific cells option.
        random_button: button to reveal another random cell with said option.
        specific_cells_solve_again_button: button to solve again with specific cells option.
        grid_frame: frame containing the puzzle grid.
        navigation_buttons: forward (solve) and back buttons.
    """

    def __init__(self, choices: "ui_cfg.ConfigureSudokuFrame"):
        """Initiate frame.

        Args:
            choices: previous screen that contains important information.
        """
        ttk.Frame.__init__(
            self, choices.containing_frame, style="Background.TFrame"
        )

        self.app_window = choices.app_window
        self.chosen_cells = []
        self.subtype = choices.subtype_choice
        self.type = choices.type_choice

        theme_config = solvd_theming.load_config()
        colours = solvd_theming.load_colours()

        app_title = f"Solve {self.subtype}"
        if self.type == "standard":
            app_title = f"{app_title} Sudoku"
        solvd_ui_ctrl.change_title(self.app_window, app_title)

        # TODO: make tk style
        instructions = tk.Message(
            master=self,
            text="Select a option from below.",
            bg=colours["bg0"],
            font=[theme_config["font"], theme_config["font-size"]],
            fg=colours["fg0"],
            pady=10,
        )
        instructions.grid(column=0, row=0, columnspan=2)

        solve_options_frame = ttk.LabelFrame(
            self, text="Solving Options", style="Standard.TLabelframe"
        )
        solve_options_frame.grid(column=0, row=1)

        solve_option = tk.StringVar()

        solve_all_radiobutton = ttk.Radiobutton(
            solve_options_frame,
            text="Solve all cells",
            variable=solve_option,
            value="all",
            command=lambda: all_radiobutton_click(),
            style="Standard.TRadiobutton",
        )
        solve_all_radiobutton.grid(column=0, row=0, sticky="w")

        solve_random_radiobutton = ttk.Radiobutton(
            solve_options_frame,
            text="Solve random cell",
            variable=solve_option,
            value="random",
            command=lambda: random_radiobutton_click(),
            style="Standard.TRadiobutton",
        )
        solve_random_radiobutton.grid(column=0, row=1, sticky="w")

        solve_specific_radiobutton = ttk.Radiobutton(
            solve_options_frame,
            text="Solve specific cell(s)",
            variable=solve_option,
            value="specific",
            style="Standard.TRadiobutton",
            command=lambda: specific_radiobutton_click(),
        )
        solve_specific_radiobutton.grid(column=0, row=2, sticky="w")

        check_progress_radiobutton = ttk.Radiobutton(
            solve_options_frame,
            text="Check progress",
            variable=solve_option,
            value="progress",
            style="Standard.TRadiobutton",
            command=lambda: progress_radiobutton_click(),
        )
        check_progress_radiobutton.grid(column=0, row=3, sticky="w")

        other_buttons_frame = ttk.Frame(self, style="Background.TFrame")
        other_buttons_frame.grid(row=2, column=0)

        self.random_button = ttk.Button(
            other_buttons_frame,
            style="Standard.TButton",
            text="Reveal another cell",
            command=lambda: random_button_click(),
        )

        specific_cells_button = ttk.Button(
            other_buttons_frame,
            style="Standard.TButton",
            text="Select Cell(s)",
            command=lambda: specific_button_click(),
        )

        self.specific_cells_solve_again_button = ttk.Button(
            other_buttons_frame,
            style="Standard.TButton",
            text="Solve with new cells",
            command=lambda: specific_again_button_click(),
            state="disabled",
        )

        progress_enter_guesses_button = ttk.Button(
            other_buttons_frame,
            style="Standard.TButton",
            text="Enter Guess(es)",
            command=lambda: progress_button_click(),
        )

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.grid(column=1, row=1, rowspan=2)

        match self.type:
            case "standard":
                self.ratio = "square"
                subtype_words = self.subtype.split()
                self.dimension = int(subtype_words[0])
                box_size = math.sqrt(self.dimension)
                if not box_size.is_integer():
                    self.ratio = subtype_words[-2]
                    self.ratio = self.ratio[1:]
                self.puzzle_grid = ui_grids.Standard(self)
            case "multidoku":
                match self.subtype:
                    case "Butterfly Sudoku":
                        self.dimension = 12
                        self.puzzle_grid = ui_grids.ButterflyGrid(self)
                    case "Cross Sudoku":
                        self.dimension = 21
                        self.puzzle_grid = ui_grids.CrossGrid(self)
                    case "Flower Sudoku":
                        self.dimension = 15
                        self.puzzle_grid = ui_grids.FlowerGrid(self)
                    case "Gattai-3":
                        self.dimension = 15
                        self.puzzle_grid = ui_grids.GattaiGrid(self)
                    case "Kazaguruma":
                        self.dimension = 21
                        self.puzzle_grid = ui_grids.KazagurumaGrid(self)
                    case "Samurai Sudoku":
                        pass
                    case "Sohei Sudoku":
                        pass
                    case "Tripledoku":
                        pass
                    case "Twodoku":
                        pass
            case "variants":
                match self.subtype:
                    case "Argyle":
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
        self.puzzle_grid.grid(column=0, row=0)

        self.navigation_buttons = solvd_ui_elements.NavigationButtons(self)
        self.navigation_buttons.grid(row=3, column=0, columnspan=2)
        self.navigation_buttons.back_button.configure(
            text="Back to configure Sudoku",
            command=lambda: back_to_config_sudoku(),
        )
        self.navigation_buttons.forward_button.configure(
            text="Solve",
            command=lambda: forward_button_click(),
            state="disabled",
        )

        def back_to_config_sudoku():
            """Go back to previous screen."""
            solvd_ui_ctrl.show_page(self.app_window.configure_sudoku_page, self)
            solvd_ui_ctrl.change_title(self.app_window, "Configure Sudoku")

        def forward_button_click():
            """Solve or clear puzzle, dependent on status of the forward button."""
            match self.navigation_buttons.forward_button["text"]:
                case "Solve":
                    solve_button_click()
                case "Clear":
                    clear_button_click()

        def all_radiobutton_click():
            """Change UI for solving all cells."""
            self.enable_solve_button()
            solvd_ui_ctrl.hide_widget(specific_cells_button)
            solvd_ui_ctrl.hide_widget(self.specific_cells_solve_again_button)
            solvd_ui_ctrl.hide_widget(progress_enter_guesses_button)
            instructions.configure(
                text="Enter the clues into the grid and then click Solve."
            )

        def random_radiobutton_click():
            """Change UI for solving random cells."""
            self.enable_solve_button()
            solvd_ui_ctrl.hide_widget(specific_cells_button)
            solvd_ui_ctrl.hide_widget(self.specific_cells_solve_again_button)
            solvd_ui_ctrl.hide_widget(progress_enter_guesses_button)
            instructions.configure(
                text="Enter the clues into the grid and then click Solve to reveal the solution to a randomly selected cell."
            )

        def specific_radiobutton_click():
            """Change UI for solving specific cells."""
            solvd_ui_ctrl.disable_button(self.navigation_buttons.forward_button)
            solvd_ui_ctrl.hide_widget(progress_enter_guesses_button)
            specific_cells_button.grid(column=0, row=0)
            instructions.configure(
                text="Enter the clues into the grid, and then click Select Cell(s) to choose which cell(s) will have their solution revealed."
            )

        def progress_radiobutton_click():
            """Change UI for checking progress."""
            solvd_ui_ctrl.hide_widget(specific_cells_button)
            instructions.configure(
                text="Enter the clues into the grid, and then click Enter Guess(es)."
            )
            progress_enter_guesses_button.grid(column=0, row=0)

        def random_button_click():
            """Reveal a random cell when the random button is clicked."""
            solving_ctrl.reveal_random_cell(self)

        def specific_button_click():
            """Open window to choose cells for specific cells option."""
            ui_cell.SpecificCellsWindow(self)

        def specific_again_button_click():
            """Change UI when the solve again for specific cells button is clicked."""
            solving_ctrl.reveal_specific_cells(self)
            solvd_ui_ctrl.disable_button(self.specific_cells_solve_again_button)

        def progress_button_click():
            """Change UI and change cells so they are now guesses."""
            for cell in self.puzzle_grid.cells:
                if cell.is_empty():
                    cell.make_guess()
                else:
                    cell.cell_text.configure(state="disabled")
            solvd_ui_ctrl.disable_button(progress_enter_guesses_button)
            self.enable_solve_button()
            instructions.configure(
                text="Enter the guesses into the grid, then click solve."
            )

        def solve_button_click():
            """Solve the puzzle and update UI."""
            solving_ctrl.solve_sudoku(self)
            match solve_option.get():
                case "all":
                    for cell in self.puzzle_grid.cells:
                        if cell.is_empty():
                            cell.show_true_value()
                case "random":
                    self.random_button.grid(column=0, row=0)
                    solving_ctrl.reveal_random_cell(self)
                case "specific":
                    solving_ctrl.reveal_specific_cells(self)
                    self.specific_cells_solve_again_button.grid(row=0, column=1)
                    solvd_ui_ctrl.disable_button(
                        self.specific_cells_solve_again_button
                    )
                case "progress":
                    for cell in self.puzzle_grid.cells:
                        if (not cell.is_empty()) and cell.is_guess:
                            if int(cell.get_text()) == cell.true_value:
                                cell.mark_correct()
                            else:
                                cell.mark_incorrect()
            self.navigation_buttons.forward_button["text"] = "Clear"

        def clear_button_click():
            """Clear the puzzle and update UI."""
            self.navigation_buttons.forward_button["text"] = "Solve"
            for cell in self.puzzle_grid.cells:
                cell.true_value = 0
                cell.cell_text.delete("1.0", "end")
            match solve_option.get():
                case "random":
                    solvd_ui_ctrl.hide_widget(self.random_button)
                case "specific":
                    solvd_ui_ctrl.hide_widget(
                        self.specific_cells_solve_again_button
                    )
                case _:
                    pass

    def enable_solve_button(self):
        """Enable the solve button."""
        solvd_ui_ctrl.enable_button(self.navigation_buttons.forward_button)

"""The UI for solving a Sudoku puzzle."""

import math
import tkinter as tk
from tkinter import ttk

import backend.misc_funcs
import controller.controller
import ui.elements
import ui.sudoku.config
import ui.theming


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

    def __init__(self, choices: "ui.sudoku.config.ConfigureSudokuFrame"):
        """Initiate frame.

        Args:
            choices: previous screen that contains important information.
        """
        ttk.Frame.__init__(self, choices.containing_frame, style="Background.TFrame")

        self.app_window = choices.app_window
        self.chosen_cells = []

        theme_config = ui.theming.load_config()
        colours = ui.theming.load_colours()

        app_title = "Solvd - Solve " + choices.subtype_choice
        if choices.type_choice == "standard":
            app_title = app_title + " Sudoku"
        controller.controller.change_title(self.app_window, app_title)

        instructions = tk.Message(
            master=self,
            text="Select a option from below.",
            bg=colours["background0"],
            font=[theme_config["font"], theme_config["font-size"]],
            fg=colours["foreground0"],
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

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.grid(column=1, row=1, rowspan=2)

        if choices.type_choice == "standard":
            self.ratio = "square"
            subtype_words = choices.subtype_choice.split()
            self.dimension = int(subtype_words[0])
            box_size = math.sqrt(self.dimension)
            if not box_size.is_integer():
                self.ratio = subtype_words[-2]
                self.ratio = self.ratio[1:]
            self.puzzle_grid = StandardGrid(self)
        self.puzzle_grid.grid(column=0, row=0)

        self.navigation_buttons = ui.elements.NavigationButtons(self)
        self.navigation_buttons.grid(row=3, column=0, columnspan=2)
        self.navigation_buttons.back_button.configure(
            text="Back to configure Sudoku", command=lambda: back_to_config_sudoku()
        )
        self.navigation_buttons.forward_button.configure(
            text="Solve", command=lambda: forward_button_click(), state="disabled"
        )

        def back_to_config_sudoku():
            """Go back to previous screen."""
            controller.controller.show_page(self.app_window.configure_sudoku_page, self)
            controller.controller.change_title(self.app_window, "Solvd - Configure Sudoku")

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
            controller.controller.hide_widget(specific_cells_button)
            controller.controller.hide_widget(self.specific_cells_solve_again_button)
            instructions.configure(text="Enter the clues into the grid and then click Solve.")

        def random_radiobutton_click():
            """Change UI for solving random cells."""
            self.enable_solve_button()
            controller.controller.hide_widget(specific_cells_button)
            controller.controller.hide_widget(self.specific_cells_solve_again_button)
            instructions.configure(
                text="Enter the clues into the grid and then click Solve to reveal the solution to a randomly selected cell."
            )

        def specific_radiobutton_click():
            """Change UI for solving specific cells."""
            controller.controller.disable_button(self.navigation_buttons.forward_button)
            specific_cells_button.grid(column=0, row=0)
            instructions.configure(
                text="Enter the clues into the grid, and then click Select Cell(s) to choose which cell(s) will have their solution revealed."
            )

        def progress_radiobutton_click():
            """Change UI for checking progress."""
            controller.controller.hide_widget(specific_cells_button)
            instructions.configure(text="")

        def random_button_click():
            """Reveal a random cell when the random button is clicked."""
            controller.controller.reveal_random_cell(self)

        def specific_button_click():
            """Open window to choose cells for specific cells option."""
            SpecificCellsWindow(self)

        def specific_again_button_click():
            """Change UI when the solve again for specific cells button is clicked."""
            controller.controller.reveal_specific_cells(self)
            controller.controller.disable_button(self.specific_cells_solve_again_button)

        def solve_button_click():
            """Solve the puzzle and update UI."""
            controller.controller.solve_sudoku(self)
            match solve_option.get():
                case "all":
                    for cell in self.puzzle_grid.cells:
                        if cell.is_empty():
                            cell.show_true_value()
                case "random":
                    self.random_button.grid(column=0, row=0)
                    controller.controller.reveal_random_cell(self)
                case "specific":
                    controller.controller.reveal_specific_cells(self)
                    self.specific_cells_solve_again_button.grid(row=0, column=1)
                    controller.controller.disable_button(self.specific_cells_solve_again_button)
                case "progress":
                    pass
            self.navigation_buttons.forward_button["text"] = "Clear"

        def clear_button_click():
            """Clear the puzzle and update UI."""
            self.navigation_buttons.forward_button["text"] = "Solve"
            for cell in self.puzzle_grid.cells:
                cell.true_value = 0
                cell.cell_text.delete("1.0", "end")
            match solve_option.get():
                case "random":
                    controller.controller.hide_widget(self.random_button)
                case "specific":
                    controller.controller.hide_widget(self.specific_cells_solve_again_button)
                case _:
                    pass

    def enable_solve_button(self):
        """Enable the solve button."""
        controller.controller.enable_button(self.navigation_buttons.forward_button)


class StandardGrid(tk.Canvas):
    """The puzzle grid.

    Attributes:
        cell_width: height/width of a cell (in px).
        dimension: the side length of the puzzle.
        colours: colour theme.
        grid_width: height/width of the grid (in px).
        cells: list of the cells.
    """

    def __init__(self, puzzle_page: PuzzlePage):
        """Draws the puzzle.

        Args:
            puzzle_page: parent frame.
        """
        self.cell_width = 80
        self.dimension = puzzle_page.dimension
        self.colours = ui.theming.load_colours()

        grid_width = puzzle_page.dimension * self.cell_width
        self.grid_width = grid_width
        tk.Canvas.__init__(self, puzzle_page.grid_frame, width=grid_width, height=grid_width)

        # draw grid border
        self.create_rectangle(
            0,
            0,
            grid_width,
            grid_width,
            fill=self.colours["background1"],
            outline=self.colours["foreground1"],
            width=5,
        )

        # draw box borders
        if puzzle_page.ratio != "square":
            box_size_short, box_size_long = backend.misc_funcs.calculate_box_sizes(
                puzzle_page.dimension
            )
            box_size_short_px = self.cell_width * box_size_short
            box_size_long_px = self.cell_width * box_size_long

            if puzzle_page.ratio == "wide":
                for i in range(1, box_size_short):
                    bsl_i = i * box_size_long_px
                    self.draw_vertical_line(bsl_i, 5)
                for i in range(1, box_size_long):
                    bss_i = i * box_size_short_px
                    self.draw_horizontal_line(bss_i, 5)

            if puzzle_page.ratio == "tall":
                for i in range(1, box_size_long):
                    bss_i = i * box_size_short_px
                    self.draw_vertical_line(bss_i, 5)
                for i in range(1, box_size_short):
                    bsl_i = i * box_size_long_px
                    self.draw_horizontal_line(bsl_i, 5)
        else:
            box_size = backend.misc_funcs.calculate_square_box_size(puzzle_page.dimension)
            box_width = self.cell_width * box_size
            for i in range(1, box_size):
                bw_i = box_width * i
                self.draw_vertical_line(bw_i, 5)
                self.draw_horizontal_line(bw_i, 5)

        # draw cell borders:
        for i in range(1, puzzle_page.dimension):
            cw_i = self.cell_width * i
            self.draw_vertical_line(cw_i, 2)
            self.draw_horizontal_line(cw_i, 2)

        # create cells
        self.cells = []
        for r in range(puzzle_page.dimension):
            for c in range(puzzle_page.dimension):
                box_index = backend.misc_funcs.calculate_box_index(puzzle_page, c, r)
                cell = Cell(self, r, c, box_index)
                self.cells.append(cell)

    def draw_vertical_line(self, x: int, width: int):
        """Draw a vertical line on the grid.

        Args:
            x: x co-ordinate of the line.
            width: width of the line.
        """
        self.create_line(x, 0, x, self.grid_width, fill=self.colours["foreground1"], width=width)

    def draw_horizontal_line(self, y: int, width: int):
        """Draw a horizontal line on the grid.

        Args:
            y: y co-ordinate of the line.
            width: width of the line.
        """
        self.create_line(0, y, self.grid_width, y, fill=self.colours["foreground1"], width=width)


class Cell:
    """An individual cell.

    Attributes:
        row: the cell's row (indexes from 0).
        col: the cell's column (indexes from 0).
        box: the cell's box (indexes from 0).
        true_value: the solution to the cell.
        cell_text: the text currently in the cell.
    """

    def __init__(self, container: StandardGrid, row: int, col: int, box: int):
        """Initiates the cell.

        Args:
            container: container of the cell.
            row: the cell's row.
            col: the cell's column.
            box: the cell's box.
        """
        self.row = row
        self.col = col
        self.box = box
        self.true_value = 0
        config = ui.theming.load_config()
        colours = ui.theming.load_colours()

        if container.dimension < 10:
            char_width = 1
        else:
            char_width = 2

        self.cell_text = tk.Text(
            container,
            height=1,
            width=char_width,
            font=(config["font"], config["font-size"]),
            relief="flat",
            borderwidth=0,
            highlightbackground=colours["background1"],
            highlightcolor=colours["background1"],
            foreground=colours["foreground0"],
            background=colours["background1"],
        )
        self.cell_text.tag_configure("center", justify="center")
        self.cell_text.tag_add("center", 1.0, "end")

        cell_center = container.cell_width // 2
        cell_x = (container.cell_width * col) + cell_center
        cell_y = (container.cell_width * row) + cell_center

        container.create_window(cell_x, cell_y, window=self.cell_text)

    def show_true_value(self):
        """Display the cell's solved value."""
        self.cell_text.insert("1.0", str(self.true_value))

    def is_empty(self) -> bool:
        """Check if a cell had no text in it.

        Returns:
            True if it is empty, False otherwise.
        """
        value = self.cell_text.get("1.0", "end - 1c")
        if value == "":
            return True
        else:
            return False

    def get_text(self) -> str:
        """Get the text from the cell.

        Returns:
            the cell's text
        """
        return self.cell_text.get("1.0", "end - 1c")


class SpecificCellsWindow(tk.Toplevel):
    """Window where cells are selected for the specific cells option."""

    def __init__(self, puzzle_page: PuzzlePage):
        """Initiates window.

        Args:
            puzzle_page: parent frame.
        """
        colours = ui.theming.load_colours()

        tk.Toplevel.__init__(self, puzzle_page.app_window, background=colours["background0"])
        controller.controller.change_title(self, "Solvd - Choose Cells to Solve")

        cell_buttons = []
        for r in range(puzzle_page.dimension):
            for c in range(puzzle_page.dimension):
                cell_button = CellButton(self, c, r)
                cell_buttons.append(cell_button)
                cell_button.grid(column=c, row=r, padx=10, pady=10)

        for cell in puzzle_page.puzzle_grid.cells:
            if not cell.is_empty():
                for cell_button in cell_buttons:
                    if (cell_button.row == cell.row) and (cell_button.col == cell.col):
                        cell_button["text"] = cell.get_text()
                        controller.controller.disable_button(cell_button)

        ok_button = ttk.Button(
            self, text="OK", style="Standard.TButton", command=lambda: ok_button_click()
        )
        ok_button.grid(
            row=puzzle_page.dimension, column=0, columnspan=puzzle_page.dimension, pady=10
        )

        def ok_button_click():
            """Close window and return to main page."""
            puzzle_page.enable_solve_button()
            controller.controller.enable_button(puzzle_page.specific_cells_solve_again_button)
            for cell in cell_buttons:
                if cell.selected:
                    puzzle_page.chosen_cells.append(cell)
            self.destroy()


class CellButton(ttk.Button):
    """Button that represents a cell. For use with SpecificCellsWindow.

    Attributes:
        col: column of the represented cell.
        row: row of the represented cell.
        selected: whether the cell has been selected or not.
    """

    def __init__(self, container: tk.Toplevel, col: int, row: int):
        """Initiates button.

        Args:
            container: parent container.
            col: column of the represented cell.
            row: row of the represented cell.
        """
        ttk.Button.__init__(self, container, command=lambda: cell_button_click())
        self["style"] = "Cell.Standard.TButton"
        self.col = col
        self.row = row
        self.selected = False

        def cell_button_click():
            """Toggle the button on and off."""
            if self.selected:
                self.selected = False
                self["style"] = "Cell.Standard.TButton"
            else:
                self.selected = True
                self["style"] = "Selected.Cell.Standard.TButton"

    def __str__(self) -> str:
        return "C: " + str(self.col) + ", R: " + str(self.row) + ", " + str(self.selected)

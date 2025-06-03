import tkinter as tk
from tkinter import ttk

import controller.ui_ctrl
import ui.sudoku.grids
import ui.sudoku.puzzle
import ui.theming


class Cell:
    """An individual cell.

    Attributes:
        row: the cell's row (indexes from 0).
        col: the cell's column (indexes from 0).
        box: the cell's box (indexes from 0).
        true_value: the solution to the cell.
        cell_text: the text currently in the cell.
        is_guess: whether the cell contains a guess or not (for use with progress option)
        colours: loaded in colourscheme.
    """

    def __init__(self, container: "ui.sudoku.grids.StandardGrid", row: int, col: int, box: int):
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
        self.is_guess = False
        config = ui.theming.load_config()
        self.colours = ui.theming.load_colours()

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
            highlightbackground=self.colours["background1"],
            highlightcolor=self.colours["background1"],
            foreground=self.colours["foreground0"],
            background=self.colours["background1"],
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

    def make_guess(self):
        """Turn the cell into a guess from a clue."""
        self.is_guess = True
        self.cell_text.configure(foreground=self.colours["yellow"])

    def mark_correct(self):
        """Mark a guessed cell as correct."""
        self.cell_text.configure(foreground=self.colours["green"])

    def mark_incorrect(self):
        """Mark a guessed cell as incorrect."""
        self.cell_text.configure(foreground=self.colours["red"])


class SpecificCellsWindow(tk.Toplevel):
    """Window where cells are selected for the specific cells option."""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """Initiates window.

        Args:
            puzzle_page: parent frame.
        """
        colours = ui.theming.load_colours()

        tk.Toplevel.__init__(self, puzzle_page.app_window, background=colours["background0"])
        controller.ui_ctrl.change_title(self, "Solvd - Choose Cells to Solve")

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
                        controller.ui_ctrl.disable_button(cell_button)

        ok_button = ttk.Button(
            self, text="OK", style="Standard.TButton", command=lambda: ok_button_click()
        )
        ok_button.grid(
            row=puzzle_page.dimension, column=0, columnspan=puzzle_page.dimension, pady=10
        )

        def ok_button_click():
            """Close window and return to main page."""
            puzzle_page.enable_solve_button()
            controller.ui_ctrl.enable_button(puzzle_page.specific_cells_solve_again_button)
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

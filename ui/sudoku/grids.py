"""UI for sudoku grids."""

import tkinter as tk

import backend.misc_funcs
import ui.sudoku.cells
import ui.sudoku.puzzle
import ui.theming


class Base(tk.Canvas):
    """The base class of a sudoku grid.

    Attributes:
        cell_width: the width of a cell (px).
        colours: the UI colour theme.
        cells: the grid's cells.
        dimension: width of the puzzle (number of cells).
        grid_width: width of the grid (px).
    """

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """Initialise the base class.

        Args:
            puzzle_page: parent frame.
        """
        self.cell_width = 40
        self.colours = ui.theming.load_colours()
        self.cells = []
        self.dimension = puzzle_page.dimension
        self.grid_width = self.dimension * self.cell_width

        tk.Canvas.__init__(
            self, puzzle_page.grid_frame, width=self.grid_width, height=self.grid_width
        )

        self.draw_background()

    def draw_vertical_line(self, x: int, width: str):
        """Draw a vertical line on the grid which spans the whole grid.

        Args:
            x: x co-ordinate of the line.
            width: width of the line. "thick" or "thin".
        """
        match width:
            case "thick":
                self.create_line(x, 0, x, self.grid_width, fill=self.colours["fg1"], width=5)
            case "thin":
                self.create_line(x, 0, x, self.grid_width, fill=self.colours["fg1"], width=2)

    def draw_partial_vertical_line(self, x: int, y_start: int, y_stop: int, width: str):
        """Draw a vertical line on the grid.

        Args:
            x: x co-ordinate of the line.
            y_start: start y co-ordinate of the line.
            y_stop: end y co-ordinate of the line.
            width: width of the line. "thick" or "thin".
        """
        match width:
            case "thick":
                self.create_line(x, y_start, x, y_stop, fill=self.colours["fg1"], width=5)
            case "thin":
                self.create_line(x, y_start, x, y_stop, fill=self.colours["fg1"], width=2)

    def draw_horizontal_line(self, y: int, width: str):
        """Draw a horizontal line on the grid which spans the whole grid.

        Args:
            y: y co-ordinate of the line.
            width: width of the line. "thick" or "thin".
        """
        match width:
            case "thick":
                self.create_line(0, y, self.grid_width, y, fill=self.colours["fg1"], width=5)
            case "thin":
                self.create_line(0, y, self.grid_width, y, fill=self.colours["fg1"], width=2)

    def draw_partial_horizontal_line(self, y: int, x_start: int, x_stop: int, width: str):
        """Draw a horizontal line on the grid.

        Args:
            y: y co-ordinate of the line.
            x_start: start x co-ordinate of the line.
            x_stop: end x co-ordinate of the line.
            width: width of the line. "thick" or "thin".
        """
        match width:
            case "thick":
                self.create_line(x_start, y, x_stop, y, fill=self.colours["fg1"], width=5)
            case "thin":
                self.create_line(x_start, y, x_stop, y, fill=self.colours["fg1"], width=2)

    def draw_background(self):
        """Colour the grid background."""
        self.create_rectangle(
            0,
            0,
            self.grid_width,
            self.grid_width,
            fill=self.colours["bg1"],
            outline=self.colours["fg1"],
        )


class Standard(Base):
    """The standard puzzle grid."""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """Draws the puzzle.

        Args:
            puzzle_page: parent frame.
        """

        Base.__init__(self, puzzle_page)

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
                    self.draw_vertical_line(bsl_i, "thick")
                for i in range(1, box_size_long):
                    bss_i = i * box_size_short_px
                    self.draw_horizontal_line(bss_i, "thick")

            if puzzle_page.ratio == "tall":
                for i in range(1, box_size_long):
                    bss_i = i * box_size_short_px
                    self.draw_vertical_line(bss_i, "thick")
                for i in range(1, box_size_short):
                    bsl_i = i * box_size_long_px
                    self.draw_horizontal_line(bsl_i, "thick")
        else:
            box_size = backend.misc_funcs.calculate_square_box_size(puzzle_page.dimension)
            box_width = self.cell_width * box_size
            for i in range(1, box_size):
                bw_i = box_width * i
                self.draw_vertical_line(bw_i, "thick")
                self.draw_horizontal_line(bw_i, "thick")

        # draw cell borders:
        for i in range(1, puzzle_page.dimension):
            cw_i = self.cell_width * i
            self.draw_vertical_line(cw_i, "thin")
            self.draw_horizontal_line(cw_i, "thin")

        # create cells
        self.cells = []
        for r in range(puzzle_page.dimension):
            for c in range(puzzle_page.dimension):
                box_index = backend.misc_funcs.calculate_box_index(puzzle_page, c, r)
                cell = ui.sudoku.cells.Cell(self, r, c, box_index)
                self.cells.append(cell)


class ButterflyGrid(Base):
    """Grid for butterfly sudoku."""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """Draws the puzzle.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        # draw box borders
        box_width = self.cell_width * 3
        for i in range(1, 4):
            bw_i = box_width * i
            self.draw_vertical_line(bw_i, "thick")
            self.draw_horizontal_line(bw_i, "thick")

        # draw cell borders
        for i in range(1, 12):
            cw_i = self.cell_width * i
            self.draw_horizontal_line(cw_i, "thin")
            self.draw_vertical_line(cw_i, "thin")

        # create cells
        for r in range(12):
            for c in range(12):
                box_index = backend.misc_funcs.calculate_butterfly_box_index(r, c)
                cell = ui.sudoku.cells.Cell(self, r, c, box_index)
                self.cells.append(cell)


class CrossGrid(Base):
    """Grid for cross sudoku."""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """Draws the grid.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        # full length lines
        box_width = self.cell_width * 3
        for i in range(2, 6):
            bw_i = box_width * i
            self.draw_vertical_line(bw_i, "thick")
            self.draw_horizontal_line(bw_i, "thick")
        for i in range(6, 15):
            cw_i = self.cell_width * i
            self.draw_horizontal_line(cw_i, "thin")
            self.draw_vertical_line(cw_i, "thin")

        # partial lines
        start = box_width * 2
        stop = box_width * 5
        self.draw_partial_vertical_line(box_width, start, stop, "thick")
        self.draw_partial_horizontal_line(box_width, start, stop, "thick")
        self.draw_partial_vertical_line(self.grid_width - box_width, start, stop, "thick")
        self.draw_partial_horizontal_line(self.grid_width - box_width, start, stop, "thick")
        for i in range(1, 6):
            cw_i = self.cell_width * i
            self.draw_partial_horizontal_line(cw_i, start, stop, "thin")
            self.draw_partial_vertical_line(cw_i, start, stop, "thin")
            self.draw_partial_horizontal_line(self.grid_width - cw_i, start, stop, "thin")
            self.draw_partial_vertical_line(self.grid_width - cw_i, start, stop, "thin")

        # cells
        for r in range(21):
            for c in range(21):
                if 6 <= r <= 14:
                    box_index = backend.misc_funcs.calculate_cross_box_index(r, c)
                    cell = ui.sudoku.cells.Cell(self, r, c, box_index)
                    self.cells.append(cell)
                else:
                    if 6 <= c <= 14:
                        box_index = backend.misc_funcs.calculate_cross_box_index(r, c)
                        cell = ui.sudoku.cells.Cell(self, r, c, box_index)
                        self.cells.append(cell)


class FlowerGrid(Base):
    """Grid for flower sudoku."""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """draws the grid.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        # full length lines
        box_width = self.cell_width * 3
        for i in range(1, 5):
            bw_i = box_width * i
            self.draw_vertical_line(bw_i, "thick")
            self.draw_horizontal_line(bw_i, "thick")
        for i in range(3, 13):
            cw_i = self.cell_width * i
            self.draw_vertical_line(cw_i, "thin")
            self.draw_horizontal_line(cw_i, "thin")

        # partial length lines
        start = box_width
        stop = box_width * 4
        self.draw_partial_vertical_line(0, start, stop, "thick")
        self.draw_partial_vertical_line(self.grid_width, start, stop, "thick")
        self.draw_partial_horizontal_line(0, start, stop, "thick")
        self.draw_partial_horizontal_line(self.grid_width, start, stop, "thick")
        for i in range(1, 3):
            cw_i = self.cell_width * i
            self.draw_partial_vertical_line(cw_i, start, stop, "thin")
            self.draw_partial_vertical_line(self.grid_width - cw_i, start, stop, "thin")
            self.draw_partial_horizontal_line(cw_i, start, stop, "thin")
            self.draw_partial_horizontal_line(self.grid_width - cw_i, start, stop, "thin")

        # cells
        for r in range(15):
            for c in range(15):
                if 3 <= r <= 11:
                    box_index = backend.misc_funcs.calculate_flower_box_index(r, c)
                    cell = ui.sudoku.cells.Cell(self, r, c, box_index)
                    self.cells.append(cell)
                else:
                    if 3 <= c <= 11:
                        box_index = backend.misc_funcs.calculate_flower_box_index(r, c)
                        cell = ui.sudoku.cells.Cell(self, r, c, box_index)
                        self.cells.append(cell)

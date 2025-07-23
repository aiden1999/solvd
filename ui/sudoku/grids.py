"""UI for sudoku grids."""

import tkinter as tk

import backend.box_indices
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
            self,
            puzzle_page.grid_frame,
            width=self.grid_width,
            height=self.grid_width,
            relief="flat",
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

    def add_cell(self, box_calculator, row: int, col: int):
        """Add a cell to the grid.

        Args:
            box_calculator (function): function to calculate the box index.
            row: cell's row index.
            col: cell's column index.
        """
        box_index = box_calculator(row, col)
        cell = ui.sudoku.cells.Cell(self, row, col, box_index)
        self.cells.append(cell)


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
            box_size_short, box_size_long = backend.box_indices.calculate_box_sizes(
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
            box_size = backend.box_indices.calculate_square_box_size(puzzle_page.dimension)
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
                box_index = backend.box_indices.calculate_standard(puzzle_page, c, r)
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
                self.add_cell(backend.box_indices.calculate_butterfly, r, c)


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
                    self.add_cell(backend.box_indices.calculate_cross, r, c)
                else:
                    if 6 <= c <= 14:
                        self.add_cell(backend.box_indices.calculate_cross, r, c)


class FlowerGrid(Base):
    """Grid for flower sudoku."""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """Draws the grid.

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
                    self.add_cell(backend.box_indices.calculate_flower, r, c)
                else:
                    if 3 <= c <= 11:
                        self.add_cell(backend.box_indices.calculate_flower, r, c)


class GattaiGrid(Base):
    """Grid for Gattai-3 sudoku."""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """Draws the grid.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        box_width = self.cell_width * 3

        # north grid
        top, bottom, left, right = 0, box_width * 3, box_width, box_width * 4
        # thick lines
        for i in range(4):
            self.draw_partial_vertical_line(left + (box_width * i), top, bottom, "thick")
            self.draw_partial_horizontal_line(box_width * i, left, right, "thick")
        # thin lines
        for i in range(10):
            self.draw_partial_vertical_line(left + (self.cell_width * i), top, bottom, "thin")
            self.draw_partial_horizontal_line(self.cell_width * i, left, right, "thin")

        # east grid
        top, bottom, left, right = box_width, box_width * 4, box_width * 2, self.grid_width
        # thick lines
        for i in range(4):
            self.draw_partial_vertical_line(left + (box_width * i), top, bottom, "thick")
            self.draw_partial_horizontal_line(top + (box_width * i), left, right, "thick")
        # thin lines
        for i in range(10):
            self.draw_partial_vertical_line(left + (self.cell_width * i), top, bottom, "thin")
            self.draw_partial_horizontal_line(top + (self.cell_width * i), left, right, "thin")

        # south-west grid
        top, bottom, left, right = box_width * 2, self.grid_width, 0, box_width * 3
        # thick lines
        for i in range(4):
            self.draw_partial_vertical_line(left + (box_width * i), top, bottom, "thick")
            self.draw_partial_horizontal_line(top + (box_width * i), left, right, "thick")
        # thin lines
        for i in range(10):
            self.draw_partial_vertical_line(left + (self.cell_width * i), top, bottom, "thin")
            self.draw_partial_horizontal_line(top + (self.cell_width * i), left, right, "thin")

        # cells
        for r in range(0, 3):
            for c in range(3, 12):
                self.add_cell(backend.box_indices.calculate_gattai, r, c)
        for r in range(3, 6):
            for c in range(3, 15):
                self.add_cell(backend.box_indices.calculate_gattai, r, c)
        for r in range(6, 12):
            for c in range(15):
                self.add_cell(backend.box_indices.calculate_gattai, r, c)
        for r in range(12, 15):
            for c in range(0, 9):
                self.add_cell(backend.box_indices.calculate_gattai, r, c)


class KazagurumaGrid(Base):
    """Grid for Kazaguruma sudoku."""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """Draws the grid.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        box_width = self.cell_width * 3
        bw3 = box_width * 3
        bw4 = box_width * 4
        bw6 = box_width * 6

        for i in range(1, 3):
            i4 = i + 4
            # thick lines
            self.draw_vertical_line(box_width * (2 + i), "thick")
            self.draw_horizontal_line(box_width * (2 + i), "thick")
            self.draw_partial_vertical_line(box_width * i, 0, bw6, "thick")
            self.draw_partial_vertical_line(box_width * i4, box_width, self.grid_width, "thick")
            self.draw_partial_horizontal_line(box_width * i4, 0, bw6, "thick")
            self.draw_partial_horizontal_line(box_width * i, box_width, self.grid_width, "thick")
            # thin lines
            self.draw_vertical_line(bw3 + (self.cell_width * i), "thin")
            self.draw_horizontal_line(bw3 + (self.cell_width * i), "thin")
            self.draw_partial_vertical_line(self.cell_width * i, bw3, bw6, "thin")
            self.draw_partial_vertical_line(bw6 + (self.cell_width * i), box_width, bw4, "thin")
            self.draw_partial_horizontal_line(self.cell_width * i, box_width, bw4, "thin")
            self.draw_partial_horizontal_line(bw6 + (self.cell_width * i), bw3, bw6, "thin")
        for i in range(1, 6):
            cwi = self.cell_width * i
            self.draw_partial_vertical_line(box_width + cwi, 0, bw6, "thin")
            self.draw_partial_vertical_line(bw4 + cwi, box_width, self.grid_width, "thin")
            self.draw_partial_horizontal_line(box_width + cwi, box_width, self.grid_width, "thin")
            self.draw_partial_horizontal_line(bw4 + cwi, 0, bw6, "thin")
        self.draw_partial_vertical_line(0, bw3, bw6, "thick")
        self.draw_partial_vertical_line(self.grid_width, box_width, bw4, "thick")
        self.draw_partial_horizontal_line(0, box_width, bw4, "thick")
        self.draw_partial_horizontal_line(self.grid_width, bw3, bw6, "thick")

        # cells
        for r in range(3):
            for c in range(3, 12):
                self.add_cell(backend.box_indices.calculate_kazaguruma, r, c)
        for r in range(3, 9):
            for c in range(3, 21):
                self.add_cell(backend.box_indices.calculate_kazaguruma, r, c)
        for r in range(9, 12):
            for c in range(21):
                self.add_cell(backend.box_indices.calculate_kazaguruma, r, c)
        for r in range(12, 18):
            for c in range(18):
                self.add_cell(backend.box_indices.calculate_kazaguruma, r, c)
        for r in range(18, 21):
            for c in range(9, 18):
                self.add_cell(backend.box_indices.calculate_kazaguruma, r, c)

        for cell in self.cells:
            cell.cell_text.insert("1.0", str(cell.box))

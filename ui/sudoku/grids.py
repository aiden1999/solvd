"""[TODO:description]

[TODO:description]
"""

import tkinter as tk

import backend.misc_funcs
import ui.sudoku.cells
import ui.sudoku.puzzle
import ui.theming


class Base(tk.Canvas):
    """[TODO:description]

    Attributes:
        cell_width: [TODO:attribute]
        colours: [TODO:attribute]
        cells: [TODO:attribute]
        dimension: [TODO:attribute]
        grid_width: [TODO:attribute]
    """

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """[TODO:description]

        Args:
            puzzle_page: [TODO:description]
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
        """Draw a thick vertical line on the grid.

        Args:
            x: x co-ordinate of the line.
            width: [TODO]
        """
        match width:
            case "thick":
                self.create_line(x, 0, x, self.grid_width, fill=self.colours["fg1"], width=5)
            case "thin":
                self.create_line(x, 0, x, self.grid_width, fill=self.colours["fg1"], width=2)

    def draw_partial_vertical_line(self, x: int, y_start: int, y_stop: int, width: str):
        """[TODO:description]

        Args:
            x: [TODO:description]
            y_start: [TODO:description]
            y_stop: [TODO:description]
            width: [TODO]
        """
        match width:
            case "thick":
                self.create_line(x, y_start, x, y_stop, fill=self.colours["fg1"], width=5)
            case "thin":
                self.create_line(x, y_start, x, y_stop, fill=self.colours["fg1"], width=2)

    def draw_horizontal_line(self, y: int, width: str):
        """Draw a thick horizontal line on the grid.

        Args:
            y: y co-ordinate of the line.
            width: TODO
        """
        match width:
            case "thick":
                self.create_line(0, y, self.grid_width, y, fill=self.colours["fg1"], width=5)
            case "thin":
                self.create_line(0, y, self.grid_width, y, fill=self.colours["fg1"], width=2)

    def draw_partial_horizontal_line(self, y: int, x_start: int, x_stop: int, width: str):
        """[TODO:description]

        Args:
            y: [TODO:description]
            x_start: [TODO:description]
            x_stop: [TODO:description]
            width: TODO
        """
        match width:
            case "thick":
                self.create_line(x_start, y, x_stop, y, fill=self.colours["fg1"], width=5)
            case "thin":
                self.create_line(x_start, y, x_stop, y, fill=self.colours["fg1"], width=2)

    def draw_background(self):
        """[TODO:description]"""
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
    """[TODO:description]"""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """[TODO:description]

        Args:
            puzzle_page: [TODO:description]
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
    """[TODO:description]"""

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        """[TODO:description]

        Args:
            puzzle_page: [TODO:description]
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

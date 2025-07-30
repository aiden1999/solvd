"""UI for sudoku grids."""

import tkinter as tk

import solvd.common.theming as solvd_theming
import solvd.sudoku.common.box_indices as common_bi
import solvd.sudoku.ui.cell as ui_cell
import solvd.sudoku.ui.puzzle_page as ui_pp


class Base(tk.Canvas):
    """The base class of a sudoku grid.

    Attributes:
        cell_width: the width of a cell (px).
        colours: the UI colour theme.
        cells: the grid's cells.
        dimension: width of the puzzle (number of cells).
        grid_width: width of the grid (px).
    """

    def __init__(self, puzzle_page: "ui_pp.PuzzlePage"):
        """Initialise the base class.

        Args:
            puzzle_page: parent frame.
        """
        self.cell_width = 40
        self.colours = solvd_theming.load_colours()
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
                self.create_line(
                    x, 0, x, self.grid_width, fill=self.colours["fg1"], width=5
                )
            case "thin":
                self.create_line(
                    x, 0, x, self.grid_width, fill=self.colours["fg1"], width=2
                )

    def draw_partial_vertical_line(
        self, x: int, y_start: int, y_stop: int, width: str
    ):
        """Draw a vertical line on the grid.

        Args:
            x: x co-ordinate of the line.
            y_start: start y co-ordinate of the line.
            y_stop: end y co-ordinate of the line.
            width: width of the line. "thick" or "thin".
        """
        match width:
            case "thick":
                self.create_line(
                    x, y_start, x, y_stop, fill=self.colours["fg1"], width=5
                )
            case "thin":
                self.create_line(
                    x, y_start, x, y_stop, fill=self.colours["fg1"], width=2
                )

    def draw_horizontal_line(self, y: int, width: str):
        """Draw a horizontal line on the grid which spans the whole grid.

        Args:
            y: y co-ordinate of the line.
            width: width of the line. "thick" or "thin".
        """
        match width:
            case "thick":
                self.create_line(
                    0, y, self.grid_width, y, fill=self.colours["fg1"], width=5
                )
            case "thin":
                self.create_line(
                    0, y, self.grid_width, y, fill=self.colours["fg1"], width=2
                )

    def draw_partial_horizontal_line(
        self, y: int, x_start: int, x_stop: int, width: str
    ):
        """Draw a horizontal line on the grid.

        Args:
            y: y co-ordinate of the line.
            x_start: start x co-ordinate of the line.
            x_stop: end x co-ordinate of the line.
            width: width of the line. "thick" or "thin".
        """
        match width:
            case "thick":
                self.create_line(
                    x_start, y, x_stop, y, fill=self.colours["fg1"], width=5
                )
            case "thin":
                self.create_line(
                    x_start, y, x_stop, y, fill=self.colours["fg1"], width=2
                )

    def draw_3x3_box(self, x: int, y: int):
        """Draw a 3 x 3 sudoku box.

        Args:
            x: "box index" from left to right. Starts at 0.
            y: "box index" from top to bottom. Starts at 0.
        """
        grid_width = self.cell_width * 3
        start_x = x * grid_width
        end_x = start_x + grid_width
        start_y = y * grid_width
        end_y = start_y + grid_width
        self.draw_partial_vertical_line(start_x, start_y, end_y, "thick")
        self.draw_partial_vertical_line(end_x, start_y, end_y, "thick")
        self.draw_partial_horizontal_line(start_y, start_x, end_x, "thick")
        self.draw_partial_horizontal_line(end_y, start_x, end_x, "thick")
        for i in range(1, 3):
            cw_i = self.cell_width * i
            self.draw_partial_vertical_line(
                start_x + cw_i, start_y, end_y, "thin"
            )
            self.draw_partial_horizontal_line(
                start_y + cw_i, start_x, end_x, "thin"
            )

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
        cell = ui_cell.Cell(self, row, col, box_index)
        self.cells.append(cell)


class Standard(Base):
    """The standard puzzle grid."""

    def __init__(self, puzzle_page: "ui_pp.PuzzlePage"):
        """Draws the puzzle.

        Args:
            puzzle_page: parent frame.
        """

        Base.__init__(self, puzzle_page)

        # draw box borders
        if puzzle_page.ratio != "square":
            box_size_short, box_size_long = common_bi.calculate_box_sizes(
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
            box_size = common_bi.calculate_square_box_size(
                puzzle_page.dimension
            )
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
                box_index = common_bi.calculate_standard(puzzle_page, c, r)
                cell = ui_cell.Cell(self, r, c, box_index)
                self.cells.append(cell)


class ButterflyGrid(Base):
    """Grid for butterfly sudoku."""

    def __init__(self, puzzle_page: "ui_pp.PuzzlePage"):
        """Draws the puzzle.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        # boxes
        for x in range(4):
            for y in range(4):
                self.draw_3x3_box(x, y)

        # create cells
        for r in range(12):
            for c in range(12):
                self.add_cell(common_bi.calculate_butterfly, r, c)


class CrossGrid(Base):
    """Grid for cross sudoku."""

    def __init__(self, puzzle_page: "ui_pp.PuzzlePage"):
        """Draws the grid.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        # boxes
        for x in range(2, 5):
            for y in range(2):
                self.draw_3x3_box(x, y)
        for x in range(7):
            for y in range(2, 5):
                self.draw_3x3_box(x, y)
        for x in range(2, 5):
            for y in range(5, 7):
                self.draw_3x3_box(x, y)

        # cells
        for r in range(21):
            for c in range(21):
                if 6 <= r <= 14:
                    self.add_cell(common_bi.calculate_cross, r, c)
                elif 6 <= c <= 14:
                    self.add_cell(common_bi.calculate_cross, r, c)


class FlowerGrid(Base):
    """Grid for flower sudoku."""

    def __init__(self, puzzle_page: "ui_pp.PuzzlePage"):
        """Draws the grid.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        # boxes
        for x in range(1, 4):
            self.draw_3x3_box(x, 0)
        for x in range(5):
            for y in range(1, 4):
                self.draw_3x3_box(x, y)
        for x in range(1, 4):
            self.draw_3x3_box(x, 4)

        # cells
        for r in range(15):
            for c in range(15):
                if 3 <= r <= 11:
                    self.add_cell(common_bi.calculate_flower, r, c)
                elif 3 <= c <= 11:
                    self.add_cell(common_bi.calculate_flower, r, c)


class GattaiGrid(Base):
    """Grid for Gattai-3 sudoku."""

    def __init__(self, puzzle_page: "ui_pp.PuzzlePage"):
        """Draws the grid.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        # boxes
        for x in range(1, 4):
            self.draw_3x3_box(x, 0)
        for x in range(1, 5):
            self.draw_3x3_box(x, 1)
        for x in range(5):
            for y in range(2, 4):
                self.draw_3x3_box(x, y)
        for x in range(3):
            self.draw_3x3_box(x, 4)

        # cells
        for r in range(0, 3):
            for c in range(3, 12):
                self.add_cell(common_bi.calculate_gattai, r, c)
        for r in range(3, 6):
            for c in range(3, 15):
                self.add_cell(common_bi.calculate_gattai, r, c)
        for r in range(6, 12):
            for c in range(15):
                self.add_cell(common_bi.calculate_gattai, r, c)
        for r in range(12, 15):
            for c in range(0, 9):
                self.add_cell(common_bi.calculate_gattai, r, c)


class KazagurumaGrid(Base):
    """Grid for Kazaguruma sudoku."""

    def __init__(self, puzzle_page: "ui_pp.PuzzlePage"):
        """Draws the grid.

        Args:
            puzzle_page: parent frame.
        """
        Base.__init__(self, puzzle_page)

        # boxes
        for x in range(1, 4):
            self.draw_3x3_box(x, 0)
        for x in range(1, 7):
            for y in range(1, 3):
                self.draw_3x3_box(x, y)
        for x in range(7):
            self.draw_3x3_box(x, 3)
        for x in range(6):
            for y in range(4, 6):
                self.draw_3x3_box(x, y)
        for x in range(3, 6):
            self.draw_3x3_box(x, 6)

        # cells
        for r in range(3):
            for c in range(3, 12):
                self.add_cell(common_bi.calculate_kazaguruma, r, c)
        for r in range(3, 9):
            for c in range(3, 21):
                self.add_cell(common_bi.calculate_kazaguruma, r, c)
        for r in range(9, 12):
            for c in range(21):
                self.add_cell(common_bi.calculate_kazaguruma, r, c)
        for r in range(12, 18):
            for c in range(18):
                self.add_cell(common_bi.calculate_kazaguruma, r, c)
        for r in range(18, 21):
            for c in range(9, 18):
                self.add_cell(common_bi.calculate_kazaguruma, r, c)


class SamuraiGrid(Base):
    """[TODO:description]"""

    def __init__(self, puzzle_page: "ui_pp.PuzzlePage"):
        """[TODO:description]

        Args:
            puzzle_page: [TODO:description]
        """
        Base.__init__(self, puzzle_page)

        # boxes
        for x in range(3):
            for y in range(2):
                self.draw_3x3_box(x, y)
                self.draw_3x3_box(x + 4, y)
                self.draw_3x3_box(x, y + 5)
                self.draw_3x3_box(x + 4, y + 5)
        for x in range(7):
            self.draw_3x3_box(x, 2)
            self.draw_3x3_box(x, 4)
        for x in range(2, 5):
            self.draw_3x3_box(x, 3)

        # cells
        for r in range(6):
            for c in range(9):
                self.add_cell(common_bi.calculate_samurai, r, c)
                self.add_cell(common_bi.calculate_samurai, r, c + 12)
                self.add_cell(common_bi.calculate_samurai, r + 15, c)
                self.add_cell(common_bi.calculate_samurai, r + 15, c + 12)
        for r in range(6, 9):
            for c in range(21):
                self.add_cell(common_bi.calculate_samurai, r, c)
                self.add_cell(common_bi.calculate_samurai, r + 6, c)
        for r in range(9, 12):
            for c in range(6, 15):
                self.add_cell(common_bi.calculate_samurai, r, c)

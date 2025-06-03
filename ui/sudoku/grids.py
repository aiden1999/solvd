import tkinter as tk

import backend.misc_funcs
import ui.sudoku.cells
import ui.sudoku.puzzle
import ui.theming


class StandardGrid(tk.Canvas):
    """The puzzle grid.

    Attributes:
        cell_width: height/width of a cell (in px).
        dimension: the side length of the puzzle.
        colours: colour theme.
        grid_width: height/width of the grid (in px).
        cells: list of the cells.
    """

    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
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
                cell = ui.sudoku.cells.Cell(self, r, c, box_index)
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


class ButterflyGrid(StandardGrid):
    def __init__(self, puzzle_page: "ui.sudoku.puzzle.PuzzlePage"):
        StandardGrid.__init__(self, puzzle_page)

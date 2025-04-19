import math
import tkinter as tk

import controller

cell_width = 80  # HACK: make configurable/use window dimension


class ConfigureOptionFrame(tk.Frame):
    def __init__(
        self, containing_frame: tk.Frame, type: str, subtype: str, app_window: tk.Tk
    ):
        tk.Frame.__init__(self, containing_frame)

        app_title = "Solvd - Solve " + subtype
        if type == "standard":
            app_title = app_title + " Sudoku"
        controller.change_title(app=app_window, app_title=app_title)

        solve_options_frame = tk.LabelFrame(self, text="Solving Options")
        solve_options_frame.grid(column=0, row=0)

        solve_option = tk.StringVar()
        solve_all_radiobutton = tk.Radiobutton(
            solve_options_frame,
            text="Solve all cells",
            variable=solve_option,
            value="all",
        )
        solve_all_radiobutton.grid(column=0, row=0)
        solve_random_radiobutton = tk.Radiobutton(
            solve_options_frame,
            text="Solve random cell",
            variable=solve_option,
            value="random",
        )
        solve_random_radiobutton.grid(column=0, row=1)
        solve_specific_radiobutton = tk.Radiobutton(
            solve_options_frame,
            text="Solve specific cell(s)",
            variable=solve_option,
            value="specific",
        )
        solve_specific_radiobutton.grid(column=0, row=2)
        check_progress_radiobutton = tk.Radiobutton(
            solve_options_frame,
            text="Check progress",
            variable=solve_option,
            value="progress",
        )
        check_progress_radiobutton.grid(column=0, row=3)

        grid_frame = tk.Frame(self)
        grid_frame.grid(column=1, row=0)

        if type == "standard":
            ratio = "square"
            subtype_words = subtype.split()
            dimension = int(subtype_words[0])
            box_size = math.sqrt(dimension)
            if not box_size.is_integer():
                ratio = subtype_words[-2]
                ratio = ratio[1:]
            puzzle_grid = StandardGrid(grid_frame, dimension, ratio)

        puzzle_grid.grid(column=0, row=0)


class StandardGrid(tk.Canvas):
    def __init__(self, container: tk.Frame, dimension: int, ratio: str):
        grid_width = dimension * cell_width
        tk.Canvas.__init__(self, container, width=grid_width, height=grid_width)

        # draw grid border
        self.create_rectangle(
            0, 0, grid_width, grid_width, fill="white", outline="black", width=5
        )

        # draw box borders
        if ratio != "square":
            if dimension == 12:
                box_size_short = 3
            else:
                box_size_short = 2
            box_size_long = dimension // box_size_short
            box_size_short_px = cell_width * box_size_short
            box_size_long_px = cell_width * box_size_long

            if ratio == "wide":
                # vertical lines
                for i in range(1, box_size_short):
                    bsl_i = i * box_size_long_px
                    self.create_line(bsl_i, 0, bsl_i, grid_width, fill="black", width=5)
                # horizontal lines
                for i in range(1, box_size_long):
                    bss_i = i * box_size_short_px
                    self.create_line(0, bss_i, grid_width, bss_i, fill="black", width=5)

            if ratio == "tall":
                # vertical lines
                for i in range(1, box_size_long):
                    bss_i = i * box_size_short_px
                    self.create_line(bss_i, 0, bss_i, grid_width, fill="black", width=5)
                # horizontal lines
                for i in range(1, box_size_short):
                    bsl_i = i * box_size_long_px
                    self.create_line(0, bsl_i, grid_width, bsl_i, fill="black", width=5)

        else:
            box_size = int(math.sqrt(dimension))
            box_width = cell_width * box_size
            for i in range(1, box_size):
                bw_i = box_width * i
                self.create_line(bw_i, 0, bw_i, grid_width, fill="black", width=5)
                self.create_line(0, bw_i, grid_width, bw_i, fill="black", width=5)

        # draw cell borders:
        for i in range(1, dimension):
            cw_i = cell_width * i
            # vertical lines
            self.create_line(cw_i, 0, cw_i, grid_width, fill="black", width=2)
            # horizontal lines
            self.create_line(0, cw_i, grid_width, cw_i, fill="black", width=2)

        # create cells
        cells = []
        for r in range(dimension):
            for c in range(dimension):
                match ratio:
                    case "square":
                        x = c % box_size
                        y = (r // box_size) * box_size
                    case "wide":
                        x = c % box_size_long
                        y = (r // box_size_short) * box_size_short
                    case "tall":
                        x = c % box_size_short
                        y = (r // box_size_long) * box_size_long
                box_index = int(x) + int(y)
                cell = Cell(self, r, c, box_index)
                cells.append(cell)


class Cell:
    def __init__(self, container: tk.Canvas, row: int, col: int, box: int):
        self.row = row
        self.col = col
        self.box = box

        self.cell_text = tk.Text(
            container,
            height=1,
            width=2,
            font=("Arial", 24),
            relief="flat",
        )  # HACK: make configurable/use window size
        # TODO: hide text borders
        self.cell_text.tag_configure("center", justify="center")
        self.cell_text.tag_add("center", 1.0, "end")

        cell_center = cell_width // 2
        cell_x = (cell_width * col) + cell_center
        cell_y = (cell_width * row) + cell_center

        cell_window = container.create_window(cell_x, cell_y, window=self.cell_text)

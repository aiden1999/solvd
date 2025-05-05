import math
import tkinter as tk

from backend.misc_funcs import (
    calculate_box_index,
    calculate_box_sizes,
    calculate_square_box_size,
)
from controller.controller import (
    change_title,
    enable_button,
    show_page,
    solve_sudoku,
)
from ui.elements import NavigationButtons


class ConfigureOptionFrame(tk.Frame):
    def __init__(self, containing_frame: tk.Frame, type: str, subtype: str, app_window):
        tk.Frame.__init__(self, containing_frame)

        app_title = "Solvd - Solve " + subtype
        if type == "standard":
            app_title = app_title + " Sudoku"
        change_title(app=app_window, app_title=app_title)

        solve_options_frame = tk.LabelFrame(self, text="Solving Options")
        solve_options_frame.grid(column=0, row=0)

        solve_option = tk.StringVar()
        solve_all_radiobutton = tk.Radiobutton(
            solve_options_frame,
            text="Solve all cells",
            variable=solve_option,
            value="all",
            command=lambda: enable_solve_button(),
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

        navigation_buttons = NavigationButtons(self)
        navigation_buttons.grid(row=1, column=0, columnspan=2)
        navigation_buttons.back_button["text"] = "Back to configure Sudoku"
        navigation_buttons.back_button["command"] = lambda: back_to_config_sudoku()
        navigation_buttons.forward_button["text"] = "Solve"
        navigation_buttons.forward_button["command"] = lambda: solve_button_click()
        navigation_buttons.forward_button["state"] = "disabled"

        def back_to_config_sudoku():
            show_page(app_window.configure_sudoku_page, self)
            change_title(app_window, "Solvd - Configure Sudoku")

        def solve_button_click():
            solve_sudoku(puzzle_grid.cells, dimension, ratio)
            match solve_option.get():
                case "all":
                    for cell in puzzle_grid.cells:
                        if cell.is_empty():
                            cell.show_true_value()
                case "random":
                    pass
                case "specific":
                    pass
                case "progress":
                    pass

        def enable_solve_button():
            enable_button(navigation_buttons.forward_button)


class StandardGrid(tk.Canvas):
    def __init__(self, container: tk.Frame, dimension: int, ratio: str):
        self.cell_width = 80
        self.dimension = dimension

        grid_width = dimension * self.cell_width
        tk.Canvas.__init__(self, container, width=grid_width, height=grid_width)

        # draw grid border
        self.create_rectangle(0, 0, grid_width, grid_width, fill="white", outline="black", width=5)

        # draw box borders
        if ratio != "square":
            box_size_short, box_size_long = calculate_box_sizes(dimension)
            box_size_short_px = self.cell_width * box_size_short
            box_size_long_px = self.cell_width * box_size_long

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
            box_size = calculate_square_box_size(dimension)
            box_width = self.cell_width * box_size
            for i in range(1, box_size):
                bw_i = box_width * i
                self.create_line(bw_i, 0, bw_i, grid_width, fill="black", width=5)
                self.create_line(0, bw_i, grid_width, bw_i, fill="black", width=5)

        # draw cell borders:
        for i in range(1, dimension):
            cw_i = self.cell_width * i
            # vertical lines
            self.create_line(cw_i, 0, cw_i, grid_width, fill="black", width=2)
            # horizontal lines
            self.create_line(0, cw_i, grid_width, cw_i, fill="black", width=2)

        # create cells
        self.cells = []
        for r in range(dimension):
            for c in range(dimension):
                box_index = calculate_box_index(dimension, c, r, ratio)
                cell = Cell(self, r, c, box_index)
                self.cells.append(cell)


class Cell:
    def __init__(self, container: StandardGrid, row: int, col: int, box: int):
        self.row = row
        self.col = col
        self.box = box
        self.true_value = 0

        if container.dimension < 10:
            char_width = 1
        else:
            char_width = 2

        self.cell_text = tk.Text(
            container,
            height=1,
            width=char_width,
            font=("Arial", 24),
            relief="flat",
            borderwidth=0,
            highlightbackground="white",
            highlightcolor="white",
        )  # HACK: make configurable/use window size
        self.cell_text.tag_configure("center", justify="center")
        self.cell_text.tag_add("center", 1.0, "end")

        cell_center = container.cell_width // 2
        cell_x = (container.cell_width * col) + cell_center
        cell_y = (container.cell_width * row) + cell_center

        container.create_window(cell_x, cell_y, window=self.cell_text)

    def show_true_value(self):
        self.cell_text.insert("1.0", str(self.true_value))

    def is_empty(self) -> bool:
        value = self.cell_text.get("1.0", "end - 1c")
        if value == "":
            return True
        else:
            return False

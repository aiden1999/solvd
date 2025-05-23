import tkinter as tk
from math import sqrt
from tkinter import ttk

from backend.misc_funcs import (
    calculate_box_index,
    calculate_box_sizes,
    calculate_square_box_size,
)
from controller.controller import (
    change_title,
    disable_button,
    enable_button,
    hide_widget,
    reveal_random_cell,
    reveal_specific_cells,
    show_page,
    solve_sudoku,
)
from ui.elements import NavigationButtons
from ui.theming import load_colours, load_config


class ConfigureOptionFrame(ttk.Frame):
    def __init__(self, containing_frame: ttk.Frame, type: str, subtype: str, app_window):
        ttk.Frame.__init__(self, containing_frame, style="Background.TFrame")

        self.app_window = app_window
        self.chosen_cells = []  # used with specific cells option

        app_title = "Solvd - Solve " + subtype
        if type == "standard":
            app_title = app_title + " Sudoku"
        change_title(self.app_window, app_title)

        solve_options_frame = ttk.LabelFrame(
            self, text="Solving Options", style="Standard.TLabelframe"
        )
        solve_options_frame.grid(column=0, row=0)

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
        other_buttons_frame.grid(row=1, column=0)

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

        grid_frame = ttk.Frame(self)
        grid_frame.grid(column=1, row=0, rowspan=2)

        if type == "standard":
            ratio = "square"
            subtype_words = subtype.split()
            self.dimension = int(subtype_words[0])
            box_size = sqrt(self.dimension)
            if not box_size.is_integer():
                ratio = subtype_words[-2]
                ratio = ratio[1:]
            self.puzzle_grid = StandardGrid(grid_frame, self.dimension, ratio)

        self.puzzle_grid.grid(column=0, row=0)

        self.navigation_buttons = NavigationButtons(self)
        self.navigation_buttons.grid(row=2, column=0, columnspan=2)
        self.navigation_buttons.back_button.configure(
            text="Back to configure Sudoku", command=lambda: back_to_config_sudoku()
        )
        self.navigation_buttons.forward_button.configure(
            text="Solve", command=lambda: forward_button_click(), state="disabled"
        )

        def back_to_config_sudoku():
            show_page(self.app_window.configure_sudoku_page, self)
            change_title(self.app_window, "Solvd - Configure Sudoku")

        def forward_button_click():
            match self.navigation_buttons.forward_button["text"]:
                case "Solve":
                    solve_button_click()
                case "Clear":
                    clear_button_click()

        def all_radiobutton_click():
            self.enable_solve_button()
            hide_widget(specific_cells_button)
            hide_widget(self.specific_cells_solve_again_button)

        def random_radiobutton_click():
            self.enable_solve_button()
            hide_widget(specific_cells_button)
            hide_widget(self.specific_cells_solve_again_button)

        def specific_radiobutton_click():
            disable_button(self.navigation_buttons.forward_button)
            specific_cells_button.grid(column=0, row=0)

        def progress_radiobutton_click():
            hide_widget(specific_cells_button)

        def random_button_click():
            reveal_random_cell(self)

        def specific_button_click():
            SpecificCellsWindow(self)

        def specific_again_button_click():
            reveal_specific_cells(self)
            disable_button(self.specific_cells_solve_again_button)

        def solve_button_click():
            solve_sudoku(self.puzzle_grid.cells, self.dimension, ratio)
            match solve_option.get():
                case "all":
                    for cell in self.puzzle_grid.cells:
                        if cell.is_empty():
                            cell.show_true_value()
                case "random":
                    self.random_button.grid(column=0, row=0)
                    reveal_random_cell(self)
                case "specific":
                    reveal_specific_cells(self)
                    self.specific_cells_solve_again_button.grid(row=0, column=1)
                    disable_button(self.specific_cells_solve_again_button)
                case "progress":
                    pass
            self.navigation_buttons.forward_button["text"] = "Clear"

        def clear_button_click():
            self.navigation_buttons.forward_button["text"] = "Solve"
            for cell in self.puzzle_grid.cells:
                cell.true_value = 0
                cell.cell_text.delete("1.0", "end")
            match solve_option.get():
                case "random":
                    hide_widget(self.random_button)
                case "specific":
                    hide_widget(self.specific_cells_solve_again_button)
                case _:
                    pass

    def enable_solve_button(self):
        enable_button(self.navigation_buttons.forward_button)


class StandardGrid(tk.Canvas):
    def __init__(self, container: ttk.Frame, dimension: int, ratio: str):
        self.cell_width = 80
        self.dimension = dimension
        colours = load_colours()

        grid_width = dimension * self.cell_width
        tk.Canvas.__init__(self, container, width=grid_width, height=grid_width)

        # draw grid border
        self.create_rectangle(
            0,
            0,
            grid_width,
            grid_width,
            fill=colours["background1"],
            outline=colours["foreground1"],
            width=5,
        )

        # draw box borders
        if ratio != "square":
            box_size_short, box_size_long = calculate_box_sizes(dimension)
            box_size_short_px = self.cell_width * box_size_short
            box_size_long_px = self.cell_width * box_size_long

            if ratio == "wide":
                # vertical lines
                for i in range(1, box_size_short):
                    bsl_i = i * box_size_long_px
                    self.create_line(
                        bsl_i, 0, bsl_i, grid_width, fill=colours["foreground1"], width=5
                    )
                # horizontal lines
                for i in range(1, box_size_long):
                    bss_i = i * box_size_short_px
                    self.create_line(
                        0, bss_i, grid_width, bss_i, fill=colours["foreground1"], width=5
                    )

            if ratio == "tall":
                # vertical lines
                for i in range(1, box_size_long):
                    bss_i = i * box_size_short_px
                    self.create_line(
                        bss_i, 0, bss_i, grid_width, fill=colours["foreground1"], width=5
                    )
                # horizontal lines
                for i in range(1, box_size_short):
                    bsl_i = i * box_size_long_px
                    self.create_line(
                        0, bsl_i, grid_width, bsl_i, fill=colours["foreground1"], width=5
                    )

        else:
            box_size = calculate_square_box_size(dimension)
            box_width = self.cell_width * box_size
            for i in range(1, box_size):
                bw_i = box_width * i
                self.create_line(bw_i, 0, bw_i, grid_width, fill=colours["foreground1"], width=5)
                self.create_line(0, bw_i, grid_width, bw_i, fill=colours["foreground1"], width=5)

        # draw cell borders:
        for i in range(1, dimension):
            cw_i = self.cell_width * i
            # vertical lines
            self.create_line(cw_i, 0, cw_i, grid_width, fill=colours["foreground1"], width=2)
            # horizontal lines
            self.create_line(0, cw_i, grid_width, cw_i, fill=colours["foreground1"], width=2)

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
        config = load_config()
        colours = load_colours()

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
        self.cell_text.insert("1.0", str(self.true_value))

    def is_empty(self) -> bool:
        value = self.cell_text.get("1.0", "end - 1c")
        if value == "":
            return True
        else:
            return False

    def get_text(self) -> str:
        return self.cell_text.get("1.0", "end - 1c")


class SpecificCellsWindow(tk.Toplevel):
    def __init__(self, option_frame: ConfigureOptionFrame):
        colours = load_colours()

        tk.Toplevel.__init__(self, option_frame.app_window, background=colours["background0"])
        change_title(self, "Solvd - Choose Cells to Solve")

        cell_buttons = []
        for r in range(option_frame.dimension):
            for c in range(option_frame.dimension):
                cell_button = CellButton(self, c, r)
                cell_buttons.append(cell_button)
                cell_button.grid(column=c, row=r, padx=10, pady=10)

        for cell in option_frame.puzzle_grid.cells:
            if not cell.is_empty():
                for cell_button in cell_buttons:
                    if (cell_button.row == cell.row) and (cell_button.col == cell.col):
                        cell_button["text"] = cell.get_text()
                        disable_button(cell_button)

        ok_button = ttk.Button(
            self, text="OK", style="Standard.TButton", command=lambda: ok_button_click()
        )
        ok_button.grid(
            row=option_frame.dimension, column=0, columnspan=option_frame.dimension, pady=10
        )

        def ok_button_click():
            option_frame.enable_solve_button()
            enable_button(option_frame.specific_cells_solve_again_button)
            for cell in cell_buttons:
                if cell.selected:
                    option_frame.chosen_cells.append(cell)
            self.destroy()


class CellButton(ttk.Button):
    def __init__(self, container: tk.Toplevel, col: int, row: int):
        ttk.Button.__init__(self, container, command=lambda: cell_button_click())
        self["style"] = "Cell.Standard.TButton"
        self.col = col
        self.row = row
        self.selected = False

        def cell_button_click():
            if self.selected:
                self.selected = False
                self["style"] = "Cell.Standard.TButton"
            else:
                self.selected = True
                self["style"] = "Selected.Cell.Standard.TButton"

    def __str__(self) -> str:
        return "C: " + str(self.col) + ", R: " + str(self.row) + ", " + str(self.selected)

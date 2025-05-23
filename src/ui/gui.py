import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

import ui.sudoku
from controller.controller import (
    change_title,
    clear_combobox,
    disable_button,
    enable_button,
    goto_main_menu,
    show_example_image,
    show_page,
)
from ui.elements import NavigationButtons
from ui.theming import configure_style, load_colours


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        colours = load_colours()
        self.configure(background=colours["background0"])
        style = ttk.Style(self)
        configure_style(style)

        containing_frame = ttk.Frame(self, style="Background.TFrame")
        containing_frame.pack(anchor="center", expand=True)

        # create different frames
        self.choose_puzzle_page = ChoosePuzzleFrame(containing_frame, self)
        self.configure_sudoku_page = ConfigureSudokuFrame(containing_frame, self)
        self.configure_water_sort_page = ConfigureWaterSortFrame(containing_frame)
        self.configure_nonogram_page = ConfigureNonogramFrame(containing_frame)
        self.configure_rubiks_cube_page = ConfigureRubiksCubeFrame(containing_frame)

        show_page(self.choose_puzzle_page, "none")
        change_title(self, "Solvd - Select your puzzle")


class ChoosePuzzleFrame(ttk.Frame):
    def __init__(self, containing_frame, app_window):
        ttk.Frame.__init__(self, containing_frame)

        self.containing_frame = containing_frame
        self.app_window = app_window

        self.style = configure_style(self)
        self["style"] = "Background.TFrame"

        solve_sudoku_button = ttk.Button(
            self,
            text="Solve Sudoku",
            command=lambda: self.selected_puzzle("Sudoku", self.app_window.configure_sudoku_page),
            style="Standard.TButton",
        )
        solve_sudoku_button.grid(column=0, row=0, pady=10)

        solve_water_sort_button = ttk.Button(
            self,
            text="Solve Water Sort",
            command=lambda: self.selected_puzzle(
                "Water Sort", self.app_window.configure_water_sort_page
            ),
            style="Standard.TButton",
        )
        solve_water_sort_button.grid(column=0, row=1, pady=10)

        solve_nonogram_button = ttk.Button(
            self,
            text="Solve Nonogram",
            command=lambda: self.selected_puzzle(
                "Nonogram", self.app_window.configure_nonogram_page
            ),
            style="Standard.TButton",
        )
        solve_nonogram_button.grid(column=0, row=2, pady=10)

        solve_rubiks_cube_button = ttk.Button(
            self,
            text="Solve Rubik's Cube",
            command=lambda: self.selected_puzzle(
                "Rubik's Cube",
                self.app_window.configure_rubiks_cube_page,
            ),
            style="Standard.TButton",
        )
        solve_rubiks_cube_button.grid(column=0, row=3, pady=10)

    def selected_puzzle(self, puzzle_type: str, config_page: ttk.Frame):
        show_page(config_page, self.app_window.choose_puzzle_page)
        change_title(self.app_window, "Solvd - Configure " + puzzle_type)


class ConfigureSudokuFrame(ttk.Frame):
    def __init__(self, containing_frame, app_window):
        ttk.Frame.__init__(self, containing_frame)

        self.containing_frame = containing_frame
        self.app_window = app_window

        self.style = configure_style(self)
        self["style"] = "Background.TFrame"

        radiobutton_frame = ttk.Frame(self, style="Background.TFrame")
        radiobutton_frame.grid(row=0, column=0)

        sudoku_type_choice = tk.StringVar()
        standard_sudoku_radiobutton = ttk.Radiobutton(
            radiobutton_frame,
            text="Standard Sudoku",
            variable=sudoku_type_choice,
            value="standard",
            command=lambda: enable_combobox(standard_sudoku_combobox),
            style="Standard.TRadiobutton",
        )
        standard_sudoku_radiobutton.grid(row=0, column=0, sticky="w")
        standard_sudoku_choice = tk.StringVar()
        standard_sudoku_combobox = ttk.Combobox(
            radiobutton_frame,
            textvariable=standard_sudoku_choice,
            state="disabled",
            style="Standard.TCombobox",
        )
        standard_sudoku_combobox["values"] = (
            "4 x 4",
            "6 x 6 (wide boxes)",
            "6 x 6 (tall boxes)",
            "8 x 8 (wide boxes)",
            "8 x 8 (tall boxes)",
            "9 x 9",
            "10 x 10 (wide boxes)",
            "10 x 10 (tall boxes)",
            "12 x 12 (wide boxes)",
            "12 x 12 (tall boxes)",
            "16 x 16",
        )
        standard_sudoku_combobox.bind(
            "<<ComboboxSelected>>",
            lambda _: combobox_option_selected(standard_sudoku_combobox),
        )
        standard_sudoku_combobox.grid(row=1, column=0, sticky="w")

        multidoku_radiobutton = ttk.Radiobutton(
            radiobutton_frame,
            text="Multidoku",
            variable=sudoku_type_choice,
            value="multidoku",
            command=lambda: enable_combobox(multidoku_combobox),
            style="Standard.TRadiobutton",
        )
        multidoku_radiobutton.grid(row=2, column=0, sticky="w")
        multidoku_choice = tk.StringVar()
        multidoku_combobox = ttk.Combobox(
            radiobutton_frame,
            textvariable=multidoku_choice,
            state="disabled",
            style="Standard.TCombobox",
        )
        multidoku_combobox["values"] = (
            "Butterfly Sudoku",
            "Cross Sudoku",
            "Flower Sudoku",
            "Gattai-3",
            "Kazaguruma",
            "Samurai Sudoku",
            "Sohei Sudoku",
            "Tripledoku",
            "Twodoku",
        )
        multidoku_combobox.bind(
            "<<ComboboxSelected>>",
            lambda _: combobox_option_selected(multidoku_combobox),
        )
        multidoku_combobox.grid(row=3, column=0, sticky="w")

        sudoku_variants_radiobutton = ttk.Radiobutton(
            radiobutton_frame,
            text="Sudoku Variants",
            variable=sudoku_type_choice,
            value="variant",
            command=lambda: enable_combobox(sudoku_variants_combobox),
            style="Standard.TRadiobutton",
        )
        sudoku_variants_radiobutton.grid(row=4, column=0, sticky="w")
        sudoku_variants_choice = tk.StringVar()
        sudoku_variants_combobox = ttk.Combobox(
            radiobutton_frame,
            textvariable=sudoku_variants_choice,
            state="disabled",
            style="Standard.TCombobox",
        )
        sudoku_variants_combobox["values"] = (
            "Argyle Sudoku",
            "Asterisk Sudoku",
            "Center Dot Sudoku",
            "Chain Sudoku",
            "Chain Sudoku 6 x 6",
            "Consecutive Sudoku",
            "Even-Odd Sudoku",
            "Girandola Sudoku",
            "Greater Than Sudoku",
            "Jigsaw Sudoku",
            "Killer Sudoku",
            "Little Killer Sudoku",
            "Rossini Sudoku",
            "Skyscraper Sudoku",
            "Sudoku DG",
            "Sudoku Mine",
            "Sudoku X",
            "Sudoku XV",
            "Sujiken",
            "Vudoku",
            "Windoku",
        )
        sudoku_variants_combobox.bind(
            "<<ComboboxSelected>>",
            lambda _: combobox_option_selected(sudoku_variants_combobox),
        )
        sudoku_variants_combobox.grid(row=5, column=0, sticky="w")

        comboboxes = [
            standard_sudoku_combobox,
            multidoku_combobox,
            sudoku_variants_combobox,
        ]

        example_image_frame = ttk.Frame(self)
        example_image_frame.grid(row=0, column=1)
        img = ImageTk.PhotoImage(Image.open("images/placeholder.png"))
        example_image = ttk.Label(example_image_frame, image=img)
        example_image.image = img  # ignore error
        example_image.grid(row=0, column=0)

        navigation_buttons = NavigationButtons(containing_frame=self)
        navigation_buttons.grid(row=1, column=0, columnspan=2)
        navigation_buttons.back_button.configure(
            text="Back to selection", command=lambda: goto_main_menu(self.app_window, self)
        )
        navigation_buttons.forward_button.configure(
            text="Continue", command=lambda: go_to_sudoku_option_config(), state="disabled"
        )

        def combobox_option_selected(combobox: ttk.Combobox):
            enable_button(navigation_buttons.forward_button)
            choice = combobox.get()
            show_example_image(choice, example_image)

        def enable_combobox(combobox: ttk.Combobox):
            disable_button(navigation_buttons.forward_button)
            for box in comboboxes:
                clear_combobox(box)
                box["state"] = "disabled"
            combobox["state"] = "readonly"

        def go_to_sudoku_option_config():
            type_choice = sudoku_type_choice.get()
            subtype_choice = ""
            match type_choice:
                case "standard":
                    subtype_choice = standard_sudoku_choice.get()
                case "multidoku":
                    subtype_choice = multidoku_choice.get()
                case "variant":
                    subtype_choice = sudoku_variants_choice.get()
            config_frame = ui.sudoku.ConfigureOptionFrame(
                containing_frame=self.containing_frame,
                type=type_choice,
                subtype=subtype_choice,
                app_window=self.app_window,
            )
            show_page(config_frame, self)
            # draw configuration thing


class ConfigureWaterSortFrame(ttk.Frame):
    def __init__(self, containing_frame):
        ttk.Frame.__init__(self, containing_frame)

        label = ttk.Label(self, text="water sort config")
        label.grid(row=0, column=0)


class ConfigureNonogramFrame(ttk.Frame):
    def __init__(self, containing_frame):
        ttk.Frame.__init__(self, containing_frame)

        label = ttk.Label(self, text="nonogram config")
        label.grid(row=0, column=0)


class ConfigureRubiksCubeFrame(ttk.Frame):
    def __init__(self, containing_frame):
        ttk.Frame.__init__(self, containing_frame)

        label = tk.Label(self, text="rubik's cube config")
        label.grid(row=0, column=0)

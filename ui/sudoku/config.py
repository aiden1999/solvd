import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

import controller.controller
import ui.elements
import ui.gui
import ui.sudoku.puzzle
import ui.theming


class ConfigureSudokuFrame(ttk.Frame):
    def __init__(self, app_window: "ui.gui.App"):
        ttk.Frame.__init__(self, app_window.containing_frame)

        self.containing_frame = app_window.containing_frame
        self.app_window = app_window
        self.type_choice = None
        self.subtype_choice = None

        self.style = ui.theming.configure_style(self)
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

        navigation_buttons = ui.elements.NavigationButtons(containing_frame=self)
        navigation_buttons.grid(row=1, column=0, columnspan=2)
        navigation_buttons.back_button.configure(
            text="Back to selection",
            command=lambda: back_button_click(),
        )
        navigation_buttons.forward_button.configure(
            text="Continue", command=lambda: go_to_sudoku_option_config(), state="disabled"
        )

        def combobox_option_selected(combobox: ttk.Combobox):
            controller.controller.enable_button(navigation_buttons.forward_button)
            choice = combobox.get()
            controller.controller.show_example_image(choice, example_image)

        def enable_combobox(combobox: ttk.Combobox):
            controller.controller.disable_button(navigation_buttons.forward_button)
            for box in comboboxes:
                controller.controller.clear_combobox(box)
                box["state"] = "disabled"
            combobox["state"] = "readonly"

        def go_to_sudoku_option_config():
            self.type_choice = sudoku_type_choice.get()
            match self.type_choice:
                case "standard":
                    self.subtype_choice = standard_sudoku_choice.get()
                case "multidoku":
                    self.subtype_choice = multidoku_choice.get()
                case "variant":
                    self.subtype_choice = sudoku_variants_choice.get()
            puzzle_page = ui.sudoku.puzzle.PuzzlePage(choices=self)
            controller.controller.show_page(puzzle_page, self)

        def back_button_click():
            controller.controller.show_page(self.app_window.choose_puzzle_page, self)
            controller.controller.change_title(self.app_window, "Solvd - Select your puzzle")

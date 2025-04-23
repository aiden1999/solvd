import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from controller.controller import (
    show_page,
    change_title,
    goto_main_menu,
    enable_button,
    show_example_image,
    disable_button,
    clear_combobox,
)
import ui.sudoku
from ui.elements import NavigationButtons


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        containing_frame = tk.Frame(self)
        containing_frame.grid(column=0, row=0)

        # create different frames
        self.choose_puzzle_page = ChoosePuzzleFrame(containing_frame, self)
        self.configure_sudoku_page = ConfigureSudokuFrame(containing_frame, self)
        self.configure_water_sort_page = ConfigureWaterSortFrame(containing_frame)
        self.configure_nonogram_page = ConfigureNonogramFrame(containing_frame)
        self.configure_rubiks_cube_page = ConfigureRubiksCubeFrame(containing_frame)

        show_page(frame_choice=self.choose_puzzle_page, previous_frame="none")
        change_title(app=self, app_title="Solvd - Select your puzzle")


class ChoosePuzzleFrame(tk.Frame):
    def __init__(self, containing_frame, app_window):
        tk.Frame.__init__(self, containing_frame)

        self.containing_frame = containing_frame
        self.app_window = app_window

        solve_sudoku_button = tk.Button(
            self,
            text="Solve Sudoku",
            command=lambda: self.selected_puzzle(
                puzzle_type="Sudoku",
                config_page=self.app_window.configure_sudoku_page,
            ),
        )
        solve_sudoku_button.grid(column=0, row=0)

        solve_water_sort_button = tk.Button(
            self,
            text="Solve Water Sort",
            command=lambda: self.selected_puzzle(
                puzzle_type="Water Sort",
                config_page=self.app_window.configure_water_sort_page,
            ),
        )
        solve_water_sort_button.grid(column=0, row=1)

        solve_nonogram_button = tk.Button(
            self,
            text="Solve Nonogram",
            command=lambda: self.selected_puzzle(
                puzzle_type="Nonogram",
                config_page=self.app_window.configure_nonogram_page,
            ),
        )
        solve_nonogram_button.grid(column=0, row=2)

        solve_rubiks_cube_button = tk.Button(
            self,
            text="Solve Rubik's Cube",
            command=lambda: self.selected_puzzle(
                puzzle_type="Rubik's Cube",
                config_page=self.app_window.configure_nonogram_page,
            ),
        )
        solve_rubiks_cube_button.grid(column=0, row=3)

    def selected_puzzle(self, puzzle_type: str, config_page: tk.Frame):
        show_page(
            frame_choice=config_page, previous_frame=self.app_window.choose_puzzle_page
        )
        change_title(app=self.app_window, app_title="Solvd - Configure " + puzzle_type)


class ConfigureSudokuFrame(tk.Frame):
    def __init__(self, containing_frame, app_window):
        tk.Frame.__init__(self, containing_frame)

        self.containing_frame = containing_frame
        self.app_window = app_window

        radiobutton_frame = tk.Frame(self)
        radiobutton_frame.grid(row=0, column=0)

        sudoku_type_choice = tk.StringVar()
        standard_sudoku_radiobutton = tk.Radiobutton(
            radiobutton_frame,
            text="Standard Sudoku",
            variable=sudoku_type_choice,
            value="standard",
            command=lambda: enable_combobox(standard_sudoku_combobox),
        )
        standard_sudoku_radiobutton.grid(row=0, column=0, sticky="w")
        standard_sudoku_choice = tk.StringVar()
        standard_sudoku_combobox = ttk.Combobox(
            radiobutton_frame,
            textvariable=standard_sudoku_choice,
            state="disabled",
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

        multidoku_radiobutton = tk.Radiobutton(
            radiobutton_frame,
            text="Multidoku",
            variable=sudoku_type_choice,
            value="multidoku",
            command=lambda: enable_combobox(multidoku_combobox),
        )
        multidoku_radiobutton.grid(row=2, column=0, sticky="w")
        multidoku_choice = tk.StringVar()
        multidoku_combobox = ttk.Combobox(
            radiobutton_frame, textvariable=multidoku_choice, state="disabled"
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

        sudoku_variants_radiobutton = tk.Radiobutton(
            radiobutton_frame,
            text="Sudoku Variants",
            variable=sudoku_type_choice,
            value="variant",
            command=lambda: enable_combobox(sudoku_variants_combobox),
        )
        sudoku_variants_radiobutton.grid(row=4, column=0, sticky="w")
        sudoku_variants_choice = tk.StringVar()
        sudoku_variants_combobox = ttk.Combobox(
            radiobutton_frame, textvariable=sudoku_variants_choice, state="disabled"
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

        example_image_frame = tk.Frame(self)
        example_image_frame.grid(row=0, column=1)
        img = ImageTk.PhotoImage(Image.open("images/placeholder.png"))
        example_image = tk.Label(example_image_frame, image=img)
        example_image.image = img  # ignore error
        example_image.grid(row=0, column=0)

        navigation_buttons = NavigationButtons(containing_frame=self)
        navigation_buttons.grid(row=1, column=0, columnspan=2)
        navigation_buttons.back_button["text"] = "Back to selection"
        navigation_buttons.back_button["command"] = lambda: goto_main_menu(
            app=self.app_window,
            current_page=self,
        )
        navigation_buttons.forward_button["text"] = "Continue"
        navigation_buttons.forward_button["command"] = (
            lambda: go_to_sudoku_option_config()
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


class ConfigureWaterSortFrame(tk.Frame):
    def __init__(self, containing_frame):
        tk.Frame.__init__(self, containing_frame)

        label = tk.Label(self, text="water sort config")
        label.grid(row=0, column=0)


class ConfigureNonogramFrame(tk.Frame):
    def __init__(self, containing_frame):
        tk.Frame.__init__(self, containing_frame)

        label = tk.Label(self, text="nonogram config")
        label.grid(row=0, column=0)


class ConfigureRubiksCubeFrame(tk.Frame):
    def __init__(self, containing_frame):
        tk.Frame.__init__(self, containing_frame)

        label = tk.Label(self, text="rubik's cube config")
        label.grid(row=0, column=0)

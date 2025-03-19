from ast import match_case
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        containing_frame = tk.Frame(self)
        containing_frame.grid(column=0, row=0)

        # create different frames
        self.choose_puzzle_page = ChoosePuzzleFrame(containing_frame, self)
        self.configure_sudoku_page = ConfigureSudokuFrame(containing_frame, self)
        self.configure_water_sort_page = ConfigureWaterSortFrame(containing_frame, self)
        self.configure_nonogram_page = ConfigureNonogramFrame(containing_frame, self)
        self.configure_rubiks_cube_page = ConfigureRubiksCubeFrame(
            containing_frame, self
        )

        self.show_page(self.choose_puzzle_page, "none")
        self.change_title("Solvd - Select your puzzle")

    def show_page(self, frame_choice, previous_frame):
        if previous_frame != "none":
            previous_frame.grid_remove()
        frame_choice.grid(row=0, column=0)

    def change_title(self, app_title):
        self.title(app_title)

    def back_to_menu(self, current_page):
        self.show_page(self.choose_puzzle_page, current_page)
        self.change_title("Solvd - Select your puzzle")


class ChoosePuzzleFrame(tk.Frame):
    def __init__(self, containing_frame, app_window):
        tk.Frame.__init__(self, containing_frame)

        self.containing_frame = containing_frame
        self.app_window = app_window

        label = tk.Label(self, text="test")
        label.grid(row=0, column=0)

        solve_sudoku_button = tk.Button(
            self,
            text="Solve Sudoku",
            command=lambda: self.selected_puzzle("Sudoku"),
        )
        solve_water_sort_button = tk.Button(
            self,
            text="Solve Water Sort",
            command=lambda: self.selected_puzzle("Water Sort"),
        )
        solve_nonogram_button = tk.Button(
            self,
            text="Solve Nonogram",
            command=lambda: self.selected_puzzle("Nonogram"),
        )
        solve_rubiks_cube_button = tk.Button(
            self,
            text="Solve Rubik's Cube",
            command=lambda: self.selected_puzzle("Rubik's Cube"),
        )

        solve_sudoku_button.grid(column=0, row=0)
        solve_water_sort_button.grid(column=0, row=1)
        solve_nonogram_button.grid(column=0, row=2)
        solve_rubiks_cube_button.grid(column=0, row=3)

    def selected_puzzle(self, puzzle_type: str):
        menu = self.app_window.choose_puzzle_page
        match puzzle_type:
            case "Sudoku":
                self.app_window.show_page(self.app_window.configure_sudoku_page, menu)
            case "Water Sort":
                self.app_window.show_page(
                    self.app_window.configure_water_sort_page, menu
                )
            case "Nonogram":
                self.app_window.show_page(self.app_window.configure_nonogram_page, menu)
            case "Rubik's Cube":
                self.app_window.show_page(
                    self.app_window.configure_rubiks_cube_page, menu
                )
        self.app_window.change_title("Solvd - Configure " + puzzle_type)


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
            command=lambda: enable_combobox("standard sudoku"),
        )
        multidoku_radiobutton = tk.Radiobutton(
            radiobutton_frame,
            text="Multidoku",
            variable=sudoku_type_choice,
            value="multidoku",
            command=lambda: enable_combobox("multidoku"),
        )
        sudoku_variants_radiobutton = tk.Radiobutton(
            radiobutton_frame,
            text="Sudoku Variants",
            variable=sudoku_type_choice,
            value="variant",
            command=lambda: enable_combobox("sudoku variants"),
        )
        standard_sudoku_radiobutton.grid(row=0, column=0, sticky="w")
        multidoku_radiobutton.grid(row=2, column=0, sticky="w")
        sudoku_variants_radiobutton.grid(row=4, column=0, sticky="w")

        standard_sudoku_choice = tk.StringVar()
        multidoku_choice = tk.StringVar()
        sudoku_variants_choice = tk.StringVar()
        standard_sudoku_combobox = ttk.Combobox(
            radiobutton_frame, textvariable=standard_sudoku_choice, state="disabled"
        )
        multidoku_combobox = ttk.Combobox(
            radiobutton_frame, textvariable=multidoku_choice, state="disabled"
        )
        sudoku_variants_combobox = ttk.Combobox(
            radiobutton_frame, textvariable=sudoku_variants_choice, state="disabled"
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
        standard_sudoku_combobox.grid(row=1, column=0, sticky="w")
        multidoku_combobox.grid(row=3, column=0, sticky="w")
        sudoku_variants_combobox.grid(row=5, column=0, sticky="w")

        example_image_frame = tk.Frame(self)
        example_image_frame.grid(row=0, column=1)
        img = ImageTk.PhotoImage(Image.open("images/placeholder.png"))
        example_image = tk.Label(example_image_frame, image=img)
        example_image.image = img  # ignore error
        example_image.grid(row=0, column=0)

        navigation_buttons_frame = tk.Frame(self)
        navigation_buttons_frame.grid(row=1, column=0, columnspan=2)
        back_button = tk.Button(
            navigation_buttons_frame,
            text="Back to selection",
            command=lambda: self.app_window.back_to_menu(
                self.app_window.configure_sudoku_page
            ),
        )
        back_button.grid(row=0, column=0)
        continue_button = tk.Button(navigation_buttons_frame, text="Continue")
        continue_button.grid(row=0, column=1)

        def enable_combobox(sudoku_type):
            standard_sudoku_combobox["state"] = "disabled"
            multidoku_combobox["state"] = "disabled"
            sudoku_variants_combobox["state"] = "disabled"
            match sudoku_type:
                case "standard sudoku":
                    standard_sudoku_combobox["state"] = "readonly"
                case "multidoku":
                    multidoku_combobox["state"] = "readonly"
                case "sudoku variants":
                    sudoku_variants_combobox["state"] = "readonly"


class ConfigureWaterSortFrame(tk.Frame):
    def __init__(self, containing_frame, app_window):
        tk.Frame.__init__(self, containing_frame)

        label = tk.Label(self, text="water sort config")
        label.grid(row=0, column=0)


class ConfigureNonogramFrame(tk.Frame):
    def __init__(self, containing_frame, app_window):
        tk.Frame.__init__(self, containing_frame)

        label = tk.Label(self, text="nonogram config")
        label.grid(row=0, column=0)


class ConfigureRubiksCubeFrame(tk.Frame):
    def __init__(self, containing_frame, app_window):
        tk.Frame.__init__(self, containing_frame)

        label = tk.Label(self, text="rubik's cube config")
        label.grid(row=0, column=0)

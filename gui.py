import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.grid(column=0, row=0)

        # create different frames
        choose_puzzle_page = ChoosePuzzleFrame(container, self)
        choose_puzzle_page.grid(row=0, column=0)
        configure_sudoku_page = ConfigureSudokuFrame(container, self)
        configure_sudoku_page.grid(row=0, column=0)

        self.show_page(choose_puzzle_page)
        self.change_title("Solvd - Select your puzzle")

    def show_page(self, frame_choice):
        frame_choice.tkraise()

    def change_title(self, app_title):
        self.title(app_title)


class ChoosePuzzleFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        label = tk.Label(self, text="test")
        label.grid(row=0, column=0)

        solve_sudoku_button = tk.Button(
            self,
            text="Solve Sudoku",
            command=self.on_puzzle_type_button_click("Sudoku"),
        )
        solve_water_sort_button = tk.Button(self, text="Solve Water Sort")
        solve_nonogram_button = tk.Button(self, text="Solve Nonogram")
        solve_rubiks_cube_button = tk.Button(self, text="Solve Rubik's Cube")

        solve_sudoku_button.grid(column=0, row=0)
        solve_water_sort_button.grid(column=0, row=1)
        solve_nonogram_button.grid(column=0, row=2)
        solve_rubiks_cube_button.grid(column=0, row=3)

    def on_puzzle_type_button_click(self, puzzle_type: str):
        match puzzle_type:
            case "Sudoku":
                self.controller.show_page(ConfigureSudokuFrame)
            case "Water Sort":
                pass
            case "Nonogram":
                pass
            case "Rubik's Cube":
                pass
        self.controller.change_title("Solvd - Configure " + puzzle_type)


class ConfigureSudokuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="sudoku config")
        label.grid(row=0, column=0)

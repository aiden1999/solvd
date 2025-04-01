import tkinter as tk
import controller


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

        test_text = tk.Label(self, text="hewwo? 👉🥺👈 ")
        test_text.grid(column=0, row=1)


class StandardGrid(tk.Canvas):
    def __init__(self, container: tk.Frame, dimension: int, ratio):
        tk.Canvas.__init__(self, container)

        c1 = 25
        c2 = (25 * 50) + 25
        self.create_polygon(
            c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="white", outline="black"
        )

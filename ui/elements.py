import tkinter as tk


class NavigationButtons(tk.Frame):
    def __init__(self, containing_frame):
        tk.Frame.__init__(self, containing_frame)

        self.back_button = tk.Button(self)
        self.back_button.grid(row=0, column=0)
        self.forward_button = tk.Button(self)
        self.forward_button.grid(row=0, column=1)

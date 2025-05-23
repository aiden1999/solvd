from tkinter import ttk


class NavigationButtons(ttk.Frame):
    def __init__(self, containing_frame):
        ttk.Frame.__init__(self, containing_frame)

        self.back_button = ttk.Button(self, style="Standard.TButton")
        self.back_button.grid(row=0, column=0)
        self.forward_button = ttk.Button(self, style="Standard.TButton")
        self.forward_button.grid(row=0, column=1)

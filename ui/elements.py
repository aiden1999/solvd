"""Miscellaneous UI elements."""

from tkinter import ttk


class NavigationButtons(ttk.Frame):
    """Buttons for navigation between pages.

    Attributes:
        back_button: button to go back a page.
        forward_button: button to forward a page/confirm an action.
    """

    def __init__(self, containing_frame: ttk.Frame):
        """Creates the frame containing the buttons.

        Args:
            containing_frame: parent frame.
        """
        ttk.Frame.__init__(self, containing_frame)

        self.back_button = ttk.Button(self, style="Standard.TButton")
        self.back_button.grid(row=0, column=0)
        self.forward_button = ttk.Button(self, style="Standard.TButton")
        self.forward_button.grid(row=0, column=1)

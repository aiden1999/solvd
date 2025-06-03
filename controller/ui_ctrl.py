"""Abstraction of UI changes."""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def show_page(frame_choice: ttk.Frame, previous_frame: ttk.Frame | str):
    """Change which frame is currently visible.

    Args:
        frame_choice: the frame to be shown.
        previous_frame: the current frame, which will be hidden.
    """
    if not isinstance(previous_frame, str):
        hide_widget(previous_frame)
    frame_choice.grid(row=0, column=0)


def change_title(app: tk.Tk | tk.Toplevel, app_title: str):
    """Change the title of a window.

    Args:
        app: the window in question.
        app_title: text for the title to be changed to.
    """
    app.title(app_title)


def enable_button(button: ttk.Button):
    """Enable a button so it can be clicked.

    Args:
        button: the button to be enabled.
    """
    button["state"] = "normal"


def disable_button(button: ttk.Button):
    """Disable a button so it cannot be clicked.

    Args:
        button: the button to be disabled.
    """
    button["state"] = "disabled"


def clear_combobox(combobox: ttk.Combobox):
    """Clear a selection from a combobox.

    Args:
        combobox: the combobox to be cleared.
    """
    combobox.set("")


def show_example_image(choice: str, image_label: ttk.Label):
    """Display an image showing an example of the chosen puzzle type.

    Args:
        choice: chosen puzzle type.
        image_label: image container.
    """
    choice = choice.lower()
    choice = choice.replace(" ", "_")
    choice = choice.replace("(", "")
    choice = choice.replace(")", "")
    img = ImageTk.PhotoImage(Image.open("images/" + choice + ".png"))
    image_label.configure(image=img)
    image_label.image = img


def hide_widget(widget: tk.Widget):
    """Remove a widget.

    Args:
        widget: widget to be removed.
    """
    widget.grid_remove()

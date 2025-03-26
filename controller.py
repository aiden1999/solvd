import tkinter as tk
from tkinter import ttk


def show_page(frame_choice: tk.Frame, previous_frame):
    if previous_frame != "none":
        previous_frame.grid_remove()
    frame_choice.grid(row=0, column=0)


def change_title(app: tk.Tk, app_title: str):
    app.title(app_title)


def back_to_menu(app: tk.Tk, current_page: tk.Frame, menu: tk.Frame):
    show_page(menu, current_page)
    change_title(app, "Solvd - Select your puzzle")


def enable_button(button: tk.Button):
    button["state"] = "normal"


def disable_button(button: tk.Button):
    button["state"] = "disabled"


def clear_combobox(combobox: ttk.Combobox):
    combobox.set("")

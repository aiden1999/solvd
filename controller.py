import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


def show_page(frame_choice: tk.Frame, previous_frame):
    if previous_frame != "none":
        previous_frame.grid_remove()
    frame_choice.grid(row=0, column=0)


def change_title(app, app_title: str):
    app.title(app_title)


def goto_main_menu(app, current_page: tk.Frame):
    show_page(app.choose_puzzle_page, current_page)
    change_title(app, "Solvd - Select your puzzle")


def enable_button(button: tk.Button):
    button["state"] = "normal"


def disable_button(button: tk.Button):
    button["state"] = "disabled"


def clear_combobox(combobox: ttk.Combobox):
    combobox.set("")


def show_example_image(choice: str, image_label: tk.Label):
    choice = choice.lower()
    choice = choice.replace(" ", "_")
    choice = choice.replace("(", "")
    choice = choice.replace(")", "")
    img = ImageTk.PhotoImage(Image.open("images/" + choice + ".png"))
    image_label["image"] = img
    image_label.image = img

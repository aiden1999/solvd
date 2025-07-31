"""Theming of the UI."""

import tkinter as tk
from tkinter import ttk

import tomllib

# NOTE: padding is [left, top, right, bottom]


def load_config() -> dict:
    """Load the configuration in the TOML file.

    Returns:
        the configuration as key-value pairs.
    """
    with open("config/config.toml", "rb") as file:
        config = tomllib.load(file)
    return config


def load_colours() -> dict:
    """Load the colours from the theme chosen in configuration.

    Returns:
        the colours as key-value pairs.
    """
    config = load_config()
    colour_theme = config["colours"]
    file_path = f"config/themes/{colour_theme}.toml"
    with open(file_path, "rb") as file:
        colours = tomllib.load(file)
    return colours


def theme_cell_text(cell_text: tk.Text):
    config = load_config()
    colours = load_colours()
    cell_text["height"] = 1
    cell_text["font"] = (config["font"], config["font-size"])
    cell_text["relief"] = "flat"
    cell_text["borderwidth"] = 0
    cell_text["highlightbackground"] = colours["bg1"]
    cell_text["highlightcolor"] = colours["bg1"]
    cell_text["foreground"] = colours["fg0"]
    cell_text["background"] = colours["bg1"]
    cell_text.tag_configure("center", justify="center")
    cell_text.tag_add("center", 1.0, "end")


def configure_style():
    """Configure the styles used in the app."""
    style = ttk.Style()
    style.theme_use("alt")
    config = load_config()
    colours = load_colours()

    style.configure("Background.TFrame", background=colours["bg0"])

    style.configure(
        "Std.TButton",
        background=colours["bg2"],
        foreground=colours["fg0"],
        font=(config["font"], config["font-size"]),
        padding=[20, 10, 20, 10],
        relief="flat",
    )
    style.map(
        "Std.TButton",
        background=[("active", colours["bg3"]), ("disabled", colours["bg1"])],
        foreground=[("disabled", colours["fg2"])],
        relief=[("active", "flat"), ("disabled", "flat")],
    )

    style.configure("P1.Std.TButton", width=18)

    style.configure("Cell.Std.TButton", width=2)

    style.configure("Selected.Cell.Std.TButton", background=colours["accent1"])
    style.map(
        "Selected.Cell.Std.TButton",
        background=[("active", colours["accent0"])],
    )

    style.configure(
        "Std.TRadiobutton",
        background=colours["bg0"],
        foreground=colours["fg0"],
        font=(config["font"], config["font-size"]),
        relief="flat",
        padding=[20, 10, 20, 10],
    )
    style.map(
        "Std.TRadiobutton",
        background=[("active", colours["bg0"])],
        indicatorcolor=[("selected", colours["accent1"])],
    )

    style.configure(
        "Std.TCombobox",
        font=(config["font"], config["font-size"]),
        fieldbackground=colours["bg2"],
        relief="flat",
    )
    style.map(
        "Std.TCombobox",
        background=[("disabled", colours["bg1"]), ("readonly", colours["bg2"])],
    )

    style.configure(
        "Std.TLabelframe",
        background=colours["bg0"],
        relief="solid",
        bordercolor=colours["fg0"],
    )
    style.configure(
        "Std.TLabelframe.Label",
        background=colours["bg0"],
        foreground=colours["fg0"],
        font=(config["font"], config["font-size"]),
    )
    style.configure(
        "Instructions.TLabel",
        background=colours["bg0"],
        font=[config["font"], config["font-size"]],
        foreground=colours["fg0"],
        pady=10,
    )

"""Theming of the UI."""

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


def configure_style():
    """Configure the styles used in the app."""
    style = ttk.Style()
    style.theme_use("alt")
    config = load_config()
    colours = load_colours()

    style.configure("Background.TFrame", background=colours["bg0"])

    style.configure(
        "Standard.TButton",
        background=colours["bg2"],
        foreground=colours["fg0"],
        font=(config["font"], config["font-size"]),
        padding=[20, 10, 20, 10],
        relief="flat",
    )
    style.map(
        "Standard.TButton",
        background=[("active", colours["bg3"]), ("disabled", colours["bg1"])],
        foreground=[("disabled", colours["fg2"])],
        relief=[("active", "flat"), ("disabled", "flat")],
    )

    style.configure("P1.Standard.TButton", width=18)

    style.configure("Cell.Standard.TButton", width=2)

    style.configure(
        "Selected.Cell.Standard.TButton", background=colours["accent1"]
    )
    style.map(
        "Selected.Cell.Standard.TButton",
        background=[("active", colours["accent0"])],
    )

    style.configure(
        "Standard.TRadiobutton",
        background=colours["bg0"],
        foreground=colours["fg0"],
        font=(config["font"], config["font-size"]),
        relief="flat",
        padding=[20, 10, 20, 10],
    )
    style.map(
        "Standard.TRadiobutton",
        background=[("active", colours["bg0"])],
        indicatorcolor=[("selected", colours["accent1"])],
    )

    style.configure(
        "Standard.TCombobox",
        font=(config["font"], config["font-size"]),
        fieldbackground=colours["bg2"],
        relief="flat",
    )
    style.map(
        "Standard.TCombobox",
        background=[("disabled", colours["bg1"]), ("readonly", colours["bg2"])],
    )

    style.configure(
        "Standard.TLabelframe",
        background=colours["bg0"],
        relief="solid",
        bordercolor=colours["fg0"],
    )
    style.configure(
        "Standard.TLabelframe.Label",
        background=colours["bg0"],
        foreground=colours["fg0"],
        font=(config["font"], config["font-size"]),
    )

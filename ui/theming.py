import tomllib
from tkinter import ttk


# NOTE: padding is [left, top, right, bottom]


def load_config() -> dict:
    with open("config/config.toml", "rb") as file:
        config = tomllib.load(file)
    return config


def load_colours() -> dict:
    config = load_config()
    colour_theme = config["colours"]
    file_path = "config/themes/" + colour_theme + ".toml"
    with open(file_path, "rb") as file:
        colours = tomllib.load(file)
    return colours


def configure_style(container):
    style = ttk.Style(container)
    style.theme_use("alt")
    config = load_config()
    colours = load_colours()

    style.configure("Background.TFrame", background=colours["background0"])

    style.configure(
        "Standard.TButton",
        background=colours["background2"],
        foreground=colours["foreground0"],
        font=(config["font"], config["font-size"]),
        padding=[20, 10, 20, 10],
        relief="flat",
    )
    style.map(
        "Standard.TButton",
        background=[("active", colours["background3"]), ("disabled", colours["background1"])],
        foreground=[("disabled", colours["foreground2"])],
        relief=[("active", "flat"), ("disabled", "flat")],
    )

    style.configure("Cell.Standard.TButton", width=2)

    style.configure("Selected.Cell.Standard.TButton", background=colours["accent1"])
    style.map("Selected.Cell.Standard.TButton", background=[("active", colours["accent0"])])

    style.configure(
        "Standard.TRadiobutton",
        background=colours["background0"],
        foreground=colours["foreground0"],
        font=(config["font"], config["font-size"]),
        relief="flat",
        padding=[20, 10, 20, 10],
    )
    style.map(
        "Standard.TRadiobutton",
        background=[("active", colours["background0"])],
        indicatorcolor=[("selected", colours["accent1"])],
    )

    style.configure(
        "Standard.TCombobox",
        font=(config["font"], config["font-size"]),
        fieldbackground=colours["background2"],
        relief="flat",
    )
    style.map(
        "Standard.TCombobox",
        background=[("disabled", colours["background1"]), ("readonly", colours["background2"])],
    )

    return style

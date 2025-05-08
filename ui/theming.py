import tomllib


def load_config() -> dict:
    with open("config/config.toml", "rb") as file:
        config = tomllib.load(file)
    colour_theme = config["colours"]
    file_path = "config/themes/" + colour_theme + ".toml"
    with open(file_path, "rb") as file:
        colours = tomllib.load(file)
    return colours


def create_style():
    pass

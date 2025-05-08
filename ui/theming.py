import tomllib


def load_theme() -> dict:
    config = load_config()
    theme = load_colours(config)
    return theme


def load_config() -> dict:
    with open("config/config.toml", "rb") as file:
        config = tomllib.load(file)
    return config


def load_colours(config: dict) -> dict:
    colour_theme = config["colours"]
    file_path = "config/themes/" + colour_theme + ".toml"
    with open(file_path, "rb") as file:
        colours = tomllib.load(file)
    return colours

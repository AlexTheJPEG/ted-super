from pathlib import Path
from random import choice

import tomllib


def load_bot_settings() -> dict:
    with Path("bot_settings.toml").open("rb") as settings:
        return tomllib.load(settings)


def get_bot_version() -> str:
    with Path("pyproject.toml").open("rb") as project:
        toml = tomllib.load(project)
        return toml["tool"]["poetry"]["version"]


def print_splash() -> None:
    print()

    with Path("splash.txt").open() as splash:
        lines = splash.read().splitlines()

        for line in lines[:5]:
            print(line)

        with Path("splash_texts.txt").open() as splash_texts:
            splash_text = choice(splash_texts.read().splitlines())
        print(lines[5].format(splash_text.center(42, " ")))

        for line in lines[6:10]:
            print(line)

        version_text = f"Version {get_bot_version()}"
        print(lines[10].format(version_text.center(42, " ")))

        for line in lines[11:]:
            print(line)

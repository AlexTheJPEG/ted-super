from pathlib import Path

import tomllib


def load_bot_settings() -> dict:
    with Path("bot_settings.toml").open("rb") as settings:
        return tomllib.load(settings)


def get_bot_version() -> str:
    with Path("pyproject.toml").open("rb") as project:
        toml = tomllib.load(project)
        return toml["project"]["version"]


def print_splash() -> None:
    print()

    with Path("splash.txt").open() as splash:
        lines = splash.read().splitlines()

        for line in lines[:5]:
            print(line)

        splash_text = "TODO: splash text"
        print(lines[5].format(splash_text.center(42, " ")))

        for line in lines[6:10]:
            print(line)

        version_text = f"Version {get_bot_version()}"
        print(lines[10].format(version_text.center(42, " ")))

        for line in lines[11:]:
            print(line)

<p align="center">
    <img width="200" src="./assets/ted.svg" alt="Ted face">
</p>

# 🌟 Ted Super 🌟 
A "retcon" and re-imagining of my Discord bot in Python. This version of the bot will be more focused on minigames and interactions between server members.
Written using [Pycord](https://github.com/Pycord-Development/pycord).

## 🛠 Development Setup
**Note: These instructions assume you are using a Linux system, or Windows via WSL. Change any instructions to fit your operating system as needed.**

To get started, [create a Discord application](https://discord.com/developers/applications) and add a bot user for it. Then, scroll down and make sure the **"Message content intent"** option is toggled on. Finally, add the bot to your server of choice.

After you've made your application, clone this repo somewhere on your machine, then create a file in the root of the project directory called `bot_settings.toml`. This will contain all the settings required for the bot.

The file should contain at least the settings below. An example file has also been provided in the project directory.
```toml
[bot]
token = "your token here"
```

Dependencies are handled by [Poetry](https://python-poetry.org/). Install Poetry on your machine if you haven't already, then simply run `poetry install` in the project directory.

To run the bot, `cd` into the root of the project directory and run `poetry run python -m ted_super` (or activate the virtual environment created by Poetry using `poetry shell` and run `python -m ted_super` in the project directory). If everything has worked, you'll be greeted by an ASCII Ted!
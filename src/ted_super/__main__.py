import discord
from ted_utils.files import load_bot_settings, print_splash

bot = discord.Bot()
settings = load_bot_settings()


@bot.event
async def on_ready() -> None:
    print_splash()


cogs_list = (
    "ping",
    "rps",
)
for cog in cogs_list:
    bot.load_extension(f"ted_cogs.{cog}")

bot.run(settings["bot"]["token"])

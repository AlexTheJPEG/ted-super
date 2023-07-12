import discord
from ted_utils.files import load_bot_settings, print_splash

intents = discord.Intents.default() | discord.Intents.message_content
bot = discord.Bot(intents=intents)
settings = load_bot_settings()


@bot.event
async def on_ready() -> None:
    print_splash()


cogs_list = (
    "ping",
    "rps",
    "guessinggame",
)
for cog in cogs_list:
    bot.load_extension(f"ted_cogs.{cog}")

bot.run(settings["bot"]["token"])

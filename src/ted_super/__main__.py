import discord
from ted_utils.files import load_bot_settings, print_splash

bot = discord.Bot()
settings = load_bot_settings()


@bot.event
async def on_ready() -> None:
    print_splash()


@bot.slash_command()
async def hello(ctx: discord.ApplicationContext) -> None:
    await ctx.respond("hello")


bot.run(settings["bot"]["token"])

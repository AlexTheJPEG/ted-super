import discord
from discord.ext import commands


class GuessingGame(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.slash_command(name="guessinggame", description="Play a number guessing game!")
    @discord.option(
        "max_number",
        description="The highest number I can think of (default: 100)",
        type=int,
        default=100,
        min_value=2,
        max_value=1_000_000,
    )
    async def guessinggame(self, ctx: discord.ApplicationContext, max_number: int) -> None:
        await ctx.respond(max_number)


def setup(bot: discord.Bot) -> None:
    bot.add_cog(GuessingGame(bot))

import random
from asyncio import TimeoutError

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
        random.randint(1, max_number)

        await ctx.respond(
            f"{ctx.author.mention} I'm thinking of a number from 1 to {max_number}...try to guess it! "
            '(Type "cancel" to cancel this game.)'
        )

        def is_number(message: discord.Message) -> bool:
            return message.author == ctx.author and message.content.isdigit()

        try:
            response: discord.Message = await self.bot.wait_for("message", check=is_number, timeout=30)
            await response.reply("yep that's a number")
        except TimeoutError:
            await ctx.respond("You took too long to guess. Cancelled.")


def setup(bot: discord.Bot) -> None:
    bot.add_cog(GuessingGame(bot))

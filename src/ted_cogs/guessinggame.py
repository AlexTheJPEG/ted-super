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
        number = random.randint(1, max_number)
        total_guesses = 0

        await ctx.respond(
            f"{ctx.author.mention} I'm thinking of a number from 1 to {max_number}...try to guess it! "
            '(Type "cancel" at any time to cancel this game.)'
        )

        def check(message: discord.Message) -> bool:
            return message.author == ctx.author and (message.content.isdigit() or message.content == "cancel")

        try:
            while True:
                response: discord.Message = await self.bot.wait_for("message", check=check, timeout=30)

                if response.content == "cancel":
                    await response.reply("Cancelled.")
                    break

                guess = int(response.content)
                total_guesses += 1
                if not 1 <= guess <= max_number:
                    await response.reply(f"That number isn't between 1 and {number}...try again!")
                elif guess < number:
                    await response.reply("My number is higher. Try again!")
                elif guess > number:
                    await response.reply("My number is lower. Try again!")
                else:
                    await response.reply(f"You got it! It took you {total_guesses} guesses!")
                    break
        except TimeoutError:
            await ctx.respond("You took too long to guess. Cancelled.")


def setup(bot: discord.Bot) -> None:
    bot.add_cog(GuessingGame(bot))

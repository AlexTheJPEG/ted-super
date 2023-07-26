from enum import Enum
from random import shuffle

import aiohttp
import discord
from discord.ext import commands
from ted_utils.web import HEADERS


class TriviaAnswer(Enum):
    NO_ANSWER = -1
    A = 0
    B = 1
    C = 2
    D = 3


class TriviaView(discord.ui.View):
    def __init__(self, player: discord.Member | discord.User, *args, **kwargs) -> None:
        self.player = player
        self.answer = TriviaAnswer.NO_ANSWER
        super().__init__(*args, **kwargs)

    async def button_check(self, answer: TriviaAnswer, interaction: discord.Interaction) -> None:
        if interaction.user != self.player:
            await interaction.response.send_message(
                f"Hey! These buttons are for {self.player.mention} only!",
                ephemeral=True,
            )
            return

        self.answer = answer
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="A", style=discord.ButtonStyle.primary)
    async def a_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(TriviaAnswer.A, interaction)

    @discord.ui.button(label="B", style=discord.ButtonStyle.primary)
    async def b_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(TriviaAnswer.B, interaction)

    @discord.ui.button(label="C", style=discord.ButtonStyle.primary)
    async def c_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(TriviaAnswer.C, interaction)

    @discord.ui.button(label="D", style=discord.ButtonStyle.primary)
    async def d_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(TriviaAnswer.D, interaction)


class Trivia(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.slash_command(name="trivia", description="Answer some trivia questions!")
    async def trivia(self, ctx: discord.ApplicationContext) -> None:
        # Get a random question
        async with aiohttp.ClientSession() as session, session.get(
            "https://the-trivia-api.com/api/questions?limit=1&region=US", headers=HEADERS
        ) as response:
            question_json = (await response.json())[0]

        category = question_json["category"]
        question = question_json["question"]

        # Shuffle the answers
        correct_answer = question_json["correctAnswer"].strip()
        answers = [answer.strip() for answer in question_json["incorrectAnswers"] + [correct_answer]]
        shuffle(answers)
        correct_answer_index = answers.index(correct_answer)

        # Correspond each answer with a letter
        answers_with_letters = {chr(97 + i): answers[i] for i in range(len(answers))}

        answers_list = [f":regional_indicator_{k}: {v}" for k, v in answers_with_letters.items()]
        answers_string = "\n".join(answers_list)
        trivia_string = [f"**Category: {category}**", question, answers_string]

        trivia_view = TriviaView(ctx.author, timeout=30, disable_on_timeout=True)
        await ctx.respond("\n\n".join(trivia_string), view=trivia_view)
        await trivia_view.wait()
        if trivia_view.answer == TriviaAnswer.NO_ANSWER:
            await ctx.respond("You took too long to answer. Cancelled.")
            return

        if trivia_view.answer.value == correct_answer_index:
            await ctx.respond(f"{ctx.author.mention} That is correct!")
        else:
            await ctx.respond(
                f"{ctx.author.mention} That is incorrect. The answer is {answers_list[correct_answer_index]}"
            )


def setup(bot: discord.Bot) -> None:
    bot.add_cog(Trivia(bot))

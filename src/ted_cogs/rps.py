from enum import Enum

import asyncio
import discord
from discord.ext import commands


class RPSStatus(Enum):
    WAITING = 0
    ACCEPTED = 1
    DECLINED = 2


class RPSMove(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class RPSRequestView(discord.ui.View):
    def __init__(self, opponent: discord.Member, *args, **kwargs) -> None:
        self.opponent = opponent
        self.status = RPSStatus.WAITING
        super().__init__(*args, **kwargs)

    async def button_check(self, status: RPSStatus, interaction: discord.Interaction) -> None:
        if interaction.user != self.opponent:
            await interaction.response.send_message(
                f"Hey! These buttons are for {self.opponent.mention} only!",
                ephemeral=True,
            )
            return

        self.status = status
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, emoji="👍")
    async def accept_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSStatus.ACCEPTED, interaction)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, emoji="👎")
    async def decline_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSStatus.DECLINED, interaction)


class RPSSelectView(discord.ui.View):
    def __init__(self, player: discord.Member, *args, **kwargs) -> None:
        self.player = player
        self.move = None
        super().__init__(*args, **kwargs)

    async def button_check(self, move: RPSMove, interaction: discord.Interaction) -> None:
        if interaction.user != self.player:
            await interaction.response.send_message(
                f"Hey! These buttons are for {self.player.mention} only!",
                ephemeral=True,
            )
            return

        self.move = move
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.gray, emoji="🪨")
    async def rock_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSMove.ROCK, interaction)

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.gray, emoji="📜")
    async def paper_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSMove.PAPER, interaction)

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.gray, emoji="✂️")
    async def scissors_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSMove.SCISSORS, interaction)


class RPS(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="rps", description="Challenge someone to rock-paper-scissors!")
    async def rps(self, ctx: discord.ApplicationContext, opponent: discord.Member) -> None:
        # Match request flow
        if opponent == ctx.author:
            await ctx.respond("You can't challenge yourself!", ephemeral=True)
            return

        rps_request = RPSRequestView(opponent, timeout=30, disable_on_timeout=True)
        await ctx.respond(
            f"{opponent.mention}, you have been challenged to a rock-paper-scissors match"
            f" by {ctx.author.mention}! Do you accept?\n\nYou have 30 seconds to respond.",
            view=rps_request,
        )
        await rps_request.wait()

        match rps_request.status:
            case RPSStatus.WAITING:
                await ctx.respond(f"{opponent.mention} took too long to respond. Cancelled.")
                return
            case RPSStatus.DECLINED:
                await ctx.respond(f"{opponent.mention} declined the match.")
                return

        # Game flow
        player_select = RPSSelectView(ctx.author, timeout=30, disable_on_timeout=True)
        await ctx.respond(
            f"{ctx.author.mention} Pick your move! You have 30 seconds.",
            view=player_select,
        )
        await player_select.wait()
        if player_select.move is None:
            await ctx.respond(
                f"{ctx.author.mention} took too long to make a move. {opponent.mention} wins by default!"
            )
            return

        opponent_select = RPSSelectView(opponent, timeout=30, disable_on_timeout=True)
        await ctx.respond(
            f"{ctx.author.mention} Pick your move! You have 30 seconds.",
            view=opponent_select,
        )
        await opponent_select.wait()
        if opponent_select.move is None:
            await ctx.respond(
                f"{opponent.mention} took too long to make a move. {ctx.author.mention} wins by default!"
            )
            return
        
        game_string = f"{ctx.author.mention} {opponent.mention} Rock, paper, scissors, shoot!"
        game_message = await ctx.respond(game_string)
        
        await asyncio.sleep(2)

        game_string += f"\n\n{ctx.author.mention} "
        match player_select.move:
            case RPSMove.ROCK:
                game_string += "🪨   "
            case RPSMove.PAPER:
                game_string += "📜   "
            case RPSMove.SCISSORS:
                game_string += "✂️   "
        match opponent_select.move:
            case RPSMove.ROCK:
                game_string += "🪨 "
            case RPSMove.PAPER:
                game_string += "📜 "
            case RPSMove.SCISSORS:
                game_string += "✂️ "
        game_string += f"{opponent.mention}\n\n"
        
        match (player_select.move, opponent_select.move):
            case (RPSMove.ROCK, RPSMove.ROCK):
                game_string += "It's a draw."
            case (RPSMove.ROCK, RPSMove.PAPER):
                game_string += f"{opponent.mention} wins!"
            case (RPSMove.ROCK, RPSMove.SCISSORS):
                game_string += f"{ctx.author.mention} wins!"
            case (RPSMove.PAPER, RPSMove.ROCK):
                game_string += f"{ctx.author.mention} wins!"
            case (RPSMove.PAPER, RPSMove.PAPER):
                game_string += "It's a draw."
            case (RPSMove.PAPER, RPSMove.SCISSORS):
                game_string += f"{opponent.mention} wins!"
            case (RPSMove.SCISSORS, RPSMove.ROCK):
                game_string += f"{opponent.mention} wins!"
            case (RPSMove.SCISSORS, RPSMove.PAPER):
                game_string += f"{ctx.author.mention} wins!"
            case (RPSMove.SCISSORS, RPSMove.SCISSORS):
                game_string += "It's a draw."
        
        await game_message.edit(game_string)


def setup(bot: discord.Bot):
    bot.add_cog(RPS(bot))

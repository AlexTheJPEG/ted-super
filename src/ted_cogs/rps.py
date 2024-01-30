import asyncio
import random
from enum import Enum

import discord
from discord.ext import commands


class RPSGame(Enum):
    PVP = 0
    PVB = 1


class RPSStatus(Enum):
    WAITING = 0
    ACCEPTED = 1
    DECLINED = 2


class RPSMove(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


RPS_EMOJIS = {
    RPSMove.ROCK: "🪨",
    RPSMove.PAPER: "📜",
    RPSMove.SCISSORS: "✂",
}


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
    async def accept_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSStatus.ACCEPTED, interaction)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, emoji="👎")
    async def decline_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSStatus.DECLINED, interaction)


class RPSSelectView(discord.ui.View):
    def __init__(self, player: discord.Member | discord.User, *args, **kwargs) -> None:
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
    async def rock_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSMove.ROCK, interaction)

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.gray, emoji="📜")
    async def paper_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSMove.PAPER, interaction)

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.gray, emoji="✂️")
    async def scissors_button_callback(self, _: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSMove.SCISSORS, interaction)


class RPS(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.slash_command(name="rps", description="Challenge someone to rock-paper-scissors!")
    @discord.option(
        "opponent",
        description="Who you want to play against",
        type=discord.Member,
        required=True,
    )
    @discord.option(
        "replay_after_draw",
        description="Whether another game starts automatically after a draw (default: true)",
        type=bool,
        required=False,
        default=True,
    )
    async def rps(self, ctx: discord.ApplicationContext, opponent: discord.Member, replay_after_draw: bool) -> None:
        # Match request flow

        if opponent == ctx.author:
            # Players can't play against themselves
            await ctx.respond("You can't challenge yourself!", ephemeral=True)
            return

        if opponent == self.bot.user:
            # Player plays against the bot
            game_type = RPSGame.PVB

            await ctx.respond("Alright, I accept your challenge!")
        else:
            # Player requests to play against another player
            game_type = RPSGame.PVP

            # Prompt for opponent player to accept / decline
            rps_request = RPSRequestView(opponent, timeout=30, disable_on_timeout=True)
            await ctx.respond(
                f"{opponent.mention}, you have been challenged to a rock-paper-scissors match"
                f" by {ctx.author.mention}! Do you accept?"
                + ("\n**(auto-replay after draw is off)**" if not replay_after_draw else "")
                + "\n\nYou have 30 seconds to respond.",
                view=rps_request,
            )
            await rps_request.wait()

            # If the opponent doesn't respond / declines the match
            match rps_request.status:
                case RPSStatus.WAITING:
                    await ctx.respond(f"{opponent.mention} took too long to respond. Cancelled.")
                    return
                case RPSStatus.DECLINED:
                    await ctx.respond(f"{opponent.mention} declined the match.")
                    return

        # Game flow
        game_running = True

        while game_running:
            # Player selects move
            player_select = RPSSelectView(ctx.author, timeout=30, disable_on_timeout=True)
            await ctx.respond(
                f"{ctx.author.mention} Pick your move! You have 30 seconds.",
                view=player_select,
            )
            await player_select.wait()

            # If the player takes too long to move
            if player_select.move is None:
                if game_type == RPSGame.PVP:
                    await ctx.respond(f"{ctx.author.mention} took too long to make a move. {opponent.mention} wins by default!")
                else:
                    await ctx.respond("You took too long to make a move. I win by default!")
                return
            # Otherwise set the player move
            player_move = player_select.move

            # Opponent selects move
            if game_type == RPSGame.PVP:
                opponent_select = RPSSelectView(opponent, timeout=30, disable_on_timeout=True)
                await ctx.respond(
                    f"{opponent.mention} Pick your move! You have 30 seconds.",
                    view=opponent_select,
                )
                await opponent_select.wait()
                if opponent_select.move is None:
                    await ctx.respond(f"{opponent.mention} took too long to make a move. {ctx.author.mention} wins by default!")
                    return
                opponent_move = opponent_select.move
            else:
                opponent_move = random.choice([RPSMove.ROCK, RPSMove.PAPER, RPSMove.SCISSORS])

            # Rock, paper, scissors, shoot!
            if game_type == RPSGame.PVP:
                game_string = f"{ctx.author.mention} {opponent.mention} Rock, paper, scissors, shoot!"
            else:
                game_string = f"{ctx.author.mention} Rock, paper, scissors, shoot!"
            game_message = await ctx.respond(game_string)
            await asyncio.sleep(2)

            # Update game string with each player's moves and the result
            game_string += f"\n\n{ctx.author.mention if game_type == RPSGame.PVP else 'You'} "
            game_string += f"{RPS_EMOJIS[player_move]}  {RPS_EMOJIS[opponent_move]}"
            game_string += f" {opponent.mention if game_type == RPSGame.PVP else 'Me'}\n\n"

            match (player_move, opponent_move):
                # Draw
                case (RPSMove.ROCK, RPSMove.ROCK) | (RPSMove.PAPER, RPSMove.PAPER) | (RPSMove.SCISSORS, RPSMove.SCISSORS):
                    game_string += "It's a draw."
                    if not replay_after_draw:
                        game_running = False

                # Opponent wins
                case (RPSMove.ROCK, RPSMove.PAPER) | (RPSMove.PAPER, RPSMove.SCISSORS) | (RPSMove.SCISSORS, RPSMove.ROCK):
                    if game_type == RPSGame.PVP:
                        game_string += f"{opponent.mention} wins!"
                    else:
                        game_string += "I win!"
                    game_running = False

                # Player wins
                case (RPSMove.ROCK, RPSMove.SCISSORS) | (RPSMove.PAPER, RPSMove.ROCK) | (RPSMove.SCISSORS, RPSMove.PAPER):
                    if game_type == RPSGame.PVP:
                        game_string += f"{ctx.author.mention} wins!"
                    else:
                        game_string += "You win."
                    game_running = False

            if game_running:
                game_string += " Replaying..."

            await game_message.edit(game_string)

            if game_running:
                await asyncio.sleep(2)


def setup(bot: discord.Bot) -> None:
    bot.add_cog(RPS(bot))

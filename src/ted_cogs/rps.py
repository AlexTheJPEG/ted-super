from enum import Enum

import discord
from discord.ext import commands


class RPSStatus(Enum):
    WAITING = 0
    ACCEPTED = 1
    DECLINED = 2


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
        self.stop()

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, emoji="👍")
    async def accept_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSStatus.ACCEPTED, interaction)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, emoji="👎")
    async def decline_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check(RPSStatus.DECLINED, interaction)


class RPS(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    @discord.slash_command(name="rps", description="Challenge someone to rock-paper-scissors!")
    async def rps(self, ctx: discord.ApplicationContext, against: discord.Member) -> None:
        if against == ctx.author:
            await ctx.respond("You can't challenge yourself!", ephemeral=True)
            return

        rps_request = RPSRequestView(against, timeout=30, disable_on_timeout=True)
        await ctx.respond(
            f"{against.mention}, you have been challenged to a rock-paper-scissors match"
            f" by {ctx.author.mention}! Do you accept?\n\nYou have 30 seconds to respond.",
            view=rps_request,
        )
        await rps_request.wait()

        match rps_request.status:
            case RPSStatus.WAITING:
                await ctx.respond(f"{against.mention} took too long to respond. Cancelled.")
                return
            case RPSStatus.DECLINED:
                await ctx.respond(f"{against.mention} declined the match.")
                return

        await ctx.respond("Game on! TODO")


def setup(bot: discord.Bot):
    bot.add_cog(RPS(bot))
import discord
from discord.ext import commands


class RPSRequestView(discord.ui.View):
    def __init__(self, against: discord.Member, *args, **kwargs) -> None:
        self.against = against
        self.status = ""  # TODO: Use enum
        super().__init__(*args, **kwargs)
    
    async def button_check(self, status: str, interaction: discord.Interaction) -> None:
        if interaction.user != self.against:
            await interaction.response.send_message(
                f"Hey! These buttons are for {self.against.mention} only!",
                ephemeral=True,
            )
            return
        for child in self.children:
            child.disabled = True
        self.status = status
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, emoji="👍")
    async def accept_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check("Accepted", interaction)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, emoji="👎")
    async def decline_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        await self.button_check("Declined", interaction)


class RPS(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    @discord.slash_command(name="rps", description="Challenge someone to rock-paper-scissors!")
    async def rps(self, ctx: discord.ApplicationContext, against: discord.Member) -> None:
        if against == ctx.author:
            await ctx.respond("You can't challenge yourself!", ephemeral=True)
            return

        rps_request = RPSRequestView(against, timeout=30)
        await ctx.respond(
            f"{against.mention}, you have been challenged to a rock-paper-scissors match"
            f" by {ctx.author.mention}! Do you accept?\n\nYou have 30 seconds to respond.",
            view=rps_request,
        )
        await rps_request.wait()
        match rps_request.status:
            case "":
                await ctx.respond(f"{against.mention} took too long to respond. Cancelled.")
                return
            case "Declined":
                await ctx.respond(f"{against.mention} declined the match.")
                return
        await ctx.respond("Game on! TODO")


def setup(bot: discord.Bot):
    bot.add_cog(RPS(bot))
import discord
from discord.ext import commands


class RPSRequestView(discord.ui.View):
    def __init__(self, against: discord.Member, *args, **kwargs) -> None:
        self.against = against
        self.status = ""  # TODO: Use enum
        super().__init__(*args, **kwargs)

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, emoji="👍")
    async def accept_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, emoji="👎")
    async def decline_button_callback(self, button: discord.Button, interaction: discord.Interaction) -> None:
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)


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



def setup(bot: discord.Bot):
    bot.add_cog(RPS(bot))
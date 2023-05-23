import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    @discord.slash_command(name="ping", description="Ping Ted")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(f"🏓 Pong! (**{round(self.bot.latency * 1000, 1)} ms**)")


def setup(bot: discord.Bot):
    bot.add_cog(Ping(bot))
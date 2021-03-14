import discord
from config import BotConfig
from discord.ext import commands
from extra_tools import bot_says, fstat


class Minecraft(commands.Cog, name="Minecraft Info! ⛏"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="minecraft", aliases=["mc"])
    async def minecraft(self, ctx):
        """Replies with minecraft info"""
        with open("dev_meta/minecraft_info.txt") as minecraft_info:
            minecraft_info = minecraft_info.read()
        await ctx.send(embed=bot_says("Goon Lagoon Info ⛏", minecraft_info, multi_line=True))


def setup(bot):
    bot.add_cog(Minecraft(bot))

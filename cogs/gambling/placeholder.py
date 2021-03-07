from discord.ext import commands
from extra_tools import bot_says


class PlaceHolder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="games", aliases=["mug", "s3", "rps"])
    async def games(self, ctx):
        """Placeholder for coin games"""
        await ctx.send(embed=bot_says("👷‍♂️ Gambling games are in production"))


def setup(bot):
    bot.add_cog(PlaceHolder(bot))

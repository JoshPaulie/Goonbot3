import random

from discord.ext import commands
from extra_tools import bot_says


class HoboUsernames(commands.Cog, name="Hobo Usernames 📃"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        with open("cogs_helpers/hobo_usernames/base_usernames.txt", mode="r") as usernames:
            self.usernames_list = usernames.readlines()

    @commands.command(name="username", aliases=["un"])
    async def username(self, ctx):
        """Responds with one of Hobo's signature usernames"""
        picked_username = random.choice(self.usernames_list)
        self.usernames_list.remove(picked_username)
        random.shuffle(self.usernames_list)
        await ctx.send(embed=bot_says(picked_username.strip("\n")))


def setup(bot):
    bot.add_cog(HoboUsernames(bot))

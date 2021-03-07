import discord
from discord.ext import commands
from pyyoutube import Api
from pprint import pprint
from config import BotConfig
from extra_tools import bot_says


class YoutubeCommands(commands.Cog, name="Youtube Commands! 🎥"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="campbell", aliases=["drcampbell", "camp"])
    async def campbell(self, ctx):
        """Returns a link to the latest Dr. Campbell video"""
        # ? For the record, I'm not sure how most of this works. Pray it doesn't break.
        ytapi = Api(api_key="AIzaSyARUGlMzOddcIW9QDaQ35sdPhHJnGGIz4E")
        camp_uploaded_pl = "UUF9IOB2TExg3QIBupFtBDxg"
        latest_upload = ytapi.get_playlist_items(playlist_id=camp_uploaded_pl, count=1)
        latest_url = "https://www.youtube.com/watch?v=" + latest_upload.items[0].snippet.resourceId.videoId
        await ctx.send(latest_url)


def setup(bot):
    bot.add_cog(YoutubeCommands(bot))

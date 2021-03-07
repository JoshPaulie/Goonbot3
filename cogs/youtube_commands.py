from pprint import pprint

import arrow
import discord
from config import BotConfig
from discord.ext import commands
from extra_tools import bot_says
from pyyoutube import Api


class YoutubeCommands(commands.Cog, name="Youtube Commands! 🎥"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="campbell", aliases=["drcampbell", "camp"])
    async def campbell(self, ctx):
        """Returns a link to the latest Dr. Campbell video"""
        # ? For the record, I'm not sure how most of this works. Pray it doesn't break.
        ytapi = Api(api_key=BotConfig.Keys.google_api)
        camp_uploaded_pl = "UUF9IOB2TExg3QIBupFtBDxg"
        latest_upload = ytapi.get_playlist_items(playlist_id=camp_uploaded_pl, count=1)
        latest_url = "https://www.youtube.com/watch?v=" + latest_upload.items[0].snippet.resourceId.videoId
        latest_published_at = latest_upload.items[0].snippet.publishedAt
        await ctx.send(f"{latest_url} (*{arrow.get(latest_published_at).humanize()}*)")


def setup(bot):
    bot.add_cog(YoutubeCommands(bot))

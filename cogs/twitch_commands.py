import discord
import twitch
import arrow
from discord.ext import commands

from config import BotConfig
from extra_tools import bot_says

goon_twitch = [
    "sailexstreams",
    "joshpaulie",
    "boxrog",
    "ectoplax",
    "poydok",
    "mltsimpleton",
    "howtobeangry",
    "cradmajone",
    "a_toxic_hobo",
]

ttv = twitch.Helix(BotConfig.Keys.twitch_client_id, BotConfig.Keys.twitch_client_secret)


def make_ttv_embed(ttv_username):
    link_embed = discord.Embed(color=BotConfig.color)
    ttv_username = ttv.user(ttv_username)
    if ttv_username is not None:
        link_embed.url = f"https://www.twitch.tv/{ttv_username.display_name}"
        if ttv_username.is_live:
            link_embed.title = f"{ttv_username.display_name} is live!"
            link_embed.set_thumbnail(url=ttv_username.profile_image_url)
            link_embed.description = "\n".join(
                [
                    ttv_username.stream.title,
                    f"*Began {arrow.get(ttv_username.stream.started_at).humanize()}*",
                ]
            )
        else:
            link_embed.title = f"{ttv_username.display_name} is offline 😌"
            link_embed.set_thumbnail(url=ttv_username.offline_image_url)
    else:
        link_embed.title = "The username you search doesn't exist"
        link_embed.description = "*Is it possible they changed their name, or was banned?*"

    return link_embed


class TwitchCommands(commands.Cog, name="Twitch Commands! 📺"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="live", aliases=["online", "twitch"])
    async def live(self, ctx, twitch_username: str = None):
        """Check to see if any g00ns are live on Twitch!

        Alternatively: You can add any username to check if they are live
        Syntax: `.live` or `.live souljaboy`"""

        if twitch_username is None:
            """ MAKE LIST OF THOSE ONLINE """
            online_goons = []
            for goon in goon_twitch:
                goon = ttv.user(goon)
                if goon.is_live:
                    online_goons.append(goon)

            """ BUILD AND SEND EMBED FROM THOSE ONLINE """

            if len(online_goons) > 0:
                for goon in online_goons:
                    await ctx.send(embed=make_ttv_embed(goon.display_name))
            else:
                await ctx.send(embed=bot_says("No goons are streaming! 💤"))
        else:
            await ctx.send(embed=make_ttv_embed(twitch_username))

    @commands.command(name="paypig", aliases=["dekar"])
    async def paypig(self, ctx):
        """Link to Dekar's stream"""
        link = await ctx.send(embed=make_ttv_embed("dekar173"))
        await link.add_reaction("🐽")

    @commands.command(name="jerma", aliases=["jerma985"])
    async def jerma(self, ctx):
        """Link to Jerma's Stream"""
        link = await ctx.send(embed=make_ttv_embed("jerma985"))
        await link.add_reaction("🤡")

    @commands.command(name="tyler1", aliases=["tyler", "t1", "loltyler1"])
    async def tyler1(self, ctx):
        """Link to Tyler's Stream"""
        link = await ctx.send(embed=make_ttv_embed("loltyler1"))
        await link.add_reaction("🏆")

    # the_happy_hob
    @commands.command(name="hob", aliases=["happyhob"])
    async def happy_hob(self, ctx):
        """Link to The Happy Hob's Stream"""
        await ctx.send(embed=make_ttv_embed("the_happy_hob"))

    @commands.command(name="dangheesling", aliases=["dan", "dang"])
    async def dangheesling(self, ctx):
        """Link to Tyler's Stream"""
        await ctx.send(embed=make_ttv_embed("dangheesling"))

    @commands.command(name="dunkstream", aliases=["videogamedunkey", "dunkey", "dunk"])
    async def dunkstream(self, ctx):
        """Link to dunkey's Stream"""
        await ctx.send(embed=make_ttv_embed("dunkstream"))


def setup(bot):
    bot.add_cog(TwitchCommands(bot))

import random

from discord.ext import commands
from discord.ext.commands import BucketType
from config import BotConfig

from extra_tools import bot_says

random_emoji = random.choice(
    [
        "♥",
        "💜",
        "❣",
        "🧡",
        "💓",
        "💟",
        "💞",
        "🤍",
        "😻",
        "🥰",
        "😍",
        "💌",
        "❤",
        "💕",
        "🖤",
        "💛",
    ]
)


class Affirmations(commands.Cog, name="Affirmations 💞"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.cooldown(1, 60, type=BucketType.user)
    @commands.command(name="cily")
    async def cily(self, ctx):
        """Reminds Conrad about your true feelings for him"""
        possible_letters = [
            "Conrad, I love you",
            "Conrad I love you",
            "You are my best friend",
            "I love the way you mow lawns",
        ]

        await ctx.send(
            embed=bot_says(f"{random.choice(possible_letters)} <@164600098142158848> {random_emoji}")
        )

    @cily.error
    async def cilyError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=bot_says(f"You can tell him again in `{round(error.retry_after)}` seconds 🤗")
            )

    @commands.cooldown(1, 60, type=BucketType.user)
    @commands.command(name="jyb")
    async def jyb(self, ctx):
        """At any moment, somewhere in the world, Justin is being based."""
        possible_letters = [
            "Justin you're based",
            "Justin, you're based.",
            "god you're based.",
            "Hey, I didn't know based was on the menu!",
            "It's looking pretty based.",
        ]

        await ctx.send(embed=bot_says(f"{random.choice(possible_letters)} <@104488534936666112> 😎"))

    @jyb.error
    async def jybError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=bot_says(f"You can tell him again in `{round(error.retry_after)}` seconds 🤗")
            )

    @commands.cooldown(1, 60, type=BucketType.user)
    @commands.command(name="ily")
    async def ily(self, ctx):
        """Send an affirmation to a random goon!"""
        possible_letters = ["I love you"]

        await ctx.send(
            embed=bot_says(
                f"{random.choice(possible_letters)} <@{random.choice(BotConfig.GoonIDs.goons)}> {random_emoji}"
            )
        )

    @ily.error
    async def ilyError(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                embed=bot_says(f"You can tell them again in `{round(error.retry_after)}` seconds 🤗")
            )


def setup(bot):
    bot.add_cog(Affirmations(bot))

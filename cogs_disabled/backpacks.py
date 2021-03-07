import discord
from discord.ext import commands
from pymongo.errors import DuplicateKeyError

from config import BotConfig
from extra_tools import bot_says


class Backpacks(commands.Cog, name="Backpacks 🎒"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def has_backpack(self, discord_id):
        """Creates backpack for provided discord_id user"""
        try:
            await self.bot.backpacks.insert_one({"_id": discord_id})
        except DuplicateKeyError:
            pass

        user_backpack = await self.bot.backpacks.find_one(discord_id)
        return user_backpack

    @commands.command(name="backpack", aliases=["bp"])
    async def backpack(self, ctx):
        """Opens up your backpack!"""
        author = ctx.message.author
        user_backpack = await self.has_backpack(author.id)

        bp_embed = discord.Embed(title=f"{author.name}'s Backpack", color=BotConfig.color)
        for item, count in user_backpack.items():
            if item not in ["_id", "wallet"]:
                bp_embed.add_field(name=item, value=f"**{count}**", inline=True)

        if len(bp_embed.fields) > 0:
            await ctx.send(embed=bp_embed)
        else:
            await ctx.send(embed=bot_says("It looks like your backpack is empty!"))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Watches for reactions and adds to backpack"""
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji = payload.emoji
        user_backpack = await self.has_backpack(message.author.id)

        if emoji.is_custom_emoji() is False:
            await self.bot.backpacks.update_one(user_backpack, {"$inc": {emoji.name: 1}})
        else:
            await self.bot.backpacks.update_one(user_backpack, {"$inc": {f"<:{emoji.name}:{emoji.id}>": 1}})


def setup(bot):
    bot.add_cog(Backpacks(bot))

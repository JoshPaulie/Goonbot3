import asyncio
import datetime
import random

import discord
import requests
from discord.ext import commands

from config import BotConfig
from extra_tools import bot_says, is_bexli


class GeneralCommands(commands.Cog, name="General Commands 🤖"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="vtuber", aliases=["vtubers", "vt"])
    async def vtuber(self, ctx):
        """Better than ever!"""
        await ctx.message.delete()
        await ctx.send("🤫", delete_after=1)

    @commands.command(name="pfp", aliases=["pic"])
    async def pfp(self, ctx, user: discord.User = None):
        """GOON BOT BEATS BONGO 1000:1"""
        if user is None:
            selected_user = ctx.author
        else:
            selected_user = user

        pfp_url = str(selected_user.avatar_url_as(format=None, static_format="png", size=2048))

        if requests.get(pfp_url).status_code == 404:
            await ctx.send(
                embed=bot_says(f"Image failed. Nothing matters and life sucks."),
                delete_after=2,
            )
        else:
            embed = discord.Embed(color=BotConfig.color)
            embed.set_author(name=f"{selected_user.name} 📸", url=pfp_url)
            embed.set_image(url=pfp_url)
            await ctx.send(embed=embed)

    @commands.command(name="todo")
    async def todo(self, ctx):
        """Replies wit current todo list"""
        with open("dev_meta/todo.txt") as todo_list:
            todo_list = todo_list.read()
        await ctx.send(embed=bot_says("To-do list", todo_list, multi_line=True))

    @commands.command(name="coinflip", aliases=["coin", "cf", "flip", "50/50"])
    async def coin_flip(self, ctx):
        """Flips a coin!"""
        coin_sides = ["Heads", "Tails"]
        flip = random.choice(coin_sides)
        await ctx.send(embed=bot_says(f"{flip}!"))

    @commands.command(name="wni", aliases=["invite?", "invite"])
    async def wow_no_invite(self, ctx):
        """Wow, no invite?"""
        complaint = random.choice(
            [
                "Wow, no invite?",
                "WOW..no invite?",
                "My invite must have gotten lost in the mail",
                "Wow no invite?",
                "WOW. NOT INVITED, NOT SURPRISED.",
                "WOW. NO INVITE, NOT SURPRISED.",
                "come on man not cool",
                "i thought we were friends",
                "guess ill hangout here... alone... again",
                "hey, come on! I like darts too",
                "Is it a surprise party for me?\nIs that why I don't know?",
            ]
        )
        await ctx.send(embed=bot_says(complaint))

    @is_bexli()
    @commands.command(name="changes", aliases=["changelog"])
    async def change(self, ctx):
        """Announce changes made to Goonbot!"""
        await ctx.message.delete()
        with open("dev_meta/recent_changes.txt") as changes:
            changes = changes.read()
        await ctx.send(embed=bot_says("Goonbot was updated!", changes, multi_line=True))

    @change.error
    async def change_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(embed=bot_says("Only the author can announce new changes.", is_error=True))


def setup(bot):
    bot.add_cog(GeneralCommands(bot))

""" Helper Functions for around the bot"""
from discord.ext import commands

from config import BotConfig

import discord


def bot_says(message, extended_message=None, multi_line=False, footer=None, is_error=False):
    bot_embed = discord.Embed(title=message)
    if extended_message:
        if multi_line is False:
            bot_embed.description = extended_message
        else:
            bot_embed.description = f"```\n{extended_message}\n```"

    if footer:
        bot_embed.set_footer(text=footer)

    if is_error:
        bot_embed.colour = discord.Colour.red()
    else:
        bot_embed.colour = BotConfig.color
    return bot_embed


def fstat(stat, desc):
    """Formatted-stat."""
    if isinstance(stat, int):
        return f"**{stat:,d}** {desc}"
    else:
        return f"**{stat}** {desc}"


def is_bexli():
    def predicate(ctx):
        return ctx.message.author.id == BotConfig.GoonIDs.josh_paulie

    return commands.check(predicate)

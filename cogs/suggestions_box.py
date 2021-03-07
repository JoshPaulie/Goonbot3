import arrow
from discord.ext import commands

from config import BotConfig
from extra_tools import bot_says


def psuggestion(suggestion, author, timestamp):
    """Pretty Suggestion (Formatting)"""
    return f"({arrow.get(timestamp).humanize()}) **{suggestion}** - {author}"


class SuggestionsBox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="suggestion", aliases=["request", "suggest", "demand"])
    async def suggestion(self, ctx, *, suggestion):
        """Make a suggestion for Goonbot!"""
        suggestion = suggestion.capitalize()
        suggestion_form = {
            "author": ctx.author.name,
            "suggestion": suggestion,
            "timestamp": str(arrow.utcnow()),
            "open": True,
        }
        await self.bot.suggestions.insert_one(suggestion_form)
        await ctx.send(embed=bot_says("Suggestions submitted!", suggestion))

    @commands.command(name="suggestions", aliases=["requests"])
    async def suggestions(self, ctx):
        """Display a list of open community suggestions"""
        suggestions = []
        closed_suggestions = 0
        async for suggestion in self.bot.suggestions.find():
            if suggestion["open"]:
                suggestions.append(
                    psuggestion(
                        suggestion["suggestion"],
                        suggestion["author"],
                        suggestion["timestamp"],
                    )
                )
            else:
                closed_suggestions += 1

        await ctx.send(
            embed=bot_says(
                "Open community suggestions!",
                "\n".join(suggestions),
                footer=f"{closed_suggestions} closed suggestions",
            )
        )


def setup(bot):
    bot.add_cog(SuggestionsBox(bot))

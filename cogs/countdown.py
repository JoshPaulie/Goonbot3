from discord.ext import commands
from cogs_helpers.countdown.special_dates import special_dates_dict
from extra_tools import bot_says
import datetime


class Countdown(commands.Cog, name="Countdowns! 📅"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="today")
    async def today(self, ctx):
        """Is today a special day?"""
        today = datetime.date.today()
        is_big_day = False
        today_event = None
        next_big_event = None
        remaining_until_big_day = 365

        for big_date, big_event in special_dates_dict.items():
            if big_date == today:
                is_big_day = True
                today_event = big_event
            else:
                days_until = (big_date - today).days
                if remaining_until_big_day > days_until > 0:
                    remaining_until_big_day = days_until
                    next_big_event = big_event

        if is_big_day:
            await ctx.send(embed=bot_says(f"Today is {today_event}"))
        else:
            await ctx.send(
                embed=bot_says(
                    f"Not today!",
                    f"The next event is **{next_big_event}** in **{remaining_until_big_day}** day(s)!",
                )
            )


def setup(bot):
    bot.add_cog(Countdown(bot))

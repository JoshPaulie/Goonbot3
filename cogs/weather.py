import discord
from discord.ext import commands

from cogs_helpers.weather.openweather_class import OpenWeather
from config import BotConfig
from extra_tools import fstat


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="weather", aliases=["current"])
    async def weather(self, ctx):
        """Gets current temps for our zipcodes"""
        ow = OpenWeather()
        zips = sorted([73072, 85250, 21075, 93065, 73135])
        city_stats = []
        for zip_code in zips:
            city = await ow.current_city_by_zip(zip_code)
            city_stats.append(city)

        weather_embed = discord.Embed(title="Weather ⛈", color=BotConfig.color)
        for city in city_stats:
            weather_embed.add_field(
                name=f" | {city.name}",
                value="\n".join(
                    [
                        fstat(f"{city.temp_current} ({city.feels_like})", "🌡"),
                        fstat(city.temp_max, "H ☀"),
                        fstat(city.temp_min, "L ❄"),
                    ]
                ),
                inline=True,
            )
        await ctx.send(embed=weather_embed)


def setup(bot):
    bot.add_cog(Weather(bot))

from discord.ext import commands
from fuzzywuzzy import process


class PerfectGoonSummoner(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        def correct_name(query):
            with open("cogs_helpers/league/names/goon_summoner_names.txt", mode="r") as names_list:
                names = names_list.read().split("\n")
                compared_results = process.extractOne(query, names)
            return compared_results

        picked_name = correct_name(argument)
        if picked_name[1] > 50:
            return str(picked_name[0])
        else:
            return str(argument)

import discord
from cassiopeia import Summoner
from discord.ext import commands

from cogs_helpers.league.last_game_class import LastGameAnalysis
from cogs_helpers.league.perfect_name_classes import PerfectGoonSummoner
from cogs_helpers.league.calculators import victory_defeat_dict, embed_color_tier
from cogs_helpers.league.summoner_lookup_class import SummonerLookupAnalysis
from config import BotConfig
from extra_tools import fstat, bot_says


class LeagueOfLegends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="lastgame", aliases=["lg", "last"])
    async def lastgame(self, ctx, summoner: PerfectGoonSummoner):
        """An analysis of a summoner's last game
        Syntax: `<prefix> lastgame [summoner]`"""
        """ QoL Variables """
        prompt = await ctx.send(embed=discord.Embed(title="Loading...", colour=0xFED9D2))
        summoner = Summoner(name=str(summoner))
        match_data = LastGameAnalysis(summoner)

        """ Building Embed"""
        lg_embed = discord.Embed(
            title=f"{summoner.name}'s last game",
            description=f"{victory_defeat_dict[match_data.match_outcome]} "
            f"(*{match_data.queue.name.replace('_', ' ')}*)\n"
            f"Duration **{match_data.match.duration}** ({match_data.end_time.humanize()})\n",
        )

        lg_embed.add_field(
            name="⚔ Kills, Deaths, Assists",
            value=BotConfig.pipe.join(match_data.kda_stats()),
            inline=False,
        )

        lg_embed.add_field(
            name="👨‍🌾 Farming Stats",
            value=BotConfig.pipe.join(match_data.farm_stats()),
            inline=False,
        )

        lg_embed.add_field(
            name="💥 Damage Dealt!",
            value=BotConfig.pipe.join(match_data.damage_dealt_stats()),
            inline=False,
        )

        lg_embed.add_field(
            name="💪 Carry Stats",
            value=BotConfig.pipe.join(match_data.carry_stats()),
            inline=False,
        )

        lg_embed.add_field(
            name="⚡ Multi-Kills & Sprees",
            value=BotConfig.pipe.join(match_data.multi_kills_stats()),
            inline=False,
        )

        lg_embed.add_field(
            name="👀 Vision Stats",
            value=BotConfig.pipe.join(match_data.vision_stats()),
            inline=False,
        )

        """ Pretty & Send Embed """
        lg_embed.set_thumbnail(url=match_data.participant.champion.image.url)
        if match_data.match_outcome is True:
            lg_embed.colour = 0x3CB371
        else:
            lg_embed.colour = 0xCD5C5C

        await prompt.edit(embed=lg_embed)

    @lastgame.error
    async def lastgame_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=bot_says("You must include a summoner name!"))

    @commands.command(name="lookup", aliases=["whois", "who", "summoner", "rank", "ranked"])
    async def lookup(self, ctx, summoner: PerfectGoonSummoner):
        """Look up a summoner's profile & ranked stats
        Syntax: `<prefix> lookup [summoner name]`"""
        """ VARIABLES """
        prompt = await ctx.send(
            embed=discord.Embed(
                title="Loading... ⏳",
                colour=0xFED9D2,
            )
        )
        summoner = Summoner(name=str(summoner))
        analysis = SummonerLookupAnalysis(summoner)
        solo_rank, flex_rank = analysis.ranked_stats()

        """ BUILD EMBED """
        ranked_embed = discord.Embed(
            title=f"About {summoner.name}",
            description=BotConfig.pipe.join(
                [
                    fstat(summoner.level, "level"),
                    fstat(analysis.ranked_match_count, "SoloQ games played"),
                ]
            ),
        )
        if len(solo_rank):
            ranked_embed.add_field(name="👑 Solo Queue", value=BotConfig.pipe.join(solo_rank))
        if len(flex_rank):
            ranked_embed.add_field(name="💪 Flex Queue", value=BotConfig.pipe.join(flex_rank))
        ranked_embed.add_field(
            name="❤ Fav Champions (Mastery Points)",
            value=BotConfig.pipe.join(analysis.favorite_champs()),
            inline=False,
        )
        ranked_embed.add_field(
            name="📊 Last 20 Champ W/R",
            value="\n".join(analysis.champion_win_rates()),
            inline=False,
        )

        """ PRETTY EMBED """
        ranked_embed.set_thumbnail(url=summoner.profile_icon.url)
        if analysis.is_placed_solo():
            ranked_embed.colour = embed_color_tier[summoner.league_entries.fives.tier.name.upper()]
        else:
            ranked_embed.colour = BotConfig.color

        await prompt.edit(embed=ranked_embed)

    @lookup.error
    async def lookup_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=bot_says("You must include a summoner name!"))


def setup(bot):
    bot.add_cog(LeagueOfLegends(bot))

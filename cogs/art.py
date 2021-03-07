import random

import discord
from discord.ext import commands
from config import BotConfig


async def make_art_embed(ctx, image):
    art_embed = discord.Embed()

    if type(image) == str:
        art_embed.set_image(url=image)
    elif type(image) == list:
        image = random.choice(image)
        art_embed.set_image(url=image)

    if ctx.command.name != "art":
        art_embed.set_author(name=ctx.command.name)

    art_embed.colour = BotConfig.color
    await ctx.send(embed=art_embed)


class Art(commands.Cog, name="Art! 🎨"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="art")
    async def art(self, ctx):
        """Grabs a random piece of gooner art"""
        command = random.choice(self.get_commands())
        if command.name != "art":
            await command(ctx)
        else:
            await self.art(ctx)

    @commands.command()
    async def bringe(self, ctx):
        """Better Cringe. Duh."""
        image = "https://cdn.discordapp.com/attachments/531913512822243358/651997904751427624/Hudboy.png"
        await make_art_embed(ctx, image)

    @commands.command(name="f-word", aliases=["f", "small", "child", "kid", "fword"])
    async def fword(self, ctx):
        """Small child with heart of stone"""
        image = "https://cdn.discordapp.com/attachments/531913512822243358/651997280290734101/gamer.jpg"
        await make_art_embed(ctx, image)

    @commands.command(name="pizza")
    async def pizza(self, ctx):
        """finna get pizza pied"""
        image = "https://cdn.discordapp.com/attachments/177125557954281472/731242309446008893/image0.jpg"
        await make_art_embed(ctx, image)

    @commands.command(name="clown")
    async def clown(self, ctx):
        """...baby..."""
        image = "https://cdn.discordapp.com/attachments/177125557954281472/651996397041877006/clown_2.0.jpg"
        await make_art_embed(ctx, image)

    @commands.command(name="ygg", aliases=["yougoodgirl", "ygg?"])
    async def ygg(self, ctx):
        """You good girl?"""
        image = (
            "https://cdn.discordapp.com/attachments/"
            "733685825379893339/756322976034586654/c00a411b-1fea-4593-b528-56cfc2dea9cf.png"
        )
        await make_art_embed(ctx, image)

    @commands.command(name="frog", aliases=["foot"])
    async def frog(self, ctx):
        """Fantasy Frog Fetish"""
        image = [
            "https://i.imgur.com/lqZM3sR.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/814729226031726632/1614310329958.jpg",
        ]
        await make_art_embed(ctx, image)

    @commands.command(name="soy")
    async def soy(self, ctx):
        """California-Grown"""
        image = (
            "https://cdn.discordapp.com/attachments/"
            "177125557954281472/727968713231302766/Soy_Food_Package.jpg"
        )
        await make_art_embed(ctx, image)

    @commands.command(name="joker")
    async def joker(self, ctx):
        """Lex Fully Evolved"""
        image = (
            "https://cdn.discordapp.com/attachments/"
            "177125557954281472/754429776571138238/lex_true_form.jpg"
        )
        await make_art_embed(ctx, image)

    @commands.command(name="meatsale")
    async def meatsale(self, ctx):
        """Man sellings meat"""
        image = (
            "https://4.bp.blogspot.com/-E1AkMj_FYSQ/V1CXfLyOVxI/AAAAAAAAAEo/"
            "_NLfDHCZRgQBeB86V2kP4QB81s45GI4GgCLcB/s1600/DANIELCHANTLAND.png"
        )
        await make_art_embed(ctx, image)

    @commands.command(name="wolfchris")
    async def wolfchris(self, ctx):
        """Chad Chris"""
        image = (
            "https://2.bp.blogspot.com/-589mdkan4to/V1CXYEDqsbI/AAAAAAAAAEk/"
            "XCuTKlHzABYeSy9sRlEt_vUH-uImRVidACLcB/s1600/CHRISTOPHERCHILAKE.png"
        )
        await make_art_embed(ctx, image)

    @commands.command(name="real?", aliases=["real", "whip", "dancecat"])
    async def is_this_real(self, ctx):
        """Evidence of paranormal cativity"""
        cats = [
            "https://cdn.discordapp.com/attachments/177125557954281472/810598965190983720/1612730989587.gif",
            "https://media1.tenor.com/images/5416c3b664a81ad99275761d701edcfd/tenor.gif?itemid=16255347",
        ]
        await make_art_embed(ctx, cats)

    @commands.command(name="rool")
    async def rool(self, ctx):
        """G8r man!"""
        image = "https://media1.tenor.com/images/c071dcb215cc774f730c1630a5971fb4/tenor.gif?itemid=12340096"
        await make_art_embed(ctx, image)

    #
    @commands.command(name="rat")
    async def rat(self, ctx):
        """Anti-Mice Movement© logo """
        image = [
            "https://cdn.discordapp.com/attachments/177125557954281472/811445843553943562/1612582813090.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/811446460775792680/unknown.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/810999022805581828/1612582814575.jpg",
            "https://cdn.discordapp.com/attachments/177125557954281472/810999043575644160/1612579730792.jpg",
            "https://cdn.discordapp.com/attachments/177125557954281472/816519126964633620/1614564304374.jpg",
            "https://cdn.discordapp.com/attachments/177125557954281472/816394414016430100/1614666338169.jpg",
            "https://cdn.discordapp.com/attachments/177125557954281472/815669296511975454/1614481522902.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/815375638981902376/1614467122999.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/814327866094780436/1614200422861.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/814295252021018685/1614017575951.gif",
            "https://cdn.discordapp.com/attachments/177125557954281472/814295259558707250/1614017519563.jpg",
            "https://cdn.discordapp.com/attachments/177125557954281472/814191917611876382/1614137309138.jpg",
            "https://cdn.discordapp.com/attachments/177125557954281472/811531265504837672/1611705215429.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/817796408034852874/1615045778199.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/817796396031279124/1615045524249.png",
            "https://cdn.discordapp.com/attachments/177125557954281472/817642770297782282/1614997769621.png",
            "https://cdn.discordapp.com/attachments/188013306341097472/817636974986919956/1615010071942.jpg",
        ]
        await make_art_embed(ctx, image)


def setup(bot):
    bot.add_cog(Art(bot))

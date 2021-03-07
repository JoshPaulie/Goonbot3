from discord.ext import commands
from pymongo.errors import DuplicateKeyError


class WalletManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def get_wallet(self, discord_user):
        """Returns user wallet. Creates one if doesn't exist."""
        if type(discord_user) != str:
            discord_user = discord_user.id
        # ! This should be an if-statement but idk how
        try:
            await self.bot.wallets.insert_one({"_id": discord_user, "coins": 0})
        except DuplicateKeyError:
            pass

        user_wallet = await self.bot.wallets.find_one(discord_user)
        return user_wallet

    async def change_coin(self, discord_user, change_amount):
        wallet = await self.get_wallet(discord_user)
        await self.bot.wallets.update_one(wallet, {"$inc": {"coins": change_amount}})

    @commands.command(name="wallet")
    async def wallet(self, ctx):
        """Shows the user's wallet"""
        wallet = await self.get_wallet(ctx.author)
        await ctx.send(wallet)

    @commands.command(name="add")
    async def add(self, ctx, discord_user, change_amount: int):
        """temp"""
        await self.change_coin(discord_user, change_amount)


def setup(bot):
    bot.add_cog(WalletManager(bot))

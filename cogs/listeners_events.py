from discord.ext import commands

from extra_tools import bot_says


class ListenersEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Deletes messages with Nx litter emote lolol"""
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reactions = message.reactions

        for reaction in reactions:
            if reaction.emoji == "🚮":
                if reaction.count == 5:
                    await channel.send(
                        embed=bot_says(
                            "By community vote, a message was deleted",
                            f"*Message by {message.author.name}*\n",
                        )
                    )
                    await message.delete()


def setup(bot):
    bot.add_cog(ListenersEvents(bot))

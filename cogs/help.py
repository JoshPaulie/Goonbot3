import discord
from discord.ext import commands
from discord.utils import get
from config import BotConfig
from extra_tools import bot_says


def cmd_lookup_embed(curious_cmd):
    embed = discord.Embed(
        title=f"{curious_cmd.name}'s Extended Help",
        description=curious_cmd.help,
        color=BotConfig.color,
    )

    if len(curious_cmd.aliases):
        embed.add_field(name="Aliases", value=", ".join(curious_cmd.aliases))

    return embed


class Help(commands.Cog, name="Help Command 🙋"):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def available_commands_embed(self):
        embed = discord.Embed(
            title="Available commands! 📜",
            color=BotConfig.color,
        )

        all_bot_cogs = self.bot.cogs
        for cog_name, CogClass in all_bot_cogs.items():

            cog_cmds = CogClass.get_commands()
            cog_cmd_list = []

            for cmd in cog_cmds:
                cog_cmd_list.append(cmd.name)

            if len(cog_cmd_list):  # * ignore cogs that don't have any commands
                cmd_str = ", ".join(sorted(cog_cmd_list))
                embed.add_field(name=cog_name, value=cmd_str, inline=False)

        embed.set_footer(text="You can expand any command with .help <command> 🙂")

        return embed

    @commands.command(name="help")
    async def help(self, ctx, cmd=None):
        """Replies with list of commands.
        If provided a command, the command is expanded"""
        """
        if no command provided:
            send all commands
        elseif command IS provided:
            if command exists:
                send details
            else:
                send error
        """
        if cmd is None:
            await ctx.send(embed=self.available_commands_embed())
        else:
            curious_cmd = get(self.bot.commands, name=cmd)
            if curious_cmd:
                await ctx.send(embed=cmd_lookup_embed(curious_cmd))
            else:
                await ctx.send(
                    embed=bot_says(
                        "That command doesn't exist",
                        "Note: you cannot extend command help by aliases",
                    )
                )


def setup(bot):
    bot.add_cog(Help(bot))

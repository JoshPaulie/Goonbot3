from pathlib import Path

import discord
import arrow
from tqdm import tqdm
from motor import motor_asyncio
from discord.ext import commands
from config import BotConfig

intents = discord.Intents(messages=True, guilds=True, reactions=True)
bot = commands.Bot(
    command_prefix=BotConfig.prefix,
    case_insensitive=True,
    intents=intents,
    help_command=None,
)

bot.client = motor_asyncio.AsyncIOMotorClient(BotConfig.Keys.mongo_url)
bot.db = bot.client["goondiscord"]
bot.suggestions = bot.db["suggestions"]
bot.wallets = bot.db["wallets"]


def collect_cogs():
    files = Path("cogs").rglob("*.py")
    for file in files:
        if "__init__" not in file.name:
            yield file.as_posix()[:-3].replace("/", ".")


def load_cogs():
    for cog in tqdm(collect_cogs(), unit=" cogs"):
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f"Failed to load cog {cog}\n{e}")


@bot.event
async def on_ready():
    print("Started =)")
    await bot.change_presence(activity=discord.Game(name=BotConfig.status))


# Command processor
@bot.event
async def on_message(message):
    await bot.process_commands(message)


# Print Commands
@bot.event
async def on_command(ctx):
    """Prints commands to PSEUDO console"""
    if ctx.author.id != BotConfig.GoonIDs.josh_paulie:
        message = ctx.message
        content = message.content
        goon = message.author.name

        print(BotConfig.pipe.join(["[CI]", goon, content]))


""" 🤖🧠 """
collect_cogs()
load_cogs()
bot.run(BotConfig.Keys.discord_token)

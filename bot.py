import os

from dotenv import load_dotenv
from discord.ext import commands

client = commands.Bot(command_prefix="!")
load_dotenv()

@client.event
async def on_ready():
    print('Bot initiated.')

for cog in os.listdir('cogs'):
    if cog.endswith('.py'):
        client.load_extension(f'cogs.{cog[:-3]}')

client.run(os.getenv('BOT_TOKEN'))
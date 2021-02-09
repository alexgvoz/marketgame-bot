import os

from dotenv import load_dotenv
from discord.ext import commands
from boto.s3.connection import S3Connection

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('Bot initiated.')

for cog in os.listdir('cogs'):
    if cog.endswith('.py'):
        client.load_extension(f'cogs.{cog[:-3]}')

client.run(S3Connection(os.environ['BOT_TOKEN']))
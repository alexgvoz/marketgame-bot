import requests
import discord

from discord.ext import commands, tasks
from bs4 import BeautifulSoup
from datetime import datetime


class finvizScreener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None

    def cog_unload(self):
        self.get_data.cancel()

    @commands.command(name='fvs')
    async def start_get_data(self, ctx):
        self.channel = ctx.channel
        self.get_data.start()
        await ctx.channel.send('FinViz Screener tracker started.')

    @commands.command(name='stopfvs')
    async def end_get_data(self, ctx):
        self.get_data.cancel()
        await ctx.channel.send('FinViz Screener tracker stopped.')

    @tasks.loop(seconds=180.0)
    async def get_data(self):
        url = 'https://finviz.com/screener.ashx?v=141&f=sh_price_u20,sh_relvol_o1.5,ta_change_u,ta_sma50_pb&o=-relativevolume'
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers)
        content = BeautifulSoup(resp.text, 'lxml')
        div = content.find('div', id='screener-content')
        tds = div.find_all(class_='screener-body-table-nw')
        brklist = [tds[x:x + 16] for x in range(0, len(tds), 16)]

        embed = discord.Embed(title='FinViz Screener',
                              color=discord.Color.blue(),
                              url=url)
        embed.set_footer(
            text=f'Pulled on {datetime.today().strftime("%d-%m-%Y")} at {datetime.today().strftime("%I:%M %p")}')

        for i in brklist[:-2]:
            embed.add_field(name=f'{i[0].text}. {i[1].text}', value=f'Price | {i[13].text}\nRel. Vol. | {i[12].text}\n')

        await self.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(finvizScreener(bot))

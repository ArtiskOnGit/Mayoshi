import sys
sys.path.insert(1, './/')
import discord
from discord.ext import commands
import giphyAPI
#import TOK
import stats

s = stats.stat()
g = giphyAPI.Giphy()
class FortniteStats(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog commands is up")

    @commands.command()
    async def ping(self,ctx):
        await ctx.send("Pong !")

    @commands.command()
    async def pong(self,ctx):
        await ctx.send("¨Ping !")

    ##FORTNITE STAT COMMANDS
    @commands.command()
    async def stat(self,ctx, platform, player):
        print("Fortnite Stat command in comming deploy on sector A2")
        await ctx.send(s.player(player,platform,False))

    @commands.command()
    async def statactual(self,ctx, platform, player):
        print("Fortnite Stat Actual command in comming deploy on sector A2")
        await ctx.send(s.player(player,platform,True))

    @commands.command()
    async def gif(self,ctx, tag):
        print("Fortnite Stat Actual command in comming deploy on sector A2")
        await ctx.send(g.randomGif(tag))


class GifsCommand(commands.Cog):
    def __init__(self,client):
        self.client = client
def setup(client):
    client.add_cog(FortniteStats(client))

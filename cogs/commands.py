import sys
sys.path.insert(1, './/')
import discord
from discord.ext import commands
import giphyAPI
#import TOK
import stats
import youtube_dl
import wikipediaApi
import json


s = stats.stat()
g = giphyAPI.Giphy()

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ytdl_before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"


ffmpeg_options = {
    'options': '-vn -preload 20'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename,before_options = ytdl_before_options, **ffmpeg_options), data=data)




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
    @commands.command(aliases =["stats","sta"])
    async def stat(self,ctx, platform, joueur):
        print("Fortnite Stat command in comming deploy on sector A2")
        await ctx.send(s.joueur(joueur,platform,False))

    @commands.command(aliases =["stat current","statcurr","current","curr","statactual"])
    async def statcurrent(self,ctx, platform, player):
        print("Fortnite Stat Actual command in comming deploy on sector A2")
        await ctx.send(s.player(player,platform,True))




players = {}

class GifsCommand(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases =["gifs","giff"])
    async def gif(self,ctx, tag):
        print("Gif command in comming deploy on sector A2")
        await ctx.send(g.randomGif(tag))



players = {}

class Music(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context = True,aliases =["summon","j","invoke","connect"])
    async def join(self,ctx):
        if ctx.message.guild.voice_client == None:
            if ctx.message.author.voice != None:
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()

            else :
                await ctx.send("Vous n'etes pas dans un chanel vocal")
        else :
            await ctx.send("Mayoshi est deja connectée")
    @commands.command(pass_context = True,aliases =["l","leavemealone"])
    async def leave(self,ctx):
        guild = ctx.message.guild
        if guild.voice_client != None:
            voice_client = guild.voice_client
            await voice_client.disconnect()
        else :
            await ctx.send("Mayoshi n'est pas connectée")

    @commands.command(pass_context = True,aliases =["pl","stream"])
    async def play(self,ctx,*,url):
        id = ctx.message.guild.id
        #Streams from a url
        if ctx.voice_client != None :
            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        else :
            await ctx.send("Mayoshi n'est pas connectée essayez ::join")

        await ctx.send('Now playing: {}'.format(player.title))


        with open("guilds.json") as file:
            guildsData = json.loads(file.read())

        try :
            ctx.voice_client.source.volume = guildsData[id]["vol"] / 100
            print("suscsessfuly reached the stored volume")
        except :
            ctx.voice_client.source.volume = 50 / 100



    @commands.command(pass_context = True,aliases =["vol","sound"])
    async def volume(self, ctx, volume: int):
        id = str(ctx.guild.id)

        if ctx.voice_client is None:
            return await ctx.send("Mayoshi n'est connectée à aucun channel.")

        file = open("guilds.json","r")
        guildsData = json.loads(file.read())
        print(guildsData)
        thisGuild = {}
        try :
            thisGuild = guildsData[id]
            print("suscsessfuly load data from files")
        except KeyError :
            guildsData.update({id : { "vol" :50, "prefix" : "::","lang" : "ENG"}})
            thisGuild = guildsData[id]
            thisGuild.update({"vol" : volume})
            print("sadly iam here ")

        guildsData.update({id : thisGuild})
        print(guildsData)

        file = open("guilds.json","w")
        file.write(json.dumps(guildsData))
        file.close()

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Volume changé à {volume}")


    @commands.command(pass_context = True,aliases =["st","stfu"])
    async def stop(self,ctx):
        #print(f" \n voice client : {ctx.voice_client} ")
        if ctx.voice_client != None:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("Musique arrétée.")
            else :
                await ctx.send("Aucune musique lancée")
        else :
            await ctx.send("Mayoshi n'est pas connectée")

    @commands.command(pass_context = True, aliases =["p","pau"])
    async def pause(self,ctx):
        #print(f" \n voice client : {ctx.voice_client} ")
        if ctx.voice_client!= None:

            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                await ctx.send("Paused Music.")
            else:
                ctx.send("No music playing.")
        else :
            await ctx.send("Mayoshi n'est pas connectée")


    @commands.command(pass_context = True, aliases =["cb","imissu","res","resum"])
    async def resume(self,ctx):

        if ctx.voice_client!= None:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                await ctx.send("Resumed Music.")
            else:
                await ctx.send("Music is not paused.")


class wikipediaInfos(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context = True, aliases =["wikipedia","wikip"])
    async def wiki(self,ctx,lf):
        await ctx.send(wikipediaApi.wiki.WSearch(lf))


def setup(client):
    client.add_cog(FortniteStats(client))
    client.add_cog(GifsCommand(client))
    client.add_cog(Music(client))
    client.add_cog(wikipediaInfos(client))

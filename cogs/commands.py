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
import asyncio

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

def CreateGuildData(id,volume):
    print("writing a new data set for a guild")


    with open("guilds.json") as file:
        guildsData = json.loads(file.read())

    file = open("guilds.json","w")
    thisGuild = {"vol" :volume, "prefix" : "::","lang" : "EN"}
    guildsData.update({str(id) : thisGuild})
    file.write(json.dumps(guildsData))



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
        await ctx.send(s.player(joueur,platform,False))

    @commands.command(aliases =["stat current","statcurr","current","curr","statactual"])
    async def statcurrent(self,ctx, platform, player):
        print("Fortnite Stat Actual command in comming deploy on sector A2")
        await ctx.send(s.player(player,platform,True))

class GifsCommand(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases =["gifs","giff"])
    async def gif(self,ctx, tag):
        print("Gif command in comming deploy on sector A2")
        await ctx.send(g.randomGif(tag))


queue = {}
class Music(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.client.loop.create_task(self.bouclePlay())



    def ChangingVolumeFromFile(self,ctx):
        #Change the volume to the volume stored for this server
        with open("guilds.json") as file:
                guildsData = json.loads(file.read())
        try :
            ctx.voice_client.source.volume = guildsData[id]["vol"] / 100
            print(f"suscsessfuly reached the stored volume and volume was set to {guildsData[id]['vol']}")
        except KeyError:
            ctx.voice_client.source.volume = 50 / 100
            print("Unable to reached the stored vol")



    async def bouclePlay(self):
        await self.client.wait_until_ready()

        while queue != {}:
            for key,value in queue.items():
                if value != []:
                    self.playern,self.ctx = value[0]
                    if self.ctx.voice_client.is_playing() == False :
                        id = str(self.ctx.message.guild.id)
                        await self.ctx.send(f"Now playing : {self.playern.title}")
                        self.ctx.voice_client.play(self.playern)
                        self.ChangingVolumeFromFile(self.ctx)
                        queue[id].pop(0)
                        if value == []:
                            del queue[id]
            await asyncio.sleep(3)


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

    @commands.command(name = "play", pass_context = True,aliases =["pl","stream"])
    async def play(self,ctx,*,url):
        id = str(ctx.message.guild.id)
        if ctx.voice_client != None :
            print(f"this guild have is playing : {ctx.voice_client.is_playing()}")
            try :
                q = queue[id]
            except KeyError:
                queue[id] = []

            print("adding a player in queue")
            self.playerq = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            self.nextsong = (self.playerq,ctx)
            self.actqueue = queue[id]
            self.actqueue.append(self.nextsong)
            queue.update({id : self.actqueue})
            print(self.nextsong)
            print(queue)
            await ctx.send(f"Added to queue : {self.playerq.title}")
            await self.bouclePlay()












        else :
            await ctx.send("Mayoshi n'est pas connectée essayez ::join")


    @commands.command(pass_context = True)
    async def queue(self,ctx):
        id = str(ctx.message.guild.id)
        try :
            if queue[id] != []:
                queue[id]
                await ctx.send(f"The queue is :")
                for i in queue[id]:
                    self.nextPlayer,_ = i
                    await ctx.send(f" - {self.nextPlayer.title}")
        except KeyError:
                await ctx.send("No queue available")


    @commands.command(pass_context = True,aliases =["vol","sound"])
    async def volume(self, ctx, volume: int):
        id = str(ctx.guild.id)

        if ctx.voice_client is None:
            return await ctx.send("Mayoshi n'est connectée à aucun channel.")

        if ctx.voice_client.source is None:
            return await ctx.send("Mayoshi ne joue pas de musique.")

        print("Volume command input")
        file = open("guilds.json","r")
        guildsData = json.loads(file.read())
        print("guildsData.json have been opened and loaded")

        try :
            thisGuild = guildsData[id]
            print(f"suscsessfuly load this guild data from files for guild : {id}")
            thisGuild.update({"vol" : volume})
            guildsData.update({id : thisGuild})
            print(guildsData)
            file = open("guilds.json","w")
            file.write(json.dumps(guildsData))
            file.close()
        except KeyError :
            print("Creating guild data")
            CreateGuildData(id,volume)




        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Volume changé à {volume}")


    @commands.command(pass_context = True,aliases =["st","stfu"])
    async def stop(self,ctx):
        id = str(ctx.message.guild.id)
        #print(f" \n voice client : {ctx.voice_client} ")
        if ctx.voice_client != None:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("Musique arrétée.")
                queue[id] = []
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

    @commands.command(pass_context = True, aliases =["sk"])
    async def skip(self,ctx):
        id = str(ctx.message.guild.id)
        #print(f" \n voice client : {ctx.voice_client} ")
        if ctx.voice_client != None:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("Musique arrétée.")
            else :
                await ctx.send("Aucune musique lancée")
        else :
            await ctx.send("Mayoshi n'est pas connectée")



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

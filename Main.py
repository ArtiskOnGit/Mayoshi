import TOK
import stats
import discord
from giphy import giphyAPI

TOKEN = TOK.Token
s = stats.stat()
g = giphyAPI.Giphy()


client = discord.Client()
@client.event
async def on_ready():
    print("Bot connected")

@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return

    elif message.content == "ping" or message.content == "Ping":
        await message.channel.send("pong !")
    elif message.content == "pong" or message.content == "Pong" or message.content == "Pong !" or message.content == "pong !":
        await message.channel.send("ping !")

    elif msg.startswith("::"):
        print("Command input in coming")
        if msg.startswith("::stat "):
            if "pc" in msg or "xb1" in msg or "psn" in msg:
                if "pc" in msg:
                    print("yes")
                    plat = "pc"
                elif "xb1" in msg:
                    plat = "xb1"
                elif "psn" in msg:
                    plat = "psn"
                msg = msg.replace("pc", "")
                msg = msg.replace("xb1", "")
                msg = msg.replace("psn", "")

                if msg.startswith("::stat actual"):
                    new_msg = msg.replace("::stat actual","")
                    print(new_msg)
                    await message.channel.send(s.player(new_msg,plat,True))

                else:
                    new_msg = msg.replace("::stat","")
                    print(new_msg)
                    await message.channel.send(s.player(new_msg,plat,False))
            else:
                await message.channel.send("Veuillez specifier la plateforme")

        elif msg.startswith("::lastGame"):
            new_msg = msg.replace("::lastGame","")
            lg = s.lastGame(new_msg)



        elif msg.startswith("::chall"):
            await message.channel.send("On pourra voir les challenges du jour aussi, incroyable")

        elif msg.startswith("::gif "):
            await message.channel.send(g.randomGif(msg.replace("::gif ","gif")))

client.run(TOKEN)

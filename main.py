import TOK
import discord
from discord.ext import commands
import os

TOKEN = TOK.Token

client = commands.Bot(command_prefix = '::')

@client.event
async def on_ready():
    print("Bot connected")

def is_it_admin(ctx):
    return(ctx.author.id == 323132281545949185)


@client.command()
@commands.check(is_it_admin)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Reloaded extension : {extension}")



@client.command()
@commands.check(is_it_admin)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Loaded extension : {extension}")


@client.command()
@commands.check(is_it_admin)
async def status(ctx,*,message):
    await client.change_presence(activity=discord.Game(message))

@client.command()
@commands.check(is_it_admin)
async def guilds(ctx, extension):
    for guild in client.guilds:
        await ctx.send(guild)


client.load_extension("cogs.commands")



client.run(TOKEN)

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hi(ctx):
    await ctx.send('hi')

bot.run('') #тут тупо введи токен бота

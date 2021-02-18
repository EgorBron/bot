import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient

tamada = commands.Bot(command_prefix='!', intents = discord.Intents.all())
cluster = AsyncIOMotorClient('сюда ссылку на Атлас')
party = cluster.ecodb.trivivaparty

@tamada.event 
async def on_ready():
    print('Подъём, просыпайтесь!') 

@tamada.command()
async def ping(ctx):
    await ctx.send('pong')

tamada.run('') #тут тупо введи токен бота

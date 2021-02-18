import discord
import os
import random
import asyncio
from players import typeplayers
from discord.ext import commands, tasks
from motor.motor_asyncio import AsyncIOMotorClient


tamada =  commands.Bot(command_prefix = 'tmp!', intents = discord.Intents.all())
tamada.remove_command('help')

#cluster = AsyncIOMotorClient('mongodb+srv://megagopa:megagopa123@cluster0.j90ds.mongodb.net/ecodb?retryWrites=true&w=majority')
cluster = AsyncIOMotorClient('mongodb://localhost:27017')
party = cluster.ecodb.trivivaparty


@tamada.event
async def on_ready():
	print('Подъём. Просыпайтесь!')

@tamada.command()
async def gameprep(ctx):
	await party.insert_one({
		'guild': ctx.guild.id,
		'gamestart': False,
		'players': 0,
		'audience': True,
		'round': 0,
		'minigames': [],
		'leaderboard': {}
	})
	await ctx.send('Отель готов к заселению... Ну, почти...')

@tamada.command()
async def gamestart(ctx):
	await party.update_one({'gamestart': False, 'round': 0}, {'$set': {'gamestart': True}})
	await ctx.send('@everyone', embed = discord.Embed(tittle = 'Отель Смерти открыт!', description = 'Скорее заселяйтесь!', color = 0x7F1111))

@tamada.command()
async def join(ctx):
	rans = [
		'После прошлой вечеринки разбили вазу моей мамы! Я в ярости, и потому не пущу тебя!',
		"У меня уже есть уборщик, так что убирайся! Блин, как двояко прозвучало",
		 'Кыш!'
	]
	game = await party.find_one({'guild': ctx.guild.id})
	if not game['gamestart']:
		return await ctx.message.reply(f'Эй! {random.choice(rans)}')
	if await party.find_one({'plid': ctx.author.id}): return await ctx.send('Ты уже зашёл!')
	while True:
		ins = typeplayers[random.randint(0, 7)]
		if await party.find_one(ins) == None:
			ins['plid'] = ctx.author.id
			print(ins)
			await party.insert_one(ins)
			await skewers(ctx, ctx.author.name, ctx.author, [])
			break
		else:
			continue


async def skewers_check(payload):
	pass

async def skewers(ctx, player, player_as_member: discord.Member, safety: list):
	await party.update_one({'guild': ctx.guild.id, 'gamestart': True}, {'$push': {'minigames': 'skewers'}})
	msg = await player_as_member.send('Выбери место, где хочешь спрятаться\n:zero::one::two::three:\n:four::five::six::seven:\n:eight::nine::keycap_ten::hash:')
	reactions = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '#️⃣']
	for react in reactions:
		await msg.add_reaction(react)
	await tamada.wait_for('raw_reaction_add', check = skewers_check)

async def losewheel(player, player_as_member: discord.Member):
	pass

token = 'ODEwNTg2NTA5NDM0MjkwMTg3.YClzgw.Opk_tLU1HEgaPgr27gknGJPg8cE'

tamada.run(token)

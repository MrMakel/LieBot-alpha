import discord
from discord.ext import commands
import random
import youtube_dl
from datetime import date

client = discord.Client()
bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="Zwiedzić Kuala Lumpur", type=0))

bot.remove_command('help')

@bot.command()
async def help():
	helpList = discord.Embed(title="LieBot", description="Lista komend:", color=0x146233)
	helpList.add_field(name="&roll", value="Rzuca D6")
	helpList.add_field(name="&clear <ilość>", value="Usuwa <ilość> ostatnich wiadomości")
	helpList.add_field(name="&q add <treść> ~ <autor>", value="Dodaje nowy cytat")
	helpList.add_field(name="&q del <id>", value="Usuwa cytat o <id>")
	helpList.add_field(name="&q quote", value="Wyświetla losowy cytat")
	
	await bot.say(embed=helpList)

@bot.command()
async def roll():
	await bot.say(random.randint(1,6))

@bot.command(pass_context=True)
async def clear(ctx, num):
	num = int(num)
	
	async for x in bot.logs_from(ctx.message.channel, limit = num):
		await bot.delete_message(x)
	msg='Usunięto ostatnie ' + str(num) + ' wiadomości'
	await bot.say(msg)
'''
@bot.command(pass_context=True)
async def join(ctx):
	author = ctx.message.author
	voiceChannel = author.voice_channel
	voice = await bot.join_voice_channel(voiceChannel)
	player = await voice.create_ytdl_player('https://youtu.be/nrAiokI2Dn8')
	player.start()
'''
@bot.command(pass_context=True)
async def q(ctx):
	new_quote = ctx.message.content
	
	new_quote = new_quote[3:]
	
	new_quote = new_quote.split('~')

	quotes_db = open('quotes.txt', 'r')
	
	quotes_db = quotes_db.read().split('\n')
	
	i = 0
	
	for line in quotes_db: #<fix ids on start
		if line == '':
			break
		line = line.split('¦')
		line[0] = str(i)
		quotes_db[i] = '¦'.join(line) + '\n'
		
		max_id = i #get highest id
		i += 1
		
	quotes_db_fix = open('quotes.txt', 'w')
	
	
	quotes_db_fix.write(''.join(quotes_db))
	quotes_db_fix.close()
	#id fix end>
	
	#<get command
	new_quote_split = new_quote[0].split(' ')
	command = new_quote_split[0]
	#get command>
	
	if str(command) == 'add': #add new quote
		quotes_db = open('quotes.txt', 'a+')
		
		max_id += 1
		
		new_quote[0] = new_quote[0][4:]
		
		quotes_db.write(str(max_id) + '¦')
		
		for part in new_quote:
			quotes_db.write(part + '¦')
		
		quotes_db.write(str(date.today().strftime('%d/%m/%Y')) + '\n')
		
		quotes_db.close()
		
		await bot.say('Dodano nowy cytat!')
	
	if str(command) == 'quote': #print random quote
		id = random.randint(2,max_id + 1)
		rnd_quote = quotes_db[id-1].split('¦')
		
		await bot.say('Cytat #' + rnd_quote[0] + ': "' + rnd_quote[1] + '"' + ' ~ ' + rnd_quote[2] + ', ' + rnd_quote[3])
	
	if str(command) == 'del': #remove quote by id
		del_id = ''.join(new_quote).split(' ')
		del_id = int(del_id[1])
		quotes_db_del = quotes_db[:del_id] + quotes_db[del_id+1:]
		
		quotes_db = open('quotes.txt', 'w')
		quotes_db.write(''.join(quotes_db_del))
		quotes_db.close()
		
		await bot.say('Usunięto cytat #' + str(del_id))

@bot.event
async def on_message(message):
	#bot wont answer on its own messages
	if message.author == bot.user:
		return
	
	#needed for commands to work
	await bot.process_commands(message)


bot.run('NTQ5MjQ3Mjk0ODQ3ODQ0MzUy.D1RGaw.CD1HJQx5ZnYkt71QPTfSzNKc4wU')
import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.remove_command('help')

@bot.command()
async def help():
	helpList = discord.Embed(title="LieBot", description="Lista komend:", color=0x146233)
	helpList.add_field(name="&roll", value="Rzuca D6")
	helpList.add_field(name="&clear [ilość]", value="Usuwa [ilość] ostatnich wiadomości")
	
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


@bot.event
async def on_message(message):
	#bot wont answer on its own messages
	if message.author == bot.user:
		return

	if message.content.find("idiota") != -1:
		await bot.send_message(message.channel, 'Co za pacan')
	
	#needed for commands to work
	await bot.process_commands(message)


bot.run('NDg3Mzc3ODY0NDQyOTA0NTg2.DnQKmQ.fGIS7Ait15XADlIdNrlkNKRVjtw')
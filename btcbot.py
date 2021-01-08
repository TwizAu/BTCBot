import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
import requests
import json
from pricewatch import pricewatch

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX')

bot = commands.Bot(command_prefix=PREFIX, description="BTC Bot")

@bot.event
async def on_ready():
	print('Logged in as {0.user}'.format(bot))
	print(discord.__version__)
	watcher = pricewatch()
	await watcher.watch(bot)

# Loads all commands from the cogs directory
cogs = [i for i in os.listdir("cogs") if i.endswith(".py")]

for cog in cogs:
	cog_name = cog.split(".py")[0]
	bot.load_extension("cogs.{0}".format(cog_name))

#URL blacklist
@bot.event
async def on_message(message):
	if os.getenv('ENABLE_BLACKLIST') == "1" and not any(role.name == "mod" for role in message.author.roles):
		blacklist = list(filter(None, os.getenv('BLACKLIST').split(",")))
		if len(blacklist) == 0:
			return

		for item in blacklist:
			if message.content.lower().find(item) != -1:
				print("Deleting Message: " + message.author.mention + " - "+ message.content)
				await message.delete()
	print(os.getenv('ENABLE_IMAGEONLY'))
	if os.getenv('ENABLE_IMAGEONLY') == "1" and message.channel.name == os.getenv('IMAGEONLY_CHANNEL'):
		imageFound = True
		for a in message.attachments:
			if not isinstance(a.width, int):
				imageFound = False
				break
		try:
			if(len(message.attachments) < 1 or not imageFound ):
				await message.delete()
		except:
			await message.delete()
			
	await bot.process_commands(message)

# Disables the default help command from discord.py
bot.remove_command('help')
# bot.run(username, password, bot=False)
bot.run(TOKEN)


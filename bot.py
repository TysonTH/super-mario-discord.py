import os
import discord
import logging
import subprocess
from discord.ext import commands
from dotenv import load_dotenv
from subprocess import call

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Functions

def log(text):
	print('[General]: ' + text)

#Load Bot Token and Guild information
load_dotenv()
token = os.getenv('token')
guild = os.getenv('guild')

#Sounds
hello = os.getenv('hello')

#Initialize bot
client = commands.Bot(command_prefix='$')

#Initialize extensions
extensions = (
	"cogs.minecraft",
)

print('Loading cogs:')

for extension in extensions:
	try:
		client.load_extension(extension)
	except Exception as e:
		print(f'Failed to load extension {extension}')

print('\n')

#Events

@client.event
async def on_ready():
	log('Logged on as: (' + str(client.user) + ').')

@client.event
async def on_message(message):
	
	# don't respond to ourselves
	if message.author == client.user:
		return
	
	await client.process_commands(message)
			
	if message.content == 'hello mario':
		await message.channel.send('Hello!')
		#await message.channel.send(file=discord.File(hello))
		#Easter Egg
		
#@client.event
#async def on_command_error(error, ctx):
	#await error.send('An error has occurred.')

#Commands		

	#General
	
@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')
	

	#Server
	
#@client.command(aliases = ['boot', 'start'])
#async def run(ctx, *, game):
	
	#if game == 'minecraft':
		#await ctx.send('The Minecraft server script has been executed, please wait a moment as the server initializes.')
		#subprocess.call(minecraftServer, shell = True)
		
#Error Handlers

#@run.error
#async def run_error(error, ctx):
	#await error.send("You must specify a game!")
			
#Run bot with corresponding token
client.run(token)

#To do list
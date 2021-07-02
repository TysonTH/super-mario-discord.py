import discord
import logging
import os
import os.path
import subprocess
import time
import urllib.request
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from dotenv import load_dotenv
from os import path
from subprocess import call

#Log information
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

#Open Ports
minecraftPort = os.getenv('minecraftPort')

#Scripts
minecraftServer = os.getenv('minecraftServer')

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

	# *General*
	
@client.command(brief = 'Outputs the latency between Discord and the bot')
async def ping(ctx):
	await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')
	

	# *Server*
	
#Please check /scripts and .env and add your directories, otherwise this will break
@client.command(aliases = ['boot', 'start'], brief = 'Initializes a server for compatible games', description = 'Initializes a server for compatible games, type $run usage for more info.')
@commands.cooldown(1.0, 30.0, BucketType.guild)
async def run(ctx, *, game):
	
	if game == 'usage':
		await ctx.send('```$run [game], Example: $run minecraft\n\n' +
					   'List of compatible games:\n' +
					   '• Minecraft```')
	
	#Run a server if .running does not exist
	elif path.exists('.running') == False:
	
		if game == 'minecraft' or game == 'mc':
			await ctx.send('The Minecraft server script has been executed, please wait a moment as the server initializes.')
			subprocess.call(minecraftServer, shell = True)
			log('A Minecraft server has been initialized.')
			
            #Start 30 second timer to inform server should now be in service
			time.sleep(30)
			await ctx.send('The Minecraft server should now be up and running!')
	
	#Otherwise, inform the user a server cannot be executed and give further instructions.
	else:
		await ctx.send('A server is already running! Please contact a server administrator to request a restart or termination of the current session.')
		
#@client.command(aliases = ['address'], brief = 'Displays the server\'s external IP and open ports')
#@commands.cooldown(1.0, 30.0, BucketType.guild)
#async def ip(ctx):
	
	#Contact ident.me and store IP address as string
	#extIP = urllib.request.urlopen('https://ident.me').read().decode('utf8')

	#await ctx.send("Server IP: `" + extIP + "`" +
				   #"\nOpen Ports:" +
				   #"\n```Minecraft: " + minecraftPort + "```")
	
		
#Error Handlers

@run.error
async def runError(ctx, error):
	
	#Check if currently on cooldown
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send('This command has a 30 second cooldown. You may use it again in `{:.2f}`s'.format(error.retry_after))
	
	else:
		await ctx.send("You must specify a game!")
		
#@ip.error
#async def ipError(ctx, error):
	
	#Check if currently on cooldown
	#if isinstance(error, commands.CommandOnCooldown):
		#await ctx.send('This command has a 30 second cooldown. You may use it again in `{:.2f}`s'.format(error.retry_after))
	
	#else:
		#await ctx.send("An unknown error has occurred.")
			
#Run bot with corresponding token
client.run(token)

#To do list

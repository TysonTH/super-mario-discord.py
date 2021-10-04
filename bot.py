import asyncio
import botConfig
import discord
import logging
import os
import os.path
import subprocess
import time
import urllib.request
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
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

#Bot Config
token = botConfig.token
guild = botConfig.guild
prefix = botConfig.prefix

#Links
botRepo = botConfig.botRepo

#Open Ports
minecraftPort = botConfig.minecraftPort

#Scripts
minecraftServer = botConfig.minecraftServer

#Sounds
hello = botConfig.helloSound

#Initialize bot
client = commands.Bot(command_prefix=prefix)

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
		try:
			await message.channel.send(file=discord.File(hello))
		except Exception as e:
			log('User has found an easter egg but no sound file was provided!')
		#Easter Egg
		
#@client.event
#async def on_command_error(error, ctx):
	#await error.send('An error has occurred.')

#Commands

	# *General*
	
@client.command(aliases = ['github', 'repo', 'repository', 'source', 'download'], brief = 'Links to the current repository for this bot!')
async def codebase(ctx):
	await ctx.send(botRepo)
	
@client.command(brief = 'Outputs the latency between Discord and the bot')
async def ping(ctx):
	await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')
	

	# *Server*
	
#Please check /scripts and configure .env and add your directories, otherwise this will not work
@client.command(aliases = ['boot', 'start'], brief = 'Initializes a server for compatible games', description = 'Initializes a server for compatible games, type {0}run usage for more info.'.format(prefix))
@commands.cooldown(1.0, 30.0, BucketType.guild)
async def run(ctx, *, game):
	
	if game == 'usage':
		await ctx.send('```{0}run [game], Example: $run minecraft\n\n'.format(prefix) +
					   'List of compatible games:\n' +
					   '• Minecraft```')
	
	#Run a server if .running does not exist
	elif path.exists('.running') == False:
	
		if game == 'minecraft' or game == 'mc':
			try:
				await ctx.send('The Minecraft server script has been executed, please wait a moment as the server initializes.')
				subprocess.call(minecraftServer, shell = True)
				log('A Minecraft server has been initialized.')
				
			except Exception as e:
				await ctx.send('Could not successfully initialize the server, please contact bot administrator.')
				log('A Minecraft server could not be initialized. Please check /scripts/runMinecraft.sh to make sure everything is set correctly. You must also ensure the script has execute permissions.')
			
            #Start 50 second timer to inform server should now be in service
			time.sleep(50)
			await ctx.send('The Minecraft server should now be up and running!')
	
	#Otherwise, inform the user a server cannot be executed and give further instructions.
	else:
		await ctx.send('A server is already running! Please contact a server administrator to request a restart or termination of the current session.')
		
@client.command(aliases = ['address'], brief = 'Displays the server\'s external IP and open ports')
@commands.cooldown(1.0, 30.0, BucketType.guild)
async def ip(ctx):
	
	#Check if command is allowed by bot Administrator
	if botConfig.ipCmdAllowed == True:
		#Contact URL stored in botConfig and store IP address as string
		extIP = urllib.request.urlopen(botConfig.ipTest).read().decode('utf8')
		await ctx.send("Server IP: `" + extIP + "`" +
					   "\nOpen Ports:" +
					   "\n```Minecraft: " + minecraftPort + "```")
	
	else:
		await ctx.send('Bot administrator has not authorized this command.')
		log('IP grab attempt blocked. To change this behavior open botConfig.py and find the line: ' +
			'\'ipCmdAllowed = False\'' +
			'\nand replace False with True')

@client.command(aliases = ['bandwidth'], brief = 'Perform a speedtest, powered by Ookla™')
@commands.cooldown(1.0, 90.0, BucketType.guild)		
async def speedtest(ctx):
	
	#Check if command is allowed by bot Administrator
	if botConfig.speedtestCmdAllowed == True:
		import speedtest
		
		log('A user has just initiated a speedtest.')
		await ctx.send('Attempting to perform Speedtest...')
		
		#https://github.com/sivel/speedtest-cli/wiki
		
		servers = []
		threads = None
		
		attempt = speedtest.Speedtest()
		attempt.get_servers(servers)
		attempt.get_best_server()
		
		await ctx.send('Performing download test...')
		attempt.download(threads=threads)
		
		await ctx.send('Performing upload test...')
		attempt.upload(threads=threads)
		
		log('Here are the results: ' + attempt.results.share())
		await ctx.send(attempt.results.share())
		
	else:
		await ctx.send('Bot administrator has not authorized this command.')
		log('Speedtest attempt blocked. To change this behavior open botConfig.py and find the line: ' +
			'\'speedtestCmdAllowed = False\'' +
			'\nand replace False with True')
		
		
#Error Handlers

@run.error
async def runError(ctx, error):
	
	#Check if currently on cooldown
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send('This command has a 30 second cooldown. You may use it again in `{:.2f}`s'.format(error.retry_after))
	
	else:
		await ctx.send("You must specify a game!")
		
@ip.error
async def ipError(ctx, error):
	
	#Check if currently on cooldown
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send('This command has a 30 second cooldown. You may use it again in `{:.2f}`s'.format(error.retry_after))
	
	else:
		await ctx.send("An unknown error has occurred.")
		
@speedtest.error
async def speedtestError(ctx, error):
	
	#Check if currently on cooldown
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send('This command has a 90 second cooldown. You may use it again in `{:.2f}`s'.format(error.retry_after))
	
	else:
		await ctx.send("An unknown error has occurred.")
			
#Run bot with corresponding token
client.run(token)

#To do list

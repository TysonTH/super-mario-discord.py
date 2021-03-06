import botConfig
import discord
import minecraftConfig
import os
import os.path
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from mcstatus import MinecraftServer
from os import path

#Bot Config
prefix = botConfig.prefix

#Channels
announcements = minecraftConfig.serverStatus

#Directories
coordinatesDirectory = minecraftConfig.coordinatesDirectory

#Open Ports
minecraftPort = minecraftConfig.minecraftPort
minecraftQueryPort = minecraftConfig.minecraftQueryPort

#Links
modsDirectory = minecraftConfig.modsDirectory


class Minecraft(commands.Cog):

	
	def __init__(self, client):
		self.client = client
		
		
	@commands.Cog.listener()
	
	async def on_ready(self):
		
		#Inform users that the Minecraft server can now be initialized.
		channel = self.client.get_channel(announcements)
		
		await channel.send('[Minecraft]: The server computer has successfully logged in, you can now start the Minecraft server with:\n`{0}run minecraft`'.format(prefix))
		log('Users have been informed the Minecraft server can now be started.')
		
	
	@commands.command(aliases = ['coords'], brief = 'Allows users to store coordinates into a directory', description = 'Store a set of coordinates with a corresponding tag, type {0}coordinates usage for more info.'.format(prefix))
	async def coordinates(self, ctx, *args):
		
		if args[0] == "usage":
			await ctx.send('```{0}coordinates make [tag] [x] [y] [z], Example: {0}coordinates make home -1000 64 2000\n'.format(prefix) +
						   '{0}coordinates get [tag], Example: {0}coordinates get home\n'.format(prefix) +
						   '{0}coordinates replace [tag] [x] [y] [z], Example: {0}coordinates replace home -3000 72 2500\n'.format(prefix) +
						   '{0}coordinates delete [tag], Example: {0}coordinates delete home```'.format(prefix))
			
		else:
			#Open coordinatesDirectory as stored in minecraftConfig.py
			filename = coordinatesDirectory + args[1] + ".txt"
		
			#If the user sends more than 4 arguments
			if len(args) > 5:
				await ctx.send('You have sent too many parameters!')
		
			#Do this if the user wants to store a new set of coordinates 
			elif args[0] == "make" or args[0] == "store":
			
				#Continue creating set if it doesn't exist
				if path.exists(filename) == False:
					locationFile = open(filename, "w")
			
					location = '(' + args[2] + ', ' + args[3] + ', ' + args[4] + ')'
					locationFile.write(location)
		
					await ctx.send('Coordinates have been saved as: `' + args[1] + '`!')
					locationFile.close()
				
					log(args[1] + ".txt has been created.")
			
				#Inform the user this set already exists
				else:
					await ctx.send("The name you've selected for your location already exists! Please use another and try again" +
							   	"or use `{0}coordinates replace [tag] [x] [y] [z]` (no square brackets).".format(prefix))
		
			#Read the coordinates out to the user
			elif args[0] == "get":
			
				if path.exists(filename) == True:
					
					locationFile = open(filename, "r")
					location = locationFile.read()
		
					await ctx.send('Coordinates: ' + location)
					locationFile.close()
				
				else: 
					await ctx.send("`" + args[1] + "` does not exist!")
		
			#Overwrite a set of coordinates
			elif args[0] == "replace" or args[0] == "overwrite":
			
				#Check if file exists
				if path.exists(filename) == True:
					locationFile = open(filename, "w")
			
					location = '(' + args[2] + ', ' + args[3] + ', ' + args[4] + ')'
					locationFile.write(location)
		
					await ctx.send('Coordinates have overwritten: `' + args[1] + '`!')
					locationFile.close()
				
					log(args[1] + ".txt has been overwritten.")
				
				else:
					await ctx.send("`" + args[1] + "` does not exist!")
		
		
			#Delete a set of coordinates
			elif args[0] == "delete" or args[0] == "erase":
			
				#Check if file exists
				if path.exists(filename) == True:
					os.remove(filename)
					await ctx.send('Coordinates that were saved as `' + args[1] + '` have been deleted.')
					log(args[1] + ".txt has been deleted.")
				
				else:
					await ctx.send('These coordinates do not exist, check to make sure the name is correct.')
					
	@commands.command(aliases = ['minecraft'], brief = 'Subset of tools for Minecraft, refer to {0}mc usage'.format(prefix))
	@commands.cooldown(1.0, 5.0, BucketType.guild)
	async def mc(self, ctx, *, arg):
		
		if arg == "mods":
			await ctx.send(modsDirectory)
			
		elif arg == "status":
			
			#Pull computer's local IP address and port number
			serverAddress = MinecraftServer('localhost', minecraftPort)
			
			#Record status and output to user
			status = serverAddress.status()
			await ctx.send("`{0}` is currently online with {1} player(s) and responded in `{2}??s`".format(status.description, status.players.online, status.latency * 1000))
			
		elif arg == "query":
			
			#Same as status, but must have query enabled
			serverAddress = MinecraftServer('localhost', minecraftQueryPort)
			query = serverAddress.query()
			
			#If list of players is empty, inform the users the server is vacant.
			if len(query.players.names) == 0:
				await ctx.send("`{0}` has no players online.".format(query.motd))
				
			#List players currently in-game	
			else:
				await ctx.send("`{0}` has the following players online: ```\n{1}```".format(query.motd, ", ".join(query.players.names)))
		
	#Error Handlers
		
	@coordinates.error
	async def coordinatesError(self, ctx, error):
		await ctx.send("Your parameters are incorrect, try again!")
		
	@mc.error
	async def mcError(self, ctx, error):
	
		#Check if currently on cooldown
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send('This command has a 5 second cooldown. You may use it again in `{:.2f}s`'.format(error.retry_after))
	
		else:
			await ctx.send("The server is either down, has query disabled and/or the host's ports may not be properly forwarded.")
	
#Functions

def setup(client):
	client.add_cog(Minecraft(client))
	print('[Minecraft]')
	
def log(text):
	print('[Minecraft]: ' + text)
	
#To do list
	#Rework {0}coordinates command to store as a dictionary instead of individual text files
	#Add minimum parameter check to {0}coordinates make

import discord
import os
import os.path
from discord.ext import commands
from dotenv import load_dotenv
from os import path

load_dotenv()

#Channels
announcements = int(os.getenv('general'))

#Directories
coordinateDatabase = str(os.getenv('coordinateDatabase'))

#Links
minecraftDirectory = str(os.getenv('minecraftDirectory'))

class Minecraft(commands.Cog):

	
	def __init__(self, client):
		self.client = client
		
		
	@commands.Cog.listener()
	
	async def on_ready(self):
		
		#Inform users that the Minecraft server can now be initialized.
		channel = self.client.get_channel(announcements)
		
		await channel.send('[Minecraft]: The server computer has successfully logged in, you can now start the Minecraft server with:\n`$run minecraft`')
		log('Users have been informed the Minecraft server can now be started.')
		
	
	@commands.command(aliases = ['coords'], brief = 'Allows users to store coordinates into a directory', description = 'Store a set of coordinates with a corresponding tag, type $coordinates usage for more info.')
	async def coordinates(self, ctx, *args):
		
		if args[0] == "usage":
			await ctx.send('```$coordinates make [tag] [x] [y] [z], Example: $coordinates make home -1000 64 2000\n' +
						   '$coordinates get [tag], Example: $coordinates get home\n' +
						   '$coordinates replace [tag] [x] [y] [z], Example: $coordinates replace home -3000 72 2500\n' +
						   '$coordinates delete [tag], Example: $coordinates delete home```')
			
		else:
			filename = coordinateDatabase + args[1] + ".txt"
		
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
							   	"or use `$coordinates replace [tag] [x] [y] [z]` (no square brackets).")
		
			#Read the coordinates out to the user
			elif args[0] == "get":
			
				locationFile = open(filename, "r")
				location = locationFile.read()
		
				await ctx.send('Coordinates: ' + location)
				locationFile.close()
		
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
					
		
	@commands.command()
	async def mods(self, ctx):
		await ctx.send(minecraftDirectory)
		
	#Error Handlers
		
	@coordinates.error
	async def coordinates_error(self, error, ctx):
		await error.send("Your parameters are incorrect, try again!")
	
#Functions

def setup(client):
	client.add_cog(Minecraft(client))
	print('[Minecraft]')
	
def log(text):
	print('[Minecraft]: ' + text)
	
#To do list
	#Rework $coordinates command to store as a dictionary instead of individual text files
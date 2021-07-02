 #!/bin/sh
screen -d -m -S minecraft bash -c 'touch .running; cd; cd directory/to/your/minecraft/server; ./start.sh; cd; cd directory/to/super-mario/bot; rm .running; exit; exec bash'
#In Layman's terms:

#[Before server starts]
#Open a virtual terminal with the name 'minecraft', create a hidden file called '.running', go to root directory, go to minecraft server directory,
#execute server initialization script (MUST HAVE EXECUTE PERMISSIONS)

#[After server shuts down]
#Go to root directory, go to this Discord bot's directory, delete '.running' file so that the $run command can be used once again, exit the virtual terminal so that
#this current session is terminated and there are not multiple terminals named 'minecraft'

#i hope this makes sense

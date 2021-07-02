# super-mario
Discord bot with some basic features written in Python

This was written with only private use  in mind, so it does not have any security features in place that you would expect a public Discord bot to have.

This has not been tested on Windows so it assumes you will be running this under Debian Linux and a bash shell.

Requirements for the bot to run properly are:

`pip install python-dotenv`
`pip install discord.py`

You will also need to fill in the bot token and other information in the .env files stored in root and cogs folders.

Sounds are also not provided as they are copyrighted material but a list of sounds the program expects is included.

## Current Features

**Initialize a game server remotely with some initial setup required from the host running the bot**

**Display host's external IP address to provide ease of access if the host has a dynamic IP address and no DDNS configured (left commented out for security reasons)**

**Tools to increase game immersion such as storing Minecraft coordinates (still a rudimentary system) and more...**

## Planned Features

**Interface with Minecraft server via [mcstatus](https://github.com/Dinnerbone/mcstatus) to provide further support for players**

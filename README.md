# super-mario
Discord bot with some basic features written in Python

This was written with only private use  in mind, so it does not have any security features in place that you would expect a public Discord bot to have.

This has not been tested on Windows so it assumes you will be running this under Debian Linux and a bash shell, but it should be easy to setup with a little know-how.

## Requirements

`pip install discord.py`
`pip install mcstatus`
`pip install speedtest`

## Configuration

You will also need to fill in the bot token and other information in the config files stored in root.

`botConfig.py` `minecraftConfig.py`

Sounds are also not provided as they are copyrighted material but a list of sounds the program expects is included.

## Current Features

**Initialize a game server remotely with some initial setup required from the host running the bot**

**Display host's external IP address to provide ease of access if the host has a dynamic IP address and no DDNS configured**

**Perform a speedtest to test connection stability.**

**Tools to increase game immersion such as storing Minecraft coordinates (still a rudimentary system) and more...**

**Interface with Minecraft server via [mcstatus](https://github.com/Dinnerbone/mcstatus) to provide further support for players**

**Restrict the usage of certain commands, off by default**

## Planned Features

**Disable and enable commands through Discord's interface to require less editing of the python files**

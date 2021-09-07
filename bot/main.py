import datetime
import logging
import logging.config
import os
import platform  # For getting the operating system name
import subprocess  # For executing a shell command
import sys
import time
from pathlib import Path

import discord
import psutil
import requests
from discord import ChannelType
from discord.ext import commands
from discord.ext.dashboard import Dashboard
from discord_slash import SlashCommand
from discordTogether import DiscordTogether

from botconfig import botconfig
from kuzaku.cls import kuzaku
from kuzaku.exts import *
from kuzaku.logger import error, log, warning

intents=discord.Intents.default()
intents.members = True
intents.guilds = True
ver='0.0.1'
startTime=time.time()
def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command, stdout=subprocess.PIPE) == 0


bot=kuzaku(command_prefix='k.', intents=intents)
if os.getenv('PRODUCTION') == 'yes':
    bot_dashboard = Dashboard(bot,
	os.getenv('ipckey'), 
	"https://kuzaku.ml/dash_handler"
    )
else:
    bot_dashboard = Dashboard(bot,
	os.getenv('ipckey'), 
	"http://127.0.0.1:5000/dash_handler"
    )
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


@bot_dashboard.route
async def get_stats(data):
    channels_list = []
    for guild in bot.guilds:
        for channel in guild.channels:
            channels_list.append(channel)
    return {"status":"200", "message":"all is ok", "guilds":str(len(bot.guilds)), "users":str(len(bot.users)), "channels": len(channels_list)}

@bot_dashboard.route
async def get_invite_url(data):
    return f'https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot+applications.commands&permissions=473197655'
@bot_dashboard.route
async def get_mutual_guilds(data):
    guild_ids = []
    for guild in bot.guilds:
        guild_ids.append(guild.id)
    return guild_ids

if __name__ == '__main__':
    print('''
 __                             __               
[  |  _                        [  |  _           
 | | / ] __   _   ____   ,--.   | | / ] __   _   
 | '' < [  | | | [_   ] `'_\ :  | '' < [  | | |  
 | |`\ \ | \_/ |, .' /_ // | |, | |`\ \ | \_/ |, 
[__|  \_]'.__.'_/[_____]\-;__/[__|  \_]'.__.'_/   

                                       
        ﹝ kuzaku - the discord bot ﹞
''')
    load_cogs(bot, ['channels'])
    bot.run(botconfig['token'])






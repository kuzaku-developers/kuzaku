from kuzaku.logger import log, warning, error
import datetime
import os
import platform
from pathlib import Path
import time
from os import listdir
from os.path import join, realpath, split, splitext
import requests
import discord
import psutil
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from discord import ChannelType
from discord.ext import commands
from discord.ext.dashboard import Dashboard
from discord_slash import SlashCommand
from discordTogether import DiscordTogether
from botconfig import botconfig
import sys
import logging
import logging.config
startTime=time.time()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[92m'
    OKGREEN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[1;33;40m'
class kuzaku(discord.ext.commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.together = DiscordTogether(self)
        self.log=log
        self.warning=warning
        self.error=error
    async def on_connect(self):
        sec = int(round(time.time() - startTime))
        self.log(f'<main> :: Bot info', f'    {self.user} connected successfully in {sec} seconds')
    async def on_ready(self):
        await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name=f'{len(self.guilds)} guilds | /help'))
        self.log('<main> :: Bot', '    Bot is ready to use')
        self.log('<api> :: Trying to ping website...')
        try:
            if ping('kuzaku.ml'):
                self.log('    Website is working!')
            else:
                self.warning('    Website is not working!')
        except: 
            self.warning('    Website is not working!')
    async def on_message(self, message):
        await bot_dashboard.process_request(message)
        await self.process_commands(message)

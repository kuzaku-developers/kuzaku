#imports
import datetime
import os
import platform
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
rootdir=os.path.abspath(os.path.join(os.curdir))
def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
mkdir_p(os.path.dirname('logs/log.log'))
logging.basicConfig(filename="logs/log.log", 
					format='%(message)s', 
					filemode='a') 
logger=logging.getLogger()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
logger.setLevel(logging.INFO) 
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




def log (*msg):
    def _ (msg):
        logging.log(level=logging.INFO, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  LOG  | {msg}')
        if os.getenv('DONTUSECOLORS') != 'yes':
            print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.OKCYAN}  LOG  {bcolors.ENDC}| {bcolors.HEADER}{msg}')
        else: 
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  LOG  | {msg}')
    list(map (_, msg))
def warning(*msg):
    def _ (msg):
        logging.log(level=logging.WARNING, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ALERT | {msg}')
        if os.getenv('DONTUSECOLORS') != 'yes':
            print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {bcolors.ENDC}|{bcolors.OKGREEN} ALERT {bcolors.ENDC}| {bcolors.HEADER}{msg}')
        else:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ALERT | {msg}')
    list(map (_, msg))
def error(*msg):
    def _ (msg):
        logging.log(level=logging.ERROR, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ERROR | {msg}')
        if os.getenv('DONTUSECOLORS') != 'yes':
            print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.FAIL} ERROR {bcolors.ENDC}| {bcolors.HEADER}{msg}')
        else:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ERROR | {msg}')
    list(map (_, msg))

class kuzaku(discord.ext.commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)
        self.together = DiscordTogether(self)
    def log (self, *msg):
        def _ (msg):
            logging.log(level=logging.INFO, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  LOG  | {msg}')
            if os.getenv('DONTUSECOLORS') != 'yes':
                print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.OKCYAN}  LOG  {bcolors.ENDC}| {bcolors.HEADER}{msg}')
            else: 
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  LOG  | {msg}')
        list(map (_, msg))
    def cmd (self, *msg):
        def _ (msg):
            logging.log(level=logging.INFO, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  CMD  | {msg}')
            if os.getenv('DONTUSECOLORS') != 'yes':
                print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.OKCYAN}  CMD  {bcolors.ENDC}| {bcolors.HEADER}{msg}')
            else: 
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  CMD  | {msg}')
        list(map (_, msg))
    def warning(self, *msg):
        def _ (msg):
            logging.log(level=logging.WARNING, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ALERT | {msg}')
            if os.getenv('DONTUSECOLORS') != 'yes':
                print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {bcolors.ENDC}|{bcolors.OKGREEN} ALERT {bcolors.ENDC}| {bcolors.HEADER}{msg}')
            else:
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ALERT | {msg}')
        list(map (_, msg))
    def error(self, *msg):
        def _ (msg):
            logging.log(level=logging.ERROR, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ERROR | {msg}')
            if os.getenv('DONTUSECOLORS') != 'yes':
                print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.FAIL} ERROR {bcolors.ENDC}| {bcolors.HEADER}{msg}')
            else:
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ERROR | {msg}')
        list(map (_, msg))
    async def on_connect(self):
        sec = int(round(time.time() - startTime))
        self.log(f'<main> :: Bot info', f'  {self.user} connected successfully in {sec} seconds')
    async def on_ready(self):
        await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name=f'{len(self.guilds)} guilds | /help'))
        self.log('<main> :: Bot', '  Bot is ready to use')
        self.log('<api> :: Trying to ping website...')
        if os.getenv('PRODUCTION')=='yes':
            try:
                if ping('kuzaku.ml'):
                    self.log('  Website is working!')
                else:
                    self.warning('  Website is not working!')
            except: 
                self.warning('  Website is not working!')
        else:
            try:
                if ping('127.0.0.1'):
                    self.log('  Website is working!')
                else:
                    self.warning('  Website is not working!')
            except:
                self.warning('  Website is not working!')
    async def on_message(self, message):
        await bot_dashboard.process_request(message)
        await self.process_commands(message)

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
def load_ext(bot,dir):
    bot.load_extension('jishaku')
    log('<main> :: Cogs loader')
    log(f'  Loading \'{dir}/*\' ...')
    if platform.system() in ["Darwin", 'Windows']:
        for filename in os.listdir(f'bot/cogs'):
            if filename.endswith('.py'):
                #log(f'trying to load cog {filename[:-3]}')
                try:
                    bot.load_extension(f'{dir}.{filename[:-3]}')
                    log(f'  loaded: {dir}/{filename[:-3]}')
                except Exception as e:
                    error(f'  not loaded: {dir}/{filename[:-3]}', f'  error: {e}')
    elif platform.system()=='Linux':
        for filename in os.listdir(f'{os.curdir}/bot/cogs'):
            if filename.endswith('.py'):
                #log(f'trying to load cog {filename[:-3]}')
                try:
                    bot.load_extension(f'bot.cogs.{filename[:-3]}')
                    log(f'  loaded: {dir}/{filename[:-3]}')
                except Exception as e:
                    error(f'  not loaded: {dir}/{filename[:-3]}', f'  error: {e}')
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
    load_ext(bot, 'cogs')
    bot.run(botconfig['token'])







#imports
import datetime
import os
import platform
import time
from os import listdir
from os.path import join, realpath, split, splitext
import discord
import psutil
from discord import ChannelType
from discord.ext import commands
from discord.ext.dashboard import Dashboard
from discord_slash import SlashCommand
from discordTogether import DiscordTogether
from botconfig import botconfig

rootdir=os.path.abspath(os.path.join(os.curdir))
intents=discord.Intents.default()
intents.members = True
intents.guilds = True
ver='0.0.1'
startTime=time.time()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[1;33;40m'




def log (*msg):
    def _ (msg):
        if os.getenv('DONTUSECOLORS') != 'yes':
            print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.OKCYAN}  LOG  {bcolors.ENDC}| {bcolors.HEADER}{msg}')
        else: 
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  LOG  | {msg}')
    list(map (_, msg))
def warning(*msg):
    def _ (msg):
        if os.getenv('DONTUSECOLORS') != 'yes':
            print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.WARNING} | ALERT | {bcolors.HEADER}{msg}')
        else:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ALERT | {msg}')
    list(map (_, msg))
def error(*msg):
    def _ (msg):
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
            if os.getenv('DONTUSECOLORS') != 'yes':
                print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.OKCYAN}  LOG  {bcolors.ENDC}| {bcolors.HEADER}{msg}')
            else: 
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  LOG  | {msg}')
        list(map (_, msg))
    def warning(self, *msg):
        def _ (msg):
            if os.getenv('DONTUSECOLORS') != 'yes':
                print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.WARNING} | ALERT | {bcolors.HEADER}{msg}')
            else:
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ALERT | {msg}')
        list(map (_, msg))
    def error(self, *msg):
        def _ (msg):
            if os.getenv('DONTUSECOLORS') != 'yes':
                print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.FAIL} ERROR {bcolors.ENDC}| {bcolors.HEADER}{msg}')
            else:
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ERROR | {msg}')
        list(map (_, msg))

    async def on_ready(self):
        sec = int(round(time.time() - startTime))
        await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name=f'{len(self.guilds)} guilds | k.help'))
        self.log(f'<main> :: Bot info', f'  {self.user} started successfully in {sec} seconds')
        load_ext(bot, 'cogs')
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
    log('<main> :: Cogs loader')
    log(f'  Loading \'{dir}/*\' ...')
    if platform.system() in ["Darwin", 'Windows']:
        for filename in os.listdir(f'{rootdir}/bot/cogs'):
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
    log('<main> :: Bot', '  Bot is ready to use')
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
    bot.run(botconfig['token'])







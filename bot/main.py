#imports
import os
import platform
import time
from os import listdir
from os.path import join, realpath, split, splitext
from discord_slash import SlashCommand

import discord
from discord import ChannelType
import psutil
from discord.ext import commands
from discord.ext.dashboard import Dashboard

from botconfig import botconfig

#
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

def line(color):
    print(f"{color}-----------")
print(f"{bcolors.OKBLUE}-----------")
print('''
 __                             __               
[  |  _                        [  |  _           
 | | / ] __   _   ____   ,--.   | | / ] __   _   
 | '' < [  | | | [_   ] `'_\ :  | '' < [  | | |  
 | |`\ \ | \_/ |, .' /_ // | |, | |`\ \ | \_/ |, 
[__|  \_]'.__.'_/[_____]\'-;__/[__|  \_]'.__.'_/                                             
''')
print(f"{bcolors.OKBLUE}-----------")
def log(log):
    print(f'{bcolors.OKBLUE}[#] {log}')
def warning(warn):
    print(f'{bcolors.WARNING}[!] {warn}')
def error(error):
    print(f'{bcolors.FAIL}{error}')

class kuzaku(discord.ext.commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)

    async def on_connect(self):
        log('бот подключается...')
        line(bcolors.OKBLUE)
    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f'{len(self.guilds)} guilds | k.help'))
        log(f'бот подключен к discord\'у!\n[#] имя пользователя: {self.user}\n[#] id: {self.user.id}\n[#] кол-во серверов: {len(self.guilds)}\n[#] количество пользователей: {len(self.users)}')
        line(bcolors.OKBLUE)
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
    if platform.system() in ["Darwin", 'Windows']:
        for filename in os.listdir(f'{rootdir}/bot/cogs'):
            if filename.endswith('.py'):
                log(f'загружаю ког {filename[:-3]}')
                try:
                    bot.load_extension(f'{dir}.{filename[:-3]}')
                    log(f'ког {filename[:-3]} загружен')
                except Exception as e:
                    error(f'загрузка кога {filename[:-3]} НЕ УДАЛАСЬ!\n[#] ошибка:\n{e}')
    elif platform.system()=='Linux':
        for filename in os.listdir(f'{os.curdir}/bot/cogs'):
            if filename.endswith('.py'):
                log(f'загружаю ког {filename[:-3]}')
                try:
                    bot.load_extension(f'bot.cogs.{filename[:-3]}')
                    log(f'ког {filename[:-3]} загружен')
                except Exception as e:
                    error(f'загрузка кога {filename[:-3]} НЕ УДАЛАСЬ!\n[#] ошибка:\n{e}')
load_ext(bot, 'cogs')
line(bcolors.OKBLUE)

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
    bot.run(botconfig['token'])







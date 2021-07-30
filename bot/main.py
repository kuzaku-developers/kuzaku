#imports
import os
import platform
import time
from os import listdir
from os.path import join, realpath, split, splitext
from discord_slash import SlashCommand
rootdir=os.path.abspath(os.path.join(os.curdir))
import discord
import psutil
from discord.ext import commands

from botconfig import botconfig

#
intents=discord.Intents.all()
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
        log(f'бот подключен к discord\'у!\n[#] имя пользователя: {self.user}\n[#] кол-во серверов: {len(self.guilds)}\n[#] количество пользователей: {len(self.users)}')
        line(bcolors.OKBLUE)


bot=kuzaku(command_prefix='k.', intents=intents)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
@bot.event
async def on_message(message):
    banned=[]
    if str(message.author.id) in banned and message.content.startswith('k.'):
        return await message.reply('ты забанен')
        
    await bot.process_commands(message)
def load_ext(bot,dir):
    if platform.system() in ["Darwin", 'Windows']:
        for filename in os.listdir(f'{rootdir}/bot/cogs'):
            if filename.endswith('.py'):
                log(f'загружаю ког {filename[:-3]}')
                try:
                    bot.load_extension(f'{dir}.{filename[:-3]}')
                    log(f'ког {filename[:-3]} загружен')
                except Exception as e:
                    log(f'загрузка кога {filename[:-3]} НЕ УДАЛАСЬ!\n[#] ошибка:\n{e}')
    elif platform.system()=='Linux':
        for filename in os.listdir(f'{os.curdir}/bot/cogs'):
            if filename.endswith('.py'):
                log(f'загружаю ког {filename[:-3]}')
                try:
                    bot.load_extension(f'bot.cogs.{filename[:-3]}')
                    log(f'ког {filename[:-3]} загружен')
                except Exception as e:
                    log(f'загрузка кога {filename[:-3]} НЕ УДАЛАСЬ!\n[#] ошибка:\n{e}')
load_ext(bot, 'cogs')
line(bcolors.OKBLUE)
bot.load_extension('jishaku')
if __name__ == '__main__':
    bot.run(botconfig['token'])







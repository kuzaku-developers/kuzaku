import discord
from termcolor import cprint

import kuzaku.exts as ext
from botconfig import botconfig as config
from kuzaku.classes   import Kuzaku

if __name__ != '__main__':
    raise ImportError ('Cannot import main.py, it must be main file')

intents = discord.Intents.default ()
intents.members = True
intents.guilds  = True

bot = Kuzaku (command_prefix = config ['default_prefix'], intents = intents)

botname = f"Kuzaku Prod Ed. Ver {config['botver']}" if config ["production"] else "Kuzaku DEV ed."

cprint(f'''
 __                                __
[  |  _                           [  |  _
 | | / ]  __   _    ____    ,--.   | | / ]  __   _
 | '' <  [  | | |  [_   ]  `'_\ :  | '' <  [  | | |
 | |`\ \  | \_/ |,  .' /_  // | |, | |`\ \  | \_/ |
[__|  \_] '.__.'_/ [_____] \-;__/ [__|  \_] '.__.'_/


     ﹝ {botname} - the discord bot ﹞''',

    color = 'red', attrs = {'bold'}
)

print ('\n')

ext.load_cogs (bot, ignore = config ['ignore_cogs'])

bot.run (config ['token'])
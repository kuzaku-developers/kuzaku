import time
import os

import discord
from discord.ext.commands import Context
from discord.ext.dashboard import Dashboard

from discordTogether import DiscordTogether
from discord_slash import SlashCommand

from botconfig import botconfig as config
from kuzaku.logger import Kuzaku_logger
from kuzaku.exts   import ping
from kuzaku.dashboard import init_dashboard

class Kuzaku_context (Context):
    pass

    '''
    # * Example howdoi custom accsessor

    @property
    async def db_get (ctx):
        ...

        return value
    '''

class Kuzaku (discord.ext.commands.Bot):
    def __init__ (self, **options):
        super().__init__ (**options)

        self.together = DiscordTogether (self)
        self.slash = SlashCommand (self, sync_commands=True, sync_on_cog_reload=True)

        self.log = Kuzaku_logger ('root')

        if config ['production']:
            self.dashboard = Dashboard (
                self, os.getenv('ipckey'), "https://kuzaku.ml/dash_handler"
            )

        else:
            self.dashboard = Dashboard (
                self, os.getenv('ipckey'), "http://127.0.0.1:5000/dash_handler"
            )

        init_dashboard (self)

    async def on_connect(self):
        sec = int (round (time.time () - config ['start_time']))
        self.log.info(f'<main> :: Bot info')
        self.log.info(f'    {self.user} connected successfully in {sec} seconds')

    async def on_ready(self):
        await self.change_presence (
            status   = discord.Status.dnd,
            activity = discord.Activity (
                type = discord.ActivityType.competing,
                name = f'{len (self.guilds)} guilds! | /help'
            )
        )

        self.log.info('<main> :: Bot')
        self.log.info('    Bot is ready to use')
        self.log.info('<api> :: Trying to ping website...')
        try:
            if ping('kuzaku.ml'):
                self.log.log('    Website is working!')
            else:
                self.log.warn('    Website is not working!')
        except:
            self.log.warn('    Website is not working!')

    async def on_message(self, message):
        await self.dashboard.process_request(message)
        await self.process_commands(message)

    async def get_context(self, message, *, cls = Kuzaku_context):
        return await super().get_context(message, cls = cls)

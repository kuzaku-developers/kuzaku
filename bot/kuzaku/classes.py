import time
import os

import discord
from discord.ext.commands import Context
from discord.ext.dashboard import Dashboard

from discordTogether import DiscordTogether
import dislash
from dislash import InteractionClient
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
        self.slash = InteractionClient(self)

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
class MobileWebSocket(discord.gateway.DiscordWebSocket):
    async def identify(self):
        """Sends the IDENTIFY packet."""
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "ios",
                    "$browser": "Discord iOS",
                    "$device": "discord.py",
                    "$referrer": "",
                    "$referring_domain": "",
                },
                "compress": True,
                "large_threshold": 250,
                "v": 3,
            },
        }

        if not self._connection.is_bot:
            payload["d"]["synced_guilds"] = []

        if self.shard_id is not None and self.shard_count is not None:
            payload["d"]["shard"] = [self.shard_id, self.shard_count]

        state = self._connection
        if state._activity is not None or state._status is not None:
            payload["d"]["presence"] = {
                "status": state._status,
                "game": state._activity,
                "since": 0,
                "afk": False,
            }

        await self.send_as_json(payload)
        discord.gateway.log.info(
            "Shard ID %s has sent the IDENTIFY payload.", self.shard_id
        )


discord.client.DiscordWebSocket = MobileWebSocket
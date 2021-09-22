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
bot.run (config ['token'])
import time
import os
import disnake
from disnake.ext.commands import Context
from disnake.ext import commands
from discord.ext.dashboard import Dashboard
import disnake
from discordTogether import DiscordTogether
from botconfig import botconfig as config
from kuzaku.logger import Kuzaku_logger
from kuzaku.exts import ping
from kuzaku.dashboard import init_dashboard


class Kuzaku_context(Context):
    pass

    """
    # * Example howdoi custom accsessor

    @property
    async def db_get (ctx):
        ...

        return value
    """


class Kuzaku(disnake.ext.commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)

        self.together = DiscordTogether(self)

        self.log = Kuzaku_logger.new()

        if config["production"]:
            self.dashboard = Dashboard(
                self, os.getenv("ipckey"), "https://kuzaku.ml/dash_handler"
            )

        else:
            self.dashboard = Dashboard(
                self, os.getenv("ipckey"), "http://127.0.0.1:5000/dash_handler"
            )

        init_dashboard(self)

    async def on_connect(self):
        sec = int(round(time.time() - config["start_time"]))
        with self.log.get("CONNECTED") as sub:
            sub.info(f"{self.user} connected successfully in {sec} seconds")

        sub.exit()

    async def on_ready(self):
        await self.change_presence(
            activity=disnake.Activity(
                type=disnake.ActivityType.competing,
                name=f"{len (self.guilds)} guilds! | /help",
            )
        )
        sub = self.log.get("ready").enter()
        sub.info("Bot is ready to use")
        try:
            if ping("kuzaku.ml"):
                sub.log("Website is working!")
            else:
                sub.warn("    Website is not working!")
        except:
            sub.warn("    Website is not working!")
        sub.exit()

    async def on_message(self, message):
        await self.dashboard.process_request(message)
        await self.process_commands(message)

    async def get_context(self, message, *, cls=Kuzaku_context):
        return await super().get_context(message, cls=cls)


class MobileWebSocket(disnake.gateway.DiscordWebSocket):
    async def identify(self):
        """Sends the IDENTIFY packet."""
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "ios",
                    "$browser": "Discord iOS",
                    "$device": "nextcord",
                    "$referrer": "",
                    "$referring_domain": "",
                },
                "compress": True,
                "large_threshold": 250,
                "v": 3,
            },
        }

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

        if state._intents is not None:
            payload["d"]["intents"] = state._intents.value

        await self.call_hooks(
            "before_identify", self.shard_id, initial=self._initial_identify
        )
        await self.send_as_json(payload)
        disnake.gateway._log.info(
            "Shard ID %s has sent the IDENTIFY payload.", self.shard_id
        )


disnake.client.DiscordWebSocket = MobileWebSocket

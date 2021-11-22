import disnake
from disnake.ext import commands
import socketio
import os
import json
import asyncio

sio = socketio.AsyncClient(reconnection=False)


class premiumdon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @sio.on("connect")
    async def on_connect():
        await sio.emit(
            "add-user", {"token": os.getenv("DONATIONTOKEN"), "type": "alert_widget"}
        )

    @sio.on("donation")
    async def on_message(data):
        y = json.loads(data)
        user = disnake.utils.get(self.bot.get_all_members(), id=str(y["username"]))
        print(user)
        print(y["username"])
        print(y["message"])
        print(y["amount"])
        print(y["currency"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log.info("<premium> :: connecting to sockets")
        try:
            await sio.connect(
                "wss://socket.donationalerts.ru:443", transports="websocket"
            )
            self.bot.log.info("    connected to sockets!")
        except Exception as e:
            self.bot.log.info("    can't connect to sockets!")


def setup(bot: commands.Bot):
    bot.add_cog(premiumdon(bot))

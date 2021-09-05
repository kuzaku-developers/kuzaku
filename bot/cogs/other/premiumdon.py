import discord
from discord.ext import commands
import socketio
import json
import asyncio
sio = socketio.AsyncClient(reconnection=False)
class premiumdon(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @sio.on('connect')
    async def on_connect():
	    await sio.emit('add-user', {"token": 'LATER', "type": "alert_widget"})
    @sio.on('donation')
    async def on_message(data):
        y = json.loads(data)

        print(y['username'])
        print(y['message'])
        print(y['amount'])
        print(y['currency'])
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log('<premium> :: connecting to sockets')
        try:
            await sio.connect('wss://socket.donationalerts.ru:443',transports='websocket')
            self.bot.log('    connected to sockets!')
        except Exception as e:
            print(e)
            self.bot.log('    can\'t connect to sockets!')
def setup(bot:commands.Bot):
    bot.add_cog(premiumdon(bot))
import discord
from discord.ext import commands
import socketio
import json
sio = socketio.Client()
class premiumdon(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @sio.on('connect')
    def on_connect():
	    sio.emit('add-user', {"token": 'F63EDCqojc7msE0DzkaV', "type": "alert_widget"})

    @sio.on('donation')
    def on_message(data):
	    y = json.loads(data)

	    print(y['username'])
	    print(y['message'])
	    print(y['amount'])
	    print(y['currency'])
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log('<premium> :: connecting to sockets')
        try:
            sio.connect('wss://socket.donationalerts.ru:443',transports='websocket')
            self.bot.log('    connected to sockets!')
        except Exception as e:
            print(e)
            self.bot.log('    can\'t connect to sockets!')
def setup(bot:commands.Bot):
    bot.add_cog(premiumdon(bot))
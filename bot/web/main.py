import json
from firebase import Firebase
import requests
import discord
from main import bot
from discord import Webhook, RequestsWebhookAdapter
from quart import Quart, render_template, request, session, redirect, url_for, Response
import os
if os.getenv("PRODUCTION")!="yes":
    import dotenv
    dotenv.load_dotenv()
configfb = {
    "apiKey": os.getenv("fapiKey"),
    "authDomain": os.getenv("fauthDomain"),
    "databaseURL": os.getenv("fdatabaseURL"),
    "storageBucket": os.getenv("fstorageBucket")
}


firebase = Firebase(configfb)
db = firebase.database()
app = Quart(__name__)


@app.route('/api/v1/premium',methods = ['POST'])
async def premium():
    print(request.json)
    print(request.json)
    data = {
        'premium': 'True'
    }
    if request.json['custom']['secret']==os.getenv('apisecret'):
        db.child("db").child("premium").child(request.json['custom']['id']).set(data)
    else:
        return Response(status=401)
    # Webhook URL for your Discord channel.
    WEBHOOK_URL = os.getenv('webhook')
    embed=discord.Embed(title='ого, купили премиум!',description=f'премиум купил {request.json["custom"]["name"]}!\nнаше уважение, премим уже выдан для {request.json["custom"]["member_men"]}!')
    embed.set_footer(text='kuzaku', icon_url='https://cdn.discordapp.com/avatars/781162235673968651/392391e3893cfff8e4f2892e761eb660.webp?size=1024')
    embed.set_author(name=request.json['custom']['name'], icon_url=request.json['custom']['avatar'])
    # Initialize the webhook class and attaches data.
    webhook=Webhook.from_url(WEBHOOK_URL,adapter=RequestsWebhookAdapter())
    webhook.send(embed=embed, username='покупка премиума', avatar_url=request.json['custom']['avatar'])
    return Response(status=200)

@app.route('/api/v1/statistic/')
async def stats():
    txtchannel_list = []
    voicechannel_list = []
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.type == ChannelType.text:
                txtchannel_list.append(channel)
            elif channel.type == ChannelType.voice:
                voicechannel_list.append(channel)
    return {"status":"200", "message":"all is ok", "guilds":str(len(bot.guilds)), "users":str(len(bot.users)), "txtchannels": str(len(txtchannel_list)), "voicechannels": str(len(voicechannel_list))}






@app.route('/docs')
async def docs():
    return redirect('https://docs.kuzaku.ml')
    
@app.route('/api/v1/ping/')
async def ping():
    return {"code":"200","message":"bot is working!"}

@app.errorhandler(404)
async def page_not_found(e):
    return await render_template('404.html'), 404

@app.route('/api/v1/')
async def api():
    return {"code":"200","message":"api is working!"}

@app.route('/')
async def main():
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.type == ChannelType.text:
                txtchannel_list.append(channel)
            elif channel.type == ChannelType.voice:
                voicechannel_list.append(channel)
    stats = {"status":"200", "message":"all is ok", "guilds":str(len(bot.guilds)), "users":str(len(bot.users)), "txtchannels": str(len(txtchannel_list)), "voicechannels": str(len(voicechannel_list))}

    return await render_template('index.html', guilds=stats['guilds'], users=stats['users'], txtchannels=stats['txtchannels'], voicechannels=stats['voicechannels'])
@app.route('/commands')
async def commands():
    return await render_template('commands.html')
@app.route('/invite/')
async def invite():
    return redirect('https://google.com')

if os.getenv('PRODUCTION')!='yes':
    app.run()
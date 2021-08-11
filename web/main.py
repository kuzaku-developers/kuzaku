import json
from firebase import Firebase
import requests
import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext.dashboard import Server
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
app_dashboard = Server(
	app,
	os.getenv('ipckey'), 
	webhook_url=os.getenv('webhook_ipc'),
	sleep_time=1
)

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
async def test():
    if await app_dashboard.request("get_stats"):
        return await app_dashboard.request("get_stats"), 200
    else:
        return {"code":"503","message":"bot is offline!"}, 503

@app.route("/dash_handler", methods=["POST"])
async def dash_handler():
	# Don't worry about authorization, the bot will handle it
    try:
	    await app_dashboard.process_request(request)
    except:
        pass


@app.route('/docs')
async def docs():
    return redirect('https://docs.kuzaku.ml')
    
@app.route('/api/v1/ping/')
async def ping():
    if await app_dashboard.request("get_stats"):
        return {"code":"200","message":"bot is working!"}, 200
    else:
        return {"code":"503","message":"bot is offline!"}, 503


@app.errorhandler(404)
async def page_not_found(e):
    return await render_template('404.html'), 404

@app.route('/api/v1/')
async def api():
    return {"code":"200","message":"api is working!"}, 200

@app.route('/')
async def main():
    if await app_dashboard.request("get_stats"):
        return await render_template('index.html', guilds=dict(await app_dashboard.request("get_stats"))['guilds'], users=dict(await app_dashboard.request("get_stats"))['users'], txtchannels=dict(await app_dashboard.request("get_stats"))['txtchannels'], voicechannels=dict(await app_dashboard.request("get_stats"))['voicechannels'])
    else:
        return await render_template('index.html', guilds='-', users='-', txtchannels='-', voicechannels='-')

@app.route('/commands')
async def commands():
    return await render_template('commands.html')

@app.route('/status')
async def status():
    return await render_template('status.html')

@app.route('/invite/')
async def invite():
    return redirect(await app_dashboard.request("get_invite_url"))

app.run(host='0.0.0.0', port=os.getenv("PORT", 5000))

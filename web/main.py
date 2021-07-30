import json
from firebase import Firebase
import requests
import discord
from discord import Webhook, RequestsWebhookAdapter
from flask import Flask, request, Response
import os
from flask import Flask, redirect, render_template
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
app = Flask(__name__)


@app.route('/v1/api/premium',methods = ['POST'])
def premium():
    print(request.json)
    print(request.json)
    data = {
        'premium': 'True'
    }
    if request.json['custom']['secret']==os.getenv('apisecret'):
        db.child("premium").child(request.json['custom']['id']).set(data)
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


@app.route('/v1/api/ping/')
def ping():
    return {"code":"200","message":"bot is working!"}

@app.route('/v1/api/')
def api():
    return {"code":"200","message":"api is working!"}

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/commands')
def commands():
    return render_template('commands.html')
@app.route('/invite/')
def invite():
    return redirect(f'https://google.com/')

if os.getenv('PRODUCTION')!='yes':
    app.run()
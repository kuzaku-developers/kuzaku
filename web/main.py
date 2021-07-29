<<<<<<< HEAD
import json
from firebase import Firebase
import requests
import discord
from discord import Webhook, RequestsWebhookAdapter
from flask import Flask, request
import os
configfb = {
    "apiKey": "AIzaSyCfJSX5JyY03MXT-PeLopJb_iH0M8O9nvU",
    "authDomain": "142115676780.firebaseapp.com",
    "databaseURL": "https://chatik-dcd54.firebaseio.com/",
    "storageBucket": "chatik-dcd54.appspot.com"
}

firebase = Firebase(configfb)
db = firebase.database()

app=Flask(__name__)

@app.route('/api/premium',methods = ['POST'])
def index():
    print(request.json)
    data = {
        'premium': 'True'
    }
    if request.json['custom']['secret']==os.getenv('apisecret'):
        db.child("premium").child(request.json['custom']['id']).set(data)
    else:
        return
    # Webhook URL for your Discord channel.
    if request.json['custom']['test'] == 'false':
        testli='это не тестовая покупка!'
    else:
        testli = 'это тестовая покупка!'
    WEBHOOK_URL = 'https://discord.com/api/webhooks/802842133937258518/K1G_UJeYD_l_XWqyZVi_Wf-NUdPfJgp1BI3MpWpO7Srq7R_zI2NuHpow3DA_Fg6OyEu-'
    embed=discord.Embed(title='ого, купили премиум!',description=f'премиум купил {request.json["custom"]["name"]}!\nнаше уважение, премим уже выдан для {request.json["custom"]["member_men"]}!\n{testli}')
    embed.set_footer(text=request.json['custom']['bot_name'], icon_url='https://cdn.discordapp.com/avatars/781162235673968651/392391e3893cfff8e4f2892e761eb660.webp?size=1024')
    embed.set_author(name=request.json['custom']['name'], icon_url=request.json['custom']['avatar'])
    # Initialize the webhook class and attaches data.
    webhook=Webhook.from_url(WEBHOOK_URL,adapter=RequestsWebhookAdapter())
    webhook.send(embed=embed, username='покупка премиума', avatar_url=request.json['custom']['avatar'])
    
from flask import Flask, redirect, render_template
app = Flask(__name__)


@app.route('/v1/api/ping/')
=======
import os

from flask import Flask, redirect
app = Flask(__name__)


@app.route('/api/ping/')
>>>>>>> d2e277457312a0b59961f31085629cb5ba036048
def ping():
    return "all is OK"


@app.route('/')
def main():
<<<<<<< HEAD
    return render_template('index.html')

@app.route('/commands')
def commands():
    return render_template('commands.html')
=======
    return redirect('api/ping')


>>>>>>> d2e277457312a0b59961f31085629cb5ba036048
@app.route('/invite/')
def invite():
    return redirect(f'https://google.com/')

if os.getenv('PRODUCTION')!='yes':
    app.run()
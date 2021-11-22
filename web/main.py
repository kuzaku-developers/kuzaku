import json
from firebase import Firebase
import requests
import disnake as discord
from functools import wraps
from disnake import Webhook
from discord.ext.dashboard import Server
from quart import Quart, render_template, request, session, redirect, url_for, Response
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os
import sys
import inspect

if os.getenv("PRODUCTION") != "yes":
    import dotenv

    dotenv.load_dotenv()
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from bot.utils.db import *

configfb = {
    "apiKey": os.getenv("fapiKey"),
    "authDomain": os.getenv("fauthDomain"),
    "databaseURL": os.getenv("fdatabaseURL"),
    "storageBucket": os.getenv("fstorageBucket"),
}
modules = [
    {"name": "Экономика", "url": "economy", "icon": "star_rate"},
    {"name": "Настройки бота", "url": "botsettings", "icon": "smart_toy"},
    {"name": "Роли по реакциям", "url": "rolereactions", "icon": "emoji_emotions"},
    {"name": "Модерация", "url": "moderation", "icon": "storage"},
]

firebase = Firebase(configfb)
db2 = firebase.database()
app = Quart(__name__)
app.secret_key = os.getenv("apisecret")
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("CSEC")  # Discord client secret.
if os.getenv("PRODUCTION") == "yes":
    app.config["DISCORD_REDIRECT_URI"] = "https://kuzaku.ml/callback"
    app.config["DISCORD_CLIENT_ID"] = 778648045960298568
else:
    app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
    app.config["DISCORD_CLIENT_ID"] = 788834922340679700
app.config["DISCORD_BOT_TOKEN"] = os.getenv(
    "BOTTOKEN"
)  # Required to access BOT resources.
discord = DiscordOAuth2Session(app)
app_dashboard = Server(
    app, os.getenv("ipckey"), webhook_url=os.getenv("webhook_ipc"), sleep_time=1
)


@app.route("/login/")
async def login():
    return await discord.create_session()


@app.route("/callback")
async def callback():
    await discord.callback()
    return redirect("/")


@app.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/dashboard")
async def dashboard():
    authorized = await discord.authorized
    if authorized != True:
        return redirect("/login")

    guild_ids = await app_dashboard.request("get_mutual_guilds")
    if not guild_ids:
        return "bot is offline"
    user_guilds = await discord.fetch_guilds()
    user = await discord.fetch_user()
    admin_guilds = []
    mutual_guilds = []
    for guild in user_guilds:
        if guild.permissions.administrator == True and guild.id not in guild_ids:
            admin_guilds.append(guild)
        elif guild.permissions.administrator == True and guild.id in guild_ids:
            mutual_guilds.append(guild)
    guilds = await discord.fetch_guilds()
    return await render_template(
        "dash.html",
        admin_guilds=admin_guilds,
        mutual_guilds=mutual_guilds,
        user=user,
        config={"discord_client_id": "778648045960298568"},
        modules=modules,
    )


@app.route("/dashboard/<guild_id>")
async def guild_dashboard(guild_id):
    authorized = await discord.authorized
    if authorized != True:
        return redirect("login")

    user = await discord.fetch_user()
    guilds = await discord.fetch_guilds()

    for guild in guilds:
        if guild.id == int(guild_id):
            return await render_template(
                "guild-dashboard.html", guild=guild, user=user, modules=modules
            )


@app.route("/dashboard/<guild_id>/<module>")
async def guild_dashboard_leveling(guild_id, module):
    authorized = await discord.authorized
    if authorized != True:
        return redirect("login")

    user = await discord.fetch_user()
    guilds = await discord.fetch_guilds()

    for guild in guilds:
        if guild.id == int(guild_id):
            print(get_config(guild.id))
            return await render_template(
                f"{module}.html", guild=guild, user=user, config=get_config(guild.id)
            )

    return redirect("/")


@app.route("/api/settings/change/<guild_id>", methods=["POST"])
async def api_change_setting(guild_id):
    authorized = await discord.authorized
    if authorized != True:
        return "error"

    args = await request.form
    print(args["value"])
    callback = change_config(guild_id, args["item"], args["value"])
    if callback == True:
        return "done"
    else:
        return "error"
    return "error"


@app.route("/logout")
async def logout():
    discord.revoke()
    return redirect("/")


@app.route("/api/v1/usecode", methods=["POST"])
async def usecode():
    args = dict(await request.form)
    print(args)
    existing = False
    global i
    global used_by
    for i in getpromos():
        if str(getpromos()[i]["promocode"]) == str(args["promocode"]):
            existing = True
            try:
                used_by = getpromos()[i]["usedby"]
            except:
                used_by = []
    if not existing:
        return "notexist"
    else:
        try:
            if args["id"] in used_by:
                return "used"

            else:
                used_by.append(args["id"])
                addusepromo(i, used_by)
            if getpromos()[i]["uses"] != "inf" and str(getpromos()[i]["uses"]) == "0":
                print("noueses")
                return "nouses"
            prem = int(dict(getdb()["premium"])[str(args["id"])]["count"]) + 1
        except:
            prem = 1
        data = {"premium": "True", "count": prem}
        db.child("db").child("premium").child(args["id"]).set(data)
        if getpromos()[i]["uses"] != "inf":
            setpromouses(i, int(getpromos()[i]["uses"]) - 1)
        return "activated"
    print("eee cALLED")
    args = json.dumps(await request.form)
    print(args)
    return "done"


@app.route("/api/v1/premium", methods=["POST"])
async def premium_handler():
    print(request.json)
    print(request.json)
    data = {"premium": "True", "count": "3"}
    if request.json["custom"]["secret"] == os.getenv("apisecret"):
        db2.child("db").child("premium").child(request.json["custom"]["id"]).set(data)
    else:
        return Response(status=401)
    # Webhook URL for your Discord channel.
    WEBHOOK_URL = os.getenv("webhook")
    embed = discord.Embed(
        title="ого, купили премиум!",
        description=f'премиум купил {request.json["custom"]["name"]}!\nнаше уважение, премим уже выдан для {request.json["custom"]["member_men"]}!',
    )
    embed.set_footer(
        text="kuzaku",
        icon_url="https://cdn.discordapp.com/avatars/781162235673968651/392391e3893cfff8e4f2892e761eb660.webp?size=1024",
    )
    embed.set_author(
        name=request.json["custom"]["name"], icon_url=request.json["custom"]["avatar"]
    )
    # Initialize the webhook class and attaches data.
    webhook = Webhook.from_url(WEBHOOK_URL)
    await webhook.send(
        embed=embed,
        username="покупка премиума",
        avatar_url=request.json["custom"]["avatar"],
    )
    return Response(status=200)


@app.route("/api/v1/statistic/")
async def test():
    if await app_dashboard.request("get_stats"):
        return await app_dashboard.request("get_stats"), 200
    else:
        return {"code": "418", "message": "No coffee today :("}, 418


@app.route("/dash_handler", methods=["POST"])
async def dash_handler():
    # Don't worry about authorization, the bot will handle it
    try:
        await app_dashboard.process_request(request)
    except:
        pass


@app.route("/docs")
async def docs():
    return redirect("https://docs.kuzaku.ml")


@app.route("/api/v1/ping/")
async def ping():
    if await app_dashboard.request("get_stats"):
        return {"code": "200", "message": "bot is working!"}, 200
    else:
        return {"code": "418", "message": "No coffee today :("}, 418


@app.route("/premium")
async def premium():
    authorized = await discord.authorized
    if authorized != True:
        return redirect("login")
    user = await discord.fetch_user()
    return await render_template("premium.html", user=user)


@app.errorhandler(404)
async def page_not_found(e):
    return await render_template("404.html"), 404


@app.route("/api/v1/")
async def api():
    return {"code": "200", "message": "api is working!"}, 200


@app.route("/")
async def main():
    try:
        authorized = await discord.authorized
    except:
        authorized = False
    if authorized != True:
        dashbtnname = "Войти"
        user = None
    else:
        dashbtnname = "Пользователь"
        try:
            user = await discord.fetch_user()
        except:
            return redirect("logout")
    statistic = await app_dashboard.request("get_stats")
    if statistic:
        return await render_template(
            "index.html",
            guilds=dict(statistic)["guilds"],
            users=dict(statistic)["users"],
            channels=dict(statistic)["channels"],
            dashbtnname=dashbtnname,
            user=user,
        )
    else:
        return await render_template(
            "index.html",
            guilds="0",
            users="0",
            channels="0",
            dashbtnname=dashbtnname,
            user=user,
        )


@app.route("/developers")
async def devs():
    try:
        authorized = await discord.authorized
    except:
        authorized = False
    if authorized != True:
        dashbtnname = "Войти"
        user = None
    else:
        dashbtnname = "Пользователь"
        try:
            user = await discord.fetch_user()
        except:
            return redirect("logout")
    statistic = await app_dashboard.request("get_stats")
    if statistic:
        return await render_template(
            "developers.html",
            guilds=dict(statistic)["guilds"],
            users=dict(statistic)["users"],
            channels=dict(statistic)["channels"],
            dashbtnname=dashbtnname,
            user=user,
        )
    else:
        return await render_template(
            "developers.html",
            guilds="0",
            users="0",
            channels="0",
            dashbtnname=dashbtnname,
            user=user,
        )


@app.route("/commands")
async def commands():
    return await render_template("commands.html")


@app.route("/amogus")
async def amogus():
    return await render_template("amogus.html")


@app.route("/invite/")
async def invite():
    return redirect(await app_dashboard.request("get_invite_url"))


app.run(host="0.0.0.0", port=os.getenv("PORT", 5000), debug=True)

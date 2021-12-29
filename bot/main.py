import disnake
from termcolor import cprint

from botconfig import botconfig as config
from kuzaku.classes import Kuzaku
import kuzaku.exts as ext


if __name__ != "__main__":
    raise ImportError("Cannot import main.py, it *must* be main file")

intents = disnake.Intents.default()
intents.members = True
intents.guilds = True
if config["production"]:
    bot = Kuzaku(
        command_prefix=config["default_prefix"],
        intents=intents,
        owner_ids=[704560097610825828, 732571199913328691],
    )
else:
    bot = Kuzaku(
        command_prefix=config["default_prefix"],
        intents=intents,
        owner_ids=[704560097610825828, 732571199913328691],
        test_guilds=[808013895917633546, 888371092610252800],
        reload=True,
        enable_debug_events=True

    )

botname = (
    f"Kuzaku Prod Ed. Ver {config['botver']}"
    if config["production"]
    else "Kuzaku DEV ed."
)

cprint(
    f"""
 __                                __
[  |  _                           [  |  _
 | | / ]  __   _    ____    ,--.   | | / ]  __   _
 | '' <  [  | | |  [_   ]  `'_\ :  | '' <  [  | | |
 | |`\ \  | \_/ |,  .' /_  // | |, | |`\ \  | \_/ |
[__|  \_] '.__.'_/ [_____] \-;__/ [__|  \_] '.__.'_/


     ﹝ {botname} - the discord bot ﹞""",
    color="red",
    attrs={"bold"},
)

print("\n")

ext.load_cogs(bot, ignore=config["ignore_cogs"])

if __name__ == "__main__":
    bot.ipc.start()
    bot.run(config["token"])
# Если вы это читаете, то вы подтверждаете то что вы не имеете права критиковать этот говно-код за его убогость и нечитаемость.
# Автор кода придерживается принципа пофиг-как, главное чтоб работало.

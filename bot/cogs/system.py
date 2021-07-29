import datetime
<<<<<<< HEAD
import os
import platform
import time

from dislash import Option, Type, slash_commands
from yaml import load

if platform.system() in ["Darwin", 'Windows']:
    from utils.time import pickform, visdelta
elif platform.system() == 'Linux':
    from bot.utils.time import pickform, visdelta

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except:
    from yaml import  Loader,Dumper

import discord
import psutil
from discord.ext import commands
from DiscordBar import DSprogressbar as Bar
from github import Github

=======
import platform
import time

from dislash import slash_commands, Option, Type
from yaml import load
if platform.system() in ["Darwin", 'Windows']:
    from bot.utills.time import visdelta, pickform
elif platform.system() == 'Linux':
    from bot.utills.time import visdelta, pickform

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except:
    from yaml import  Loader,Dumper
import discord
import psutil
from discord.ext import commands
from github import Github
from DiscordBar import DSprogressbar as Bar
>>>>>>> d2e277457312a0b59961f31085629cb5ba036048
if platform.system() in ["Darwin", 'Windows']:
    from main import startTime
elif platform.system() == 'Linux':
    from bot.main import startTime
rootdir=os.path.abspath(os.path.join(os.curdir))

class system(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        if platform.system() in ["Darwin", 'Windows']:
            with open(f"{rootdir}/bot/localization/ru/commands.yml", 'r') as stream:
                self.data = load(stream, Loader=Loader)
        elif platform.system() == 'Linux':
            with open("bot/localization/ru/commands.yml", 'r') as stream:
                self.data = load(stream, Loader=Loader)

    @slash_commands.command(
        description="Builds a custom embed",
        options=[
            Option('title', 'Makes the title of the embed', Type.STRING),
            Option('desc', 'Makes the description', Type.STRING),
            Option('color', 'The color of the embed', Type.STRING)

            # Note that all args are optional
            # because we didn't specify required=True in Options
        ]
    )
    async def embed(self, inter, title=None, desc=None, color=None):
        # Converting color
        if color is not None:
            try:
                color = await commands.ColorConverter().convert(inter, color)
            except:
                color = None
        if color is None:
            color = discord.Color.default()
        # Generating an embed
        emb = discord.Embed(color=color)
        if title is not None:
            emb.title = title
        if desc is not None:
            emb.description = desc
        # Sending the output
        await inter.reply(embed=emb, hide_user_input=True)

    @commands.command(name='stats')
    async def stats(self, ctx):
        sec = int(round(time.time() - startTime))
        upt = (time.gmtime(sec))
        now = psutil.virtual_memory().used
        max = psutil.virtual_memory().total
        bar = Bar(now=round(now), needed=max, type='get')
        progress = await bar.progress(line='□', fill='[■](https://kuzaku.ml)')



        embed=discord.Embed(title=self.data['system.stats.title'])
        g=Github()
        repo=g.get_repo('The-Naomi-Developers/naomi-localization')
        commit=repo.get_commits().totalCount
        date=repo.get_commits()[0].commit.author.date
        date=date.strftime("%Y-%M-%d")
        embed.add_field(name=self.data['system.stats.tech.title'], value=f'''
💻 ОС **{platform.system()} {platform.release()}**
<:python:796454672860708896> Python версии **{platform.python_version()}**
<:python:796454672860708896> discord.py версии **{discord.__version__}**
<:settings_blue:796456043416780840> версия kuzaku **{date} ({commit})**
        ''', inline=False)
        embed.add_field(name=self.data['system.stats.ram.title'], value=self.data['system.stats.ram'].format(str(psutil.virtual_memory().percent),progress,str(psutil.virtual_memory().total/(1024.**3)),str(round(psutil.virtual_memory().used/(1024.**3),2))))
        current_time = time.time()
        difference = current_time - startTime
        timee = datetime.timedelta(seconds=round(difference))
        tch_count=0
        vch_count=0
        ppl=0
        for guild in self.bot.guilds:
            for _ in guild.members:
                ppl+=1
            for channel in guild.channels:
                if channel.type == discord.ChannelType.text:
                    tch_count += 1
                if channel.type == discord.ChannelType.voice:
                    vch_count += 1
        embed.add_field(name='информация', value=f'''
:tools: Доступно {len(self.bot.all_commands)} {pickform(len(self.bot.all_commands), ['команда','команды', 'команд'])} 
:file_folder: Всего серверов: {len(self.bot.guilds)}
<:txt_channel:796381251497099356> текстовых каналов: {tch_count}
<:voice_channel:796455929133793331> голосовых каналов: {vch_count}
<:members:796455485506322493> всего людей: {ppl}
:hourglass_flowing_sand: Аптайм: {visdelta(timee)}
''')
        embed.add_field(name='задержка', value='позде')
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}stats | вызваал {ctx.author.name}', icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=embed)
def setup(bot):
    bot.add_cog(system(bot))
"""
@commands.command()
    async def stats(self, ctx):
        
        tch_count = 0
        vch_count = 0
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.type == discord.ChannelType.text:
                    tch_count+=1
                if channel.type == discord.ChannelType.voice:
                    vch_count+=1

        em = discord.Embed(
            color=0x5a91a3,
            title=f"Техническая информация {self.bot.user.name}")
            
        em.add_field(name="<:settings:852398515106611220>**Каналы**", value=f"<:voice:852398543300722718>| Голосоых: `{vch_count}`\n<:text:852398523382759434>| Текстовых: `{tch_count}`\n")
        em.add_field(name="<:settings:852398515106611220>**Статистика**", value=f"<:upward_stonks:852398532254367765>| Серверов: `{len(self.bot.guilds)}`\n<:upward_stonks:852398532254367765>| Людей: `{len(self.bot.users)}`\n<:upward_stonks:852398532254367765>| Эмоджи: `{len(self.bot.emojis)}`\n")
        em.add_field(name="<:settings:852398515106611220>**Задержка**", value=f"<:greenTick:852398498657599569>|Веб-сокет:`{round(self.bot.latency*1000, 2)}`\n<:greenTick:852398498657599569>|Работает:`{сюда}`")
        em.add_field(name="<:settings:852398515106611220>**VPS (использование)**", value=f"<:rich_presence:852398506441572373>**|** ОС: `{platform.system() + platform.release()}`\n<:rich_presence:852398506441572373>**|** ОЗУ: `{psutil.virtual_memory().percent}`%\n<:rich_presence:852398506441572373>**|** ЦП: `{psutil.cpu_percent(interval=None, percpu=False)}`%\n")
        em.add_field(name="<:settings:852398515106611220>**Версии**", value=f"<:A2python:852402187232870400> **|** discord.py: `{discord.__version__}`\n<:A2python:852402187232870400> **|** Python: `{sys.version[:5]}`\n:purple_heart: **|** Anni: `2.0.2` (41 commits)")
    
        em.set_thumbnail(url={bot.avatar_url})
        em.set_footer(text=f"Запрошено: {ctx.author.name} | Команда: a.stats", icon_url=f"{ctx.author.avatar_url}")
        await ctx.reply(embed=em)
<<<<<<< HEAD
"""
=======
"""
>>>>>>> d2e277457312a0b59961f31085629cb5ba036048

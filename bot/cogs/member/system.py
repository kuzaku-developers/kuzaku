import datetime
import os
import platform
import time
import psutil
from yaml import load
from utils.db import usedcommands
import discord
from discord.ext import commands
from multibar import ProgressBar
from github import Github
import math
from dislash import slash_command, Option, OptionType

# from discord_slash import SlashCommand
# from discord_slash.utils.manage_components import wait_for_component
# from discord_slash.utils.manage_components import create_button, create_actionrow
# from discord_slash.utils.manage_commands import create_option
# from discord_slash.model import ButtonStyle

if platform.system() in ["Darwin", 'Windows']:
    from utils.time import pickform, visdelta
    from botconfig import botconfig as config

elif platform.system() == 'Linux':
    from bot.botconfig import botconfig as config
    from bot.utils.time import pickform, visdelta

try:
    # from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except:
    # from yaml import Loader, Dumper
    pass

# if platform.system() in ["Darwin", 'Windows']:
#     from main import startTime
# elif platform.system() == 'Linux':
#     from bot.main import startTime
rootdir=os.path.abspath(os.path.join(os.curdir))

class system(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        if platform.system() in ["Darwin", 'Windows']:
            with open(f"{rootdir}/localization/ru/bot/commands.yml", 'r', encoding='utf8') as stream:
                self.data = load(stream, Loader=Loader)
        elif platform.system()=='Linux':
            with open("localization/ru/bot/commands.yml", 'r', encoding='utf8') as stream:
                self.data = load(stream, Loader=Loader)


    @slash_command(name='stats', description='Статистика бота')
    async def stats(self, ctx):
        await ctx.respond(type=5)
        def natural_size(size_in_bytes: int):
            units = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

            power = int(math.log(size_in_bytes, 1024))

            return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"
        proc = psutil.Process()
        with proc.oneshot():
            try:
                mem = proc.memory_full_info()
                using=mem.vms
                allmem=psutil.virtual_memory().total
            except psutil.AccessDenied:
                using='None'
                allmem='None'
        sec = int(round(time.time() - config ['start_time']))
        upt = (time.gmtime(sec))
        bar = ProgressBar(round(using), round(allmem), length=10)
        progress = bar.write_progress(line='□', fill='[■](https://kuzaku.ml)')



        embed=discord.Embed(title=self.data['system.stats.title'])
        g=Github()
        repo=g.get_repo('kuzaku-developers/kuzaku')
        commit=repo.get_commits().totalCount
        date=repo.get_commits()[0].commit.author.date
        date=date.strftime("%Y-%M-%d")
        embed.add_field(name=self.data['system.stats.tech.title'], value=f'''
💻 ОС **{platform.system()} {platform.release()}**
<:python:796454672860708896> Python версии **{platform.python_version()}**
<:python:796454672860708896> discord.py версии **{discord.__version__}**
<:settings_blue:796456043416780840> версия kuzaku **{date} ({commit})**
        ''', inline=True)
        current_time = time.time()
        difference = current_time - config ['start_time']
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
:hourglass_flowing_sand: Аптайм: {visdelta(timee)}
<:slashcommand:891385007397031946> Использовано команд: {usedcommands()}
''')
        embed.add_field(name="­", value="­", inline=True)
        embed.add_field(name=self.data['system.stats.ram.title'], value=self.data['system.stats.ram'].format(round(using * 100 / psutil.virtual_memory().total),progress,natural_size(allmem),natural_size(using)), inline=True)
        embed.add_field(name=self.data['system.stats.cpu.title'], value=self.data['system.stats.cpu'].format(round(using * 100 / psutil.virtual_memory().total),psutil.cpu_count(),psutil.cpu_percent(interval=None)), inline=True)
        #embed.add_field(name='последний коммит', value=f'''
#```
#{repo.get_commits()[0].commit.message}
#```
#''', inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'команда stats | вызваал {ctx.author}', icon_url=ctx.author.avatar_url)

        await ctx.edit(embed=embed)

    @slash_command(name='devs', description='разработчики бота')
    async def devs(self, ctx):
        embed = discord.Embed(title='разработчики бота')
        for i in config['devs']:
            embed.add_field(name=i, inline=False, value=f'''
{config['devs'][i]['description']} | {config['devs'][i]['site']}
        ''')
        await ctx.send(embed=embed)


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
"""

import os
import platform
import time
from utils.utils import humanbytes
from utils.db import getpremium
import datetime
import discord
from discord.ext import commands
from yaml import Loader, load
from discord_slash import SlashCommand
from discord_slash import cog_ext
rootdir=os.path.abspath(os.path.join(os.curdir))

class info(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        if platform.system() in ["Darwin", 'Windows']:
            with open(f"{rootdir}/bot/localization/ru/commands.yml", 'r', encoding='utf8') as stream:
                self.data = load(stream, Loader=Loader)
        elif platform.system()=='Linux':
            with open("bot/localization/ru/commands.yml", 'r', encoding='utf8') as stream:
                self.data = load(stream, Loader=Loader)
    @commands.guild_only()
    @cog_ext.cog_slash(name='invite',  description='Пригласить бота')
    async def invite(self, ctx):
        full_url = self.data['info.invite.fullurl'].format(self.bot.user.id)
        low_url = self.data['info.invite.lowurl'].format(self.bot.user.id)
        embed = discord.Embed(color=0xf0a302,
                              title=self.data['info.invite.embed.title'],
                              description=f'{full_url}\n{low_url}')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.author} | {self.bot.user}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @cog_ext.cog_slash(name='server', description='Информация о сервере.', guild_ids =[761991504793174117])
    @commands.guild_only()
    async def guild(self, ctx):
        """Информация о сервере.
        """
        embed = discord.Embed(title=ctx.guild.name, colour=discord.Colour(0xd9ec))

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"Запрошено {ctx.author}", icon_url=ctx.author.avatar_url)
        if getpremium(str(ctx.guild.id)):
            embed.add_field(name="Осн. информация:", value=f":gem: | **На сервере __активен__ статус Kuzaku Premium.**\n\n:clock1: | Этот сервер создан **<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}:R>** назад\n:flag_white: | Регион сервера: **{ctx.guild.region}**", inline=False)
        else:
            embed.add_field(name="Осн. информация:", value=f"<:n4_no:701392095822479370> | **На сервере __не активен__ статус Kuzaku Premium.**\n\n:clock1: | Этот сервер создан **<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}:R>** назад\n:flag_white: | Регион сервера: **{ctx.guild.region}**", inline=False)
            
        embed.add_field(name="Доп. информация:", value=f":page_facing_up: | Макс. размер вложений **{humanbytes(ctx.guild.filesize_limit)}**\n:id: | ID: `{ctx.guild.id}`", inline=False)
        embed.add_field(name="Каналы:", value=f":hash: | Всего каналов:\n- **{len(ctx.guild.channels)}**\n:dividers: | Категорий:\n- **{len(ctx.guild.categories)}**\n:pen_ballpoint: | Текстовых:\n- **{len(ctx.guild.text_channels)}**\n:loud_sound: | Голосовых:\n- **{len(ctx.guild.voice_channels)}**", inline=True)
        embed.add_field(name="Участники:", value=f":busts_in_silhouette: | Всего участников:\n- **{len(ctx.guild.members)}**\n:interrobang: | Макс. кол-во участников:\n- **{ctx.guild.max_members}**", inline=True)


        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(info(bot))

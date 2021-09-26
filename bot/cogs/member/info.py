import os
import platform
import time
from utils.utils import humanbytes
from utils.db import getpremium
import datetime
import discord
from discord.ext import commands
from yaml import Loader, load
import dislash
from dislash import slash_command, Option, OptionType
rootdir=os.path.abspath(os.path.join(os.curdir))

class info(commands.Cog):
    global data
    data={}
    def __init__(self, bot):
        self.bot=bot
        if platform.system() in ["Darwin", 'Windows']:
            with open(f"{rootdir}/localization/ru/bot/commands.yml", 'r', encoding='utf8') as stream:
                self.data = load(stream, Loader=Loader)
        elif platform.system()=='Linux':
            with open("localization/ru/bot/commands.yml", 'r', encoding='utf8') as stream:
                self.data = load(stream, Loader=Loader)
    @commands.guild_only()
    @slash_command(name='invite',  description='invite bot', test_guilds=[808013895917633546])
    async def invite(self, ctx):
        full_url = self.data['info.invite.fullurl'].format(self.bot.user.id)
        low_url = self.data['info.invite.lowurl'].format(self.bot.user.id)
        embed = discord.Embed(color=0xf0a302,
                              title=self.data['info.invite.embed.title'],
                              description=f'{full_url}\n{low_url}')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.author} | {self.bot.user}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @dislash.cooldown(1, 5, commands.BucketType.user)
    @slash_command(name='server', description='Information about server.', test_guilds=[808013895917633546])
    @commands.guild_only()
    async def guild(self, ctx):
        await ctx.respond(type=5)
        """Информация о сервере."""
        embed = discord.Embed(title=ctx.guild.name, colour=discord.Colour(0xd9ec))

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"Запрошено {ctx.author}", icon_url=ctx.author.avatar_url)
        if getpremium(str(ctx.guild.id)):
            embed.add_field(name=self.data['info.guild.embed.name'], value=self.data['info.guild.embed.maininfo.havepremium'].format(f'<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}:R>', ctx.guild.region), inline=False)
        else:
            embed.add_field(name=self.data['info.guild.embed.name'], value=self.data['info.guild.embed.maininfo.nopremium'].format(f'<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}:R>', ctx.guild.region), inline=False)
            
        embed.add_field(name="Доп. информация:", value=f":page_facing_up: | Макс. размер вложений **{humanbytes(ctx.guild.filesize_limit)}**\n:id: | ID: `{ctx.guild.id}`", inline=False)
        embed.add_field(name="Каналы:", value=f":hash: | Всего каналов:\n- **{len(ctx.guild.channels)}**\n:dividers: | Категорий:\n- **{len(ctx.guild.categories)}**\n:pen_ballpoint: | Текстовых:\n- **{len(ctx.guild.text_channels)}**\n:loud_sound: | Голосовых:\n- **{len(ctx.guild.voice_channels)}**", inline=True)
        embed.add_field(name="Участники:", value=f":busts_in_silhouette: | Всего участников:\n- **{len(ctx.guild.members)}**\n:interrobang: | Макс. кол-во участников:\n- **{ctx.guild.max_members}**", inline=True)


        await ctx.edit(embed=embed)
    @slash_command(name='avatar', description='Show member avatar!', test_guilds=[808013895917633546], options=[
    Option('member', 'Участник, аватар которого ты хочешь посмотреть.', OptionType.USER, required=False)])
    async def avatar(self, ctx, member=None):
        async with ctx.typing:
            member = member or ctx.author
            embed=discord.Embed(title=self.data['avatar.embed.title'].format(member))
            embed.set_image(url=member.avatar_url_as(format='png'))
            await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(info(bot))

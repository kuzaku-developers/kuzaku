import discord
from discord.ext import commands
from utils import card as cards
from utils.db import *
import json
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
class economy(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    @commands.guild_only()
    @cog_ext.cog_slash(name='rank', description='Ранк', guild_ids=[761991504793174117], options=[
    create_option(
    name='участник',
    description='Участник, чей ранк ты хочешь посмотреть.',
    required=False,
    option_type=6
        )], connector={'участник':'member'})
    async def rank(self, ctx, member=None):
        if not member:
            member=ctx.author
        
        try:
            ecc=geteco(ctx.guild.id, member.id)
        except Exception as e:
            print(e)
            seteco(ctx.guild.id, member.id, 0, 1, 100)
            ecc=geteco(ctx.guild.id, member.id)
        lvl=ecc['lvl']
        nextxp=ecc['nextxp']
        xp=ecc['xp']
        card=cards.RankCard()
        await card.setBackground(url='https://images.unsplash.com/photo-1600758208050-a22f17dc5bb9?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80')#(color='#98afc1')
        await card.setTextColor(color = "#a4a4ac")
        await card.setStatus(status = member.status)
        await card.setStatusBack(color = "#4e6b7f")
        await card.setAvatar(avatar = member.avatar_url)
        await card.setAvatarBack(color = "#4e6b7f")
        await card.setName(name = member.name)
        await card.setTag(tag = member.discriminator)
        await card.setLvl(lvl = lvl)
        await card.setXp(xp = xp)
        await card.setXpToNextLvl(xp = nextxp)
        await card.setBarColor(color = "#273e55")
        await card.setBarBack(color = "#4e6b7f")
        await card.setDisplayProcents(True)
        await card.setTextStyle(path='bot/font.ttf')
        file = await card.create()
        await ctx.send(file = discord.File(fp = file, filename = "rank.png"))
            
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.channel.type != 'private':
            try:
                ecc=geteco(message.guild.id, message.author.id)
            except:
                seteco(message.guild.id, message.author.id, 0, 1, 100)
                ecc=geteco(message.guild.id, message.author.id)
            lenn=len((message.content))
            if lenn>=ecc['lvl']*10:
                lenn=ecc['lvl']
            if ecc['nextxp']<=lenn:
                seteco(message.guild.id, message.author.id, 0, ecc['lvl']+1, (ecc['lvl']+1)*100)
            else:
                seteco(message.guild.id, message.author.id, ecc['xp']+lenn, ecc['lvl'], ecc['nextxp']-lenn)
        
        
def setup(bot:commands.Bot):
    bot.add_cog(economy(bot))
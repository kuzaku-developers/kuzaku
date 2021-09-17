import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
from utils.db import *
class promocodes(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @cog_ext.cog_subcommand(base='promocodes', name='use', description='Использовать промокод', guild_ids=[761991504793174117])
    async def usepromo(self, ctx, promocode):
        await ctx.defer(hidden=True)
        existing=False
        global i
        global used_by
        for i in getpromos():
            if getpromos()[i]['promocode']==promocode:
                existing=True
                try:
                    used_by=getpromos()[i]['usedby']
                except:
                    used_by=[]  
        if not existing:
            return await ctx.send(embed=discord.Embed(title='Промокоды', description='Такого промокода не существует', hidden=True))
        else:
            try:
                if ctx.author.id in used_by:
                    return await ctx.send(embed=discord.Embed(title='Промокоды', description='Вы уже использовали данный промокод!', hidden=True))
                    
                else:
                    used_by.append(ctx.author.id)
                    addusepromo(i, used_by)
                if getpromos()[i]['uses'] !='inf' and str(getpromos()[i]['uses']) =='0':
                    return await ctx.send(embed=discord.Embed(title='Промокоды', description='Ошибка! У данного промокода не осталось использований!', hidden=True))
                prem=int(dict(getdb()['premium'])[str(ctx.author.id)]['count'])+1
            except:
                prem=1
            data = {
                'premium': 'True',
                'count': prem
            }
            db.child("db").child("premium").child(ctx.author.id).set(data)
            if getpromos()[i]['uses'] !='inf':
                setpromouses(i, int(getpromos()[i]['uses'])-1)
            await ctx.send(embed=discord.Embed(title='Промокоды', description='Успех! Промокод активирован!', hidden=True))
    @commands.is_owner()
    @cog_ext.cog_subcommand(base='promocodes', name='create', description='Создать промокод', guild_ids=[761991504793174117], options=[
    create_option(
    name='promocode',
    description='Promocode to add.',
    required=True,
    option_type=3
        ),
    create_option(
    name='uses',
    description='Max uses of promocode',
    required=False,
    option_type=4
        )
            ])
    async def createpromo(self, ctx, promocode, uses=None):
        await ctx.defer(hidden=True)
        if not uses:
            uses='inf'
        existing=False
        for i in getpromos():
            if getpromos()[i]['promocode']==promocode:
                existing=True
            uuses=getpromos()[i]['uses']
            if uuses=='inf':
                uuses='Бесконечно'
        if existing:
            embed=discord.Embed(title='Промокоды', description=f'Промокод уже существует! у него {uuses} исп.')
        else:
            addpromo(promocode, uses)
            embed=discord.Embed(title='Промокоды', description=f'Промокод создан!')

        await ctx.send(embed=embed, hidden=True)
    @commands.is_owner()
    @cog_ext.cog_subcommand(base='promocodes', name='list', description='Создать промокод', guild_ids=[761991504793174117])
    async def listpromo(self, ctx):
        await ctx.defer(hidden=True)
        embed=discord.Embed(title='Промокоды', description='Все промокоды!')
        for i in getpromos():
            uuses=getpromos()[i]['uses']
            if uuses=='inf':
                uuses='Бесконечно'
            embed.add_field(name=f'{getpromos()[i]["promocode"]}', value=f'{uuses} исп.', inline=False)

        await ctx.send(embed=embed, hidden=True)



def setup(bot:commands.Bot):
    bot.add_cog(promocodes(bot))
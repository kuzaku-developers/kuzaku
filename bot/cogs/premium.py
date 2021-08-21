import json
import os
import sys

import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import Group
from discord_slash import SlashCommand, cog_ext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (create_actionrow,
                                                   create_button,
                                                   wait_for_component)
from main import slash
from requests import post
from utils.db import *

rootdir=os.path.abspath(os.path.join(os.curdir))
sys.path.append(f'{rootdir}/utils/')
from discord.ext.commands import Command
from discord.ext.commands.cooldowns import (BucketType, Cooldown,
                                            CooldownMapping)


def get_link(ctx, botname):
    testli = 'true'
    headers = {'Authorization': f'Bearer {os.getenv("kapusta")}',
                   'Content-Type': 'application/json'}
    params = {
            "amount": {
                "amount": 2000,
                "currency": "RUB"
            },
            "expire": "2023-06-17T15:45:41.000+03:00",
            "description": f'покупка премиума в боте nuclearbot для человека {str(ctx.author)}.\ndiscord id:{str(ctx.author.id)}.',
            "projectCode": "kuzaku",
            'test': testli,
            "sender": {
                "comment": "ваш комментарий для автора бота (не обязательно)"
            },
            "custom": {
                "id": int(ctx.author.id),
                "name": str(ctx.author),
                "avatar": str(ctx.author.avatar_url),
                'member_men': str(ctx.author.mention),
                'secret': os.getenv('apisecret')
            },
        }
    req = post('https://api.capusta.space/v1/partner/payment', headers=headers, json=params)
    try:
        if json.loads(req.text)['status'] != '404':
            print(req.text)
            jsons = json.loads(req.text)
            if jsons["payUrl"]:
                return jsons["payUrl"]
            else:
                return 'что-то пошло не так! 404'
        else:
            return 'что-то пошло не так! 404'
    except:
        return 'что-то пошло не так! 404'
def cooldoown(rate, per, type=BucketType.default, premium: bool = False):
    def decorator(func):
        if isinstance(func, Command):
            func._buckets = CooldownMapping(Cooldown(rate, per, type))
        else:
            if not premium:
                func.__commands_cooldown__ = Cooldown(rate, per, type)
            else:
                func.__commands_cooldown__ = Cooldown(0, per, type)
        return func
    return decorator

class premium(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        self.check_premium.start()
    @cog_ext.cog_subcommand(base='gold', name = "buy", description='Премиум!')
    @commands.guild_only()
    @cooldoown(1, 3, commands.BucketType.user, False)
    async def gold(self, ctx:commands.Context):
        guild = self.bot.get_guild(761991504793174117)
        if guild.get_member(ctx.author.id):
            premium=guild.get_role(869122020447748137)
            if premium in guild.get_member(ctx.author.id).roles:
                embed=discord.Embed(title='Премиум', description='у вас есть премиум и вы можете его активровать! используйте /gold use')
                await ctx.send(embed=embed)
            else:
                
            
                embed=discord.Embed(title='Премиум', description='у вас нет премиума! Мы были бы признательны, если бы вы приобрели подиску и активировали бонус! Для этого нажмите на кнопку снизу! :з')
                row=create_actionrow(
                                        create_button(style=ButtonStyle.green, label="Купить"))
                await ctx.send(embed=embed,  components=[row])
                button_ctx: ComponentContext = await wait_for_component(self.bot, components=row)  
                link=get_link(ctx, self.bot.user.name)
                print(link)
                if link=='что-то пошло не так! 404':
                    await button_ctx.send(content='что-то пошло не так! 404', hidden=True)
                else:
                    await button_ctx.send(content = "Отлично. Нажми на кнопку для оплаты", hidden=True,components = [create_actionrow(
                                        create_button(style=ButtonStyle.URL, url=link, label="Оплата"))])
                    


        else:
            embed=discord.Embed(title='Премиум', description='вас нет на сервере поддержки! мы [советуем вам зайти!](https://discord.gg/tmrrdRwJCU)')
            
            await ctx.send(embed=embed)
    @cog_ext.cog_subcommand(base='gold', name='use', description='использовать премиум')
    async def use(self, ctx):
        await ctx.defer()
        if int(dict(getdb()['premium'])[str(ctx.author.id)]['count']) <= 0:
            embed=discord.Embed(title='Активация!', description='Провал! У вас больше нет серверов для активации!')
            await ctx.send(embed=embed)
        else:
            print(dict(getdb()['premium'])[str(ctx.author.id)]['count'])
            if True:
                print(dict(getdb()['premium'])['guilds'])
                for i in dict(getdb()['premium'])['guilds']:
                    if str(i) == str(ctx.guild.id):
                        await ctx.send(embed=discord.Embed(title='Активация!', description='Провал! Премиум уже активирован!'))
                        break
                else:
                    try:
                        minusoneguild(ctx.author.id)
                        setsupporter(str(ctx.guild.id), True)
                        await ctx.send(embed=discord.Embed(title='Активация!', description='Успех! Премиум активирован!'))
                    except Exception as e:
                        await ctx.send(embed=discord.Embed(title='Активация!', description='Провал! Возникла неизвестная ошибка!'))
                        print(e)
    
    @tasks.loop(minutes=10)
    async def check_premium(self):
        for i in dict(getdb()['premium']):
            if i != 'guilds' and dict(getdb()['premium'])[i]['premium']:
                try:
                    user=await self.bot.fetch_user(i)
                    guild = self.bot.get_guild(761991504793174117)
                    if user in guild.members:
                        member=guild.get_member(user.id)
                        premium=guild.get_role(869122020447748137)
                        if not premium in guild.get_member(user.id).roles:
                            await member.add_roles(premium)
                        else:
                            pass
                            
                except Exception as e:
                    print(e)
                    
                        
def setup(bot:commands.Bot):
    bot.add_cog(premium(bot))

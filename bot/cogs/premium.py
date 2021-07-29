import json
import os
import sys

import discord
from discord.ext import commands
from discord.ext.commands.core import Group
from discord_components import Button, DiscordComponents, Select, SelectOption, ButtonStyle
from requests import post
from utils.db import test

rootdir=os.path.abspath(os.path.join(os.curdir))
sys.path.append(f'{rootdir}/utils/')
from discord.ext.commands import Command
from discord.ext.commands.cooldowns import (BucketType, Cooldown,
                                            CooldownMapping)
from utils.db import test

def get_link(ctx, botname):
    testli = 'true'
    headers = {'Authorization': f'Bearer {os.getenv("kapusta")}',
                   'Content-Type': 'application/json'}
    params = {
            "amount": {
                "amount": 1000,
                "currency": "RUB"
            },
            "expire": "2023-06-17T15:45:41.000+03:00",
            "description": f'покупка премиума в боте nuclearbot для человека {str(ctx.author)}.\ndiscord id:{str(ctx.author.id)}.',
            "projectCode": "kuzaku",
            'test': testli,
            "sender": {
                "name": ctx.author.name,
                "comment": "ваш комментарий для автора бота (не обязательно)"
            },
            "custom": {
                "id": int(ctx.author.id),
                "name": str(ctx.author),
                "avatar": str(ctx.author.avatar_url),
                'member_men': str(ctx.author.mention),
                'bot_name': botname,
                'test': testli,
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

    @commands.group(name = "gold")
    @commands.guild_only()
    @cooldoown(1, 3, commands.BucketType.user, False)
    async def gold(self, ctx:commands.Context):
        guild = self.bot.get_guild(761991504793174117) # find ID by right clicking on server icon and choosing "copy id" at the bottom
        if guild.get_member(ctx.author.id):
            silver=guild.get_role(869122020447748137)
            gold=guild.get_role(869122020447748137)
            diamond=guild.get_role(869122020447748137)
            ultimate=guild.get_role(869122020447748137)
            if silver in guild.get_member(ctx.author.id).roles or gold in guild.get_member(ctx.author.id).roles or diamond in guild.get_member(ctx.author.id).roles or ultimate in guild.get_member(ctx.author.id).roles:
                embed=discord.Embed(title='Премиум', description='у вас есть премиум и вы можете его активровать! используйте k.gold use')
                await ctx.reply(embed=embed)
            else:
                
            
                embed=discord.Embed(title='Премиум', description='у вас нет премиума! Мы были бы признательны, если бы вы приобрели подиску и активировали бонус! Для этого напишите k.gold buy или нажмите на кнопку снизу! :з')
                await ctx.send(embed=embed, components = [

            Button(label = "Купить")

        ])
                interaction = await self.bot.wait_for("button_click", check = lambda i: i.component.label.startswith("Купить"))
                link=get_link(ctx, self.bot.user.name)
                print(link)
                if link=='что-то пошло не так! 404':
                    await interaction.respond(content='что-то пошло не так! 404')
                else:
                    await interaction.respond(content = "Отлично. Нажми на кнопку для оплаты", components = [

            Button(style=ButtonStyle.URL, label = "Оплата", url=link)

        ])

        else:
            embed=discord.Embed(title='Премиум', description='вас нет на сервере поддержки! мы [советуем вам зайти!](https://discord.gg/tmrrdRwJCU)')
            
            await ctx.reply(embed=embed)

    
def setup(bot:commands.Bot):
    bot.add_cog(premium(bot))
import json
import os
import sys

import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import Group
from discord import Webhook, RequestsWebhookAdapter
from dislash import *
import dislash

from requests import post
from utils.db import *

rootdir=os.path.abspath(os.path.join(os.curdir))
sys.path.append(f'{rootdir}/utils/')
from discord.ext.commands import Command
from discord.ext.commands.cooldowns import (BucketType, Cooldown,
                                            CooldownMapping)


def get_link(ctx):
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
        try:
            self.check_premium.start()
        except  RuntimeError: ...
    @slash_command(name='premium', description='Premium')
    async def premium_cmd(self, ctx):
        pass
    @premium_cmd.sub_command(name = "buy", description='Премиум!')
    @commands.guild_only()
    @cooldoown(1, 3, commands.BucketType.user, False)
    async def prem(self, ctx:commands.Context):
        await ctx.respond(type=5)
        guild = self.bot.get_guild(761991504793174117)
        if guild.get_member(ctx.author.id):
            premium=guild.get_role(869122020447748137)
            if premium in guild.get_member(ctx.author.id).roles:
                embed=discord.Embed(title='Премиум', description='у вас есть премиум и вы можете его активровать! используйте /gold use')
                await ctx.edit(embed=embed)
            else:
                
            
                embed=discord.Embed(title='Премиум', description='у вас нет премиума! Мы были бы признательны, если бы вы приобрели подиску и активировали бонус! Для этого нажмите на кнопку снизу! :з')
                row=row_of_buttons = ActionRow(
                Button(
                style=ButtonStyle.green,
                label="Купить",
                custom_id="buy"
                )
                )
                def check(inter):
                    return inter.author == ctx.author                      
                msg=await ctx.edit(embed=embed,  components=[row])
                inter = await msg.wait_for_button_click(check=check)  
                link=get_link(ctx)
                if link=='что-то пошло не так! 404':
                    await inter.reply(content='что-то пошло не так! 404', ephemeral=True)
                else:
                    await inter.reply(content = "Отлично. Нажми на кнопку для оплаты", ephemeral=True,components = [ActionRow(
                Button(
                style=ButtonStyle.url,
                label="Оплата",
                custom_id="buylink",
                url=get_link(ctx)
                )
                )])
                    


        else:
            embed=discord.Embed(title='Премиум', description='вас нет на сервере поддержки! мы [советуем вам зайти!](https://discord.gg/tmrrdRwJCU)')
            
            await ctx.edit(embed=embed)
    @premium_cmd.sub_command(name='use', description='использовать премиум')
    async def use(self, ctx):
        await ctx.respond(type=5)
        try:
            if int(dict(getdb()['premium'])[str(ctx.author.id)]['count']) <= 0:
                embed=discord.Embed(title='Активация!', description='Провал! У вас больше нет серверов для активации!')
                await ctx.edit(embed=embed)
            else:
                if True:

                    for i in dict(getdb()['premium'])['guilds']:
                        if str(i) == str(ctx.guild.id):
                            await ctx.edit(embed=discord.Embed(title='Активация!', description='Провал! Премиум уже активирован!'))
                            break
                    else:
                        try:
                            minusoneguild(ctx.author.id)
                            setsupporter(str(ctx.guild.id), True)
                            await ctx.edit(embed=discord.Embed(title='Активация!', description='Успех! Премиум активирован!'))
                        except Exception as e:
                            await ctx.edit(embed=discord.Embed(title='Активация!', description='Провал! Возникла неизвестная ошибка!'))
        except:
            embed=discord.Embed(title='Активация!', description='Провал! У вас нет премиума!')
            await ctx.edit(embed=embed)
    @commands.is_owner()
    @slash_command(name='premiumgive', description='Выдать премиум', guild_ids=[761991504793174117], options=[
    Option("user", "Enter the user", OptionType.USER, required=True)])
    async def give(self, ctx, user):
        await ctx.respond(type=5)
        data = {
            'premium': 'True',
            'count': '3'
        }
        db.child("db").child("premium").child(user.id).set(data)
        # Webhook URL for your Discord channel.
        WEBHOOK_URL = os.getenv('webhook')
        embed=discord.Embed(title='ого, купили премиум!',description=f'премиум купил {user}!\nнаше уважение, премим уже выдан для {user.mention}!')
        embed.set_footer(text='kuzaku', icon_url=self.bot.user.avatar_url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        # Initialize the webhook class and attaches data.
        webhook=Webhook.from_url(WEBHOOK_URL,adapter=RequestsWebhookAdapter())
        webhook.send(embed=embed, username='покупка премиума', avatar_url=user.avatar_url)
        await ctx.edit(f'Премиум успешно выдан для {user.mention}!')
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
                    ...
                    
                        
def setup(bot:commands.Bot):
    bot.add_cog(premium(bot))

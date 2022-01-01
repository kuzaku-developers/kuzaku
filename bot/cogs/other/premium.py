import json
import os
import sys
import aiohttp
import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands.core import Group
from disnake import Webhook

from requests import post
from utils.db import *

rootdir = os.path.abspath(os.path.join(os.curdir))
sys.path.append(f"{rootdir}/utils/")
from disnake.ext.commands.cooldowns import BucketType, Cooldown, CooldownMapping


class PremView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        # we need to quote the query string to make a valid url. disnake will raise an error if it isn't valid.
        url = "https://docs.kuzaku.ml/additional-info/kuzaku-premium/"

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(disnake.ui.Button(label="Документация", url=url))


class premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.check_premium.start()
        except RuntimeError:
            ...

    @commands.slash_command(name="premium", description="Premium")
    async def premium_cmd(self, ctx):
        pass

    @premium_cmd.sub_command(name="buy", description="Премиум!")
    @commands.guild_only()
    async def prem(self, ctx):
        await ctx.response.defer()
        guild = self.bot.get_guild(761991504793174117)
        try:
            member = await guild.fetch_member(ctx.author.id)
        except:
            embed = disnake.Embed(
                title="Премиум",
                description="вас нет на сервере поддержки! мы [советуем вам зайти!](https://discord.gg/tmrrdRwJCU)",
            )

            return await ctx.send(embed=embed)
        if await guild.fetch_member(ctx.author.id):
            premium = guild.get_role(869883325265874975)
            if premium in (await guild.fetch_member(ctx.author.id)).roles:
                embed = disnake.Embed(
                    title="Премиум",
                    description="у вас есть премиум и вы можете его активровать! используйте /gold use",
                )
                await ctx.send(embed=embed)
            else:

                embed = disnake.Embed(
                    title="Премиум",
                    description="у вас нет премиума! Мы были бы признательны, если бы вы приобрели подиску и активировали бонус! Для этого посетите документацию :з",
                )

                await ctx.send(embed=embed, view=PremView())

        else:
            embed = disnake.Embed(
                title="Премиум",
                description="вас нет на сервере поддержки! мы [советуем вам зайти!](https://discord.gg/tmrrdRwJCU)",
            )

            await ctx.send(embed=embed)

    @premium_cmd.sub_command(name="use", description="использовать премиум")
    async def use(self, ctx):
        await ctx.response.defer()
        try:
            if int(dict(getdb()["premium"])[str(ctx.author.id)]["count"]) <= 0:
                embed = disnake.Embed(
                    title="Активация!",
                    description="Провал! У вас больше нет серверов для активации!",
                )
                await ctx.send(embed=embed)
            else:
                if True:

                    for i in dict(getdb()["premium"])["guilds"]:
                        if str(i) == str(ctx.guild.id):
                            await ctx.send(
                                embed=disnake.Embed(
                                    title="Активация!",
                                    description="Провал! Премиум уже активирован!",
                                )
                            )
                            break
                    else:
                        try:
                            minusoneguild(ctx.author.id)
                            setsupporter(str(ctx.guild.id), True)
                            await ctx.send(
                                embed=disnake.Embed(
                                    title="Активация!",
                                    description="Успех! Премиум активирован!",
                                )
                            )
                        except Exception as e:
                            await ctx.send(
                                embed=disnake.Embed(
                                    title="Активация!",
                                    description="Провал! Возникла неизвестная ошибка!",
                                )
                            )
        except:
            embed = disnake.Embed(
                title="Активация!", description="Провал! У вас нет премиума!"
            )
            await ctx.send(embed=embed)

    @commands.is_owner()
    @premium_cmd.sub_command(
        name="give",
        description="Выдать премиум",
    )
    async def give(self, ctx, user: disnake.User):
        await ctx.response.defer()
        data = {"premium": "True", "count": "3"}
        db.child("db").child("premium").child(user.id).set(data)
        # Webhook URL for your disnake channel.
        WEBHOOK_URL = os.getenv("webhook")
        embed = disnake.Embed(
            title="ого, купили премиум!",
            description=f"премиум купил {user}!\nнаше уважение, премим уже выдан для {user.mention}!",
        )
        embed.set_footer(text="kuzaku", icon_url=self.bot.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        # Initialize the webhook class and attaches data.
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(WEBHOOK_URL, session=session)
            await webhook.send(
                embed=embed, username="покупка премиума", avatar_url=user.avatar.url
            )
        await ctx.send(
            content=f"Премиум успешно выдан для {user.mention}!"
        )

    @tasks.loop(minutes=10)
    async def check_premium(self):
        guild = self.bot.get_guild(761991504793174117)
        premium1 = guild.get_role(899584421479477268)
        premium2 = guild.get_role(911564619557007380)
        premiumrole = guild.get_role(869883325265874975)
        for user in guild.members:
            # print((await guild.fetch_member(user.id)).roles)
            if (
                premium1 in (await guild.fetch_member(user.id)).roles
                or premium2 in ((await guild.fetch_member(user.id))).roles
            ):
                if not premiumrole in (await guild.fetch_member(user.id)).roles:
                    await (await guild.fetch_member(user.id)).add_roles(premiumrole)
                for i in dict(getdb()["premium"]):
                    if i == "guilds":
                        continue
                    # print(i)
                    if str(dict(getdb()["premium"])[i]["premium"]) == "True":
                        pass
                    else:
                        if premium1 in (await guild.fetch_member(user.id)).roles:
                            setpremium(user.id, True, 2)
                        elif premium2 in (await guild.fetch_member(user.id)).roles:
                            setpremium(user.id, True, 5)
                if premium1 in (await guild.fetch_member(user.id)).roles:
                    setpremium(user.id, True, 2)
                elif premium2 in (await guild.fetch_member(user.id)).roles:
                    setpremium(user.id, True, 5)
                continue
            for i in dict(getdb()["premium"]):
                try:

                    if await guild.fetch_member(i):
                        # print(f"{i} in guild")
                        if (
                            premium1 not in (await guild.fetch_member(i)).roles
                            and premium2 not in (await guild.fetch_member(i)).roles
                        ):
                            # print("YES")
                            if (
                                i != "guilds"
                                and str(dict(getdb()["premium"])[i]["premium"])
                                == "True"
                            ):
                                setpremium(i, False, 0)
                                if premiumrole in (await guild.fetch_member(i)).roles:
                                    await (await guild.fetch_member(i)).remove_roles(
                                        premiumrole
                                    )
                except:
                    pass


def setup(bot):
    bot.add_cog(premium(bot))

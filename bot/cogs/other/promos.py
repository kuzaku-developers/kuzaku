import disnake
from disnake.ext import commands
from utils.db import *


class promocodes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="promocodes", description="promocodes!")
    async def promocmd(self, ctx):
        pass

    @promocmd.sub_command(
        name="use",
        description="Использовать промокод",
    )
    async def usepromo(self, ctx, promocode):
        await ctx.response.defer(ephemeral=True)
        existing = False
        global i
        global used_by
        for i in getpromos():
            if getpromos()[i]["promocode"] == promocode:
                existing = True
                try:
                    used_by = getpromos()[i]["usedby"]
                except:
                    used_by = []
        if not existing:
            return await ctx.edit_original_mesage(
                embed=disnake.Embed(
                    title="Промокоды",
                    description="Такого промокода не существует",
                )
            )
        else:
            try:
                if ctx.author.id in used_by:
                    return await ctx.send(
                        embed=disnake.Embed(
                            title="Промокоды",
                            description="Вы уже использовали данный промокод!",
                        )
                    )

                else:
                    used_by.append(ctx.author.id)
                    addusepromo(i, used_by)
                if (
                    getpromos()[i]["uses"] != "inf"
                    and str(getpromos()[i]["uses"]) == "0"
                ):
                    return await ctx.send(
                        embed=disnake.Embed(
                            title="Промокоды",
                            description="Ошибка! У данного промокода не осталось использований!",
                        )
                    )
                prem = int(dict(getdb()["premium"])[str(ctx.author.id)]["count"]) + 1
            except:
                prem = 1
            data = {"premium": "True", "count": prem}
            db.child("db").child("premium").child(ctx.author.id).set(data)
            if getpromos()[i]["uses"] != "inf":
                setpromouses(i, int(getpromos()[i]["uses"]) - 1)
            await ctx.send(
                embed=disnake.Embed(
                    title="Промокоды",
                    description="Успех! Промокод активирован!",
                )
            )

    @commands.is_owner()
    @promocmd.sub_command(
        name="create",
        description="Создать промокод",
    )
    async def createpromo(self, ctx, promocode: str, uses: int = None):
        await ctx.response.defer(ephemeral=True)
        if not uses:
            uses = "inf"
        existing = False
        for i in getpromos():
            if getpromos()[i]["promocode"] == promocode:
                existing = True
            uuses = getpromos()[i]["uses"]
            if uuses == "inf":
                uuses = "Бесконечно"
        if existing:
            embed = disnake.Embed(
                title="Промокоды",
                description=f"Промокод уже существует! у него {uuses} исп.",
            )
        else:
            addpromo(promocode, uses)
            embed = disnake.Embed(title="Промокоды", description=f"Промокод создан!")

        await ctx.send(embed=embed)

    @commands.is_owner()
    @promocmd.sub_command(
        name="list",
        description="Создать промокод",
    )
    async def listpromo(self, ctx):
        await ctx.response.defer(ephemeral=True)
        embed = disnake.Embed(title="Промокоды", description="Все промокоды!")
        for i in getpromos():
            uuses = getpromos()[i]["uses"]
            if uuses == "inf":
                uuses = "Бесконечно"
            embed.add_field(
                name=f'{getpromos()[i]["promocode"]}',
                value=f"{uuses} исп.",
                inline=False,
            )

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(promocodes(bot))

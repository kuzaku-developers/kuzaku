import disnake
from disnake.ext import commands
from utils import card as cards
from utils.db import *
import json


class economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.slash_command(
        name="rank",
        description="Ранк",
    )
    async def rank(self, ctx, member: disnake.Member = None):
        await ctx.response.defer()
        if not get_config(ctx.guild.id)["eco_enabled"] == "true":
            return await ctx.edit_original_message(
                content="Извините, но на сервере выключена система рейтинга!"
            )
        if not member:
            member = ctx.author

        try:
            ecc = geteco(ctx.guild.id, member.id)
        except Exception as e:
            seteco(ctx.guild.id, member.id, 0, 1, 100)
            ecc = geteco(ctx.guild.id, member.id)
        lvl = ecc["lvl"]
        nextxp = ecc["nextxp"]
        xp = ecc["xp"]
        card = cards.RankCard()
        await card.setBackground(
            url="https://images.unsplash.com/photo-1600758208050-a22f17dc5bb9?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80"
        )  # (color='#98afc1')
        await card.setTextColor(color="#a4a4ac")
        await card.setStatus(status=member.status)
        await card.setStatusBack(color="#4e6b7f")
        await card.setAvatar(avatar=member.avatar.url)
        await card.setAvatarBack(color="#4e6b7f")
        await card.setName(name=member.name)
        await card.setTag(tag=member.discriminator)
        await card.setLvl(lvl=lvl)
        await card.setXp(xp=xp)
        await card.setXpToNextLvl(xp=nextxp)
        await card.setBarColor(color="#273e55")
        await card.setBarBack(color="#4e6b7f")
        await card.setDisplayProcents(True)
        await card.setTextStyle(path="bot/font.ttf")
        file = await card.create()
        await ctx.edit_original_message(file=disnake.File(fp=file, filename="rank.png"))

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.type != "private" and message.guild:
            try:
                if not get_config(message.guild.id)["eco_enabled"] == "true":
                    return
                ecc = geteco(message.guild.id, message.author.id)
            except:
                seteco(message.guild.id, message.author.id, 0, 1, 100)
                ecc = geteco(message.guild.id, message.author.id)
            if ecc["xp"] >= ecc["nextxp"] - 1:
                seteco(
                    message.guild.id,
                    message.author.id,
                    0,
                    ecc["lvl"] + 1,
                    (ecc["lvl"] + 1) * 100,
                )
            else:
                seteco(
                    message.guild.id,
                    message.author.id,
                    ecc["xp"] + int(get_config(message.guild.id)["xppermsg"]),
                    ecc["lvl"],
                    ecc["nextxp"],
                )


def setup(bot: commands.Bot):
    bot.add_cog(economy(bot))

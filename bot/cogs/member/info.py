import os
import platform
import time
from utils.paginator import Paginator
from utils.utils import humanbytes
import aiohttp
from utils.db import getpremium
import datetime
import disnake
from disnake import OptionType
from disnake.ext import commands
from yaml import Loader, load


rootdir = os.path.abspath(os.path.join(os.curdir))


class info(commands.Cog):
    global data
    data = {}

    def __init__(self, bot):
        self.bot = bot
        if platform.system() in ["Darwin", "Windows"]:
            with open(
                f"{rootdir}/localization/ru/bot/commands.yml", "r", encoding="utf8"
            ) as stream:
                self.data = load(stream, Loader=Loader)
        elif platform.system() == "Linux":
            with open(
                "localization/ru/bot/commands.yml", "r", encoding="utf8"
            ) as stream:
                self.data = load(stream, Loader=Loader)

    @commands.guild_only()
    @commands.slash_command(name="invite", description="invite bot")
    async def invite(self, ctx):
        full_url = self.data["info.invite.fullurl"].format(self.bot.user.id)
        low_url = self.data["info.invite.lowurl"].format(self.bot.user.id)
        embed = disnake.Embed(
            color=0xF0A302,
            title=self.data["info.invite.embed.title"],
            description=f"{full_url}\n{low_url}",
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(
            text=f"{ctx.author} | {self.bot.user}", icon_url=ctx.author.avatar.url
        )
        await ctx.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.slash_command(
        name="server",
        description="Information about server.",
    )
    @commands.guild_only()
    async def guild(self, ctx):
        await ctx.response.defer()
        """Информация о сервере."""
        embed = disnake.Embed(title=ctx.guild.name, colour=disnake.Colour(0xD9EC))

        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Запрошено {ctx.author}", icon_url=ctx.author.avatar.url)
        if getpremium(str(ctx.guild.id)):
            embed.add_field(
                name=self.data["info.guild.embed.name"],
                value=self.data["info.guild.embed.maininfo.havepremium"].format(
                    f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}:R>",
                    ctx.guild.region,
                ),
                inline=False,
            )
        else:
            embed.add_field(
                name=self.data["info.guild.embed.name"],
                value=self.data["info.guild.embed.maininfo.nopremium"].format(
                    f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}:R>",
                    ctx.guild.region,
                ),
                inline=False,
            )

        embed.add_field(
            name="Доп. информация:",
            value=f":page_facing_up: | Макс. размер вложений **{humanbytes(ctx.guild.filesize_limit)}**\n:id: | ID: `{ctx.guild.id}`",
            inline=False,
        )
        embed.add_field(
            name="Каналы:",
            value=f":hash: | Всего каналов:\n- **{len(ctx.guild.channels)}**\n:dividers: | Категорий:\n- **{len(ctx.guild.categories)}**\n:pen_ballpoint: | Текстовых:\n- **{len(ctx.guild.text_channels)}**\n:loud_sound: | Голосовых:\n- **{len(ctx.guild.voice_channels)}**",
            inline=True,
        )
        embed.add_field(
            name="Участники:",
            value=f":busts_in_silhouette: | Всего участников:\n- **{len(ctx.guild.members)}**\n:interrobang: | Макс. кол-во участников:\n- **{ctx.guild.max_members}**",
            inline=True,
        )

        await ctx.edit_original_message(embed=embed)

    @commands.slash_command(name="avatar", description="Show member avatar!")
    async def avatar(self, ctx, member: disnake.Member = None):
        await ctx.response.defer()
        member = member or ctx.author
        embed = disnake.Embed(title=self.data["avatar.embed.title"].format(member))
        embed.set_image(url=member.avatar.url)
        await ctx.edit_original_message(embed=embed)

    @commands.slash_command(name="help", description="WHAT THIS COMMAND DO?!")
    async def thelp(self, ctx, *, command: str = None):
        """help.description"""
        await ctx.response.defer()
        embs = []
        if command is None:
            __slots__ = []

            for cog in self.bot.cogs:
                __slots__.append(self.bot.get_cog(cog))

            for cog in __slots__:
                cog_commands = len(
                    [
                        x
                        for x in self.bot.slash_commands
                        if x.cog_name == cog.qualified_name
                    ]
                )
                if cog_commands == 0:
                    pass
                else:
                    embs.append(
                        disnake.Embed(
                            title=cog.qualified_name,
                            description=", ".join(
                                [
                                    f"`{x.name}`"
                                    for x in self.bot.slash_commands
                                    if x.cog_name == cog.qualified_name
                                ]
                            ),
                        )
                    )

            message = await ctx.edit_original_message(embed=embs[0])

            pages = Paginator(message, embs, ctx.author, footer=True)
            return await pages.start()
        else:
            entity = self.bot.get_slash_command(command)
            try:
                desc = entity.description
            except:
                desc = "описание отсутствует"
            if entity is None:
                clean = command.replace("@", "@\u200b")
                embed = disnake.Embed(
                    title="Помощь по командам",  # YML дата
                    description="data['help.nofound']".format(clean),
                )
                embed.set_footer(
                    text=f"{self.bot.user.name} | {len(self.bot.slash_commands)}"
                )
            else:
                subcommands = []
                for x in entity.body.options:
                    if x.type == OptionType.sub_command:
                        subcommands.append(x)
                embed = disnake.Embed(title="Помощь по командам")
                embed.add_field(
                    name=f'/{entity.name} {", ".join([x.name for x in entity.body.options if x.type != OptionType.sub_command])}',
                    value=desc,
                    inline=False,
                )
                if not len(subcommands) == 0:
                    SCmd = [
                        x.name
                        for x in entity.options
                        if x.type == OptionType.sub_command
                    ]
                    scmd2 = ""
                    try:
                        for i in range(len(SCmd)):
                            scmd2 = (
                                scmd2
                                + f'{SCmd[i]} - data[f"subcommand.{entity.name}.{SCmd[i]}.description"]\n'
                            )
                    except:
                        for i in range(len(SCmd)):
                            scmd2 = scmd2 + f"{SCmd[i]} - описание отсутствует\n"
                    embed.add_field(name="data['help.subcommands']", value=scmd2)
                embed.set_footer(
                    text=f"{self.bot.user.name} | {len(self.bot.commands)}"
                )

        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(
            text="data['help.footer']".format(
                "/", self.bot.user.name, len(self.bot.commands)
            )
        )

        await ctx.edit_original_message(embed=embed)  # самая легкая команда хелп


def setup(bot):
    bot.add_cog(info(bot))

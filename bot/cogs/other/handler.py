import sys
import traceback
import random
from disnake.ext import commands
import disnake
import disnake
import time
from utils.time import visdelta

listen = commands.Cog.listener


class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @listen()
    async def on_command_error(self, ctx, error):
        rep_guild = disnake.utils.get(self.bot.guilds, id=761991504793174117)
        rep_channel = disnake.utils.get(rep_guild.channels, id=868788281528160266)
        dev = disnake.utils.get(self.bot.users, id=704560097610825828)
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, "on_error"):
            return

        await self.error_checker(ctx, error, rep_guild, rep_channel, dev)

    @listen()
    async def on_slash_command_error(self, ctx, err):
        rep_guild = disnake.utils.get(self.bot.guilds, id=761991504793174117)
        rep_channel = disnake.utils.get(rep_guild.channels, id=868788281528160266)
        dev = disnake.utils.get(self.bot.users, id=704560097610825828)
        await self.error_checker(ctx, err, rep_guild, rep_channel, dev)

    @listen()
    async def on_component_callback_error(self, ctx, err):
        rep_guild = disnake.utils.get(self.bot.guilds, id=761991504793174117)
        rep_channel = disnake.utils.get(rep_guild.channels, id=868788281528160266)
        dev = disnake.utils.get(self.bot.users, id=704560097610825828)
        await self.error_checker(ctx, err, rep_guild, rep_channel, dev)

    @staticmethod
    async def error_checker(ctx, error, rep_guild, rep_channel, dev):
        ignored = (commands.NotOwner, disnake.NotFound, commands.CommandNotFound)
        error = getattr(error, "original", error)
        embed = disnake.Embed(color=0xFF0000)
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = disnake.Embed(color=0xFF0000).set_author(
                name=f"Указаны не все аргументы для {ctx.command}.",
                icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
            )
            try:
                await ctx.response.send_message(embed=embed)
            except disnake.errors.InteractionResponded:
                await ctx.send(embed=embed)

        elif isinstance(error, commands.DisabledCommand):
            embed = disnake.Embed(color=0xFF0000).set_author(
                name=f"Команда {ctx.command} отключена.",
                icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
            )
            try:
                return await ctx.response.send_message(embed=embed)
            except disnake.errors.InteractionResponded:
                return await ctx.send(embed=embed)

        elif isinstance(error, disnake.errors.Forbidden):
            embed = disnake.Embed(color=0xFF0000).set_author(
                name=f"У меня недостаточно прав.",
                icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
            )

            try:
                return await ctx.response.send_message(embed=embed)
            except disnake.errors.InteractionResponded:
                return await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            if not isinstance(error, commands.errors.NSFWChannelRequired):
                if isinstance(error, disnake.ext.commands.errors.MissingPermissions):
                    embed = disnake.Embed(color=0xFF0000,).set_author(
                        name=f"у вас нет прав",
                        icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
                    )
                    try:
                        return await ctx.response.send_message(embed=embed)
                    except disnake.errors.InteractionResponded:
                        return await ctx.send(embed=embed)

                embed = disnake.Embed(color=0xFF0000).set_author(
                    name="У вас нет прав.",
                    icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
                )
            else:
                embed = disnake.Embed(color=0xFF0000).set_author(
                    name=f"Эту команду нельзя выполнить здесь. (Может быть, в NSFW канале)",
                    icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
                )
            try:
                return await ctx.response.send_message(embed=embed)
            except disnake.errors.InteractionResponded:
                return await ctx.send(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = disnake.Embed(color=0xFF0000).set_author(
                    name=f"Команда {ctx.command} не может быть выполнена в ЛС.",
                    icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
                )
                try:
                    await ctx.response.send_message(embed=embed)
                except disnake.errors.InteractionResponded:
                    await ctx.send(embed=embed)
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            embed = disnake.Embed(color=0xFF0000).set_author(
                name=f"Получен неверный аргумент для {ctx.command}.",
                icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
            )
            try:
                await ctx.response.send_message(embed=embed)
            except disnake.errors.InteractionResponded:
                await ctx.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = disnake.Embed(color=0xFF0000).set_author(
                name=f"Команду {ctx.data.name} нельзя выполнять так часто. Подождите {visdelta(int(error.retry_after))}.",
                icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
            )
            try:
                await ctx.response.send_message(embed=embed)
            except disnake.errors.InteractionResponded:
                await ctx.send(embed=embed)

        # Если ничего не подходит
        embed = disnake.Embed(
            color=0xF56415,
            title="**Произошла ошибка!**",
            description=f"```python\n{type(error).__name__}: {error}```\n```python\n{type(error).__name__}:\n{type(error).__doc__}```",
        )
        embed.add_field(name="**Участник**", value=f"{ctx.author} | {ctx.author.id}")
        embed.add_field(name="**Сервер**", value=f"{ctx.guild.name} | {ctx.guild.id}")
        embed.add_field(
            name="**Время**",
            value=f"<t:{int(time.time())}> (<t:{int(time.time())}:R>).",
        )
        embed.add_field(
            name="**Команда**",
            value=f"`/{ctx.data.name} {' '.join([f'{i.name}: {i.value}' for i in ctx.data.options])}`",
        )
        embed.set_author(
            name="Обработка исключения.",
            icon_url="http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png",
        )
        try:
            tb = traceback.format_exc()
            print(tb)
            await rep_channel.send(embed=embed)

        except:
            await dev.send(embed=embed)
        try:
            errors_msgs = [
                "ОшИбКа СтОп 0000",
                "Че это? Ошибка...",
                "What a hell...",
                "BAN - BANana",
                "Я не хочу умирать...",
            ]
            embed = disnake.Embed(
                title="**Произошла неизвестная ошибка!**",
                description=f"Ошибка отправлена разработчикам. Используйте `/help {ctx.data.name}` Для просмотра справки по команде!",
            )
            embed.set_author(
                name=f"Ошибка: {error.__class__.__name__}.",
                icon_url=ctx.author.avatar.url
                or "https://cdn.discordapp.com/embed/avatars/0.png",
            )
            embed.set_footer(text=random.choice(errors_msgs))
            await ctx.response.send_message(embed=embed)
        except disnake.errors.InteractionResponded:
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(EventCog(bot))


# Если вы это читаете, то вы подтверждаете то что вы не имеете права критиковать этот говно-код за его убогость и нечитаемость.
# Автор кода придерживается принципа пофиг-как, главное чтоб работало. А теперь, молитва!

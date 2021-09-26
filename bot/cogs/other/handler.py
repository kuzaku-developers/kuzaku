import sys
import traceback
from discord.ext import commands
import discord
from dislash import slash_command, Option, OptionType
import dislash
from utils.time import visdelta
listen = commands.Cog.listener


class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @listen()
    async def on_command_error(self, ctx, error):
        rep_guild = discord.utils.get(self.bot.guilds, id=761991504793174117)
        rep_channel = discord.utils.get(rep_guild.channels, id=868788281528160266)
        dev=discord.utils.get(self.bot.users, id=704560097610825828)
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return


        await self.error_checker(ctx, error, rep_guild, rep_channel, dev)


    @listen()
    async def on_slash_command_error(self, ctx, err):
        rep_guild = discord.utils.get(self.bot.guilds, id=761991504793174117)
        rep_channel = discord.utils.get(rep_guild.channels, id=868788281528160266)
        dev=discord.utils.get(self.bot.users, id=704560097610825828)
        await self.error_checker(ctx, err, rep_guild, rep_channel, dev)

    @listen()
    async def on_component_callback_error(self, ctx, err):
        rep_guild = discord.utils.get(self.bot.guilds, id=761991504793174117)
        rep_channel = discord.utils.get(rep_guild.channels, id=868788281528160266)
        dev=discord.utils.get(self.bot.users, id=704560097610825828)
        await self.error_checker(ctx, err, rep_guild, rep_channel, dev)


    @staticmethod
    async def error_checker(ctx, error, rep_guild, rep_channel, dev):
        ignored = (commands.NotOwner, discord.NotFound, commands.CommandNotFound)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'Указаны не все аргументы для {ctx.command}.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            await ctx.send(embed=embed)

        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'Команда {ctx.command} отключена.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)

        elif isinstance(error, discord.errors.Forbidden):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'У меня недостаточно прав.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            if not isinstance(error, commands.errors.NSFWChannelRequired):
                if isinstance(error, discord.ext.commands.errors.MissingPermissions):
                    embed = discord.Embed(color=0xFF0000, ).set_author(
                        name=f'у тебя нет прав',
                        icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
                    return await ctx.send(embed=embed)
                
                embed = discord.Embed(color=0xFF0000).set_author(
                    name='У вас нет прав.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            else:
                embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Эту команду нельзя выполнить здесь. (Может быть, в NSFW канале)',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Команда {ctx.command} не может быть выполнена в ЛС.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
                return await ctx.send(embed=embed)
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'Получен неверный аргумент для {ctx.command}.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            await ctx.send(embed=embed)


        elif isinstance(error, dislash.CommandOnCooldown):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'Команду {ctx.data.name} нельзя выполнять так часто. Подождите {visdelta(int(error.retry_after))}.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
            return await ctx.send(embed=embed)

        # Если ничего не подходит
        embed = discord.Embed(
            color=0xF56415,
            title='ErrorHandler обнаружил ошибку!',
            description=f'Вызвано участником: {ctx.author}\nКоманда: {ctx.data.name}\nПодробности ошибки: ```python\n{type(error).__name__}: {error}```\n```python\n{type(error).__name__}:\n{type(error).__doc__}```'
        )
        embed.set_author(
            name='Обработка исключения.',
            icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326489locked.png')
        try:
            await rep_channel.send(embed=embed)

        except:
            await dev.send(embed=embed)

        if ctx.author.id in [704560097610825828]:
            await ctx.reply(f'{ctx.author.mention}, у меня произошла проблема.')
        else:
            await ctx.reply('произошла ошибка! Она уже отправлена разработчикам!')


def setup(bot):
    bot.add_cog(EventCog(bot))
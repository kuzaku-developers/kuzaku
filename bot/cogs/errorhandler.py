import platform
import os
import discord
from discord.ext import commands
from yaml import load, Loader

rootdir=os.path.abspath(os.path.join(os.curdir))
class errorhandler(commands.Cog):
    """Модуль обработки и оповещения об исключениях."""

    def __init__(self, bot):
        self.bot = bot
        if platform.system() in ["Darwin", 'Windows']:
            with open(f"{rootdir}/bot/localization/ru/commands.yml", 'r') as stream:
                self.data = load(stream, Loader=Loader)
        elif platform.system()=='Linux':
            with open("bot/localization/ru/commands.yml", 'r') as stream:
                self.data = load(stream, Loader=Loader)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.NotOwner, discord.NotFound, commands.CommandNotFound)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'Указаны не все аргументы для {ctx.prefix}{ctx.command}.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
            await ctx.reply(embed=embed)
            return await ctx.invoke(self.bot.get_command("help"), command=str(ctx.command))

        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'Команда {ctx.prefix}{ctx.command} отключена.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
            return await ctx.reply(embed=embed)

        elif isinstance(error, discord.errors.Forbidden):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'У меня недостаточно прав.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
            return await ctx.reply(embed=embed)

        elif isinstance(error, commands.CheckFailure):
            print(error.__module__)
            if not isinstance(error, commands.errors.NSFWChannelRequired):
                if isinstance(error, discord.ext.commands.errors.MissingPermissions):
                    embed = discord.Embed(color=0xFF0000, ).set_author(
                        name=f'у тебя нет прав',
                        icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
                    return await ctx.reply(embed=embed)
                if isinstance(error, discord.ext.commands.errors.CheckFailure):
                    embed = discord.Embed(color=0xFF0000, ).set_author(
                        name=f'добрый день, {ctx.author.name}, пошел нафиг ты забанен',
                        icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
                    return await ctx.reply(embed=embed)
                embed = discord.Embed(color=0xFF0000).set_author(
                    name='У вас нет прав.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
            else:
                embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Эту команду нельзя выполнить здесь. (Может быть, в NSFW канале)',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
            return await ctx.reply(embed=embed)
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                embed = discord.Embed(color=0xFF0000).set_author(
                    name=f'Команда {ctx.prefix}{ctx.command} не может быть выполнена в ЛС.',
                    icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
                return await ctx.send(embed=embed)
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'Получен неверный аргумент для {ctx.prefix}{ctx.command}.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
            await ctx.reply(embed=embed)
            return await ctx.invoke(self.bot.get_command("help"), command=str(ctx.command))


        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(color=0xFF0000).set_author(
                name=f'Команду {ctx.prefix}{ctx.command} нельзя выполнять так часто. Подождите немного.',
                icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
            return await ctx.reply(embed=embed)

        # Если ничего не подходит
        rep_guild = discord.utils.get(self.bot.guilds, id=761991504793174117)
        rep_channel = discord.utils.get(rep_guild.channels, id=868788281528160266)

        embed = discord.Embed(
            color=0xF56415,
            timestamp=ctx.message.created_at,
            title='ErrorHandler обнаружил ошибку!',
            description=f'Вызвано участником: {ctx.author}\nКоманда: {ctx.prefix}{ctx.command}\nПодробности ошибки: ```python\n{type(error).__name__}: {error}```\n```python\n{type(error).__name__}:\n{type(error).__doc__}```'
        )
        embed.set_author(
            name='Обработка исключения.',
            icon_url='http://s1.iconbird.com/ico/2013/11/504/w128h1281385326559hazard.png')
        try:
            await rep_channel.send(embed=embed)

        except:
            dev = discord.utils.get(self.bot.users, id=704560097610825828)
            await dev.send(embed=embed)

        if ctx.author.id in [704560097610825828, 732571199913328691]:
            await ctx.send(f'{ctx.author.mention}, у меня произошла проблема.')
        else:
            await ctx.send('произошла ошибка! Она уже отправлена разработчикам!')
def setup(bot):
    bot.add_cog(errorhandler(bot))
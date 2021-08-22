import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
class owner(commands.Cog):
    """Набор команд для отладки и тестирования."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name='logout', description='Деавторизовать от Discord', guild_ids=[761991504793174117])
    @commands.is_owner()
    async def logout(self, ctx):
        """Деавторизовать от Discord.
        """
        
        def message_check(m):
            return m.author.id == ctx.author.id
        
        row=create_actionrow(
                                        create_button(style=ButtonStyle.green, label="Да"))
        await ctx.send(':hammer_pick: А оно надо? -_-',  components=[row])
        button_ctx: ComponentContext = await wait_for_component(self.bot, components=row) 
        
        await ctx.send(':white_check_mark: Ну, как хочешь. Я спать, пока!')
        
        await self.bot.logout()

    @cog_ext.cog_slash(name='checkvoice', description='Проверить, проигрывается ли где-то музыка в моем исполнении.')
    @commands.is_owner()
    async def check_voice_clients(self, ctx):
        """Проверить, проигрывается ли где-то музыка в моем исполнении.
        """
        active_voice_clients = [x.name for x in self.bot.guilds if x.voice_client]
        await ctx.send('В данный момент я проигрываю музыку на %s серверах.' % len(active_voice_clients))

    @cog_ext.cog_slash(name='quit', description='Отключить меня от сервера.', guild_ids=[761991504793174117])
    @commands.is_owner()
    async def quit_guild(self, ctx, guild: discord.Guild = None):
        """Отключить меня от сервера.
        Аргументы:
        `:guild` - имя сервера
        __                                            __
        Например:
        ```
        !quit MyLittleGroup
        ```
        """
        try:
            if guild:
                await guild.leave()
            else:
                await ctx.guild.leave
        
        except:
            ctx.send(f'Возникла ошибка:\n{traceback.format_exc()}')
    
    @cog_ext.cog_slash(name='ping', description='Измерение задержки API, клиента.')
    @commands.is_owner()
    async def ping(self, ctx):
        """Измерение задержки API, клиента.
        """
        
        resp = await ctx.send('Тестируем...')
        diff = resp.created_at - ctx.message.created_at
        await resp.edit(
            content=f':ping_pong: Pong!\nЗадержка API: {1000 * diff.total_seconds():.1f}мс.\nЗадержка {self.bot.user.name}: {round(self.bot.latency * 1000)}мс')

    @cog_ext.cog_slash(name='restart', description='Перезагрузка', guild_ids=[761991504793174117])
    @commands.is_owner()
    async def restart(self, ctx):
        """Перезагрузка.
        """
        
        def message_check(m):
            return m.author.id == ctx.author.id
        
        active_voice_clients = [x.name for x in self.bot.guilds if x.voice_client]
        
        # Чтобы не перезагрузить бота во время проигрывания музыки.
        # В конце концов, бот перестает проигрывать ее при перезагрузке.
        if len(active_voice_clients) >= 1:
            await ctx.send(
                'В данный момент я проигрываю музыку на %s серверах.\nНе думаю, что стоит совершать перезагрузку сейчас...' % len(
                    active_voice_clients))
            try:
                msg = await self.bot.wait_for('message', check=message_check, timeout=20.0)
                if msg.content.lower() not in ['перезагрузись', 'перезапустись', 'пофиг', 'пофигу']:
                    return await ctx.send(':x: Отменено господином.')
                else:
                    pass
            
            except asyncio.TimeOutError:
                return await ctx.send(':x: Отменено - время ожидания ответа вышло.')
        
        else:
            await ctx.send('К перезагрузке готова! с:\nПросто нужно подтверждение.')
            try:
                msg = await self.bot.wait_for('message', check=message_check, timeout=20.0)
                if msg.content.lower() not in ['перезагрузись', 'да', 'угу', 'ага']:
                    return await ctx.send(':x: Отменено господином.')
                else:
                    pass
            
            except asyncio.TimeOutError:
                return await ctx.send(':x: Отменено - время ожидания ответа вышло.')
        
        await self.bot.change_presence(activity=discord.Game(name='ПЕРЕЗАГРУЗКУ...'), status=discord.Status.dnd)
        await ctx.send(embed=discord.Embed(color=0x13CFEB).set_footer(text="Перезагружаемся..."))
        os.execl(sys.executable, sys.executable, *sys.argv)

    @cog_ext.cog_slash(name='exception', description='Выдать исключение.', guild_ids=[761991504793174117])
    @commands.is_owner()
    async def exception(self, ctx):
        """Выдать исключение.
        """
        
        raise RuntimeError('Вызвано разработчиком.')

    @cog_ext.cog_slash(name='load', description='Загрузить модуль.', guild_ids=[761991504793174117])
    @commands.is_owner()
    async def cogload(self, ctx, *, cog: str):
        """Загрузить модуль.
        Аргументы:
        `:cog` - имя модуля
        __                                            __
        Например:
        ```
        !load cogs.music
        ```
        """
        
        try:
            self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`Ошибка при загрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно загружен`**')
    
    @cog_ext.cog_slash(name='unload', description='выгрузить модуль', guild_ids=[761991504793174117])
    @commands.is_owner()
    async def cogunload(self, ctx, *, cog: str):
        """Выгрузить модуль.
        Аргументы:
        `:cog` - имя модуля
        __                                            __
        Например:
        ```
        !unload tk
        ```
        """
        
        try:
            if cog == 'owner':
                await ctx.send(f'нельзя отгрузить {cog}!')
                pass
            else:
                self.bot.unload_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`Ошибка при выгрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно выгружен`**')

    @cog_ext.cog_slash(name='reload', description='Перезагрузка модуля.', guild_ids=[761991504793174117])
    @commands.is_owner()
    async def cogreload(self, ctx, *, cog: str):
        """Перезагрузка модуля.
        Аргументы:
        `:cogs` - имя модуля
        __                                            __
        Например:
        ```
        !reload fun
        ```
        """
        
        try:
            self.bot.unload_extension(f'cogs.{cog}')
            self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            await ctx.send(f'**`Ошибка при перезагрузке модуля {cog}:`** \n{type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Модуль {cog} успешно перезагружен`**')
#def setup(bot:commands.Bot):
    #bot.add_cog(owner(bot))
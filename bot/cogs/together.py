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

class together(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @cog_ext.cog_slash(name = 'chess', description='Play the chess!')
    async def chess (self, ctx):
        await ctx.defer()
        if ctx.author.voice:
            link = await self.bot.together.create_link (ctx.author.voice.channel.id, 'chess')
            await ctx.send (f'Ссылка для инициализации комнаты: \n{link}')
        else:
            await ctx.send('Вы не подключены к голосовому каналу!')
def setup(bot:commands.Bot):
    bot.add_cog(together(bot))
    


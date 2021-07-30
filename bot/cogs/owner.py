import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext

class owner(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @cog_ext.cog_slash(name='reload', description='Перезагрузить бота')
    async def reload(self, ctx):
        await ctx.send('lalalala')
    
    @commands.is_owner()
    @cog_ext.cog_slash(name='checkvoice', description='Проверить, играю ли я музыку.')
    async def check_voice_clients(self, ctx):
        """Проверить, проигрывается ли где-то музыка в моем исполнении.
        """
        active_voice_clients = [x.name for x in self.bot.guilds if x.voice_client]
        await ctx.send('В данный момент я проигрываю музыку на %s серверах.' % len(active_voice_clients), hidden=True)

def setup(bot:commands.Bot):
    bot.add_cog(owner(bot))
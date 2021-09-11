import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_commands import create_option, create_permission
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext

class automod(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @cog_ext.cog_slash(name='antiscam')


def setup(bot:commands.Bot):
    bot.add_cog(automod(bot))
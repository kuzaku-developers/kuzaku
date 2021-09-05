import discord
import datetime
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext

class logger(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_slash_command(self, ctx):
        self.bot.cmd(f'<{ctx.guild.name}> ({ctx.author}) :: {ctx.command}')

def setup(bot:commands.Bot):
    bot.add_cog(logger(bot))
import disnake
from disnake.ext import commands
from disnake_slash import SlashCommand
from disnake_slash.model import SlashCommandPermissionType
from disnake_slash.utils.manage_components import wait_for_component
from disnake_slash.utils.manage_components import create_button, create_actionrow
from disnake_slash.utils.manage_commands import create_option, create_permission
from disnake_slash.model import ButtonStyle
from disnake_slash import cog_ext


class automod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_slash(name="antiscam")
    async def antiscam(self, ctx):
        ...


def setup(bot: commands.Bot):
    bot.add_cog(automod(bot))

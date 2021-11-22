import disnake
from disnake.ext import commands
from disnake_slash import SlashCommand, cog_ext
from disnake_slash.model import ButtonStyle
from disnake_slash.utils.manage_commands import create_option
from disnake_slash.utils.manage_components import (
    create_actionrow,
    create_button,
    wait_for_component,
)


class channels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="joinchannel",
        name="set",
        description="Установить канал для оповещений!",
        options=[
            create_option(
                name="канал",
                description="Канал для установки.",
                required=True,
                option_type=7,
            )
        ],
        guild_ids=[761991504793174117],
        connector={"канал": "channel"},
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def joinchannelset(self, ctx, channel):
        await ctx.send(channel.id)

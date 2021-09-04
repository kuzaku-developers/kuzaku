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
        server = ctx.guild.name
        user = ctx.author
        command = ctx.command
        self.bot.cmd(f'<{server}> ({user}) :: {command}')
        embed=discord.Embed(
            color=0xffd700,
            timestamp=datetime.datetime.utcnow(),
            description=f"команда `/{command}` на сервере `{server}` использована пользователем `{user}`"
            )
        log_channel = await self.bot.fetch_channel(883728899152945172)
        await log_channel.send(embed=embed)
    @commands.Cog.listener()
    async def on_message(self, message):
        log_channel = await self.bot.fetch_channel(883724182662283294)
        if log_channel is None:
            print('none')
            return
        if not message.author.bot:
            self.bot.msglog(f'<{message.guild.name}> (#{message.channel}) ({message.author}) :: {message.content}')
            embed=discord.Embed(
            color=0xffd700,
            timestamp=datetime.datetime.utcnow(),
            description="в {} ({}):\n{}".format(message.channel.mention, message.guild.name, message.content)
            )
            embed.set_author(name=message.author, icon_url=message.author.avatar_url)
            embed.set_footer(text=message.author.id)
            if len(message.attachments) > 0:
                embed.set_image(url = message.attachments[0].url)
            await log_channel.send(embed=embed)


def setup(bot:commands.Bot):
    bot.add_cog(logger(bot))
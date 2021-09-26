import discord
import datetime
from utils.db import usedcmd
from discord.ext import commands
import dislash

class logger(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_slash_command(self, ctx):
        self.bot.log.info(f'<{ctx.guild.name}> ({ctx.author}) :: {ctx.data.name}')
        usedcmd()
    @commands.Cog.listener()
    async def on_auto_register(self, global_commands_patched, patched_guilds):
        self.bot.log.info('<slash> :: Slash commands is registred')
def setup(bot:commands.Bot):
    bot.add_cog(logger(bot))
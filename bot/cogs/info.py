import os
import platform
import discord
from discord.ext import commands
from yaml import Loader, load

rootdir=os.path.abspath(os.path.join(os.curdir))

class info(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        if platform.system() in ["Darwin", 'Windows']:
            with open(f"{rootdir}/bot/localization/ru/commands.yml", 'r') as stream:
                self.data = load(stream, Loader=Loader)
        elif platform.system()=='Linux':
            with open("bot/localization/ru/commands.yml", 'r') as stream:
                self.data = load(stream, Loader=Loader)

    @commands.command(name='invite')
    async def invite(self, ctx):
        full_url = self.data['info.invite.fullurl'].format(self.bot.user.id)
        low_url = self.data['info.invite.lowurl'].format(self.bot.user.id)
        embed = discord.Embed(timestamp=ctx.message.created_at, color=0xf0a302,
                              title=self.data['info.invite.embed.title'],
                              description=f'{full_url}\n{low_url}')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.prefix}{ctx.command}')
        await ctx.reply(embed=embed)
def setup(bot):
    bot.add_cog(info(bot))

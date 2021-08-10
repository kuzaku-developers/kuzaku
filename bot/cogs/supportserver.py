import discord
from discord.ext import commands


class supportserver(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        if member.guild.id == 761991504793174117:
            Role = discord.utils.get(member.guild.roles, id=868788263035498507)
            await member.add_roles(Role)
    
def setup(bot:commands.Bot):
    bot.add_cog(supportserver(bot))
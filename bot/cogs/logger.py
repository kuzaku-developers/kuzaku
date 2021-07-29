import discord
from discord.ext import commands


class logger(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(761991504793174117)
        print(self.guild)
        self.channel = discord.utils.get(self.guild.channels, id=869638984161189908)
    
    

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.id != self.bot.user.id:
            embed=discord.Embed(title="логи", description="лог сообщения!", color=0xff0000)
            embed.add_field(name=f"сообщение отправлено на сервере {message.guild.name}!", value=f"{message.author}: {message.content}", inline=False)
            await self.channel.send(embed=embed)
        

def setup(bot:commands.Bot):
    bot.add_cog(logger(bot))
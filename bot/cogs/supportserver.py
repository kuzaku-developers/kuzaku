import discord
from discord.ext import commands
from utils import card as cards

class supportserver(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        if member.guild.id == 761991504793174117:
            Role = discord.utils.get(member.guild.roles, id=868788263035498507)
            await member.add_roles(Role)
        elif False:
            ch=self.bot.get_channel(878196243334057984)
            card = cards.WelcomeCard()
            await card.setAvatar(member.avatar_url)
            await card.setAvatarBack("#424242")
            await card.setServerAvatar(member.guild.icon_url)
            await card.setServerAvatarBack("#424242")
            await card.setBackground("#a4a4ac")
            await card.setAvatarBackground("https://images.unsplash.com/photo-1600758208050-a22f17dc5bb9?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80")
            await card.setAvatarBackgroundBack("#FFFFFF")
            await card.setTextColor("#a4a4ac")
            await card.setTextStyle(path='bot/font.ttf')
            await card.setWelcomeColor('#FFFFFF')
            file=await card.create()
            await ch.send(file = discord.File(fp = file, filename = "welcome.png"))
    
def setup(bot:commands.Bot):
    bot.add_cog(supportserver(bot))
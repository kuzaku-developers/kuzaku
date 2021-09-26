import discord
from discord.ext import commands
from dislash import slash_command, Option, OptionType

class together(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command(name = 'chess', description='Play the chess!')
    async def chess (self, ctx):
        await ctx.respond(type=5)
        if ctx.author.voice:
            link = await self.bot.together.create_link (ctx.author.voice.channel.id, 'chess')
            await ctx.edit (f'Ссылка для инициализации комнаты: \n{link}')
        else:
            await ctx.edit('Вы не подключены к голосовому каналу!')
def setup(bot:commands.Bot):
    bot.add_cog(together(bot))
    


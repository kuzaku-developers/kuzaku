import disnake
from disnake.ext import commands


class together(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="together", description="Play the chess!")
    async def together(
        self,
        ctx,
        activity=commands.Param(
            choices=[
                "chess",
                "youtube",
                "poker",
                "betrayal",
                "fishing",
                "letter-tile",
                "word-snack",
            ]
        ),
    ):
        await ctx.response.defer()
        if ctx.author.voice:
            link = await self.bot.together.create_link(
                ctx.author.voice.channel.id, activity
            )
            await ctx.edit_original_message(
                content=f"Ссылка для инициализации комнаты: \n{link}"
            )
        else:
            await ctx.edit_original_message(
                content="Вы не подключены к голосовому каналу!"
            )


def setup(bot: commands.Bot):
    bot.add_cog(together(bot))

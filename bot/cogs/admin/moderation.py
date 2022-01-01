import disnake
from disnake.ext import commands
import disnake
from yaml import Loader, load
from utils.time import TimedeltaConverter, visdelta
from datetime import timedelta 
class Confirm(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout = 30

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @disnake.ui.button(emoji="✅", style=disnake.ButtonStyle.green)
    async def confirm(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        button.disabled = True
        button.style = disnake.ButtonStyle.gray
        self.value = True
        self.stop()


class moderation(commands.Cog, name="Модерация"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("localization/ru/bot/commands.yml", "r", encoding="utf8") as stream:
            self.data = load(stream, Loader=Loader)

    @commands.slash_command(name="ban", description="Банит участника.")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx, member: disnake.Member, reason: str = "Причина отсутствует."
    ):
        await ctx.response.defer()
        await ctx.guild.ban(user=member, reason=reason)

        embed = disnake.Embed(
            color=0x00FF00,
            description=f"Пользователь {member.mention} забанен!\nПричина: {reason}.",
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"{ctx.author} | kuzaku#2021")

        await ctx.send(embed=embed)

    @commands.slash_command(name="say", description="Бот что-то скажет!")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, text: str, channel: disnake.TextChannel = None):
        await ctx.response.defer(ephemeral=True)
        if not channel:
            channel = ctx.channel
        message = await channel.send(
            text
        )
        await ctx.send(
            content=self.data["say.text"].format(message.jump_url)
        )

    @commands.slash_command(name="kick", description="Кикает участника.")
    @commands.has_permissions(ban_members=True)
    async def kick(
        self, ctx, member: disnake.Member, reason: str = "Причина отсутствует."
    ):
        await ctx.response.defer()
    
        await ctx.guild.kick(user=member, reason=reason)
        embed = disnake.Embed(
                color=0x00FF00,
                description=f"Пользователь {member.mention} Кикнут!\nПричина: {reason}.",
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"{ctx.author} | kuzaku#2021")

        await ctx.send(embed=embed)
      
    @commands.slash_command(name="mute", description="Мутит участника.")
    @commands.has_permissions(manage_messages=True)
    async def mute(
        self, ctx, member: disnake.Member, time: TimedeltaConverter = commands.Param(description="Time. In format like 1h1m1s"), reason: str = "Причина отсутствует."
    ):
        await ctx.response.defer()
        await member.timeout(duration=time, reason=reason)
        embed = disnake.Embed(
                color=0x00FF00,
                description=f"Пользователь {member.mention} Замучен на {visdelta(time)}.\nПричина: {reason}.",
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.set_footer(text=f"{ctx.author} | kuzaku#2021")

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))


# Если вы это читаете, то вы подтверждаете то что вы не имеете права критиковать этот говно-код за его убогость и нечитаемость.
# Автор кода придерживается принципа пофиг-как, главное чтоб работало. А теперь, молитва!

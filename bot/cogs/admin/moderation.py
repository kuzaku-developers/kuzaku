import disnake
from disnake.ext import commands
import disnake
from yaml import Loader, load


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
        view = Confirm()
        embedd = disnake.Embed(
            title="Точно банить?",
            description=f"вы уверены, что хотите забанить пользователя {member.mention}? Тогда нажмите на кнопку!",
        )
        msg = await ctx.edit_original_message(embed=embedd, view=view)
        await view.wait()
        if view.value == None:
            for child in view.children:
   
                child.disabled = True
 
                await msg.edit(view=view)
        elif view.value:
            try:
                await ctx.guild.ban(user=member, reason=reason)
            except Exception as e:
                print(e)
                for child in view.children:
     
                    child.disabled = True
   
                await msg.edit(view=view, embed=disnake.Embed(title="Ошибка!", description="У меня нет прав!"))
                return
                

            embed = disnake.Embed(
                color=0x00FF00,
                description=f"Пользователь {member.mention} забанен!\nПричина: {reason}.",
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_footer(text=f"{ctx.author} | kuzaku#2021")

            await msg.edit(embed=embed)
        else:
            embed = disnake.Embed(
                color=0x00FF00,
                description=f"Бан отклонен.",
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_footer(text=f"{ctx.author} | kuzaku#2021")

            await msg.edit(embed=embed)

    @commands.slash_command(name="say", description="Бот что-то скажет!")
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, text: str, channel: disnake.TextChannel = None):
        await ctx.response.defer(ephemeral=True)
        if not channel:
            channel = ctx.channel
        message = await channel.send(
            text.replace("@everyone", "@ everyone").replace("@here", "@ here")
        )
        await ctx.edit_original_message(
            content=self.data["say.text"].format(message.jump_url)
        )
    @commands.slash_command(name="kick", description="Кикает участника.")
    @commands.has_permissions(ban_members=True)
    async def kick(
        self, ctx, member: disnake.Member, reason: str = "Причина отсутствует."
    ):
        await ctx.response.defer()
        view = Confirm()
        embedd = disnake.Embed(
            title="Точно Кикать?",
            description=f"вы уверены, что хотите кикнуть пользователя {member.mention}? Тогда нажмите на кнопку!",
        )
        msg = await ctx.edit_original_message(embed=embedd, view=view)
        await view.wait()
        if view.value == None:
            for child in view.children:

                child.disabled = True
   
                await msg.edit(view=view)
        elif view.value:
            try:
                await ctx.guild.ban(user=member, reason=reason)
            except Exception as e:
                print(e)
                for child in view.children:
                    print(child)
                    child.disabled = True
                    print(child)
                await msg.edit(view=view, embed=disnake.Embed(title="Ошибка!", description="У меня нет прав!"))
                return
                

            embed = disnake.Embed(
                color=0x00FF00,
                description=f"Пользователь {member.mention} Кикнут!\nПричина: {reason}.",
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_footer(text=f"{ctx.author} | kuzaku#2021")

            await msg.edit(embed=embed)
        else:
            embed = disnake.Embed(
                color=0x00FF00,
                description=f"Кик отклонен.",
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_footer(text=f"{ctx.author} | kuzaku#2021")

            await msg.edit(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))


# Если вы это читаете, то вы подтверждаете то что вы не имеете права критиковать этот говно-код за его убогость и нечитаемость.
# Автор кода придерживается принципа пофиг-как, главное чтоб работало. А теперь, молитва!

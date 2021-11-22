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
                print(child)
                child.disabled = True
                print(child)
                await msg.edit(content="timeout", view=view)
        elif view.value:
            await ctx.guild.ban(user=member, reason=reason)

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

    @commands.slash_command(name="kick", description="Кикнет участника.")
    @commands.has_permissions(ban_members=True)
    async def kick(
        self, ctx, member: disnake.Member, reason: str = "Причина отсутствует."
    ):
        await ctx.response.defer()
        embedd = disnake.Embed(
            title="Точно кикать?",
            description=f"вы уверены, что хотите кикнуть пользователя {member.mention}? Тогда нажмите на кнопку!",
        )
        msg = await ctx.edit_original_message(
            embed=embedd,
            components=[
                ActionRow(
                    Button(style=ButtonStyle.green, emoji="✅", custom_id="confirmban")
                )
            ],
        )
        on_click = msg.create_click_listener(timeout=60)

        @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter):
            # This function is called in case a button was clicked not by the author
            # cancel_others=True prevents all on_click-functions under this function from working
            # regardless of their checks
            # reset_timeout=False makes the timer keep going after this function is called
            await inter.reply("Вы не автор сообщения!", ephemeral=True)

        @on_click.matching_id("confirmban")
        async def on_test_button(inter):
            # This function only works if the author presses the button
            # Becase otherwise the previous decorator cancels this one
            await inter.guild.kick(user=member, reason=reason)

            embed = disnake.Embed(
                color=0x00FF00,
                description=f"Пользователь {member.mention} кикнут!\nПричина: {reason}.",
            )
            embed.set_author(name=ctx.author.name, icon_url=inter.author.avatar.url)
            embed.set_footer(text=f"{ctx.author} | kuzaku#2021")

            await msg.edit(embed=embed, components=[])

        @on_click.timeout
        async def on_timeout():
            await msg.edit(
                embed=embedd,
                components=[
                    ActionRow(
                        Button(
                            style=ButtonStyle.green,
                            emoji="✅",
                            custom_id="confirmban",
                            disabled=True,
                        )
                    )
                ],
            )


def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))


# Если вы это читаете, то вы подтверждаете то что вы не имеете права критиковать этот говно-код за его убогость и нечитаемость.
# Автор кода придерживается принципа пофиг-как, главное чтоб работало. А теперь, молитва!

import discord
from discord.ext import commands
import dislash
from dislash import slash_command, Option, OptionType, ActionRow, Button, ButtonStyle
from yaml import Loader, load
class moderation(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        with open("localization/ru/bot/commands.yml", 'r', encoding='utf8') as stream:
                self.data = load(stream, Loader=Loader)
    @slash_command(name='ban', description='Банит участника.',
        options=[
    Option("участник", "Участник, которого забанить.", OptionType.USER),
    Option("причина", "Причина бана.", OptionType.STRING)
            ], connectors={'участник':'member', 'причина':'reason'})
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, reason: str = 'Причина не указана.', test_guilds=[808013895917633546]):
        await ctx.respond(type=5)
        embedd=discord.Embed(title='Точно банить?', description=f'вы уверены, что хотите забанить пользователя {member.mention}? Тогда нажмите на кнопку!')
        msg=await ctx.edit(embed=embedd,  components=[ActionRow(
        Button(
            style=ButtonStyle.green,
            emoji='✅',
            custom_id="confirmban"
        )
    )])
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
            await inter.guild.ban(user=member, reason=reason)

            embed = discord.Embed(color=0x00ff00,
                description=f'Пользователь {member.mention} забанен!\nПричина: {reason}.')
            embed.set_author(name=ctx.author.name, icon_url=inter.author.avatar_url)
            embed.set_footer(text=f'{ctx.author} | kuzaku#2021')

            await msg.edit(embed=embed, components=[])

        @on_click.timeout
        async def on_timeout():
            await msg.edit(embed=embedd, components=[ActionRow(
        Button(
            style=ButtonStyle.green,
            emoji='✅',
            custom_id="confirmban",
            disabled=True
        )
    )])
    @slash_command(name='say', description='Бот что-то скажет!', 
        options=[
    Option("текст", "Текст, который сказать.", OptionType.STRING),
    Option("канал", "Канал, в который отправить текст.", OptionType.CHANNEL)
    ], connectors={'текст':'text', "канал":"channel"})
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, text, channel: discord.TextChannel = None):
        await ctx.respond(type=5, ephemeral=True)
        if not channel:
            channel=ctx.channel
        message=await channel.send(text)
        await ctx.edit(self.data['say.text'].format(message.jump_url))
    @slash_command(name='kick', description='Кикнет участника.',
        options=[
    Option("участник", "Участник, которого кикнуть.", OptionType.USER),
    Option("причина", "Причина бана.", OptionType.STRING)
            ], connectors={'участник':'member', 'причина':'reason'})
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member, reason: str = 'Причина не указана.'):
        await ctx.respond(type=5)
        embedd=discord.Embed(title='Точно кикать?', description=f'вы уверены, что хотите кикнуть пользователя {member.mention}? Тогда нажмите на кнопку!')
        msg=await ctx.edit(embed=embedd,  components=[ActionRow(
        Button(
            style=ButtonStyle.green,
            emoji='✅',
            custom_id="confirmkick"
        )
    )])
        on_click = msg.create_click_listener(timeout=60)
        @on_click.not_from_user(ctx.author, cancel_others=True, reset_timeout=False)
        async def on_wrong_user(inter):
            # This function is called in case a button was clicked not by the author
            # cancel_others=True prevents all on_click-functions under this function from working
            # regardless of their checks
            # reset_timeout=False makes the timer keep going after this function is called
            await inter.reply("Вы не автор сообщения!", ephemeral=True)

        @on_click.matching_id("confirmkick")
        async def on_test_button(inter):
            # This function only works if the author presses the button
            # Becase otherwise the previous decorator cancels this one
            await inter.guild.kick(user=member, reason=reason)

            embed = discord.Embed(color=0x00ff00,
                description=f'Пользователь {member.mention} кикнут!\nПричина: {reason}.')
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f'{ctx.author} | kuzaku#2021')

            await msg.edit(embed=embed, components=[])

        @on_click.timeout
        async def on_timeout():
            await msg.edit(embed=embedd, components=[ActionRow(
        Button(
            style=ButtonStyle.green,
            emoji='✅',
            custom_id="confirmkick",
            disabled=True
        )
    )])
def setup(bot:commands.Bot):
    bot.add_cog(moderation(bot))
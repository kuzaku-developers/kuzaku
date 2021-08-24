import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
class moderation(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    @cog_ext.cog_slash(name='ban', description='Банит участника.',
        options=[
    create_option(
    name='участник',
    description='Участник, которого забанить.',
    required=True,
    option_type=6
        ),
    create_option(
    name='причина',
    description='Причина бана. (не обязательна)',
    required=False,
    option_type=3
        )
            ], connector={'участник':'member', 'причина':'reason'})
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, reason: str = 'Причина не указана.'):
        embedd=discord.Embed(title='Точно банить?', description=f'вы уверены, что хотите забанить пользователя {member.mention}? Тогда нажмите на кнопку!')
        row=create_actionrow(
                                        create_button(style=ButtonStyle.gray, emoji='✅'))
        msg=await ctx.send(embed=embedd,  components=[row])
        button_ctx: ComponentContext = await wait_for_component(self.bot, components=row)  
        await msg.edit(embed=embedd, components=[create_actionrow(create_button(style=ButtonStyle.gray, emoji='✅', disabled=True))])
        await ctx.guild.ban(user=member, reason=reason)

        embed = discord.Embed(color=0x00ff00,
                description=f'Пользователь {member.mention} забанен!\nПричина: {reason}.')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.author} | kuzaku#2021')

        await button_ctx.send(embed=embed)
    @cog_ext.cog_slash(name='say', description='Бот что-то скажет!', 
        options=[
    create_option(
    name='текст',
    description='Текст, который сказать',
    required=True,
    option_type=3
        )
    ], connector={'текст':'text'})
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, text):
        await ctx.channel.send(text)
        embed= discord.Embed(title='Я сказала все, что могла!')
        await ctx.send(embed=embed, hidden=True)
    @cog_ext.cog_slash(name='kick',  description='Кикнет участника.',
        options=[
    create_option(
    name='участник',
    description='Участник, которого кикнуть.',
    required=True,
    option_type=6
        ),
    create_option(
    name='причина',
    description='Причина кика. (не обязательна)',
    required=False,
    option_type=3
        )
            ], connector={'участник':'member', 'причина':'reason'})
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, reason: str = 'Причина не указана.'):
        embedd=discord.Embed(title='Точно кикать?', description=f'вы уверены, что хотите кикнуть пользователя {member.mention}? Тогда нажмите на кнопку!')
        row=create_actionrow(
                                        create_button(style=ButtonStyle.gray, emoji='✅'))
        msg=await ctx.send(embed=embedd,  components=[row])
        button_ctx: ComponentContext = await wait_for_component(self.bot, components=row)  
        await msg.edit(embed=embedd, components=[create_actionrow(create_button(style=ButtonStyle.gray, emoji='✅', disabled=True))])
        await ctx.guild.kick(user=member, reason=reason)

        embed = discord.Embed(color=0x00ff00,
                description=f'Пользователь {member.mention} кикнут!\nПричина: {reason}.')
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f'{ctx.author} | kuzaku#2021')

        await button_ctx.send(embed=embed)
def setup(bot:commands.Bot):
    bot.add_cog(moderation(bot))
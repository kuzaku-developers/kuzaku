import discord
import requests
import io
from discord.ext import commands
import dislash
from dislash import slash_command, Option, OptionType
import re
class fun(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    @slash_command(name='screenshot', description='Take site screenshot!', options=[
        Option("url", "Site url", OptionType.STRING, required=True)
        # By default, Option is optional
        # Pass required=True to make it a required arg
    ])
    @commands.is_nsfw()
    async def screenshot(self, ctx, url: str):
        await ctx.respond(type=5)
        urll = re.compile(r"https?://(www\.)?")
        urlll=urll.sub('', url).strip().strip('/')
        url=f'https://{urlll}'
        embed=discord.Embed(title=f'Скриншот сайта {url}')
        response = requests.get(f'https://render-tron.appspot.com/screenshot/{url}?width=1920&height=1080') 
        file_like_object = io.BytesIO(response.content)
        imgchannel=await self.bot.fetch_channel(879049868415496213)
        msg=await imgchannel.send(file=discord.File(file_like_object, filename='screen.png'))
        print(msg.attachments[0].url)
        embed.set_image(url=msg.attachments[0].url)
        await ctx.edit(embed=embed)
        
    @slash_command(name='anime', description='search about anime', options=[
        Option("anime", "Anime to find", OptionType.STRING, required=True)
        # By default, Option is optional
        # Pass required=True to make it a required arg
    ])
    async def animesearch(self, ctx, anime: str):
        await ctx.respond(type=5)
        try:
            response = requests.get(f"https://api.jikan.moe/v3/search/anime?q={anime}")
            data = response.json()
            print(f'desc:{data["results"][0]["synopsis"]}')
            print(data['results'][0].get('url'))
            print(data['results'][0].get('episodes'))
            print(data['results'][0].get('score'))
            print(data['results'][0].get('members'))
            print(data['results'][0].get('type'))
            print(data['results'][0].get('image_url'))
            embed = discord.Embed(title=data["results"][0].get("title"))

            embed.add_field(name="Описание:",               value=f"{data['results'][0].get('synopsis')} **[Больше информации об {data['results'][0].get('title')}...]({data['results'][0].get('url')})**", inline=True)
            embed.add_field(name="Эпизодов:",               value=f"**{data['results'][0].get('episodes')}**", inline=True)
            embed.add_field(name="Оценка на MyAnimeList:",  value=f"**{data['results'][0].get('score')}/10**", inline=True)
            embed.add_field(name="Пользователей:",          value=f"**{data['results'][0].get('members')}**", inline=True)
            embed.add_field(name="Тип:",                    value=f"**{data['results'][0].get('type')}**", inline=True)

            embed.set_thumbnail(url=data['results'][0].get('image_url'))

            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.edit(embed=embed)

        except KeyError:
            await ctx.edit(f'По запросу ``{anime}`` ничего не найдено..')
    
def setup(bot:commands.Bot):
    bot.add_cog(fun(bot))
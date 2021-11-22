import requests
import io
import disnake
from disnake.ext import commands
import re


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="screenshot",
        description="Take site screenshot!",
    )
    @commands.is_nsfw()
    async def screenshot(self, ctx, url: str):
        await ctx.response.defer()
        urll = re.compile(r"https?://(www\.)?")
        urlll = urll.sub("", url).strip().strip("/")
        url = f"https://{urlll}"
        embed = disnake.Embed(title=f"Скриншот сайта {url}")
        response = requests.get(
            f"https://render-tron.appspot.com/screenshot/{url}?width=1920&height=1080"
        )
        file_like_object = io.BytesIO(response.content)
        imgchannel = await self.bot.fetch_channel(879049868415496213)
        msg = await imgchannel.send(
            file=discord.File(file_like_object, filename="screen.png")
        )
        print(msg.attachments[0].url)
        embed.set_image(url=msg.attachments[0].url)
        await ctx.edit_original_message(embed=embed)

    @commands.slash_command(
        name="anime",
        description="search about anime",
    )
    async def animesearch(self, ctx, anime: str):
        await ctx.response.defer()
        try:
            response = requests.get(f"https://api.jikan.moe/v3/search/anime?q={anime}")
            data = response.json()
            print(f'desc:{data["results"][0]["synopsis"]}')
            print(data["results"][0].get("url"))
            print(data["results"][0].get("episodes"))
            print(data["results"][0].get("score"))
            print(data["results"][0].get("members"))
            print(data["results"][0].get("type"))
            print(data["results"][0].get("image_url"))
            embed = disnake.Embed(title=data["results"][0].get("title"))

            embed.add_field(
                name="Описание:",
                value=f"{data['results'][0].get('synopsis')} **[Больше информации об {data['results'][0].get('title')}...]({data['results'][0].get('url')})**",
                inline=True,
            )
            embed.add_field(
                name="Эпизодов:",
                value=f"**{data['results'][0].get('episodes')}**",
                inline=True,
            )
            embed.add_field(
                name="Оценка на MyAnimeList:",
                value=f"**{data['results'][0].get('score')}/10**",
                inline=True,
            )
            embed.add_field(
                name="Пользователей:",
                value=f"**{data['results'][0].get('members')}**",
                inline=True,
            )
            embed.add_field(
                name="Тип:", value=f"**{data['results'][0].get('type')}**", inline=True
            )

            embed.set_thumbnail(url=data["results"][0].get("image_url"))

            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.edit_original_message(embed=embed)

        except KeyError:
            await ctx.edit_original_message(
                f"По запросу ``{anime}`` ничего не найдено.."
            )


def setup(bot):
    bot.add_cog(fun(bot))

import datetime
import random
import time
from _random import Random
import disnake
from disnake.ext import commands as commands, tasks
import asyncio
from utils.db import (
    dbsetrp,
    dbgetrpid,
    dbrpaddmoney,
    dbrpgetuser,
    dbrpsethome,
    dbrpsetcar,
    dbrpsetresume,
    dbrpsetjson,
    dbrpgetcolumn,
)


guild_ids = [730467133162782760]


def getnalog(cost):
    return cost * (dbrpgetuser("federation")["nalogi"] / 100)


def getnds(cost):
    return cost * (dbrpgetuser("federation")["nds"] / 100)


def all_digits(msg):
    int_str = ""

    for char in msg:
        if char.isdigit():
            int_str += char

    return int(int_str)


class roleplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=guild_ids,
        name="call",
        description="позвони мне, позвони! звонит человеку!",
        options=[
            Option(
                "человек", "выыбери человека для звонка", type=Type.USER, required=True
            )
        ],
    )
    async def call(self, ctx):
        caller = ctx.author
        user1 = ctx.get("человек")
        await ctx.send(
            embed=discord.Embed(
                title="дозвон!", description=f"пробуем дозвониться до {user1}!"
            ),
            ephemeral=True,
        )
        msg = await user1.send(
            embed=discord.Embed(
                title="звонок!",
                description=f"тебе звонит {ctx.user}! ✅ - принять, ❌ - отклонить",
            )
        )
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        try:

            def check(reaction, user):
                return user == user1 and str(reaction.emoji) in ["✅", "❌"]

            reaction, user = await self.bot.wait_for(
                "reaction_add", timeout=60, check=check
            )
            print(f"r:{reaction.emoji}")
            print(reaction.emoji == "✅")
            if reaction.emoji == "❌":
                print("43234")
                await ctx.author.send("звонок сброшен!")

            elif reaction.emoji == "✅":
                print("1232")
                await ctx.author.send("ок! звоним!")

                await user.send(f"дозвон! ты соединен с {ctx.user}")
                ended = 0

                def check1(author):
                    def inner_check(message):
                        return message.author == author and isinstance(
                            message.channel, disnake.DMChannel
                        )

                    return inner_check

                while ended != 1:
                    try:
                        print("1232222")
                        msgc = await self.bot.wait_for(
                            "message", timeout=30, check=check1
                        )
                        if msgc.author == caller:
                            await user.send(f"{caller}: {msgc.content}")
                        if msgc.author == user:
                            await caller.send(f"{user}: {msgc.content}")

                        print(msgc)

                    except:
                        await ctx.author.send("ответа нет! сброс")
                        await user.send("ответа нет! сброс!")
                        ended = 1
        except Exception as e:
            print(e)
            await user1.send("ожидание истекло! звонок пропущен")

    @commands.slash_command(
        guild_ids=guild_ids,
        name="pay",
        description="перевод денег!",
        options=[
            Option(
                "валюта",
                "выбери валюту",
                type=Type.STRING,
                required=True,
                choices=[
                    OptionChoice("рубли", "rub"),
                    OptionChoice("доллары", "dollars"),
                    OptionChoice("хардкоины", "hard"),
                ],
            ),
            Option(
                "количество",
                "укажи количество валюты для перевода",
                Type.INTEGER,
                required=True,
            ),
            Option("пользователь", "выбрать пользователя", Type.USER, required=True),
        ],
    )
    async def pay(self, ctx):
        # Returns <ctx.author> if "user" argument wasn't passed
        user = ctx.get("пользователь", ctx.author)
        money = ctx.get("количество")
        emb = disnake.Embed(color=discord.Color.blurple())
        emb.title = "перевод!"
        emb.description = (
            f"перевод денег пользователю `{user}`!\n"
            f"**валюта:** `{ctx.get('валюта').replace('rub', 'рубли').replace('hard', 'хардкоины').replace('dollars', 'доллары')}`"
        )
        emb.set_thumbnail(url=user.avatar_url)
        msg = await ctx.send(embed=emb)
        print(msg)
        try:
            if dbrpgetuser(ctx.user.id)["rubles"] < money:
                await msg.edit(
                    embed=discord.Embed(
                        title="ошибка",
                        description="у тебя нет столько денег! перевожу все!",
                    )
                )
                money2 = dbrpgetuser(ctx.user.id)["rubles"]
                await dbrpaddrubles(ctx.user.id, -money2)
                await dbrpaddrubles(user.id, money2)

                await msg.edit(
                    embed=discord.Embed(
                        title="перевод завершен",
                        description=f'ты перевел {money2} {pickform(money2, ["рубль", "рубля", "рублей"])}',
                    )
                )
                await asyncio.sleep(5)
                await msg.delete()
            elif dbrpgetuser(ctx.user.id)["rubles"] >= money:
                await dbrpaddrubles(ctx.user.id, -money)
                await dbrpaddrubles(user.id, money)
                await msg.edit(
                    embed=discord.Embed(
                        title="перевод завершен",
                        description=f'ты перевел {money} {pickform(money, ["рубль", "рубля", "рублей"])}',
                    )
                )
                await asyncio.sleep(5)
                await msg.delete()
        except Exception as error:
            print(error)

    @commands.slash_command(
        guild_ids=guild_ids,
        description="Builds a custom embed",
        options=[
            Option("title", "Makes the title of the embed", Type.STRING),
            Option("description", "Makes the description", Type.STRING),
            Option("color", "The color of the embed", Type.STRING)
            # Note that all args are optional
            # because we didn't specify required=True in Options
        ],
    )
    async def embed(self, inter):
        # Get arguments
        title = inter.get("title")
        desc = inter.get("description")
        color = inter.get("color")
        # Converting color
        if color is not None:
            try:
                color = await commands.ColorConverter().convert(inter, color)
            except:
                color = None
        if color is None:
            color = disnake.Color.default()
        # Generating an embed
        emb = disnake.Embed(color=color)
        if title is not None:
            emb.title = title
        if desc is not None:
            emb.description = desc
        # Sending the output
        await inter.reply(embed=emb, hide_user_input=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 835384947773669386:
            Role = disnake.utils.get(member.guild.roles, id=835559304852537404)
            await member.add_roles(Role)
        try:
            name = dbrpgetuser(member.id)
            await member.edit(nick=f'{name["rpname"]} | {name["idrp"]}')
        except:
            ...

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # -----start of reg----#
        if payload.member == self.bot.user:
            return
        Channel = self.bot.get_channel(837345395667501118)
        if payload.emoji.name == "🛬" and payload.channel_id == 837345395667501118:
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            await msg.add_reaction("🛬")
            await msg.remove_reaction("🛬", payload.member)
            Role = disnake.utils.get(payload.member.guild.roles, id=837312438881353748)
            await payload.member.add_roles(Role)
            await Channel.send(
                embed=discord.Embed(
                    title="прилет", description=f"{payload.member.mention} прилетел!"
                ),
                delete_after=5,
            )
            # -----end of reg----#
        # -----start of passport----#
        if payload.emoji.name == "📝" and payload.channel_id == 837312495634481202:
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            await msg.add_reaction("📝")
            await msg.remove_reaction("📝", payload.member)
            await payload.member.send(
                embed=discord.Embed(
                    title="регистрация",
                    description=f"{payload.member.mention}, регистрируйся!",
                ),
                delete_after=5,
            )
            await payload.member.send(
                "напиши твое РП имя и фамилию. (например БАнаН БанАНОвввиииич). это имя нельзя будет изменить без админов. это имя будет у тебя в дс сервере",
                delete_after=60,
            )

            def check(author):
                def inner_check(message):
                    return message.author == author and isinstance(
                        message.channel, disnake.DMChannel
                    )

                return inner_check

            try:
                regname = await self.bot.wait_for(
                    "message", check=check(payload.member), timeout=30
                )
                regname = regname.content
            except:
                await payload.member.send(
                    "я не могу так долго ждать! твое имя станет твоим дискорд именем!"
                )
                regname = payload.member.name
            await payload.member.send(
                "напиши свои навыки в РП. (типо лечения болезней)", delete_after=60
            )
            try:
                regnaviki = await self.bot.wait_for(
                    "message", check=check(payload.member), timeout=30
                )
                regnaviki = regnaviki.content
            except Exception as error:
                await payload.member.send(
                    "я не могу так долго ждать! ты будешь уметь жить!"
                )
                regnaviki = "жить"

            dbsetrp(payload.member.id, str(regname), str(regnaviki))
            if not len(f"{regname} | {dbgetrpid(payload.member.id)}") > 32:
                try:
                    await payload.member.edit(
                        nick=f"{regname} | {dbgetrpid(payload.member.id)}"
                    )
                except:
                    await payload.member.send("ты овнер?")
            else:
                await payload.member.send(
                    "слишком длинный ник! твой ник будет твоим дискорд ником!"
                )
                await payload.member.edit(
                    nick=f"{payload.member.name} | {dbgetrpid(payload.member.id)}"
                )
            await payload.member.send(
                embed=discord.Embed(
                    title="регистрация",
                    description="ты прошел регистрацию! приятного рп!",
                ),
                delete_after=20,
            )
            rolee = payload.member.guild.get_role(837312438881353748)
            await payload.member.remove_roles(rolee)
            Role = disnake.utils.get(payload.member.guild.roles, id=837340231937818636)
            await payload.member.add_roles(Role)
            docschannel = self.bot.get_channel(837312548856135720)
            await docschannel.send(
                embed=discord.Embed(
                    title="регистрация!",
                    description=f"""
имя человека: {payload.member.mention}.
рп имя и фамилия: {regname}
навыки: {regnaviki}
номер человека: {dbgetrpid(payload.member.id)}
            """,
                )
            )

            # -----end of passport----#
        # ------start of BOMZ------#
        if payload.emoji.name == "🙏" and payload.channel_id == 837340041176416277:
            try:
                if (
                    int(dbrpgetuser(payload.member.id)["rubles"]) >= 150
                    and dbrpgetuser(payload.member.id)["home"] == True
                    or int(dbrpgetuser(payload.member.id)["rubles"]) >= 600
                ):
                    Rolebomz = disnake.utils.get(
                        payload.member.guild.roles, id=835462674879741962
                    )
                    Roleman = disnake.utils.get(
                        payload.member.guild.roles, id=835539034914029618
                    )
                    await payload.member.remove_roles(Rolebomz)
                    await payload.member.add_roles(Roleman)
                    await payload.member.send(
                        "ВНИМАНИЕ! ЭТО ТВОИ ПОСЛЕДНИЕ ДЕНЬГИ! если ты еще не купил дом (400$), купи его! купи машину (100$), бензин (20$), заполни резме (50%) и найди работу!"
                    )
                    msg = await self.bot.get_channel(payload.channel_id).fetch_message(
                        payload.message_id
                    )
                    await msg.add_reaction("🙏")
                    await msg.remove_reaction("🙏", payload.member)
                    return
            except KeyError:
                dbrpsethome(payload.member.id, False)
                if (
                    int(dbrpgetuser(payload.member.id)["rubles"]) >= 500
                    and dbrpgetuser(payload.member.id)["home"] == True
                    or int(dbrpgetuser(payload.member.id)["rubles"]) >= 600
                ):
                    Rolebomz = disnake.utils.get(
                        payload.member.guild.roles, id=835462674879741962
                    )
                    Roleman = disnake.utils.get(
                        payload.member.guild.roles, id=835539034914029618
                    )
                    await payload.member.remove_roles(Rolebomz)
                    await payload.member.add_roles(Roleman)
                    await payload.member.send(
                        "ВНИМАНИЕ! ЭТО ТВОИ ПОСЛЕДНИЕ ДЕНЬГИ! если ты еще не купил дом (400$), купи его! купи машину (100$), бензин (20$), заполни резме (50%) и найди работу!"
                    )
                    msg = await self.bot.get_channel(payload.channel_id).fetch_message(
                        payload.message_id
                    )
                    await msg.add_reaction("🙏")
                    await msg.remove_reaction("🙏", payload.member)
                    return
            if random.randint(1, 100) > 20:
                money = random.randint(2, 4)
                dbrpaddrubles(payload.member.id, money)

                await payload.member.send(f"ты получил {money} рубля!")
            else:
                await payload.member.send("увы, вам не дали денег. попробуй еще!")
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            await msg.add_reaction("🙏")
            await msg.remove_reaction("🙏", payload.member)
            # ----end of BOMZ----#
        # ----start of shop--#

        msg = await self.bot.get_channel(payload.channel_id).fetch_message(
            payload.message_id
        )
        if (
            str(payload.emoji.name) == "1️⃣"
            and payload.channel_id == 837663284207157339
        ):
            await msg.add_reaction("1️⃣")
            await msg.remove_reaction("1️⃣", payload.member)

            airrole = disnake.utils.get(
                payload.member.guild.roles, id=837312389102698516
            )
            if airrole in payload.member.roles:
                await payload.member.send(
                    embed=discord.Embed(
                        title="у тебя уже есть airpods++",
                        description=f"ты не можешь купить те же наушники!",
                    )
                )
            elif int(dbrpgetuser(payload.user_id)["rubles"]) >= (
                45000 + getnalog(45000)
            ):
                dbrpaddrubles(payload.user_id, -(45000 + getnalog(45000)))
                await payload.member.add_roles(airrole)
                await payload.member.send(
                    embed=discord.Embed(
                        title="ты купил airpods++",
                        description=f'ты купил airpods++ за {(45000 + getnalog(45000))} {pickform(45000 + getnalog(45000), ["рубль", "рубля", "рублей"])} (с учетом коммисии)! теперь у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                    )
                )
                await dbrpaddrubles("federation", +(getnalog(45000)))
                await dbrpaddrubles("federation", +(getnds(45000)))

            else:
                await payload.member.send(
                    embed=discord.Embed(
                        title="ты не смог купить airpods++",
                        description=f'ты не можешь купить airpods++! у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {(45000 + getnalog(45000))} {pickform(45000 + getnalog(45000), ["рубль", "рубля", "рублей"])} (с учетом коммисии в 2%)!',
                    )
                )

        msg = await self.bot.get_channel(payload.channel_id).fetch_message(
            payload.message_id
        )
        if payload.emoji.name == "2️⃣" and payload.channel_id == 837663284207157339:
            macrole = disnake.utils.get(
                payload.member.guild.roles, id=837312392118927370
            )
            await msg.add_reaction("2️⃣")
            await msg.remove_reaction("2️⃣", payload.member)

            if macrole in payload.member.roles:
                await payload.member.send(
                    embed=discord.Embed(
                        title="у тебя уже есть mac pro",
                        description=f"ты не можешь купить еще 1 mac pro!",
                    )
                )

            elif dbrpgetuser(payload.user_id)["rubles"] >= (234000 + getnalog(234000)):
                dbrpaddrubles(payload.user_id, -(234000 + getnalog(234000)))
                await payload.member.add_roles(macrole)
                await payload.member.send(
                    embed=discord.Embed(
                        title="ты купил mac pro",
                        description=f'ты купил mac pro за {(234000 + getnalog(234000))} {pickform(234000 + getnalog(234000), ["рубль", "рубля", "рублей"])} теперь у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                    )
                )
                dbrpaddrubles("federation", (getnalog(234000)))
                await dbrpaddrubles("federation", (getnds(234000)))

            else:
                await payload.member.send(
                    embed=discord.Embed(
                        title="ты не смог купить mac pro",
                        description=f'ты не можешь купить mac pro! у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {(234000 + getnalog(234000))} {pickform(234000 + getnalog(234000), ["рубль", "рубля", "рублей"])}!',
                    )
                )

        if payload.emoji.name == "3️⃣" and payload.channel_id == 837663284207157339:

            msg = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            macbookrole = disnake.utils.get(
                payload.member.guild.roles, id=837312387375562832
            )
            await msg.add_reaction("3️⃣")
            await msg.remove_reaction("3️⃣", payload.member)
            try:
                if macbookrole in payload.member.roles:
                    await payload.member.send(
                        embed=discord.Embed(
                            title="у тебя уже есть macbook!",
                            description=f"ты не можешь купить macbook еще раз!",
                        )
                    )
                elif dbrpgetuser(payload.user_id)["rubles"] >= 120000 + getnalog(
                    120000
                ):
                    dbrpaddrubles(payload.user_id, -120000 + getnalog(120000))

                    await payload.member.send(
                        embed=discord.Embed(
                            title="ты купил macbook",
                            description=f'ты купил macbook за {120000 + getnalog(120000)} {pickform(120000 + getnalog(120000), ["рубля", "рубль", "рублей"])}! теперь у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                        )
                    )
                    await payload.member.add_roles(macbookrole)
                    dbrpaddrubles("federation", 120000 + getnalog(120000))
                    dbrpaddrubles("federation", 120000 + getnds(120000))

                else:
                    await payload.member.send(
                        embed=discord.Embed(
                            title="ты не смог купить macbook",
                            description=f'ты не можешь купить macbook! у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {120000 + getnalog(120000)} {pickform(120000 + getnalog(120000), ["рубль", "рубля", "рублей"])}!',
                        )
                    )
            except:
                dbrpsetjson(payload.user_id, "rubles", 0)

        if payload.emoji.name == "4️⃣" and payload.channel_id == 837663284207157339:
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            samsungrole = disnake.utils.get(
                payload.member.guild.roles, id=837312380894969888
            )
            await msg.add_reaction("4️⃣")
            await msg.remove_reaction("4️⃣", payload.member)
            try:
                if samsungrole in payload.member.roles:
                    await payload.member.send(
                        embed=discord.Embed(
                            title="у тебя уже есть Samsung S10+!",
                            description=f"ты не можешь купить Samsung S10+ еще раз!",
                        )
                    )
                elif dbrpgetuser(payload.user_id)["rubles"] >= 86000 + getnalog(86000):
                    dbrpaddrubles(payload.user_id, -86000 + getnalog(86000))

                    await payload.member.send(
                        embed=discord.Embed(
                            title="ты купил Samsung S10+",
                            description=f'ты купил Samsung S10+ за {86000 + getnalog(86000)} {pickform(86000 + getnalog(86000), ["рубль", "рубля", "рублей"])}! теперь у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                        )
                    )
                    await payload.member.add_roles(samsungrole)
                    dbrpaddrubles("federation", 86000 + getnalog(86000))
                    dbrpaddrubles("federation", 86000 + getnds(86000))

                else:
                    await payload.member.send(
                        embed=discord.Embed(
                            title="ты не смог купить Samsung S10+",
                            description=f'ты не можешь купить Samsung S10+! у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {86000 + getnalog(86000)} {pickform(86000 + getnalog(86000), ["рубль", "рубля", "рублей"])}!',
                        )
                    )
            except:
                dbrpsetjson(payload.user_id, "rubles", 0)

        if payload.emoji.name == "5️⃣" and payload.channel_id == 837663284207157339:
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(
                payload.message_id
            )
            i6role = disnake.utils.get(
                payload.member.guild.roles, id=837312385052180490
            )
            await msg.add_reaction("5️⃣")
            await msg.remove_reaction("5️⃣", payload.member)
            try:
                if i6role in payload.member.roles:
                    await payload.member.send(
                        embed=discord.Embed(
                            title="у тебя уже есть iphone 6s!",
                            description=f"ты не можешь купить iphone 6s еще раз!",
                        )
                    )
                elif dbrpgetuser(payload.user_id)["rubles"] >= 34000 + getnalog(34000):
                    dbrpaddrubles(payload.user_id, -34000 + getnalog(34000))

                    await payload.member.send(
                        embed=discord.Embed(
                            title="ты купил iphone 6s",
                            description=f'ты купил iphone 6s за {34000 + getnalog(34000)} {pickform(34000 + getnalog(34000), ["рубль", "рубля", "рублей"])}! теперь у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                        )
                    )
                    await payload.member.add_roles(i6role)
                    dbrpaddrubles("federation", 34000 + getnalog(34000))
                    dbrpaddrubles("federation", 34000 + getnds(34000))

                else:
                    await payload.member.send(
                        embed=discord.Embed(
                            title="ты не смог купить iphone 6s",
                            description=f'ты не можешь купить iphone 6s! у тебя `{dbrpgetuser(payload.user_id)["rubles"]}` {pickform(dbrpgetuser(payload.user_id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {34000 + getnalog(34000)} {pickform(34000 + getnalog(34000), ["рубль", "рубля", "рублей"])}!',
                        )
                    )
            except:
                dbrpsetjson(payload.user_id, "rubles", 0)

        # ---end of shop---#
        # ---start of works--#
        msg = await self.bot.get_channel(payload.channel_id).fetch_message(
            payload.message_id
        )
        if payload.emoji.name == "🧑‍🚒" and payload.channel_id == 835791464109572096:
            await msg.add_reaction("🧑‍🚒")
            await msg.remove_reaction("🧑‍🚒", payload.member)
            if dbrpgetuser(payload.user_id)["rubles"] >= 10:
                dbrpaddrubles(payload.user_id, -10)
                Firerole = disnake.utils.get(
                    payload.member.guild.roles, id=835932798753046578
                )
                await payload.member.add_roles(Firerole)
                await payload.member.send(
                    embed=discord.Embed(
                        title="ты стал пожарным!",
                        description="вы пожарный! вы зарабатываете `143$`/час!",
                    )
                )
            else:

                def check(reaction, user):
                    return (
                        reaction.message.id == message1.id
                        and str(reaction.emoji) == "💸"
                        and user.id == reaction.message.channel.recipient.id
                    )

                chance = random.randint(1, 7)
                message1 = await payload.member.send(
                    embed=discord.Embed(
                        title="ты не смог устроиться на работу",
                        description=f"ты не смог устроиться! у тебя нет денег на стажировку! у тебя есть {chance}% шанс устроиться без денег! нажми на реакцию, если надо. ",
                    ),
                    delete_after=31,
                )
                await message1.add_reaction("💸")
                try:
                    await self.bot.wait_for("reaction_add", check=check, timeout=30)
                    messagee = await payload.member.send(
                        embed=discord.Embed(
                            title="уговариваем работодателя",
                            description=f"пробуем устроить тебя на работу без денег",
                        ),
                        delete_after=31,
                    )
                    await asyncio.sleep(3)
                    if random.randint(1, 100) <= chance:
                        await messagee.edit(
                            embed=discord.Embed(
                                title="получилось!",
                                description=f"ты смог устроиться! поздравляю! ",
                            ),
                            delete_after=31,
                        )
                        dbrpsetjson(payload.user_id, "firefighter", True)
                    else:
                        await messagee.edit(
                            embed=discord.Embed(
                                title="не получилось!",
                                description=f"ты не смог устроиться! увы :( ",
                            ),
                            delete_after=31,
                        )

                except:
                    await payload.member.send(
                        "реакции не было, отменяю!", delete_after=10
                    )
            # ---end of works--#
        # ---start of dark.NET--#
        hardcoin = self.bot.get_emoji(837743558152421477)
        if payload.emoji == hardcoin and payload.channel_id == 837746401520779334:
            await msg.add_reaction(hardcoin)
            await msg.remove_reaction(hardcoin, payload.member)
            try:
                coins = dbrpgetuser(payload.user_id)["darkcoins"]
            except:
                dbrpsetjson(payload.user_id, "darkcoins", "100")
                coins = dbrpgetuser(payload.user_id)["darkcoins"]
            await payload.member.send(
                embed=discord.Embed(
                    title="твоя статистика в dark.NET",
                    description=f"""
            ваш баланс: {coins} <:hardcoin:837743558152421477>
            """,
                ),
                delete_after=60,
            )
            # --end of dark.net--#
        # --start of pen'koff--#
        if payload.emoji.name == "💵" and payload.channel_id == 837748832883966022:
            await msg.add_reaction("💵")
            await msg.remove_reaction("💵", payload.member)
        if payload.emoji.name == "🪙" and payload.channel_id == 837748832883966022:
            await msg.add_reaction("🪙")
            await msg.remove_reaction("🪙", payload.member)
        # ---end of penkoff--#
        # --start of deskinfo--#
        if payload.emoji.name == "❓" and payload.channel_id == 837394878866260019:
            await msg.add_reaction("❓")
            await msg.remove_reaction("❓", payload.member)
            try:
                rubles = dbrpgetuser(payload.user_id)["rubles"]

            except:
                rubles = 0
                dbrpaddrubles(payload.user_id, 0)
            try:
                dollars = dbrpgetuser(payload.user_id)["dollars"]
            except:
                dollars = 0
                dbrpadddollars(payload.user_id, 0)
            await payload.member.send(
                embed=discord.Embed(
                    title="статистика",
                    description=f"""
Паспорт:
```
твое рп имя и фамилия: {dbrpgetuser(payload.user_id)['rpname']}
твой номер паспорта: {dbrpgetuser(payload.user_id)['idrp']}
```
баланс:
```
долларов: {dollars}
рублей: {rubles}
```
""",
                ),
                delete_after=30,
            )
        # --end--#
        # --start of FBI--#
        if payload.emoji.name == "🤑" and payload.channel_id == 838829237770125342:
            await msg.add_reaction("🤑")
            await msg.remove_reaction("🤑", payload.member)
            await payload.member.send("сколько денег взять?")

            def check(author):
                def inner_check(message):
                    return message.author == author and isinstance(
                        message.channel, disnake.DMChannel
                    )

                return inner_check

            try:
                moneyhave = await self.bot.wait_for(
                    "message", check=check(payload.member), timeout=30
                )
                moneyhave = moneyhave.content
            except:
                await payload.member.send("я не могу так долго ждать! ОТМЕНА!!!!")
                return
            try:

                int(moneyhave)

                if int(dbrpgetuser("federation")["rubles"]) < int(moneyhave):
                    await payload.member.send(
                        "в казне нет столько денег! забираю всю казну..."
                    )

                    dbrpaddrubles(
                        payload.user_id, int(dbrpgetuser("federation")["rubles"])
                    )
                    await payload.member.send(
                        f'готово! ты взял {dbrpgetuser("federation")["rubles"]} рублей!'
                    )
                    dbrpaddrubles(
                        "federation", -int(dbrpgetuser("federation")["rubles"])
                    )
                else:
                    dbrpaddrubles("federation", -int(moneyhave))
                    dbrpaddrubles(payload.user_id, int(moneyhave))
                    await payload.member.send(f"готово! ты взял {moneyhave} рублей!")
            except Exception as error:
                await payload.member.send("это не число!")

        if payload.emoji.name == "💰":
            await msg.add_reaction("💰")
            await msg.remove_reaction("💰", payload.member)
            await payload.member.send("сколько денег положить?")

            def check(author):
                def inner_check(message):
                    return message.author == author and isinstance(
                        message.channel, disnake.DMChannel
                    )

                return inner_check

            try:
                moneyhave = await self.bot.wait_for(
                    "message", check=check(payload.member), timeout=30
                )
                moneyhave = moneyhave.content
            except:
                await payload.member.send("я не могу так долго ждать! ОТМЕНА!!!!")
                return
            try:

                int(moneyhave)

                if int(dbrpgetuser(payload.user_id)["rubles"]) < int(moneyhave):
                    await payload.member.send(
                        "у тебя нет столько денег! забираю все..."
                    )

                    dbrpaddrubles(
                        "federation", int(dbrpgetuser(payload.user_id)["rubles"])
                    )
                    await payload.member.send(f"готово! ты положил {moneyhave} рублей!")
                    dbrpaddrubles(
                        payload.user_id, -int(dbrpgetuser(payload.user_id)["rubles"])
                    )
                else:
                    dbrpaddrubles("federation", int(moneyhave))
                    dbrpaddrubles(payload.user_id, -int(moneyhave))
                    await payload.member.send(f"готово! ты положил {moneyhave} рублей!")
            except Exception as error:
                await payload.member.send("это не число!")

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.give_money.start()
        except:
            pass
        try:
            self.give_hp.start()
        except:
            pass

    @tasks.loop(hours=1)
    async def give_money(self):
        firework = dbrpgetcolumn("rp")
        for i in firework:
            if i == "federation":
                return
            try:

                if firework[i]["hunger"] >= 2:
                    dbrpsetjson(i, "hunger", dbrpgetuser(i)["hunger"] - 2)
                    user = self.bot.get_user(int(i))
                    if dbrpgetuser(i)["hunger"] <= 10:
                        await user.send(
                            embed=discord.Embed(
                                title="голод",
                                description=f'ты прогододался! лучше поешь, твой голод равен {dbrpgetuser(i)["hunger"]}/100!',
                            ),
                            delete_after=3600,
                        )
            except KeyError:
                if i != "federation:":
                    dbrpsetjson(i, "hunger", 100)
                    dbrpsetjson(i, "hunger", dbrpgetuser(i)["hunger"] - 2)
                    user = self.bot.get_user(int(i))
                    if dbrpgetuser(i)["hunger"] <= 10:
                        await user.send(
                            embed=discord.Embed(
                                title="голод",
                                description=f'ты прогододался! лучше поешь, твой голод равен {dbrpgetuser(i)["hunger"]}/100!',
                            ),
                            delete_after=3600,
                        )

    @tasks.loop(hours=2)
    async def give_hp(self):
        global user
        firework = dbrpgetcolumn("rp")
        for i in firework:
            try:
                try:
                    if dbrpgetuser(i)["ded"] == "1":
                        return
                except:
                    dbrpsetjson(i, "ded", "0")
                if firework[i]["hunger"] <= 0:
                    user = self.bot.get_user(int(i))
                    if firework[i]["health"] >= 1:
                        dbrpsetjson(i, "health", dbrpgetuser(i)["health"] - 1)
                        if dbrpgetuser(i)["health"] <= 20:
                            if firework[i]["health"] <= 0:
                                await user.send("ты умер")
                            else:
                                await user.send(
                                    embed=discord.Embed(
                                        title="здоровье",
                                        description=f'ты очень нездоров! лучше иди в больницу, твое здоровье равно {dbrpgetuser(i)["health"]}/100!',
                                    ),
                                    delete_after=3600,
                                )

                    elif firework[i]["health"] <= 0:
                        try:
                            await user.send("ты умер")
                        except:
                            ...
                        dbrpsetjson(i, "ded", "1")
            except KeyError:
                if i != "federation:":
                    dbrpsetjson(i, "health", 100)
                    if firework[i]["hunger"] <= 0:
                        user = self.bot.get_user(int(i))
                        if firework[i]["health"] >= 1:
                            dbrpsetjson(i, "health", dbrpgetuser(i)["health"] - 1)
                            if dbrpgetuser(i)["health"] <= 20:
                                if firework[i]["health"] <= 0:
                                    await user.send("ты умер")

                                else:
                                    await user.send(
                                        embed=discord.Embed(
                                            title="здоровье",
                                            description=f'ты очень нездоров! лучше иди в больницу, твое здоровье равно {dbrpgetuser(i)["health"]}/100!',
                                        ),
                                        delete_after=3600,
                                    )
                        elif firework[i]["health"] <= 0:
                            await user.send("ты умер")


def setup(bot):
    bot.add_cog(roleplay(bot))

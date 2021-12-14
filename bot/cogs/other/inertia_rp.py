import datetime
import random
import time
from _random import Random
import disnake
from disnake.ext import commands as commands, tasks
import asyncio
from utils.time import visdelta, pickform
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
    dbrpgetdef,
    dbrpadddollars,
)


guild_ids = [730467133162782760]

rpconfig = {
    "shops": {
        "tech": {
            "channel": 837663284207157339,
            "items": {
                "1": {"price": 45000, "name": "AirPods++"},
                "2": {"price": 234000, "name": "Mac Pro"},
                "3": {"price": 120000, "name": "MacBook"},
            },
        }
    }
}


def getnalog(cost):
    return int(cost * (dbrpgetdef("federation")["nalogi"] / 100))


def getnds(cost):
    return int(cost * (dbrpgetdef("federation")["nds"] / 100))


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
    )
    async def call(self, ctx, human: disnake.Member):
        caller = ctx.author
        user1 = human
        await ctx.send(
            embed=disnake.Embed(
                title="дозвон!", description=f"пробуем дозвониться до {user1}!"
            ),
            ephemeral=True,
        )
        msg = await user1.send(
            embed=disnake.Embed(
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

    """
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
        emb = disnake.Embed(color=disnake.Color.blurple())
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
                    embed=disnake.Embed(
                        title="ошибка",
                        description="у тебя нет столько денег! перевожу все!",
                    )
                )
                money2 = dbrpgetuser(ctx.user.id)["rubles"]
                await dbrpaddmoney(ctx.user.id, -money2)
                await dbrpaddmoney(user.id, money2)

                await msg.edit(
                    embed=disnake.Embed(
                        title="перевод завершен",
                        description=f'ты перевел {money2} {pickform(money2, ["рубль", "рубля", "рублей"])}',
                    )
                )
                await asyncio.sleep(5)
                await msg.delete()
            elif dbrpgetuser(ctx.user.id)["rubles"] >= money:
                await dbrpaddmoney(ctx.user.id, -money)
                await dbrpaddmoney(user.id, money)
                await msg.edit(
                    embed=disnake.Embed(
                        title="перевод завершен",
                        description=f'ты перевел {money} {pickform(money, ["рубль", "рубля", "рублей"])}',
                    )
                )
                await asyncio.sleep(5)
                await msg.delete()
        except Exception as error:
            print(error)
    """

    # This one is similar to the confirmation button except sets the inner value to `False`

    @commands.slash_command(
        guild_ids=guild_ids,
        description="Builds a custom embed",
    )
    async def embed(self, inter, button: bool, select: bool):
        def check(message):
            return message.author == inter.author and message.channel == inter.channel

        await inter.send("Waiting for a title", delete_after=20)
        title = await self.bot.wait_for("message", check=check)
        await title.delete()
        await inter.send("Waiting for a description", delete_after=20)
        desc = await self.bot.wait_for("message", check=check)
        await desc.delete()
        if button or select:
            view = disnake.ui.View()
        if button:
            await inter.send("How many buttons will we add?", delete_after=20)
            kolvo = await self.bot.wait_for("message", check=check)
            await kolvo.delete()
            comps = []
            for i in range(int(kolvo.content)):

                msg = await inter.channel.send("Waiting for a button emoji (react)")

                buttonemoji, user = await self.bot.wait_for("reaction_add")
                view.add_item(
                    item=disnake.ui.Button(
                        emoji=buttonemoji.emoji, style=disnake.ButtonStyle.gray
                    )
                )

                await msg.delete()
        embed = disnake.Embed(
            title=title.content, description=desc.content, color=0x000000
        )
        if button and not select:
            return await inter.channel.send(embed=embed, view=view)
        if select:
            await inter.send("How many select options will we add?", delete_after=20)
            kolvosel = await self.bot.wait_for("message", check=check)
            await kolvosel.delete()
            await inter.send("Min values?", delete_after=20)
            minvals = await self.bot.wait_for("message", check=check)
            await minvals.delete()
            await inter.send("max values?", delete_after=20)
            maxvals = await self.bot.wait_for("message", check=check)
            await maxvals.delete()
            await inter.send("placeholder for select? (write `None` for no)")
            placehmsg = await self.bot.wait_for("message", check=check, timeout=30)
            placeh = placehmsg.content
            if placeh == "None":
                placeh = None
                await inter.send("No placeholder.", delete_after=5)
            await placehmsg.delete()
            if placeh:
                sel = disnake.ui.Select(
                    max_values=maxvals.content,
                    min_values=minvals.content,
                    placeholder=placeh,
                )
            else:
                sel = disnake.ui.Select(
                    max_values=maxvals.content, min_values=minvals.content
                )
            view.add_item(item=sel)
            comps = []
            for i in range(int(kolvosel.content)):

                msg = await inter.channel.send("Waiting for a select emoji (react)")

                selemoji, user = await self.bot.wait_for("reaction_add")
                await msg.delete()
                await inter.send("label for select?", delete_after=20)
                textsel = await self.bot.wait_for("message", check=check)
                await textsel.delete()
                await inter.send("value for select?", delete_after=20)
                valsel = await self.bot.wait_for("message", check=check)
                await valsel.delete()
                await inter.send(
                    "description for select? (write `None` for no)", delete_after=30
                )
                seldescmsg = await self.bot.wait_for("message", check=check)
                seldesc = seldescmsg.content
                if seldesc == "None":
                    seldesc = None
                    await inter.send("No description.", delete_after=5)
                await seldescmsg.delete()
                if seldesc:
                    sel.add_option(
                        label=textsel.content,
                        emoji=selemoji.emoji,
                        value=valsel.content,
                        description=seldesc,
                    )
                else:
                    sel.add_option(
                        label=textsel.content,
                        emoji=selemoji.emoji,
                        value=valsel.content,
                    )

        if select:
            return await inter.channel.send(embed=embed, view=view)
        return await inter.channel.send(embed=embed)

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
    async def on_button_click(self, payload):
        print(payload)
        # -----start of reg----#
        await payload.response.defer()
        if payload.author == self.bot.user:
            return
        Channel = self.bot.get_channel(837345395667501118)
        if (
            payload.component.emoji.name == "🛬"
            and payload.channel.id == 837345395667501118
        ):
            msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                payload.message.id
            )
            Role = disnake.utils.get(payload.author.guild.roles, id=837312438881353748)
            await payload.author.add_roles(Role)
            await Channel.send(
                embed=disnake.Embed(
                    title="прилет", description=f"{payload.author.mention} прилетел!"
                ),
                delete_after=5,
            )
            # -----end of reg----#
        # -----start of passport----#
        if (
            payload.component.emoji.name == "📝"
            and payload.channel.id == 837312495634481202
        ):
            msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                payload.message.id
            )
            await payload.author.send(
                embed=disnake.Embed(
                    title="регистрация",
                    description=f"{payload.author.mention}, регистрируйся!",
                ),
                delete_after=5,
            )
            await payload.author.send(
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
                    "message", check=check(payload.author), timeout=30
                )
                regname = regname.content
            except:
                await payload.author.send(
                    "я не могу так долго ждать! твое имя станет твоим дискорд именем!"
                )
                regname = payload.author.name
            await payload.author.send(
                "напиши свои навыки в РП. (типо лечения болезней)", delete_after=60
            )
            try:
                regnaviki = await self.bot.wait_for(
                    "message", check=check(payload.author), timeout=30
                )
                regnaviki = regnaviki.content
            except Exception as error:
                await payload.author.send(
                    "я не могу так долго ждать! ты будешь уметь жить!"
                )
                regnaviki = "жить"

            dbsetrp(payload.author.id, str(regname), str(regnaviki))
            if not len(f"{regname} | {dbgetrpid(payload.author.id)}") > 32:
                try:
                    await payload.author.edit(
                        nick=f"{regname} | {dbgetrpid(payload.author.id)}"
                    )
                except:
                    await payload.author.send("ты овнер?")
            else:
                await payload.author.send(
                    "слишком длинный ник! твой ник будет твоим дискорд ником!"
                )
                await payload.author.edit(
                    nick=f"{payload.author.name} | {dbgetrpid(payload.author.id)}"
                )
            await payload.author.send(
                embed=disnake.Embed(
                    title="регистрация",
                    description="ты прошел регистрацию! приятного рп!",
                ),
                delete_after=20,
            )
            rolee = payload.author.guild.get_role(837312438881353748)
            await payload.author.remove_roles(rolee)
            Role = disnake.utils.get(payload.author.guild.roles, id=837340231937818636)
            await payload.author.add_roles(Role)
            docschannel = self.bot.get_channel(837312548856135720)
            await docschannel.send(
                embed=disnake.Embed(
                    title="регистрация!",
                    description=f"""
имя человека: {payload.author.mention}.
рп имя и фамилия: {regname}
навыки: {regnaviki}
номер человека: {dbgetrpid(payload.author.id)}
            """,
                )
            )

            # -----end of passport----#
        # ------start of BOMZ------#
        if (
            payload.component.emoji.name == "🙏"
            and payload.channel.id == 837340041176416277
        ):
            try:
                if (
                    int(dbrpgetuser(payload.author.id)["rubles"]) >= 150
                    and dbrpgetuser(payload.author.id)["home"] == True
                    or int(dbrpgetuser(payload.author.id)["rubles"]) >= 600
                ):
                    Rolebomz = disnake.utils.get(
                        payload.author.guild.roles, id=835462674879741962
                    )
                    Roleman = disnake.utils.get(
                        payload.author.guild.roles, id=835539034914029618
                    )
                    await payload.author.remove_roles(Rolebomz)
                    await payload.author.add_roles(Roleman)
                    await payload.author.send(
                        "ВНИМАНИЕ! ЭТО ТВОИ ПОСЛЕДНИЕ ДЕНЬГИ! если ты еще не купил дом (400$), купи его! купи машину (100$), бензин (20$), заполни резме (50%) и найди работу!"
                    )
                    msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                        payload.message.id
                    )

                    return
            except KeyError:
                dbrpsethome(payload.author.id, False)
                if (
                    int(dbrpgetuser(payload.author.id)["rubles"]) >= 500
                    and dbrpgetuser(payload.author.id)["home"] == True
                    or int(dbrpgetuser(payload.author.id)["rubles"]) >= 600
                ):
                    Rolebomz = disnake.utils.get(
                        payload.author.guild.roles, id=835462674879741962
                    )
                    Roleman = disnake.utils.get(
                        payload.author.guild.roles, id=835539034914029618
                    )
                    await payload.author.remove_roles(Rolebomz)
                    await payload.author.add_roles(Roleman)
                    await payload.author.send(
                        "ВНИМАНИЕ! ЭТО ТВОИ ПОСЛЕДНИЕ ДЕНЬГИ! если ты еще не купил дом (400$), купи его! купи машину (100$), бензин (20$), заполни резме (50%) и найди работу!"
                    )
                    msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                        payload.message.id
                    )

                    return
            if random.randint(1, 100) > 20:
                money = random.randint(2, 4)
                dbrpaddmoney(payload.author.id, money)

                await payload.author.send(f"ты получил {money} рубля!")
            else:
                await payload.author.send("увы, вам не дали денег. попробуй еще!")
            msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                payload.message.id
            )

            # ----end of BOMZ----#

        # ---start of works--#
        msg = await self.bot.get_channel(payload.channel.id).fetch_message(
            payload.message.id
        )
        if (
            payload.component.emoji.name == "🧑‍🚒"
            and payload.channel.id == 835791464109572096
        ):
            await msg.add_reaction("🧑‍🚒")
            await msg.remove_reaction("🧑‍🚒", payload.author)
            if dbrpgetuser(payload.author.id)["rubles"] >= 10:
                dbrpaddmoney(payload.author.id, -10)
                Firerole = disnake.utils.get(
                    payload.author.guild.roles, id=835932798753046578
                )
                await payload.author.add_roles(Firerole)
                await payload.author.send(
                    embed=disnake.Embed(
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
                message1 = await payload.author.send(
                    embed=disnake.Embed(
                        title="ты не смог устроиться на работу",
                        description=f"ты не смог устроиться! у тебя нет денег на стажировку! у тебя есть {chance}% шанс устроиться без денег! нажми на реакцию, если надо. ",
                    ),
                    delete_after=31,
                )
                await message1.add_reaction("💸")
                try:
                    await self.bot.wait_for("reaction_add", check=check, timeout=30)
                    messagee = await payload.author.send(
                        embed=disnake.Embed(
                            title="уговариваем работодателя",
                            description=f"пробуем устроить тебя на работу без денег",
                        ),
                        delete_after=31,
                    )
                    await asyncio.sleep(3)
                    if random.randint(1, 100) <= chance:
                        await messagee.edit(
                            embed=disnake.Embed(
                                title="получилось!",
                                description=f"ты смог устроиться! поздравляю! ",
                            ),
                            delete_after=31,
                        )
                        dbrpsetjson(payload.author.id, "firefighter", True)
                    else:
                        await messagee.edit(
                            embed=disnake.Embed(
                                title="не получилось!",
                                description=f"ты не смог устроиться! увы :( ",
                            ),
                            delete_after=31,
                        )

                except:
                    await payload.author.send(
                        "реакции не было, отменяю!", delete_after=10
                    )
            # ---end of works--#
        # ---start of dark.NET--#
        hardcoin = self.bot.get_emoji(837743558152421477)
        if (
            payload.component.emoji == hardcoin
            and payload.channel.id == 837746401520779334
        ):
            await msg.add_reaction(hardcoin)
            await msg.remove_reaction(hardcoin, payload.author)
            try:
                coins = dbrpgetuser(payload.author.id)["darkcoins"]
            except:
                dbrpsetjson(payload.author.id, "darkcoins", "100")
                coins = dbrpgetuser(payload.author.id)["darkcoins"]
            await payload.author.send(
                embed=disnake.Embed(
                    title="твоя статистика в dark.NET",
                    description=f"""
            ваш баланс: {coins} <:hardcoin:837743558152421477>
            """,
                ),
                delete_after=60,
            )
            # --end of dark.net--#
        # --start of pen'koff--#
        if (
            payload.component.emoji.name == "💵"
            and payload.channel.id == 837748832883966022
        ):
            pass
        if (
            payload.component.emoji.name == "🪙"
            and payload.channel.id == 837748832883966022
        ):
            pass
        # ---end of penkoff--#
        # --start of deskinfo--#
        if (
            payload.component.emoji.name == "❓"
            and payload.channel.id == 837394878866260019
        ):

            try:
                rubles = dbrpgetuser(payload.author.id)["rubles"]

            except:
                rubles = 0
                dbrpaddmoney(payload.author.id, 0)
            try:
                dollars = dbrpgetuser(payload.author.id)["dollars"]
            except:
                dollars = 0
                dbrpadddollars(payload.author.id, 0)
            await payload.author.send(
                embed=disnake.Embed(
                    title="статистика",
                    description=f"""
Паспорт:
```
твое рп имя и фамилия: {dbrpgetuser(payload.author.id)['rpname']}
твой номер паспорта: {dbrpgetuser(payload.author.id)['idrp']}
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
        if (
            payload.component.emoji.name == "🤑"
            and payload.channel.id == 838829237770125342
        ):

            await payload.author.send("сколько денег взять?")

            def check(author):
                def inner_check(message):
                    return message.author == author and isinstance(
                        message.channel, disnake.DMChannel
                    )

                return inner_check

            try:
                moneyhave = await self.bot.wait_for(
                    "message", check=check(payload.author), timeout=30
                )
                moneyhave = moneyhave.content
            except:
                await payload.author.send("я не могу так долго ждать! ОТМЕНА!!!!")
                return
            try:

                int(moneyhave)

                if int(dbrpgetuser("federation")["rubles"]) < int(moneyhave):
                    await payload.author.send(
                        "в казне нет столько денег! забираю всю казну..."
                    )

                    dbrpaddmoney(
                        payload.author.id, int(dbrpgetuser("federation")["rubles"])
                    )
                    await payload.author.send(
                        f'готово! ты взял {dbrpgetuser("federation")["rubles"]} рублей!'
                    )
                    dbrpaddmoney(
                        "federation", -int(dbrpgetuser("federation")["rubles"])
                    )
                else:
                    dbrpaddmoney("federation", -int(moneyhave))
                    dbrpaddmoney(payload.author.id, int(moneyhave))
                    await payload.author.send(f"готово! ты взял {moneyhave} рублей!")
            except Exception as error:
                await payload.author.send("это не число!")

        if payload.component.emoji.name == "💰":

            await payload.author.send("сколько денег положить?")

            def check(author):
                def inner_check(message):
                    return message.author == author and isinstance(
                        message.channel, disnake.DMChannel
                    )

                return inner_check

            try:
                moneyhave = await self.bot.wait_for(
                    "message", check=check(payload.author), timeout=30
                )
                moneyhave = moneyhave.content
            except:
                await payload.author.send("я не могу так долго ждать! ОТМЕНА!!!!")
                return
            try:

                int(moneyhave)

                if int(dbrpgetuser(payload.author.id)["rubles"]) < int(moneyhave):
                    await payload.author.send(
                        "у тебя нет столько денег! забираю все..."
                    )

                    dbrpaddmoney(
                        "federation", int(dbrpgetuser(payload.author.id)["rubles"])
                    )
                    await payload.author.send(f"готово! ты положил {moneyhave} рублей!")
                    dbrpaddmoney(
                        payload.author.id,
                        -int(dbrpgetuser(payload.author.id)["rubles"]),
                    )
                else:
                    dbrpaddmoney("federation", int(moneyhave))
                    dbrpaddmoney(payload.author.id, -int(moneyhave))
                    await payload.author.send(f"готово! ты положил {moneyhave} рублей!")
            except Exception as error:
                await payload.author.send("это не число!")

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
        ch = await self.bot.fetch_channel(837345395667501118)

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
                            embed=disnake.Embed(
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
                            embed=disnake.Embed(
                                title="голод",
                                description=f'ты прогододался! лучше поешь, твой голод равен {dbrpgetuser(i)["hunger"]}/100!',
                            ),
                            delete_after=3600,
                        )

    @tasks.loop(hours=2)
    async def give_hp(self):
        global user
        firework = dbrpgetcolumn("rp")["users"]
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
                                    embed=disnake.Embed(
                                        title="здоровье",
                                        description=f'ты очень нездоров! лучше иди в больницу, твое здоровье равно {dbrpgetuser(i)["health"]}/100!',
                                    ),
                                    delete_after=1800,
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
                                        embed=disnake.Embed(
                                            title="здоровье",
                                            description=f'ты очень нездоров! лучше иди в больницу, твое здоровье равно {dbrpgetuser(i)["health"]}/100!',
                                        ),
                                        delete_after=3600,
                                    )
                        elif firework[i]["health"] <= 0:
                            await user.send("ты умер")

    @commands.Cog.listener()
    async def on_dropdown(self, payload):
        print(payload.data.values)
        await payload.response.defer()
        # ----start of shop--#

        msg = await self.bot.get_channel(payload.channel.id).fetch_message(
            payload.message.id
        )
        for value in payload.data.values:
            if str(value) == "1" and payload.channel.id == 837663284207157339:

                airrole = disnake.utils.get(
                    payload.author.guild.roles, id=837312389102698516
                )
                if airrole in payload.author.roles:
                    await payload.send(
                        embed=disnake.Embed(
                            title="у тебя уже есть airpods++",
                            description=f"ты не можешь купить те же наушники!",
                        ),
                        ephemeral=True,
                    )
                elif int(dbrpgetuser(payload.author.id)["rubles"]) >= (
                    45000 + getnalog(45000)
                ):
                    dbrpaddmoney(payload.author.id, -(45000 + getnalog(45000)))
                    await payload.author.add_roles(airrole)
                    await payload.send(
                        embed=disnake.Embed(
                            title="ты купил airpods++",
                            description=f'ты купил airpods++ за {(45000 + getnalog(45000))} {pickform(45000 + getnalog(45000), ["рубль", "рубля", "рублей"])} (с учетом коммисии)! теперь у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                        ),
                        ephemeral=True,
                    )
                    await dbrpaddmoney("federation", +(getnalog(45000)))
                    await dbrpaddmoney("federation", +(getnds(45000)))

                else:
                    await payload.send(
                        embed=disnake.Embed(
                            title="ты не смог купить airpods++",
                            description=f'ты не можешь купить airpods++! у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {(45000 + getnalog(45000))} {pickform(45000 + getnalog(45000), ["рубль", "рубля", "рублей"])} (с учетом коммисии в 2%)!',
                        ),
                        ephemeral=True,
                    )

            msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                payload.message.id
            )
            if value == "2" and payload.channel.id == 837663284207157339:
                macrole = disnake.utils.get(
                    payload.author.guild.roles, id=837312392118927370
                )

                if macrole in payload.author.roles:
                    await payload.author.send(
                        embed=disnake.Embed(
                            title="у тебя уже есть mac pro",
                            description=f"ты не можешь купить еще 1 mac pro!",
                        )
                    )

                elif dbrpgetuser(payload.author.id)["rubles"] >= (
                    234000 + getnalog(234000)
                ):
                    dbrpaddmoney(payload.author.id, -(234000 + getnalog(234000)))
                    await payload.author.add_roles(macrole)
                    await payload.author.send(
                        embed=disnake.Embed(
                            title="ты купил mac pro",
                            description=f'ты купил mac pro за {(234000 + getnalog(234000))} {pickform(234000 + getnalog(234000), ["рубль", "рубля", "рублей"])} теперь у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                        )
                    )
                    dbrpaddmoney("federation", getnalog(234000))
                    await dbrpaddmoney("federation", getnds(234000))

                else:
                    await payload.author.send(
                        embed=disnake.Embed(
                            title="ты не смог купить mac pro",
                            description=f'ты не можешь купить mac pro! у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {(234000 + getnalog(234000))} {pickform(234000 + getnalog(234000), ["рубль", "рубля", "рублей"])}!',
                        )
                    )

            if value == "3" and payload.channel.id == 837663284207157339:

                msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                    payload.message.id
                )
                macbookrole = disnake.utils.get(
                    payload.author.guild.roles, id=837312387375562832
                )

                try:
                    if macbookrole in payload.author.roles:
                        await payload.author.send(
                            embed=disnake.Embed(
                                title="у тебя уже есть macbook!",
                                description=f"ты не можешь купить macbook еще раз!",
                            )
                        )
                    elif dbrpgetuser(payload.author.id)["rubles"] >= 120000 + getnalog(
                        120000
                    ):
                        dbrpaddmoney(payload.author.id, -(120000 + getnalog(120000)))

                        await payload.author.send(
                            embed=disnake.Embed(
                                title="ты купил macbook",
                                description=f'ты купил macbook за {120000 + getnalog(120000)} {pickform(120000 + getnalog(120000), ["рубля", "рубль", "рублей"])}! теперь у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                            )
                        )
                        await payload.author.add_roles(macbookrole)
                        dbrpaddmoney("federation", getnalog(120000))
                        dbrpaddmoney("federation", getnds(120000))

                    else:
                        await payload.author.send(
                            embed=disnake.Embed(
                                title="ты не смог купить macbook",
                                description=f'ты не можешь купить macbook! у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {120000 + getnalog(120000)} {pickform(120000 + getnalog(120000), ["рубль", "рубля", "рублей"])}!',
                            )
                        )
                except:
                    dbrpsetjson(payload.author.id, "rubles", 0)

            if value == "4" and payload.channel.id == 837663284207157339:
                msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                    payload.message.id
                )
                samsungrole = disnake.utils.get(
                    payload.author.guild.roles, id=837312380894969888
                )
                try:
                    if samsungrole in payload.author.roles:
                        await payload.author.send(
                            embed=disnake.Embed(
                                title="у тебя уже есть Samsung S10+!",
                                description=f"ты не можешь купить Samsung S10+ еще раз!",
                            )
                        )
                    elif dbrpgetuser(payload.author.id)["rubles"] >= 86000 + getnalog(
                        86000
                    ):
                        dbrpaddmoney(payload.author.id, -(86000 + getnalog(86000)))

                        await payload.author.send(
                            embed=disnake.Embed(
                                title="ты купил Samsung S10+",
                                description=f'ты купил Samsung S10+ за {86000 + getnalog(86000)} {pickform(86000 + getnalog(86000), ["рубль", "рубля", "рублей"])}! теперь у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                            )
                        )
                        await payload.author.add_roles(samsungrole)
                        dbrpaddmoney("federation", getnalog(86000))
                        dbrpaddmoney("federation", getnds(86000))

                    else:
                        await payload.author.send(
                            embed=disnake.Embed(
                                title="ты не смог купить Samsung S10+",
                                description=f'ты не можешь купить Samsung S10+! у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {86000 + getnalog(86000)} {pickform(86000 + getnalog(86000), ["рубль", "рубля", "рублей"])}!',
                            )
                        )
                except:
                    dbrpsetjson(payload.author.id, "rubles", 0)

            if value == "5" and payload.channel.id == 837663284207157339:
                msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                    payload.message.id
                )
                i6role = disnake.utils.get(
                    payload.author.guild.roles, id=837312385052180490
                )

                try:
                    if i6role in payload.author.roles:
                        await payload.author.send(
                            embed=disnake.Embed(
                                title="у тебя уже есть iphone 6s!",
                                description=f"ты не можешь купить iphone 6s еще раз!",
                            )
                        )
                    elif dbrpgetuser(payload.author.id)["rubles"] >= 34000 + getnalog(
                        34000
                    ):
                        dbrpaddmoney(payload.author.id, -(34000 + getnalog(34000)))

                        await payload.author.send(
                            embed=disnake.Embed(
                                title="ты купил iphone 6s",
                                description=f'ты купил iphone 6s за {34000 + getnalog(34000)} {pickform(34000 + getnalog(34000), ["рубль", "рубля", "рублей"])}! теперь у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                            )
                        )
                        await payload.author.add_roles(i6role)
                        dbrpaddmoney("federation", getnalog(34000))
                        dbrpaddmoney("federation", getnds(34000))

                    else:
                        await payload.author.send(
                            embed=disnake.Embed(
                                title="ты не смог купить iphone 6s",
                                description=f'ты не можешь купить iphone 6s! у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {34000 + getnalog(34000)} {pickform(34000 + getnalog(34000), ["рубль", "рубля", "рублей"])}!',
                            )
                        )
                except:
                    dbrpsetjson(payload.author.id, "rubles", 0)
            if value == "6" and payload.channel.id == 837663284207157339:
                msg = await self.bot.get_channel(payload.channel.id).fetch_message(
                    payload.message.id
                )
                nokiarole = disnake.utils.get(
                    payload.author.guild.roles, id=837312384355401778
                )

                try:
                    if nokiarole in payload.author.roles:
                        await payload.author.send(
                            embed=disnake.Embed(
                                title="у тебя уже есть nokia 3310!",
                                description=f"ты не можешь купить nokia 3310 еще раз!",
                            )
                        )
                    elif dbrpgetuser(payload.author.id)["rubles"] >= 700 + getnalog(
                        700
                    ):
                        dbrpaddmoney(payload.author.id, -(700 + getnalog(700)))

                        await payload.author.send(
                            embed=disnake.Embed(
                                title="ты купил nokia 3310",
                                description=f'ты купил nokia 3310 за {700 + getnalog(700)} {pickform(700 + getnalog(700), ["рубль", "рубля", "рублей"])}! теперь у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}!',
                            )
                        )
                        await payload.author.add_roles(nokiarole)
                        dbrpaddmoney("federation", getnalog(700))
                        dbrpaddmoney("federation", getnds(700))

                    else:
                        await payload.author.send(
                            embed=disnake.Embed(
                                title="ты не смог купить nokia 3310",
                                description=f'ты не можешь купить nokia 3310! у тебя `{dbrpgetuser(payload.author.id)["rubles"]}` {pickform(dbrpgetuser(payload.author.id)["rubles"], ["рубль", "рубля", "рублей"])}, а надо {700 + getnalog(700)} {pickform(700 + getnalog(700), ["рубль", "рубля", "рублей"])}!',
                            )
                        )
                except:
                    dbrpsetjson(payload.author.id, "rubles", 0)

        # ---end of shop---#


def setup(bot):
    bot.add_cog(roleplay(bot))

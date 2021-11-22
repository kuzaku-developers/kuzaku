from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import disnake
import io


class CardError(Exception):
    pass


class RankCard:
    def __init__(self):
        self.backgroundType = "color"
        self.backgroundImg = ""
        self.backgroundColor = "#fff"
        self.textColor = "#fff"
        self.status = disnake.Status
        self.statusBack = "#000"
        self.avatar = "https://cdn0.iconfinder.com/data/icons/pinpoint-notifocation/48/none-512.png"
        self.avatarBack = "#000"
        self.name = "NoName"
        self.lvl = 0
        self.xp = 0
        self.xp2 = 0
        self.tag = 0000
        self.proc = 1
        self.textStyles = None
        self.barColor = "#0ff"
        self.barBackColor = "#000"
        self.displayProc = False

    async def setBackground(self, url: str = None, color: str = None):
        if url is None:
            if color is None:
                self.backgroundType = "color"
                self.backgroundColor = "#2f2d30"
            else:
                self.backgroundType = "color"
                self.backgroundColor = color
        else:
            self.backgroundType = "img"
            self.backgroundImg = url

    async def setTextColor(self, color: str = None):
        if color is None:
            raise CardError("[TextColor] Укажите цвет для текста!")
        else:
            self.textColor = color

    async def setStatus(self, status: disnake.Status = None):
        if status is None:
            raise CardError("[Status] Укажите статус!")
        elif status == disnake.Status.idle:
            self.status = "idle"
        elif status == disnake.Status.online:
            self.status = "online"
        elif status == disnake.Status.offline:
            self.status = "offline"
        elif status == disnake.Status.dnd:
            self.status = "dnd"
        else:
            raise CardError("[Status] Используйте класс disnake.Status!")

    async def setStatusBack(self, color: str = None):
        if color is None:
            raise CardError("[StatusBack] Укажите цвет!")
        else:
            self.statusBack = color

    async def setAvatar(self, avatar: str = None):
        if avatar is None:
            raise CardError("[Avatar] Укажите аватарку!")
        else:
            self.avatar = avatar

    async def setAvatarBack(self, color: str = None):
        if color is None:
            self.avatarBack = "#fff0"
        else:
            self.avatarBack = color

    async def setName(self, name: str = None):
        if name is None:
            raise CardError("[Name] Укажите ник!")
        else:
            self.name = name

    async def setTag(self, tag: int = None):
        if tag is None:
            raise CardError("[Tag] Укажите тэг!")
        else:
            self.tag = tag

    async def setLvl(self, lvl: int = None):
        if lvl is None:
            raise CardError("[Lvl] Укажите уровень!")
        else:
            self.lvl = lvl

    async def setXp(self, xp: int = None):
        if xp is None:
            raise CardError("[Xp] Укажите xp!")
        else:
            self.xp = xp

    async def setXpToNextLvl(self, xp: int = None):
        if xp is None:
            raise CardError("[XpToNextLvl] Укажите xp!")
        else:
            self.xp2 = xp
            self.proc = round(self.xp / xp * 100)

    async def setTextStyle(self, path: str = None):
        if path is None:
            raise CardError("[TextStyle] Укажите путь к стилю текста!")
        else:
            self.textStyle = path

    async def setBarColor(self, color: str = None):
        if color is None:
            raise CardError("[BarColor] Укажите цвет!")
        else:
            self.barColor = color

    async def setBarBack(self, color: str = None):
        if color is None:
            raise CardError("[BarBack] Укажите цвет!")
        else:
            self.barBackColor = color

    async def setDisplayProcents(self, display: bool = None):
        if display is None:
            raise CardError(
                "[DisplayProcents] Укажите True или False(False - изначально)!"
            )
        elif display == True:
            self.displayProc = True
        elif display == False:
            self.displayProc = False
        else:
            raise CardError("[DisplayProcents] True или False")

    async def create(self, path=None):
        img = None
        if self.backgroundType == "img":
            url = requests.get(self.backgroundImg, stream=True).raw
            img = Image.open(url).resize((1270, 381))
            img = img.convert("RGBA")
        elif self.backgroundType == "color":
            img = Image.new("RGBA", (1270, 381), self.backgroundColor)
            # | Системное | #

        def prepare_mask(size, antialias=2, otc=None):
            mask = Image.new("L", (size[0] * antialias, size[1] * antialias), 0)
            ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255, outline=otc)
            return mask.resize(size, Image.ANTIALIAS)

        def crop(im, s):
            w, h = im.size
            k = w / s[0] - h / s[1]
            if k > 0:
                im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
            elif k < 0:
                im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
            return im.resize(s, Image.ANTIALIAS)

        # | --------- | #
        # | Статус | #
        def status():
            if self.status == "idle":
                return (
                    Image.open(
                        requests.get(
                            "https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F763196801741881344.png%3Fv%3D1&w=64&q=75",
                            stream=True,
                        ).raw
                    )
                    .convert("RGBA")
                    .resize((80, 80), Image.ANTIALIAS)
                )
            elif self.status == "online":
                return (
                    Image.open(
                        requests.get(
                            "https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F782348522681925672.png%3Fv%3D1&w=64&q=75",
                            stream=True,
                        ).raw
                    )
                    .convert("RGBA")
                    .resize((80, 80), Image.ANTIALIAS)
                )
            elif self.status == "offline":
                return (
                    Image.open(
                        requests.get(
                            "https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F752991021180256266.png%3Fv%3D1&w=64&q=75",
                            stream=True,
                        ).raw
                    )
                    .convert("RGBA")
                    .resize((80, 80), Image.ANTIALIAS)
                )
            elif self.status == "dnd":
                return (
                    Image.open(
                        requests.get(
                            "https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F782302404581785611.png%3Fv%3D1&w=64&q=75",
                            stream=True,
                        ).raw
                    )
                    .convert("RGBA")
                    .resize((80, 80), Image.ANTIALIAS)
                )
            else:
                return (
                    Image.open(
                        requests.get(
                            "https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F769033608924233768.png%3Fv%3D1&w=64&q=75",
                            stream=True,
                        ).raw
                    )
                    .convert("RGBA")
                    .resize((80, 80), Image.ANTIALIAS)
                )

        # | ------ | #
        # | Аватар | #
        avatar = Image.open(requests.get(self.avatar, stream=True).raw).convert("RGBA")
        size = (240, 240)

        avatar = crop(avatar, size)
        avatar.putalpha(prepare_mask(size, 4))
        # | ------ | #

        # | XP | #
        def xp(xp_proc, color):
            xp_proc = xp_proc + xp_proc * 8 - 50
            if xp_proc <= 0:
                xp_proc = 1
            img = Image.new("RGBA", (xp_proc, 50), color)
            return img

        def datexp():
            if self.lvl < 999:
                return self.xp2
            elif self.lvl >= 999:
                return "Infinity"

        # | -- | #
        name = self.name
        tag = self.tag

        line1 = xp(100, self.barBackColor)
        line2 = 0
        if datexp() == "Infinity":
            line2 = xp(100, self.barColor)
        else:
            line2 = xp(self.proc, self.barColor)

        background = Image.new("RGBA", (1230, 341), "#0000008a")
        # | Фоны | #
        statusback = Image.new("RGBA", (82, 82), self.statusBack)
        statusback = crop(statusback, (82, 82))
        statusback.putalpha(prepare_mask((82, 82), 4))
        avatarback = Image.new("RGBA", (248, 248), self.avatarBack)
        avatarback = crop(avatarback, (248, 248))
        avatarback.putalpha(prepare_mask((248, 248), 4))
        # | ---- | #

        img.paste(background, (20, 20), background)
        img.paste(avatarback, (956, 66), avatarback)
        img.paste(avatar, (960, 70), avatar)
        img.paste(line1, (80, 245), line1)
        img.paste(line2, (80, 245), line2)
        if datexp() == "Infinity":
            inf = (
                Image.open(
                    requests.get(
                        "https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F798251908862705706.png%3Fv%3D1&w=64&q=75",
                        stream=True,
                    ).raw
                )
                .convert("RGBA")
                .resize((50, 45), Image.ANTIALIAS)
            )
            img.paste(inf, (490, 248), inf)
        img.paste(statusback, (1128, 228), statusback)
        img.paste(status(), (1130, 230), status())

        idraw = ImageDraw.Draw(img)

        nameline = ImageFont.truetype(self.textStyle, size=50)
        lvlline = ImageFont.truetype(self.textStyle, size=40)
        xpline = ImageFont.truetype(self.textStyle, size=45)

        if len(name) > 10:
            for n in name:
                if len(name) > 10:
                    name = name[:-1]
            name = name + "..."

        xp_ = 620
        xps = self.xp
        xps2 = self.xp2
        if len(f"{xps2}") == 2:
            if len(f"{xps}") == 1:
                xp_ = xp_ + 350
            elif len(f"{xps}") == 2:
                xp_ = xp_ + 300
        elif len(f"{xps2}") == 3:
            if len(f"{xps}") == 1:
                xp_ = xp_ + 150
            elif len(f"{xps}") == 2:
                xp_ = xp_ + 140
            elif len(f"{xps}") == 3:
                xp_ = xp_ + 130
        elif len(f"{xps2}") == 4:
            if len(f"{xps}") == 1:
                xp_ = xp_ + 110
            elif len(f"{xps}") == 2:
                xp_ = xp_ + 100
            elif len(f"{xps}") == 3:
                xp_ = xp_ + 90
            elif len(f"{xps}") == 4:
                xp_ = xp_ + 60
        elif len(f"{xps2}") == 5:
            if len(f"{xps}") == 1:
                xp_ = xp_ + 90
            elif len(f"{xps}") == 2:
                xp_ = xp_ + 80
            elif len(f"{xps}") == 3:
                xp_ = xp_ + 70
            elif len(f"{xps}") == 4:
                xp_ = xp_ + 60
            elif len(f"{xps}") == 5:
                xp_ = xp_ + 50
        elif datexp() == "Infinity":
            if len(f"{xps}") == 1:
                xp_ = xp_ + 70
            elif len(f"{xps}") == 2:
                xp_ = xp_ + 60
            elif len(f"{xps}") == 3:
                xp_ = xp_ + 20
            elif len(f"{xps}") == 4:
                xp_ = xp_ + 15
            elif len(f"{xps}") == 5:
                xp_ = xp_ - 5
            elif len(f"{xps}") == 6:
                xp_ = xp_ - 10
        elif len(f"{xps2}") == 6:
            if len(f"{xps}") == 1:
                xp_ = xp_ - 70
            elif len(f"{xps}") == 2:
                xp_ = xp_ - 60
            elif len(f"{xps}") == 3:
                xp_ = xp_ + 15
            elif len(f"{xps}") == 4:
                xp_ = xp_ - 40
            elif len(f"{xps}") == 5:
                xp_ = xp_ - 30
            elif len(f"{xps}") == 6:
                xp_ = xp_ - 20

        if self.displayProc == True and datexp() != "Infinity":
            idraw.text((800, 245), f"{self.proc}%", font=xpline, fill=self.textColor)
        else:
            pass

        idraw.text((90, 170), f"{name}#{tag}", font=nameline, fill=self.textColor)
        idraw.text((45, 40), f"LEVEL {self.lvl}", font=lvlline, fill=self.textColor)
        idraw.text(
            (xp_, 175), f"{self.xp}/{datexp()}", font=xpline, fill=self.textColor
        )

        if path is None:
            data = io.BytesIO()
            img.save(data, "png")
            file = io.BytesIO(data.getvalue())
            return file
        elif type(path) == str:
            img.save(path)
        else:
            raise CardError("[Create] Путь неверный!")


class WelcomeCard:
    def __init__(self):
        self.avatar = "https://cdn0.iconfinder.com/data/icons/pinpoint-notifocation/48/none-512.png"
        self.avatarBack = "#0ff"
        self.savatar = "https://cdn0.iconfinder.com/data/icons/pinpoint-notifocation/48/none-512.png"
        self.savatarBack = "#000"
        self.background = "#000"
        self.abackground = "https://2.bp.blogspot.com/-JXxwkcanA7U/VwzeoorCXAI/AAAAAAAAIs0/HwR2GkxxGkItEhmchUcDyT9FHEt-MV5tACLcB/s1600/Another%2BSnapshot%2Bof%2BMilky%2BWay.png"
        self.textStyle = ""
        self.textColor = "#fff"
        self.welcColor = "#0ff"
        self.abackgroundBack = "#0ff"

    async def setAvatar(self, avatar: str = None):
        if avatar is None:
            raise CardError("[Avatar] Укажите аватарку!")
        else:
            self.avatar = avatar

    async def setAvatarBack(self, color: str = None):
        if color is None:
            raise CardError("[AvatarBack] Укажите цвет!")
        else:
            self.avatarBack = color

    async def setServerAvatar(self, avatar: str = None):
        if avatar is None:
            raise CardError("[ServerAvatar] Укажите аватарку!")
        else:
            self.savatar = avatar

    async def setServerAvatarBack(self, color: str = None):
        if color is None:
            raise CardError("[ServerAvatarBack] Укажите цвет!")
        else:
            self.savatarBack = color

    async def setBackground(self, color: str = None):
        if color is None:
            raise CardError("[Background] Укажите цвет!")
        else:
            self.background = color

    async def setAvatarBackground(self, img: str = None):
        if img is None:
            raise CardError("[AvatarBackground] Укажите фон!")
        else:
            self.abackground = img

    async def setAvatarBackgroundBack(self, color: str = None):
        if color is None:
            raise CardError("[AvatarBackgroundBack] Укажите цвет!")
        else:
            self.abackgroundBack = color

    async def setTextColor(self, color: str = None):
        if color is None:
            raise CardError("[TextColor] Укажите цвет!")
        else:
            self.textColor = color

    async def setTextStyle(self, path: str = None):
        if path is None:
            raise CardError("[TextStyle] Укажите путь!")
        else:
            self.textStyle = path

    async def setWelcomeColor(self, color: str = None):
        if color is None:
            raise CardError("[WelcomeColor] Укажите цвет!")
        else:
            self.welcColor = color

    async def create(self, path=None):
        # | Системное | #
        def prepare_mask(size, antialias=2, otc=None):
            mask = Image.new("L", (size[0] * antialias, size[1] * antialias), 0)
            ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255, outline=otc)
            return mask.resize(size, Image.ANTIALIAS)

        def crop(im, s):
            w, h = im.size
            k = w / s[0] - h / s[1]
            if k > 0:
                im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
            elif k < 0:
                im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
            return im.resize(s, Image.ANTIALIAS)

        # | --------- | #
        # | Аватар | #
        avatar = Image.open(requests.get(self.avatar, stream=True).raw).convert("RGBA")
        size = (300, 300)

        avatar = crop(avatar, size)
        avatar.putalpha(prepare_mask(size, 4))
        # | ------ | #

        image = (
            Image.open(requests.get(self.abackground, stream=True).raw)
            .convert("RGBA")
            .resize((1270, 381), Image.ANTIALIAS)
        )

        # | Back | #
        imageback = Image.new("RGBA", (1280, 391), self.abackgroundBack)

        avatarback = Image.new("RGBA", (310, 310), self.avatarBack)
        avatarback = crop(avatarback, (310, 310))
        avatarback.putalpha(prepare_mask((310, 310), 4))

        savatarback = Image.new("RGBA", (310, 310), self.savatarBack)
        savatarback = crop(savatarback, (310, 310))
        savatarback.putalpha(prepare_mask((310, 310), 4))
        # | ---- | #

        serveravatar = Image.open(requests.get(self.savatar, stream=True).raw).convert(
            "RGBA"
        )
        serveravatar = crop(serveravatar, size)
        serveravatar.putalpha(prepare_mask(size, 4))

        line = Image.new("RGBA", (1310, 110), self.welcColor)
        lineback = Image.new("RGBA", (1310, 120), self.savatarBack)

        welcline = ImageFont.truetype(self.textStyle, size=90)
        nameline = ImageFont.truetype(self.textStyle, size=50)

        # name = member.name
        # if len(name) > 10:
        #    for n in name:
        #        if len(name) > 10:
        #            name = name[:-1]
        #    name = name + '...'

        img = Image.new("RGBA", (1310, 800), self.background)
        idraw = ImageDraw.Draw(img)
        img.paste(imageback, (15, 15), imageback)
        img.paste(image, (20, 20), image)
        img.paste(avatarback, (55, 175), avatarback)
        img.paste(avatar, (60, 180), avatar)
        img.paste(lineback, (0, 540), lineback)
        img.paste(line, (0, 545), line)
        # idraw.text((570, 575), f"{name}", font = nameline, fill = '#FFFFFF')
        idraw.text((100, 545), "Welcome", font=welcline, fill=self.textColor)
        # idraw.text((100, 545), f"{sname}", font = welcline, fill = '#FFFFFF')
        img.paste(savatarback, (955, 445), savatarback)
        img.paste(serveravatar, (960, 450), serveravatar)

        if path is None:
            data = io.BytesIO()
            img.save(data, "png")
            file = io.BytesIO(data.getvalue())
            return file
        elif type(path) == str:
            img.save(path)
        else:
            raise CardError("[Create] Путь неверный!")


class GoodbyeCard:
    def __init__(self):
        self.avatar = "https://cdn0.iconfinder.com/data/icons/pinpoint-notifocation/48/none-512.png"
        self.avatarBack = "#0ff"
        self.savatar = "https://cdn0.iconfinder.com/data/icons/pinpoint-notifocation/48/none-512.png"
        self.savatarBack = "#000"
        self.background = "#000"
        self.abackground = "https://2.bp.blogspot.com/-JXxwkcanA7U/VwzeoorCXAI/AAAAAAAAIs0/HwR2GkxxGkItEhmchUcDyT9FHEt-MV5tACLcB/s1600/Another%2BSnapshot%2Bof%2BMilky%2BWay.png"
        self.textStyle = ""
        self.textColor = "#fff"
        self.goodColor = "#0ff"
        self.abackgroundBack = "#0ff"

    async def setAvatar(self, avatar: str = None):
        if avatar is None:
            raise CardError("[Avatar] Укажите аватарку!")
        else:
            self.avatar = avatar

    async def setAvatarBack(self, color: str = None):
        if color is None:
            raise CardError("[AvatarBack] Укажите цвет!")
        else:
            self.avatarBack = color

    async def setServerAvatar(self, avatar: str = None):
        if avatar is None:
            raise CardError("[ServerAvatar] Укажите аватарку!")
        else:
            self.savatar = avatar

    async def setServerAvatarBack(self, color: str = None):
        if color is None:
            raise CardError("[ServerAvatarBack] Укажите цвет!")
        else:
            self.savatarBack = color

    async def setBackground(self, color: str = None):
        if color is None:
            raise CardError("[Background] Укажите цвет!")
        else:
            self.background = color

    async def setAvatarBackground(self, img: str = None):
        if img is None:
            raise CardError("[AvatarBackground] Укажите фон!")
        else:
            self.abackground = img

    async def setAvatarBackgroundBack(self, color: str = None):
        if color is None:
            raise CardError("[AvatarBackgroundBack] Укажите цвет!")
        else:
            self.abackgroundBack = color

    async def setTextColor(self, color: str = None):
        if color is None:
            raise CardError("[TextColor] Укажите цвет!")
        else:
            self.textColor = color

    async def setTextStyle(self, path: str = None):
        if path is None:
            raise CardError("[TextStyle] Укажите путь!")
        else:
            self.textStyle = path

    async def setGoodbyeColor(self, color: str = None):
        if color is None:
            raise CardError("[GoodbyeColor] Укажите цвет!")
        else:
            self.goodColor = color

    async def create(self, path=None):
        def prepare_mask(size, antialias=2, otc=None):
            mask = Image.new("L", (size[0] * antialias, size[1] * antialias), 0)
            ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255, outline=otc)
            return mask.resize(size, Image.ANTIALIAS)

        def crop(im, s):
            w, h = im.size
            k = w / s[0] - h / s[1]
            if k > 0:
                im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
            elif k < 0:
                im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
            return im.resize(s, Image.ANTIALIAS)

        # | Аватар | #
        avatar = Image.open(requests.get(self.avatar, stream=True).raw).convert("RGBA")
        size = (300, 300)

        avatar = crop(avatar, size)
        avatar.putalpha(prepare_mask(size, 4))

        savatar = Image.open(requests.get(self.savatar, stream=True).raw).convert(
            "RGBA"
        )
        savatar = crop(savatar, size)
        savatar.putalpha(prepare_mask(size, 4))
        # | ------ | #
        img = Image.new("RGBA", (1310, 800), self.background)

        savatarback = Image.new("RGBA", (size[0] + 10, size[1] + 10), self.savatarBack)
        savatarback = crop(savatarback, (size[0] + 10, size[1] + 10))
        savatarback.putalpha(prepare_mask((size[0] + 10, size[1] + 10), 4))

        avatarback = Image.new("RGBA", (size[0] + 10, size[1] + 10), self.avatarBack)
        avatarback = crop(avatarback, (size[0] + 10, size[1] + 10))
        avatarback.putalpha(prepare_mask((size[0] + 10, size[1] + 10), 4))

        line = Image.new("RGBA", (1310, 100), self.goodColor)

        idraw = ImageDraw.Draw(img)

        goodbayline = ImageFont.truetype(self.textStyle, size=90)
        connectline = ImageFont.truetype(self.textStyle, size=40)

        image = (
            Image.open(requests.get(self.abackground, stream=True).raw)
            .convert("RGBA")
            .resize((1270, 381), Image.ANTIALIAS)
        )

        disconnect = (
            Image.open(
                requests.get(
                    "https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F284499766145056768.png%3Fv%3D1&w=64&q=75",
                    stream=True,
                ).raw
            )
            .convert("RGBA")
            .resize((150, 150), Image.ANTIALIAS)
        )

        imageback = Image.new("RGBA", (1280, 391), self.abackgroundBack)
        img.paste(imageback, (15, 15), imageback)
        img.paste(image, (20, 20), image)
        # idraw.text((60, 210), "——————————————   ————————", font = connectline, fill = "#fff")
        # idraw.text((60, 310), "————————————   ——————————", font = connectline, fill = "#fff")
        img.paste(savatarback, (955, 145), savatarback)
        img.paste(savatar, (960, 150), savatar)
        img.paste(avatarback, (45, 145), avatarback)
        img.paste(avatar, (50, 150), avatar)
        img.paste(disconnect, (570, 220), disconnect)
        img.paste(line, (0, 600), line)

        idraw.text((450, 595), "Goodbye", font=goodbayline, fill=self.textColor)

        if path is None:
            data = io.BytesIO()
            img.save(data, "png")
            file = io.BytesIO(data.getvalue())
            return file
        elif type(path) == str:
            img.save(path)
        else:
            raise CardError("[Create] Путь неверный!")


class DemCard:
    def __init__(self):
        self.textColor = "#fff"
        self.TextStyle = None
        self.img = "https://2.bp.blogspot.com/-JXxwkcanA7U/VwzeoorCXAI/AAAAAAAAIs0/HwR2GkxxGkItEhmchUcDyT9FHEt-MV5tACLcB/s1600/Another%2BSnapshot%2Bof%2BMilky%2BWay.png"
        self.text1 = ""
        self.text2 = ""

    async def setTextColor(self, color: str = None):
        if color is None:
            raise CardError("[Dem-TextColor] Укажите цвет!")
        else:
            self.textColor = color

    async def setTextStyle(self, path: str = None):
        if path is None:
            raise CardError("[Dem-TextStyle] Укажите путь!")
        else:
            self.textStyle = path

    async def setImage(self, url: str = None):
        if url is None:
            raise CardError("[Dem-Image] Укажите ссылку на картинку!")
        else:
            self.img = url

    async def setText(self, text: str = None):
        if text is None:
            raise CardError(
                "[Dem-Text] Укажите текст. Или __help__ для получения помощи!"
            )
        elif text == "__help__":
            print(
                """
            [Dem-Text] Помощь:
            Через эту настройку вы указываете все два текста.
            Указываются они через ";".
            Пример: "text1;text2".
            Можно указать 1 текст, прописав его без ";".
            """
            )
        else:
            text = text.split(";", maxsplit=1)
            self.text1 = text[0]
            try:
                self.text2 = text[1]
            except Exception:
                pass

    async def create(self, path=None):
        img = Image.new("RGBA", (1310, 1000), "#000")
        imageback = Image.new("RGBA", (1090, 640), "#fff")
        imageback2 = Image.new("RGBA", (1080, 630), "#000")
        img.paste(imageback, (105, 95), imageback)
        img.paste(imageback2, (110, 100), imageback2)
        image = (
            Image.open(requests.get(self.img, stream=True).raw)
            .convert("RGBA")
            .resize((1080, 630), Image.ANTIALIAS)
        )
        img.paste(image, (110, 100), image)
        idraw = ImageDraw.Draw(img)
        line = ImageFont.truetype(self.textStyle, size=80)
        line2 = ImageFont.truetype(self.textStyle, size=60)
        size_1 = idraw.textsize(self.text1, font=line)
        idraw.text(
            ((1310 - size_1[0]) / 2, 775), self.text1, font=line, fill=self.textColor
        )
        size_2 = idraw.textsize(self.text2, font=line2)
        idraw.text(
            ((1310 - size_2[0]) / 2, 880), self.text2, font=line2, fill=self.textColor
        )

        if path is None:
            data = io.BytesIO()
            img.save(data, "png")
            file = io.BytesIO(data.getvalue())
            return file
        elif type(path) == str:
            img.save(path)
        else:
            raise CardError("[Dem-Create] Путь неверный!")

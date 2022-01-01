from disnake.ext.commands import BadArgument, Converter
import disnake
from disnake.ext import commands
from datetime import timedelta
import datetime
def pickform(num: int, wordforms: list):
    """
    NOTE: Аргумент wordforms должен выглядеть так: ['(1) ключ', '(2) ключа', '(5) ключей']
    -> Возвращает нужную форму слова для данного числа, например "1 велосипед" или "2 велосипеда"
    """
    # Числа-исключения от 11 до 14
    if 10 < num < 15:
        return wordforms[2]
    num = num % 10  # Далее важна только последняя цифра
    if num == 1:
        return wordforms[0]
    if 1 < num < 5:
        return wordforms[1]
    return wordforms[2]

class BadTimedelta(BadArgument):
    def __init__(self, argument):
        """
        Вызывается, когда не удаётся конвертировать строку в промежуток времени <datetime.timedelta>
        Несёт в себе аргумент, который спровоцировал ошибку.
        """
        self.argument = argument


def visdelta(delta):
    """
    NOTE: Аргумент delta может быть как секундами, так и объектом <datetime.timedelta>
    -> Возвращает читаемый промежуток времени на русском языке, например "3 минуты 30 секунд"
    """
    # Если delta это просто число, то оно считывается как секунды
    if not isinstance(delta, int):
        delta = int(delta.total_seconds())
    # Вычисляем и записываем каждую единицу времени
    nt = {}
    nt["s"] = delta % 60
    delta //= 60  # Секунды
    nt["m"] = delta % 60
    delta //= 60  # Минуты
    nt["h"] = delta % 24
    delta //= 24  # Часы
    nt["d"] = delta % 7
    delta //= 7  # Дни
    nt["w"] = delta  # Недели
    # Далее идут все возможные формы слов в связке с числом (1 банан, 2 банана, 5 бананов)
    wforms = {
        "s": ["секунда", "секунды", "секунд"],
        "m": ["минута", "минуты", "минут"],
        "h": ["час", "часа", "часов"],
        "d": ["день", "дня", "дней"],
        "w": ["неделя", "недели", "недель"],
    }
    # Формируем читаемые сочетания для каждой единицы времени
    l = [f"{n} {pickform(n, wforms[k])}" for k, n in nt.items() if n > 0]
    l.reverse()  # Чтобы время писалось начиная с недель и заканчивая секундами
    # Склеиваем словосочетания
    return "0.1 секунды" if len(l) == 0 else " ".join(l)
class TimedeltaConverter(Converter):
    @commands.converter_method
    async def convert(self, ctx: disnake.ApplicationCommandInteraction, argument: str):
        """
        Предполагается, что аргумент отформатирован как в этом примере: "1d5h30m10s"
        (1 день 5 часов 30 минут 10 секунд)
        -> Возвращает соответствующий объект класса <datetime.timedelta>
        """
        # Игнор регистра
        rest = argument.lower()
        # Если аргумент это просто целое число, то по умолчанию это минуты
        if rest.isdigit():
            td = timedelta(minutes=int(rest))
        else:
            tkeys = ["w", "d", "h", "m", "s"]
            # Здесь мы создаём словарик, где всех единиц времени по нулю
            raw_delta = {tk: 0 for tk in tkeys}
            # Перебираем все единицы времени
            for tk in tkeys:
                # Отследим первый виток цикла
                # Представим строку "1d5h30m10s" для примера
                # Первый разделитель - "d"
                pair = rest.split(tk, maxsplit=1)
                # Слева в паре находится "1", а справа "5h30m10s"
                if len(pair) < 2:
                    # Если разделителя "d" не было, то считается, что дни не указаны
                    raw_delta[tk] = 0
                else:
                    # Проверяем, является ли левый элемент пары числом
                    value, rest = pair
                    if not value.isdigit():
                        # Если левый элемент пары не число, то вызываем ошибку форматирования
                        raise BadTimedelta(argument)
                    raw_delta[tk] = int(value)
                    # Если мы дошли сюда, то:
                    # 1) Аргумент дней успешно считался
                    # 2) Осталось конвертировать "5h30m10s"
                    # В следующих 3 шагах цикла мы конвертируем 5h, 30m и 10s
            # Вбиваем полученные данные в timedelta
            td = timedelta(weeks=raw_delta["w"], days=raw_delta["d"], hours=raw_delta["h"], minutes=raw_delta["m"], seconds=raw_delta["s"])
        # 0 секунд это отстой, так что лучше рассмотреть этот случай
        if td.total_seconds() > 0:
            return td
        raise BadTimedelta(argument)
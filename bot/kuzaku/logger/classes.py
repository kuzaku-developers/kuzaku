from datetime import datetime
from types import MethodType
from pathlib import Path
from enum import Enum

from termcolor import colored as c
from disnake.ext.tasks import loop

from .ext import printer
from .conf_work import powerup as get_config


class States(Enum):
    root = "Root logger"
    # For subs
    not_entered = "Not entered into ctx manager"
    entered = "Entered into ctx manager"
    closed = "Exited from ctx manager"


class Log_error(RuntimeError):
    pass


class Kuzaku_logger:
    # __slots__ = ('__parent', '__queue', '__subs', '__state', '__group', '__config', 'id')

    @classmethod
    def new(cls):
        try:
            import log_config as config

            conf = config.config

        except ImportError:
            conf = {}

        return cls("root", conf)

    def __init__(self, id: str, config: dict = ..., parent: "Kuzaku_logger" = None):
        self.id = id
        self.__parent = parent
        self.__subs = {}

        if parent is None:
            self.__state = States.root
            self.__group = 0
            self.__queue = {"finished": False, "queue": []}

            if config is ...:
                config = {}

            self.__config = get_config(config)

        else:
            self.__state = States.not_entered
            self.__group = parent.__group + 1
            self.__queue = None

            self.__config = parent.__config.copy()

        self.__task = loop()(printer)

        self.__build_functions(self.__config["funcs"])

        self.__run()

    def __enter__(self):
        if self.__state is not States.not_entered:
            if self.__state == States.root:
                raise Log_error(
                    'Root cannot enter as sublog. Tip: use root_logger.get ("<sublog name>")'
                )

            else:  # State is entered or closed
                raise Log_error("Cannot re-enter.")

        queue = {"finished": False, "queue": []}

        self.__parent.__sublog("enter", self.id)

        self.__state = States.entered
        self.__parent.__subs[self.id] = self
        self.__parent.__queue["queue"].append(queue)
        self.__queue = queue

        return self

    def __exit__(self, type, value, trace):
        self.__queue["finished"] = True

        del self.__parent.__subs[self.id]

        self.__state = States.closed

        self.__parent.__sublog("exit", self.id)

        return False

    def enter(self):
        return self.__enter__()

    def exit(self):
        return self.__exit__

    def __print(self, msg: str):
        if self.__state not in {States.entered, States.root}:
            raise Log_error("Cannot log because of logger state.")

        self.__queue["queue"].append(msg)

    def __compute_time(self):
        return format(datetime.now(), self.__config["time_pattern"])

    def __color(self, msg, color, type, icon, style=[]):
        ctime = c(self.__compute_time(), "yellow")
        cmsg = c(msg, color, attrs=style)
        cicon = c(icon, color, attrs=["bold"])
        ctype = c(type, color)

        tabs = self.__config["tabs_function"](self.__group)

        return self.__config["log_pattern"].format(
            ctime=ctime, cicon=cicon, ctype=ctype, cmsg=cmsg, tabs=tabs
        )

    def __cprint(self, msg, color, type, icon, style=[]):
        clog = self.__color(msg, color, type, icon, style)

        self.__print(clog)

        return clog

    def __build_function(self, name, kw):
        kw = kw.copy()

        def func(self, *msgs):
            for msg in msgs:
                self.__cprint(msg, **kw)

        self.__dict__[name] = MethodType(func, self)

    def __build_functions(self, kfuncs):
        for key in kfuncs:
            self.__build_function(key, kfuncs[key].copy())

    def __sublog(self, action, name):
        if action == "enter":
            msg_ = f"Entered group {name !r}."
            icon = ">"
            type = "ENTER"

        elif action == "exit":
            msg_ = f"Exited group {name !r}."
            icon = "<"
            type = "EXIT "

        else:
            raise Log_error(f"Cannot sublog action {action !r}.")

        self.__cprint(msg_, "cyan", type, icon)

    def get(self, id: str):
        if id in self.__subs:
            return self.__subs[id]

        return Kuzaku_logger(id, self.__config, self)

    def __run(self):
        if self.__state != States.root:
            # raise Log_error ('Sublog cannot run print loop.') # * ! Not today, buddy

            return

        self.__task.start(self.__queue["queue"])

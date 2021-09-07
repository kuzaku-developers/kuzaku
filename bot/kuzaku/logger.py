import logging
import logging.config
from datetime import datetime
from os.path import dirname
from pathlib import Path
from enum import Enum

from colorama import init as color_init
from termcolor import colored

def init ():
    path = Path (dirname('logs/log.log'))

    if not path.exists ():
        path.mkdir ()

    # color_init ()

    # ? Это же получается создание логгера да? Значит для каждого обьекта моего логгера он будет свой
    # logging.basicConfig (
    #     filename = "logs/log.log",
    #     format = '%(message)s',
    #     filemode = 'a'
    # )

    # logger = logging.getLogger ()
    # logging.config.dictConfig ({
    #     'version': 1,
    #     'disable_existing_loggers': True,
    # })

    # logger.setLevel (logging.INFO)

class States (Enum):
    not_entered = 'Not entered'
    entered     = 'Entered'
    closed      = 'Closed'
    root        = 'Root'

class Kuzaku_logger ():
    __slots__ =  ('parent', 'sub_group', 'sub_logger', 'logger_obj', 'state', 'name')

    def __init__ (self, name, parent: 'Kuzaku_logger' = None):
        self.sub_logger = None
        self.parent = parent
        self.name = name

        if parent is None:
            self.logger_obj = self._get_logger_obj ()
            self.sub_group = 0
            self.state = States.root

        else:
            self.logger_obj = parent.logger_obj
            self.sub_group = parent.sub_group + 1
            self.state = States.not_entered

    def _get_logger_obj (self):
        if getattr (self, 'logger_obj', None) is not None:
            return self.logger_obj

        return ... # TODO

    def __check (self):
        if self.state == States.root:
            return self.sub_logger is None

        return self.state == States.entered

    def __enter_check (self):
        return self.state == States.not_entered

    def __call__ (self, name):
        if not self.__check ():
            raise RuntimeError ('Cannot create new sublogger')

        return Kuzaku_logger (name, self)

    def __enter__ (self):
        if not self.__enter_check ():
            raise RuntimeError ('Cannot sublog')

        self.state = States.entered

        self.__sublog (self.name, False)

        return self

    def __exit__ (self, type, value, trace, native = True):
        if native:
            self.state = States.closed
            self.parent.__exit__ (type, value, trace, False)

        else:
            self.__sublog (self.name, True)
            self.sub_logger = None

    @classmethod
    def __compute_time (cls):
        return f'{datetime.now () :%Y.%m.%d %H:%M:%S [%f]}'

    def __compute_log (self, group, type, msg, icon, color, style = []):
        if not self.__check ():
            raise RuntimeError ('Cannot compute log')

        ctime = colored (text = self.__compute_time (), color = "yellow", attrs = ['dark'])
        tabs  = ('    ' * group + '|') if group else ''

        cicon = colored (text = icon, color = color, attrs = ['bold'])
        ctype = colored (text = type, color = color, attrs = ['bold'])
        cmsg  = colored (text = msg,  color = color, attrs = style)

        return f'{ctime} [{cicon}]{tabs} {ctype} | {cmsg}'

    def __sublog (self, name, _):
        if _:
            log = self.__compute_log (self.sub_group, 'GROUP', f'Exited group {name !r}', '<', 'cyan')

        else:
            log = self.__compute_log (self.sub_group, 'GROUP', f'Entered group {name !r}', '>', 'cyan')

        # * logging <- log

        print (log)

    def info (self, *msgs):
        for msg in msgs:
            log = self.__compute_log (self.sub_group, 'INFO ', msg, 'I', 'blue')

            # * logging <- log

            print (log)

    def debug (self, msg):
        log = self.__compute_log (self.sub_group, 'DEBUG', msg, '@', 'green', ['underline'])

        # ! NO logging <- log

        print (log)

    def error (self, msg):
        log = self.__compute_log (self.sub_group, 'ERROR', msg, '!', 'red', ['bold'])

        # * logging <- log

        print (log)

init ()
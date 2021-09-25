import logging
import logging.config
from datetime import date, datetime
from os import environ
from pathlib import Path
from enum import Enum
from colorama import init as color_init # * Not needed, our team is using VSCode on windows
from termcolor import colored
from dotenv import load_dotenv

# DEFAULT PATTERNS
#
# LOG_PATTERN  {ctime} [{cicon}]{tabs} {ctype} | {cmsg}
#(c* = colored *) {time} [{icon}]{tabs} {type} | {msg}
#
# TIME_PATTERN  %Y.%m.%d %H:%M:%S [%f]
# TABS_FUNCTION  n4
#

def tabs_function (name: str):
    if name.startswith ('n'):
        def get_tabs (amount):
            return ' ' * int (name [1:]) * amount

        return get_tabs

    return tabs_function ('n4')

def pattern_control (prod, key, default):
    if prod:
        return default

    return environ.get (key) or default

def get_logfile (production):
    logs_path = Path ('logs')

    if not logs_path.exists ():
        logs_path.mkdir ()

    if production:
        logfile = logs_path / f'{date.today () :%y_%m_%d}.log'

        writable = logfile.open ('a+')

        if writable.read () != '':
            writable.write ('\n')

        writable.write (f'>>>>>>>>>> {datetime.now () :%Hh %Mm %Ss} <<<<<<<<<<')
        writable.write ('\n\n')

        writable.close ()

    else:
        logfile = logs_path / 'debug.log'

        logfile.open ('w').close ()

    return logfile


prod = environ.get ('PRODUCTION') == 'yes'

if not prod: load_dotenv ()

pattern = pattern_control (prod, 'LOG_PATTERN', '{ctime} [{cicon}]{tabs} {ctype} | {cmsg}')
time_pattern = pattern_control (prod, 'TIME_PATTERN', '%Y.%m.%d %H:%M:%S [%f]')
tabs_pattern = tabs_function (pattern_control (prod, 'TABS_FUNCTION', 'n4'))

logfile = get_logfile (prod)

color_init () # * Not needed, owr team is using VSCode on windows

class Log_error (RuntimeError):
    pass

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

        return ... # ! Logger object initialisation HERE

    def __check (self):
        return (self.state in {States.root, States.entered}) and (self.sub_logger is None)

    def __enter_check (self):
        return (self.state == States.not_entered) and self.sub_logger is None

    def __call__ (self, name):
        if not self.__check ():
            raise Log_error ('Cannot create new sublogger')

        return Kuzaku_logger (name, self)

    def __enter__ (self):
        if not self.__enter_check ():
            raise Log_error ('Cannot sublog')

        self.state = States.entered
        self.parent.sub_logger = self

        self.__sublog ('enter')

        return self

    def __exit__ (self, type, value, trace, native = True):
        if native:
            self.state = States.closed
            return self.parent.__exit__ (type, value, trace, False)

        else:
            self.sub_logger = None

            if type == Log_error:
                self.__sublog ('exit', value)

                return True

            self.__sublog ('exit')

    @classmethod
    def __compute_time (cls):
        return format (datetime.now (), time_pattern)

    def __compute_log (self, group, type, msg, icon, color, style = []):
        if not self.__check ():
            raise Log_error ('Cannot compute log')

        ctime = colored (text = self.__compute_time (), color = "yellow", attrs = ['dark'])
        tabs  = tabs_pattern (group) if group else ''

        cicon = colored (text = icon, color = color, attrs = ['bold'])
        ctype = colored (text = type, color = color, attrs = ['bold'])
        cmsg  = colored (text = msg,  color = color, attrs = style)

        return pattern.format (ctime = ctime, tabs = tabs, cicon = cicon, ctype = ctype, cmsg = cmsg)

    def __sublog (self, _, error = ...):
        if _ == 'enter':
            log = self.__compute_log (self.sub_group - 1, 'GROUP', f'Entered group {self.name !r}', '>', 'cyan')

        else:
            if error == ...:
                log = self.__compute_log (self.sub_group, 'GROUP', f'Exited group {self.name !r}', '<', 'cyan')

            else:
                log = self.__compute_log (self.sub_group, 'GROUP', f'Exited group {self.name !r} with error {error !r}', '<', 'cyan', ['bold'])

        # * logging <- log
        print(log, TracingName1)

    def info (self, *msgs):
        for msg in msgs:
            log = self.__compute_log (self.sub_group, 'INFO ', msg, '#', 'blue')

            # * logging <- log

            print (log)

    def debug (self, msg):
        log = self.__compute_log (self.sub_group, 'DEBUG', msg, '@', 'green', {'underline'})

        # ! NO logging <- log

        print (log)

    def warn (self, msg):
        log = self.__compute_log (self.sub_group, 'WARN ', msg, '?', 'magenta', {'bold'})

        # * logging <- log

        print (log)

    def error (self, msg):
        log = self.__compute_log (self.sub_group, 'ERROR', msg, '!', 'red', {'bold'})

        # * logging <- log

        print (log)

def main ():
    def test_log (logger):
        logger.info ('<info>')
        logger.debug ('<debug>')
        logger.warn ('<warn>')
        logger.error ('<error>')

    logger = Kuzaku_logger ('root')

    test_log (logger)

    with logger ('sublogger') as sub:
        test_log (sub)

        logger.error ('asdf')

        test_log (sub)

if __name__ == '__main__':
    main ()
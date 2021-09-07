import sys
import logging
import logging.config
import os
import datetime
import time
rootdir=os.path.abspath(os.path.join(os.curdir))
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[92m'
    OKGREEN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[1;33;40m'
def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise
mkdir_p(os.path.dirname('logs/log.log'))
logging.basicConfig(filename="logs/log.log", 
					format='%(message)s', 
					filemode='a') 
logger=logging.getLogger()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
logger.setLevel(logging.INFO) 
def log (*msg):
        def _ (msg):
            logging.log(level=logging.INFO, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  LOG  | {msg}')
            if os.getenv('DONTUSECOLORS') != 'yes':
                print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.OKCYAN}  LOG  {bcolors.ENDC}| {bcolors.HEADER}{msg}')
            else: 
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  LOG  | {msg}')
        list(map (_, msg))
def cmd (*msg):
    def _ (msg):
        logging.log(level=logging.INFO, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  CMD  | {msg}')
        if os.getenv('DONTUSECOLORS') != 'yes':
            print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.OKCYAN}  CMD  {bcolors.ENDC}| {bcolors.HEADER}{msg}')
        else: 
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |  CMD  | {msg}')
    list(map (_, msg))
def warning(*msg):
    def _ (msg):
        logging.log(level=logging.WARNING, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ALERT | {msg}')
        if os.getenv('DONTUSECOLORS') != 'yes':
            print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {bcolors.ENDC}|{bcolors.OKGREEN} ALERT {bcolors.ENDC}| {bcolors.HEADER}{msg}')
        else:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ALERT | {msg}')
    list(map (_, msg))
def error(*msg):
    def _ (msg):
        logging.log(level=logging.ERROR, msg=f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ERROR | {msg}')
        if os.getenv('DONTUSECOLORS') != 'yes':
            print(f'{bcolors.YELLOW}{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}{bcolors.ENDC} |{bcolors.FAIL} ERROR {bcolors.ENDC}| {bcolors.HEADER}{msg}')
        else:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | ERROR | {msg}')
    list(map (_, msg))
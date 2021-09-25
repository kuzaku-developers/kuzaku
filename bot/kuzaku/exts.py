import subprocess
import platform
from pathlib import Path

# from kuzaku.logger import log, warning, error

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command, stdout=subprocess.PIPE) == 0

def load_dir (bot, logger, path, rel_to, ignore = []):
    for cog in path.iterdir ():
        if cog.is_file ():
            cog = cog.relative_to (rel_to)
            if cog.name [:-3] in ignore:
                continue

            cog = str (cog) [:-3].replace ('/', '.').replace ('\\', '.')

            try:
                bot.load_extension (f'{cog}')

            except Exception as e:
                logger.error(f'not loaded: {cog !r}')
                logger.error(f'error: {e}')

            else:
                logger.info (f'loaded: {cog !r}')

        else:
            if cog.name != '__pycache__':
                load_dir (bot, logger, cog, rel_to, ignore)


def load_cogs (bot, ignore = []):
    bot.load_extension('kuzaku.jishaku')

    with bot.log ('COG LOADER') as logger:
        path = Path.cwd () / 'bot' / 'cogs'

        load_dir (bot, logger, path, path.parent, ignore)
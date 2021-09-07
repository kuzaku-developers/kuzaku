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

def load_dir (bot, path, rel_to, ignore = []):
    for cog in path.iterdir ():
        if cog.is_file ():
            cog = cog.relative_to (rel_to)
            if cog.name [:-3] in ignore:
                continue

            cog = str (cog) [:-3].replace ('/', '.').replace ('\\', '.')

            try:
                bot.load_extension (f'{cog}')

            except Exception as e:
                bot.log.error(f'    not loaded: {cog !r}', f'    error: {e}')

            else:
                bot.log.info (f'    loaded: {cog !r}')

        else:
            if cog.name != '__pycache__':
                load_dir (bot, cog, rel_to, ignore)


def load_cogs (bot, ignore = []):
    bot.load_extension('jishaku')
    bot.log.info('<main> :: Cogs loader')
    bot.log.info(f'    Loading \'cogs/*\' ...')
    path = Path.cwd () / 'bot' / 'cogs'

    load_dir (bot, path, path.parent, ignore)
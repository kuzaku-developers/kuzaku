from kuzaku.logger import log, warning, error
from pathlib import Path
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
                error(f'    not loaded: {cog !r}', f'    error: {e}')

            else:
                log(f'    loaded: {cog !r}')

        else:
            if cog.name != '__pycache__':
                load_dir (bot, cog, rel_to, ignore)


def load_cogs (bot, ignore = []):
    bot.load_extension('jishaku')
    log('<main> :: Cogs loader')
    log(f'    Loading \'cogs/*\' ...')
    path = Path.cwd () / 'bot' / 'cogs'

    load_dir (bot, path, path.parent, ignore)
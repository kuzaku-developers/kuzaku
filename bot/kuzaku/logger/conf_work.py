# from pprint import pprint

default_config = {
    'funcs' : {
        'info':  { 'color': 'blue',    'type': 'INFO ', 'icon': '#', 'style': set () },
        'debug': { 'color': 'green',   'type': 'DEBUG', 'icon': '@', 'style': {'underline'} },
        'error': { 'color': 'red',     'type': 'ERROR', 'icon': '!', 'style': {'bold'} },
        'warn':  { 'color': 'magenta', 'type': 'WARN ', 'icon': '?', 'style': {'bold'} },
    },

    'tabs_function': 'n4',
    'log_pattern': '{ctime} [{cicon}]{tabs} {ctype} | {cmsg}',
    'time_pattern': '%Y.%m.%d %H:%M:%S [%f]'
}

def merge (new: dict):
    # pprint (new)

    if not new: return default_config.copy ()

    new = new.copy ()
    merged = default_config.copy ()

    merged ['funcs'] = default_config ['funcs'] | new.get ('funcs', {})

    if new.get ('funcs', None) is not None: del new ['funcs']

    # pprint (merged | new)

    return merged | new

def as_executable (config: dict):
    config = config.copy ()

    config ['tabs_function'] = get_tabs_function (config ['tabs_function'])

    return config

def get_tabs_function (val: str):
    if val.startswith ('n'):
        sp = int (val.removeprefix ('n'))

        return lambda n: ' ' * sp * n

    elif val.startswith ('a'):
        sep, sp = val.removeprefix ('a').split (';SEP;')

        return lambda n: sep * int (sp) * n

    else:
        return lambda n: ' ' * 4 * n

def powerup (config: dict):
    merged = merge (config)
    # print (f'{merged =}')
    return as_executable (merged)

# print = lambda a: (__builtins__.print (a), a) [1]

# def funcs_as_dict (funcs):
#     res = {}

#     for func in funcs.copy ():
#         res [func.pop ('name')] = func

#     return res

# def merge_funcs (new):
#     old = funcs_as_dict (default_config ['funcs'])
#     new = funcs_as_dict (new)

#     return dict_as_funcs (old | new)


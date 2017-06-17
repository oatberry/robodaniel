#
# commands (not just factoids!) for robodaniel
#

def help(*args):
    '[command]: show available factoids and commands or help for a specific command'
    from factoids import factoids
    import commands, re

    factoid_list = list(factoids)
    command_list = [i for i in dir(commands) if not re.match('^__', i)]

    if len(args) == 0:
        return 'list of factoids: {}\nlist of commands: {}'.format(factoid_list, command_list)
    else:
        return args[0] + ' ' + eval(args[0] + '.__doc__')

def rev(*args):
    '<string>: reverse a string of text'
    return ' '.join(i[::-1] for i in args[::-1])

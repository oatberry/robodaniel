#
# commands (not just factoids!) for robodaniel
#

def help():
    '''show available factoids and commands'''
    from factoids import factoids
    import commands, re

    factoid_list = list(factoids.keys())
    command_list = [i for i in dir(commands) if not re.compile('^__').match(i)]
  
    return 'list of factoids: {0}\nlist of commands: {1}'.format(factoid_list, command_list)

def rev(args):
    '''reverse a string of text'''
    return args[::-1]

#
# commands (not just factoids!) for robodaniel
#

def help():
    from factoids import factoids
    factoid_list = list(factoids.keys())
    
    return "list of factoids: {0}\nlist of commands: {1}".format(factoid_list, command_list)

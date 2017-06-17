#
# commands (not just factoids!) for robodaniel
#

def compliment(args, sender, sender_id, attachments):
    '<person>: send someone a compliment!'
    from data.compliments import compliments
    import random
    return random.choice(compliments)

def help(args, sender, sender_id, attachments):
    '[command]: show available factoids and commands or help for a specific command'
    from factoids import factoids
    import commands, re

    factoid_list = list(factoids)
    command_list = [i for i in dir(commands) if not re.match('^__', i)]

    if len(args) == 0:
        return 'list of factoids: {}\nlist of commands: {}'.format(factoid_list, command_list)
    else:
        return args[0] + ' ' + eval(args[0] + '.__doc__')

def rev(args, sender, sender_id, attachments):
    '<string>: reverse a string of text'
    return ' '.join(i[::-1] for i in args[::-1])

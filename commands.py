#
# commands (not just factoids!) for robodaniel
#

def compliment(args, sender, sender_id, attachments, bot):
    '[person]: send someone a compliment!'
    from data.compliments import compliments
    import random

    try:
        user_id = attachments[0]['user_ids'][0]
    except:
        return [random.choice(compliments)]

    compliment = random.choice(compliments)
    
    return give(attachments[0]['user_ids'][0], compliment, bot)

def help(args, sender, sender_id, attachments, bot):
    '[command]: show available factoids and commands or help for a specific command'
    from data.factoids import factoids
    import commands, re

    factoid_list = list(factoids)
    command_list = [i for i in dir(commands) if not re.match('^__', i)]

    if len(args) == 0:
        return ['list of factoids: {}\nlist of commands: {}'.format(factoid_list, command_list)]
    else:
        return [args[0] + ' ' + eval(args[0] + '.__doc__')]

def insult(args, sender, sender_id, attachments, bot):
    '[person]: sendeth some lout a shakespearean fig!'
    import data.insults as insults, random
    from helpers import give
    
    insult = 'Thou {} {} {}!'.format(random.choice(insults.part_1),
                                     random.choice(insults.part_2),
                                     random.choice(insults.part_3))
    return give(attachments[0]['user_ids'][0], insult, bot)

def rev(args, sender, sender_id, attachments, bot):
    '<string>: reverse a string of text'
    return [' '.join(i[::-1] for i in args[::-1])]

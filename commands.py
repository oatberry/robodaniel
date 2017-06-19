#
# commands for robodaniel
# everything is returned in a tuple or a list, period!
#

def compliment(args, sender, sender_id, attachments, bot):
    '[person]: send someone a compliment!'
    from data.compliments import compliments
    from helpers import give
    import random

    compliment = random.choice(compliments)

    try:
        user_id = attachments[0]['user_ids'][0]
    except:
        return [compliment] # send a compliment anyway if no name is given

    # use give() helper function to construct a mention
    return give(user_id, compliment, bot)

def help(args, sender, sender_id, attachments, bot):
    '[command]: show available factoids and commands or help for a specific command'
    from data.factoids import factoids
    import commands, re

    # get lists of all available factoids and commands
    factoid_list = list(factoids)
    command_list = [i for i in dir(commands) if not re.match('^__', i)]

    if len(args) == 0:
        return ['list of factoids: {}\nlist of commands: {}'.format(factoid_list, command_list)]
    else:
        return ['> {} {}'.format(args[0], eval(args[0] + '.__doc__'))]

def insult(args, sender, sender_id, attachments, bot):
    '[person]: sendeth some lout a shakespearean fig!'
    import data.insults as insults, random
    from helpers import give
    
    insult = 'thou {} {} {}!'.format(random.choice(insults.part_1),
                                     random.choice(insults.part_2),
                                     random.choice(insults.part_3))
    try:
        user_id = attachments[0]['user_ids'][0]
    except:
        return [insult] # send an insult anyway if no name is given

    return give(user_id, insult, bot)

def rev(args, sender, sender_id, attachments, bot):
    '<string>: reverse a string of text'
    return [' '.join(i[::-1] for i in args[::-1])]

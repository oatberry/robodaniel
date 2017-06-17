#
# commands (not just factoids!) for robodaniel
#

def compliment(args, sender, sender_id, mentions, bot):
    '[person]: send someone a compliment!'
    from data.compliments import compliments
    from groupy import Group, attachments
    import random

    # construct a mention for the target user
    try:
        user_id = mentions[0]['user_ids'][0]
    except:
        return [random.choice(compliments)]

    group = Group.list().filter(id=bot.group_id).first
    nickname = group.members().filter(user_id=user_id).first.nickname

    mention = attachments.Mentions([user_id], [[0, len(nickname)+1]]).as_dict()
    message = '@{}: {}'.format(nickname, random.choice(compliments))
    
    return [message, mention]

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

def rev(args, sender, sender_id, attachments, bot):
    '<string>: reverse a string of text'
    return [' '.join(i[::-1] for i in args[::-1])]

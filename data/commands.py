#
# commands for robodaniel
# everything is returned in a tuple or a list, period!
#

def compliment(args, sender, sender_id, attachments, bot):
    '[person]: send someone a compliment!'
    import helpers, random
    
    # choose a random compliment
    try:
        compliment = random.choice(bot.compliments)
    except AttributeError:
        with open('data/compliments.txt') as compliments_file:
            bot.compliments = [line for line in compliments_file]
        compliment = random.choice(bot.compliments)

    try:
        # attempt to extract target user from message
        user_id = attachments[0]['user_ids'][0]
    except IndexError:
        # send a compliment anyway if no name is given
        return [compliment]

    # use give() helper function to construct a groupme mention
    return helpers.give(user_id, compliment, bot.group)


def help(args, sender, sender_id, attachments, bot):
    '[command]: show available factoids and commands or help for a specific command'
    # get lists of all available factoids and commands
    factoid_list = list(bot.factoids)
    command_list = list(bot.command_dict)

    if len(args) == 0:
        # return list of factoids and commands
        return ['list of factoids: {}\nlist of commands: {}'.format(factoid_list, command_list)]
    else:
        # return help for a specific command
        return ['> !{} {}'.format(args[0], eval(args[0] + '.__doc__'))]


def insult(args, sender, sender_id, attachments, bot):
    '[person]: sendeth some lout a shakespearean fig!'
    import data.insults as insults
    import helpers, random
    
    # construct a random insult
    insult = 'thou {} {} {}!'.format(random.choice(insults.part_1),
                                     random.choice(insults.part_2),
                                     random.choice(insults.part_3))
    try:
        user_id = attachments[0]['user_ids'][0]
    except IndexError:
        return [insult] # send an insult anyway if no name is given

    return helpers.give(user_id, insult, bot.group)


def meme(args, sender, sender_id, attachments, bot):
    ': get a random viral meme from the last week off of imgur'
    import random, requests

    memes = []
    headers = {'authorization': 'Client-ID a022618f15e97a4'}

    for i in range(3): # fetch 3 'pages' of memes
        url = 'https://api.imgur.com/3/g/memes/viral/week/' + str(i)
        response = requests.request("GET", url, headers=headers)
        memes.extend(response.json()['data'])

    # choose a random meme from the list
    meme = random.choice(memes)

    # if fetched meme is in fact an album, choose a random image from the album
    if meme['is_album']:
        url = 'https://api.imgur.com/3/album/{}/images'.format(meme['id'])
        response = requests.request("GET", url, headers=headers)
        memes = response.json()['data']
        meme = random.choice(memes)

    return ['https://imgur.com/' + meme['id']]


def reload(args, sender, sender_id, attachments, bot):
    ': reload commands, factoids, and triggers'
    bot.gather_commands()
    bot.generate_triggers()

    return ['>reloaded commands, factoids, and triggers']


def rev(args, sender, sender_id, attachments, bot):
    '<string>: reverse a string of text'
    # since the command sent by the user is a list of words, we have to reverse
    # each word and the whole list
    return [' '.join(i[::-1] for i in args[::-1])]


def triggers(args, sender, sender_id, attachments, bot):
    ': list trigger rules'
    patterns = [p.pattern for p, _ in bot.triggers]

    return ['\n'.join(patterns)]


def talk(args, sender, sender_id, attachments, bot):
    ': say something'
    import markovify

    # fetch 500 recent messages
    messages = bot.group.messages()
    for _ in range(4):
        messages.iolder()

    # extract all message text into one string
    text = '\n'.join(m.text for m in messages if m.text)
    # create markov model
    text_model = markovify.Text(text)

    response = [None]
    while response == [None]:
        response = [text_model.make_short_sentence(140)]

    return response

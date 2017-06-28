#
# commands for robodaniel
# everything is returned in a tuple or a list, period!
#

import commands, markovify, os, re, requests
import data.insults as insults
from data.compliments import compliments
from data.factoids import factoids
from groupy import Group
from helpers import *
from random import choice as rand


def compliment(args, sender, sender_id, attachments, bot):
    '[person]: send someone a compliment!'

    compliment = rand(compliments) # choose a random compliment

    try:
        # attempt to extract target user from message
        user_id = attachments[0]['user_ids'][0]
    except:
        # send a compliment anyway if no name is given
        return [compliment]

    # use give() helper function to construct a groupme mention
    return give(user_id, compliment, bot)


def help(args, sender, sender_id, attachments, bot):
    '[command]: show available factoids and commands or help for a specific command'

    # get lists of all available factoids and commands
    factoid_list = list(factoids)
    command_list = [i for i in dir(commands) if not re.match('^__', i)]

    if len(args) == 0:
        # return list of factoids and commands
        return ['list of factoids: {}\nlist of commands: {}'.format(factoid_list, command_list)]
    else:
        # return help for a specific command
        return ['> !{} {}'.format(args[0], eval(args[0] + '.__doc__'))]


def insult(args, sender, sender_id, attachments, bot):
    '[person]: sendeth some lout a shakespearean fig!'
    
    # construct a random insult
    insult = 'thou {} {} {}!'.format(rand(insults.part_1),
                                     rand(insults.part_2),
                                     rand(insults.part_3))
    try:
        user_id = attachments[0]['user_ids'][0]
    except:
        return [insult] # send an insult anyway if no name is given

    return give(user_id, insult, bot)


def meme(args, sender, sender_id, attachments, bot):
    ': get a random viral meme from the last week off of imgur'

    memes = []
    headers = {'authorization': 'Client-ID ' + os.getenv('IMGUR_ID')}

    for i in range(3): # fetch 3 'pages' of memes
        url = 'https://api.imgur.com/3/g/memes/viral/week/' + str(i)
        response = requests.request("GET", url, headers=headers)
        memes.extend(response.json()['data'])

    # choose a random meme from the list
    image_url = rand(memes)['link']

    return [image_url]


def rev(args, sender, sender_id, attachments, bot):
    '<string>: reverse a string of text'

    # since the command sent by the user is a list of words, we have to reverse
    # each word and the whole list
    return [' '.join(i[::-1] for i in args[::-1])]


def triggers(args, sender, sender_id, attachments, bot):
    ': list trigger rules'
    
    patterns = []
    with open('data/triggers.txt') as triggers_file:
        for rule in triggers_file:
            patterns.append(rule.split()[0])

    return ['\n'.join(patterns)]

def talk(args, sender, sender_id, attachments, bot):
    ': say something'

    group = Group.list().filter(id=bot.group_id).first

    # fetch 300 recent messages
    messages = group.messages()
    for _ in range(2):
        messages.extend(messages.older())

    # extract all message text into one string
    text = '\n'.join(m.text for m in messages if m.text)
    # create markov model
    text_model = markovify.Text(text)

    response = [None]
    while response == [None]:
        response = [text_model.make_sentence(max_overlap_total=10)]

    return response

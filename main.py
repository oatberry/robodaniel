#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#   intended to be run under heroku
#

import commands, json, logging, os, re, socket, sys, time
from data.factoids import factoids
from groupy import Bot, Group, config


def generate_triggers():
    'regex-compile trigger rules into readily available bits'

    triggers = []
    with open('data/triggers.txt') as triggers_file:
        for rule in triggers_file:
            trigger = rule.split()

            pattern = re.compile(trigger[0])
            response = ' '.join(trigger[1:])
            triggers.append((pattern, response))

    return triggers


def match_trigger(triggers, message):
    'check if a message begins with "!" or matches a trigger rule'

    response = None
    if message['text'][0] == '!':
        # message contains a !command; interpret it
        logging.info('interpreted command: "{}"'.format(message['text']))
        response = interpret(message)
    else:
        # try each trigger rule
        for rule in triggers:
            if rule[0].match(message['text']):
                # response is triggered
                logging.info('trigger matched: "{}"'.format(message['text']))
                response = [rule[1]]
                break

    if response:
        # we have a response to print!
        logging.info('sending response: "{}"'.format(response))
        bot.post(*response)


def interpret(message):
    'decide what to do with a "!command" message'
    # extract the message text, minus the beginning '!'
    command = message['text'][1:]

    # put a precautionary space before each '@'; GroupMe does weird stuff with mentions
    command = re.sub('@', ' @', command)

    # check if command/factoid exists, then run it
    if command in list(factoids):
        # print a factoid
        return [factoids[command]]
    elif command.split()[0] in dir(commands):
        # run a function from `commands` with arguments
        args = command.split()
        return getattr(commands, args[0])(args=args[1:],
                                          sender=message['name'],
                                          sender_id=message['user_id'],
                                          attachments=message['attachments'],
                                          bot=bot)
    else:
        logging.warning('invalid command: {}'.format(command))
        return False


def listen():
    "listen for new messages in the bot's groupme channel"

    # heroku provides the port variable for us
    port = int(os.getenv('PORT')) or 5000

    # generate rules for matching text in messages ahead of time for efficiency
    logging.info('generating trigger rules...')
    triggers = generate_triggers()

    # open the listening socket
    logging.info('opening listener socket on port {}...'.format(port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), port))
    s.listen(10)

    # attempt to extract chat message text from received data
    while True:
        (connection, address) = s.accept()

        try:
            time.sleep(0.3)
            data = connection.recv(4096)
            message = json.loads(data.decode('utf-8').split('\n')[-1])

            if message['sender_type'] == 'user':
                logging.debug('message received: {}'.format(message))
                match_trigger(triggers, message) # try to match all messages against triggers

        except Exception:
            pass


# set up logging
logging.basicConfig(level=logging.INFO, format="--> %(levelname)s: %(message)s")
logging.getLogger('requests').setLevel(logging.WARNING) # quiet down, requests!

# set api key from env variable instead of ~/.groupy.key
config.API_KEY = os.getenv('API_KEY')
if not config.API_KEY:
    logging.error('API_KEY environment variable not set. aborting...')
    sys.exit()

# set up bot
bot = Bot.list().filter(name='RoboDaniel').first
# get group that bot is in
group = Group.list().filter(id=bot.group_id).first


if __name__ == '__main__':
    # start listening and interpreting
    logging.info('launching robodaniel...')
    listen()

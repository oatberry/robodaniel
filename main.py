#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#   intended to be run under heroku
#

import commands, json, logging, os, re, socket, sys, time
from data.factoids import factoids
from groupy import Bot, config


def generate_triggers():
    triggers = []

    with open('data/triggers.txt') as triggers_file:
        for rule in triggers_file:
            trigger = rule.split()

            pattern = re.compile(trigger[0])
            response = ' '.join(trigger[1:])
            triggers.append((pattern, response))

    return triggers


def match_trigger(triggers, message):
    response = None

    if message['text'][0] == '!':
        # message contains a !command; interpret it
        logging.info('interpreted command: "{}"'.format(command))
        response = interpret(message)
    else:
        # try each trigger rule
        for rule in triggers:
            if rule[0].match(message['text']):
                # response is triggered
                response = [rule[1]]
                break
    
    if response:
        # we have a response to print!
        logging.info('sending response: "{}"'.format(response))
        bot.post(*response)
    else:
        # message matches no triggers, do nothing
        return 


def interpret(message):
    command = message['text'][1:]
    # put a precautionary space before each '@'
    # GroupMe does weird stuff with mentions
    command = re.sub('@', ' @', command)
    # check if command/factoid exists, then run it
    if command in list(factoids):
        # print a factoid
        return [factoids[command]]
    elif command.split()[0] in dir(commands):
        # run a function from `commands` with arguments
        args = command.split()
        return getattr(commands, args[0])(args[1:],                 # command and  command arguments
                                          message['name'],          # nickname of sender
                                          message['user_id'],       # user id of sender
                                          message['attachments'],   # attachments of message
                                          bot)                      # bot object
    else:
        logging.warning('invalid command: {}'.format(command))
        return False


def listen():
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
                logging.info('message received: {}'.format(message))
                match_trigger(triggers, message) # try to match all messages against known triggers

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

bot = Bot.list().filter(name='RoboDaniel').first
botpost = bot.post


if __name__ == '__main__':
    # set up bot and start listening
    logging.info('launching robodaniel...')
    listen()

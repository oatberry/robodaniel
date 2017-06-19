#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#   intended to be run under heroku
#

import commands, json, logging, os, re, socket, sys, time
from data.factoids import factoids
from groupy import Bot, config


def interpret(message):
    command = message['text'][1:]
    # check if command/factoid exists, then run it
    if command in list(factoids):
        # print a factoid
        response = [factoids[command]]
    elif command.split()[0] in dir(commands):
        # put a precautionary space before each '@'
        # GroupMe does weird stuff with mentions
        re.sub('@', ' @', command)
        # run a function from `commands` with arguments
        args = command.split()
        response = getattr(commands, args[0])(args[1:],                 # command and  command arguments
                                              message['name'],          # nickname of sender
                                              message['user_id'],       # user id of sender
                                              message['attachments'],   # attachments of message
                                              bot)                      # bot object
    else:
        # command/factoid not found, post nothing and log a warning
        logging.warning('invalid command: {}'.format(command))
        return

    logging.info('interpreted command: "{}"'.format(command))
    logging.info('sending response: "{}"'.format(response))

    return bot.post(*response)


def listen(port=''):
    # heroku provides the port variable for us
    port = int(os.getenv('PORT'))

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
                if message['text'][0] == '!':
                    interpret(message)

        except Exception:
            pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="--> %(levelname)s: %(message)s")

    # set api key from env variable instead of ~/.groupy.key
    config.API_KEY = os.getenv('API_KEY')
    if not config.API_KEY:
        logging.error('API_KEY environment variable not set. aborting...')
        sys.exit()

    # set up bot and start listening
    logging.info('launching robodaniel...')
    bot = Bot.list().filter(name='RoboDaniel').first
    listen()

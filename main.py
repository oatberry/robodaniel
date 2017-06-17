#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#   intended to be run under heroku
#

import commands, json, logging, os, socket, sys, time
from factoids import factoids
from groupy import Bot, config


def interpret(command):
    # check if command/factoid exists, then run it
    if command in list(factoids):
        # print a factoid
        response = factoids[command]
    elif command.split()[0] in dir(commands):
        # run a function from `commands` with arguments
        f = command.split()
        response = getattr(commands, f[0])(f[1:])
    else:
        # command/factoid not found, post nothing and log a warning
        logging.warning('invalid command: {}'.format(command))
        return

    logging.info('received command: "{}"'.format(command))
    logging.info('sending response: "{}"'.format(response))

    return bot.post(response)


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
            data = json.loads(data.decode('utf-8').split('\n')[-1])

            if data['sender_type'] == "user" and data['text'][0] == '!':
                interpret(data['text'][1:])

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
    bot = Bot.list().first
    listen()

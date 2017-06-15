#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#   intended to be run under heroku
#

import json, os, socket, time, commands
from factoids import factoids
from groupy import Bot, config


def interpret(command):
    # check if command/factoid exists, then run it
    if command in list(factoids.keys()):
        # print a factoid
        response = factoids[command]
    elif command.split(' ')[0] in dir(commands):
        # run a function from `commands` with arguments
        f = command.split(' ')
        response = eval("commands." + f[0] + "(" + str(f[1:]) + ")")
    else:
        # command/factoid not found, post nothing and log a warning
        robolog('invalid command: {0}'.format(command), level='warn')
        return

    robolog('received command: "{0}"'.format(command))
    robolog('sending response: "{0}"'.format(response))

    return bot.post(response)


def listen(port=''):
    # heroku provides the port variable for us
    port = int(os.getenv('PORT'))

    # open the listening socket
    robolog('opening listener socket on port {0}...'.format(port))
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


def robolog(message, level='info'):
    bold = '\033[1m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'

    if level == 'info':
        print(bold + green + '--> INFO: robodaniel: {0}'.format(message) + end)
    elif level == 'warn':
        print(bold + yellow + '--> WARNING: robodaniel: {0}'.format(message) + end)
    elif level == 'error':
        print(bold + red + '--> ERROR: robodaniel: {0}'.format(message) + end)


if __name__ == '__main__':
    # set api key from env variable instead of ~/.groupy.key
    config.API_KEY = os.getenv('API_KEY')

    # set up bot and start listening
    robolog('launching robodaniel...')
    bot = Bot.list().first
    listen()

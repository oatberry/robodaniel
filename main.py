#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#   intended to be run under heroku
#

import json, os, socket, time
from factoids import factoids
from groupy import Bot, config

def interpret(command):
    # interpret command for bot
    # TODO: more complicated commands
    try:
        response = factoids[command]
        robolog('received command: "{0}"'.format(command))
        bot.post(factoids[command])

    except:
        robolog('invalid command: {0}'.format(command))

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
        time.sleep(0.3)
        (connection, address) = s.accept()

        try:
            data = connection.recv(4096)
            robolog('raw data: {0}'.format(data))
            data = json.loads(data.decode('utf-8').split('\n')[-1])
            robolog('json message data: {0}'.format(data))

            if data['sender_type'] == "user" and data['text'][0] == '!':
                interpret(data['text'][1:])

        except Exception:
            pass

def robolog(message):
    print('--> robodaniel: {0}'.format(message))

if __name__ == '__main__':
    # set api key from env variable instead of ~/.groupy.key
    config.API_KEY = os.getenv('API_KEY')

    # set up bot and start listening
    robolog('launching robodaniel...')
    bot = Bot.list().first
    listen()

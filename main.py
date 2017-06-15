#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#   intended to be run under heroku
#

import json, os, socket, time, commands
from factoids import factoids
from groupy import Bot, config

factoid_list = list(factoids.keys())
command_list = dir(commands)

def interpret(command):
    # check if command/factoid exists, then run it
    if command in command_list:
        response = eval('commands.' + command + '()')
    elif command in factoid_list:
        response = factoids[command]
    else:
        robolog('invalid command: {0}'.format(command))

    robolog('received command: "{0}"'.format(command))
    robolog('sending response: "{0}"'.format(response))
    bot.post(response)

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

def robolog(message):
    print('--> robodaniel: {0}'.format(message))

if __name__ == '__main__':
    # set api key from env variable instead of ~/.groupy.key
    config.API_KEY = os.getenv('API_KEY')

    # set up bot and start listening
    robolog('launching robodaniel...')
    bot = Bot.list().first
    listen()

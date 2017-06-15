#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#   intended to be run under heroku
#

import json, os, socket, traceback
from factoids import factoids
from groupy import Bot, config

def interpret(command):
    # interpret command for bot
    # TODO: more complicated commands
    bot.post(factoids[command])

def listen(port=''):
    # heroku provides the port variable for us
    try:
        port = int(os.getenv('PORT'))
    except:
        port = 5000

    # open the listening socket
    print('--> ROBODANIEL: opening listener socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), port))
    s.listen(10)

    # attempt to extract chat message text from received data
    while True:
        (connection, address) = s.accept()

        try:
            data = connection.recv(1024)
            print('--> ROBODANIEL: raw data received: {0}'.format(data))
            data = json.loads(data.decode('utf-8').split('\n')[-1])
            print('--> ROBODANIEL: json data received: {0}'.format(data))

            if data['sender_type'] == "user" and data['text'][0] == '!':
                print('--> ROBODANIEL: interpreted command: {0}'.format(data['text'][1:]))
                interpret(data['text'][1:])

        except Exception:
            print(traceback.format_exc())

if __name__ == '__main__':
    # set api key from env variable instead of ~/.groupy.key
    config.API_KEY = os.getenv('API_KEY')

    # set up bot and start listening
    print('--> ROBODANIEL: launching robodaniel...')
    bot = Bot.list().first
    listen()

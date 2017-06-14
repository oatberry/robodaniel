import json
import os
import socket
from factoids import factoids
from groupy import Bot, config

config.API_KEY = os.getenv('API_KEY')

def interpret(command):
    bot.post(factoids[command])

def listen(port=''):
    try:
        port = int(os.getenv('PORT'))
    except:
        port = 5000

    print('--> opening listener socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), port))
    s.listen(10)

    while True:
        (connection, address) = s.accept()

        try:
            data = connection.recv(1024)
            print('DATA: {0}'.format(data))
            data = json.loads(data.decode('utf-8').split('\n')[-1])

            if data['sender_type'] == "user" and data['text'][0] == '!':
                print('--> received command: {0}'.format(data['text'][1:]))
                interpret(data['text'][1:])
        except:
            pass


if __name__ == '__main__':
    print('--> launching robodaniel...')
    bot = Bot.list().first
    listen()

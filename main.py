import json
import os
import socket
from groupy import Bot, config

config.API_KEY = os.getenv('API_KEY')

def listen(port=''):
    try:
        port = os.getenv('PORT')
    except:
        port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), port))
    s.listen(10)

    while True:
        (connection, address) = serversocket.accept()

        try:
            data = connection.recv(1024)
            print(data)
            # data = json.loads(data.decode('utf-8').split('\n')[-1])

            # if data['sender_type'] == "user":

        except:
            pass


if __name__ == '__main__':
    listen()

# bot = Bot.list().first
# bot.post("bleep bloop, under construction. also, no Thomas here. just bot.")

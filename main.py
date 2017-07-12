#
#   robodaniel - a silly groupme robot
#   by oatberry - released under the MIT license
#

import configparser
import json
import logging
import os
import re
import socket
import sys
import time
from bot import Bot


def listen(address, port, bot):
    "listen for new messages in the bot's groupme channel"

    # open the listening socket
    logging.info('opening listener socket on {} port {}...'.format(address, port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((address, port))
    s.listen(10)

    # attempt to extract chat message text from received data
    try:
        while True:
            (connection, address) = s.accept()

            try:
                time.sleep(0.3)
                data = connection.recv(4096)
                message = json.loads(data.decode('utf-8').split('\n')[-1])

                # log message to group log
                if message.get('text'):
                    bot.logmsg(message)

                if message['sender_type'] == 'user':
                    logging.debug('message received: {}'.format(message))
                    bot.match_trigger(message) # try to match all messages against triggers

            except Exception:
                pass

    except KeyboardInterrupt:
        logging.info('cleaning up...')
        bot.chatlog.close()
        sys.exit()


# set up logging
logging.basicConfig(level=logging.INFO, format="--> %(levelname)s: %(message)s")
logging.getLogger('requests').setLevel(logging.WARNING) # quiet down, requests!

# get config settings
parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['RoboDaniel']

bot = Bot(api_key=config['apikey'],
          bot_id=config['botid'])

if __name__ == '__main__':
    # start listening and interpreting
    logging.info('launching robodaniel...')

    listen(address=config['bindaddress'],
           port=config.getint('listenport'),
           bot=bot)

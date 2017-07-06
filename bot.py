"""Classes for RoboDaniel"""

import importlib
import logging
import re
from data import commands
from groupy import Bot as GroupyBot
from groupy import Group
from groupy import config


class Bot:
    """RoboDaniel bot class"""

    def __init__(self, api_key, bot_id):
        config.API_KEY = api_key
        self.bot = GroupyBot.list().filter(bot_id=bot_id).first
        self.group = Group.list().filter(id=self.bot.group_id).first

        self.logger = logging.getLogger(self.bot.name)

        self.generate_triggers()
        self.gather_commands()

    def gather_commands(self):
        """gather !command functions and factoids into dicts"""
        self.logger.info('gathering !commands...')

        # reload command module for when !reload is called
        importlib.reload(commands)

        r = re.compile('^__')
        self.command_dict = {c: getattr(commands, c)
                             for c in dir(commands)
                             if not r.match(c)}

        # gather factoids
        with open('data/factoids.txt') as factoids_file:
            self.factoids = {f.split()[0]: ' '.join(f.split()[1:])
                             for f in factoids_file}
        
    def generate_triggers(self):
        """generate message trigger rules"""
        self.logger.info('generating trigger rules...')

        with open('data/triggers.txt') as triggers_file:
            self.triggers = [(re.compile(t.split()[0]), ' '.join(t.split()[1:]))
                             for t in triggers_file]

    def interpret_command(self, message):
        """decide what to do with a "!command" message"""
        # extract the message text, minus the beginning '!'
        command = message['text'][1:]

        # put a precautionary space before each '@'
        # as GroupMe does weird stuff with mentions
        command = re.sub('@', ' @', command)
        
        if command in self.factoids:
            return [self.factoids[command]]

        args = command.split()
        if args[0] in self.command_dict:
            return self.command_dict[args[0]](args=args[1:],
                                              sender=message['name'],
                                              sender_id=message['user_id'],
                                              attachments=message['attachments'],
                                              bot=self)
        else:
            self.logger.warning('invalid command: {}'.format(command))
            return False
        
    def match_trigger(self, message):
        """attempt to match a message against trigger rules"""
        response = None

        if message['text'][0] == '!':
            # message contains a !command; try to interpret it
            self.logger.info('interpreted command: "{}"'.format(message['text']))
            response = self.interpret_command(message)
        else:
            # try each trigger rule
            for pattern, trigger in self.triggers:
                if pattern.match(message['text']):
                    # response is triggered
                    self.logger.info('trigger matched: "{}"'.format(message['text']))
                    response = [trigger]
                    break

        if response:
            # we have a response to send!
            logging.info('sending response: "{}"'.format(response))
            self.post(*response)

    def post(self, *message):
        """post a message with optional attachments"""
        self.bot.post(*message)

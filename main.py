import os
from groupy import Bot, config

config.API_KEY = os.getenv('API_KEY')

bot = Bot.list().first
bot.post("bleep bloop, under construction. also, no Thomas here. just bot.")

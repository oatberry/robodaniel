from groupy import Bot, config

with open('API_KEY.txt', 'r') as f:
    config.API_KEY = f.readline()

bot = Bot.list().first
bot.post("bleep bloop, under construction. also, no Thomas here. just bot.")

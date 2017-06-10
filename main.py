from groupy import Bot, config

config.API_KEY="9acd23902f8c0135bcbe01593d258a8d"

bot = Bot.list().first
bot.post("bleep boop")

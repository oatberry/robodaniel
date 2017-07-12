# RoboDaniel
A silly GroupMe bot written in Python 3


## Usage
* Install requirements: `pip install -r requirements.txt`
* Create your bot [here](https://dev.groupme.com/bots/new) if it doesn't already exist.
* Copy `config.ini.example` to `config.ini` and edit with your GroupMe API key, your bot's ID (can be found [here.](https://dev.groupme.com/bots)), and the listen address and port.
* Run `main.py`

## Additionally
* Commands are simple python functions, stored in `data/commands.py`
* Factoids are loaded from `data/factoids.txt`
* Bot is triggered by messages beginning with '!'
* Extra regex triggers and responses can be defined in `data/triggers.txt`

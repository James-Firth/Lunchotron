from slackbot.bot import respond_to
from slackbot.bot import listen_to
import subprocess
import re
import os
import ConfigParser

lunchotron_config = None
curr_dir =  os.path.dirname(os.path.realpath(__file__))

@respond_to('What.*|where.*', re.IGNORECASE)
def post_pic(message):
		message.send('For lunch: You should eat food')

@respond_to('hi', re.IGNORECASE)
def hello(message):
		message.send('Hello, I recommend food')

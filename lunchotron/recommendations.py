from slackbot.bot import respond_to
from slackbot.bot import listen_to
import subprocess
import re
import os
import random
import ConfigParser

lunchotron_config = None
curr_dir =  os.path.dirname(os.path.realpath(__file__))

def get_random_line(file_name):
	return (random.choice(list(open(file_name))))

def get_food_fact():
	return get_random_line(os.path.join(curr_dir, "food_fun_facts.txt"))

@respond_to("fact", re.IGNORECASE)
def fun_facts(message):
	message.reply("Food Fun Fact: "+get_food_fact())

@respond_to('What.*|where.*', re.IGNORECASE)
def post_pic(message):
	message.send('For lunch: You should eat food')

@respond_to('hi|hello', re.IGNORECASE)
def hello(message):
	message.send('Hello, I recommend food')

@respond_to('friend.*', re.IGNORECASE)
def friendship(message):
	message.reply("I'll be your friend!")

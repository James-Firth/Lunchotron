#!/usr/bin/python
from slackbot.bot import Bot
import slackbot.settings as settings
import logging
import sys
import os

#for config loading
import ConfigParser

def main():
	global lunchotron_config
	logging.basicConfig()
	curr_dir = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(curr_dir)

	lunchotron_config = ConfigParser.ConfigParser()
	lunchotron_config.read("config.ini")

	settings.API_TOKEN = lunchotron_config.get("slack", "API_TOKEN")

	settings.PLUGINS = ["lunchotron"] #Overwrites other plugins. Don't need upload for instance.
	bot = Bot()
	print "[[ lunchotron online ]]"
	bot.run()

def setup_config():
	sconfig = ConfigParser.ConfigParser()
	print "Performing first time setup..."
	API_TOKEN = raw_input("Please enter your slack API_TOKEN:")
	sconfig.add_section("slack")
	sconfig.set("slack", "API_TOKEN", API_TOKEN)

	with open("config.ini", "w") as f:
		sconfig.write(f)


	return

if __name__ == "__main__":
	if os.path.isfile("config.ini"):
		print "Running bot..."
		main()
	else:
		setup_config()
		print "Setup complete, running bot..."
		main()

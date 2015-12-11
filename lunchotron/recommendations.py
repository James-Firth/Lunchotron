from slackbot.bot import respond_to
from slackbot.bot import listen_to
import slackbot.settings as settings
from googleplaces import GooglePlaces, types, lang
import googlemaps
from unidecode import unidecode
import random
import subprocess
import re
import os
import random
import ConfigParser
from datetime import datetime

lunchotron_config = None
curr_dir =  os.path.dirname(os.path.realpath(__file__))

latest_recommendation = None
request_counter = 0


def get_random_line(file_name):
	return (random.choice(list(open(file_name))))

def get_food_fact():
	return get_random_line(os.path.join(curr_dir, "food_fun_facts.txt"))

def get_time_estimate_from_work(destination,when=datetime.now()):
	result = settings.gmaps.directions("220 Portage Ave, Winnipeg, MB", destination, mode="walking", departure_time=when)
	return result[0]['legs'][0]['duration']['text']

def get_recommendation(term=""):
	global latest_recommendation, request_counter

	the_place = None
	if request_counter < 990:
		if term == "" or term == None:
			result = settings.gPlaces.nearby_search(keyword=term, location=settings.location, radius=1200, types=[types.TYPE_FOOD, types.TYPE_RESTAURANT])
		else:
			result = settings.gPlaces.text_search(query=term, location=settings.location, radius=750, types=[types.TYPE_FOOD, types.TYPE_RESTAURANT])
		if len(result.places) > 0:
			max_val = len(result.places)-1
			index = random.randint(0,max_val)
			print "index ", index
			the_place = result.places[index]
			the_place.get_details()

			request_counter += 2
			latest_recommendation = the_place
		else:
			latest_recommendation = None

	else:
		print "REQUEST LIMIT REACHED"

	return the_place

@respond_to("fact", re.IGNORECASE)
def fun_facts(message):
	message.reply("Food Fun Fact: "+get_food_fact())

@listen_to('where should we eat|where to go|where to eat', re.IGNORECASE)
@respond_to('where should we eat|where to go|where to eat', re.IGNORECASE)
def recommend_something(message):
	the_place = get_recommendation()
	if the_place != None:
		if the_place.rating != None and the_place.rating != "":
			message.send("Try eating at %s, it has a rating of %.1f/5.0 :star: and is about %s away" % (unidecode(the_place.name), float(the_place.rating), get_time_estimate_from_work(the_place.formatted_address)) )
		else:
			message.send("Try eating at %s. It has no rating :confused: and is about %s away" % (unidecode(the_place.name), get_time_estimate_from_work(the_place.formatted_address) ) )
	else:
		message.send("Uh oh something went wrong. Maybe I hit my daily request limit?")

@respond_to("I want (.*)", re.IGNORECASE)
@listen_to("I want (.*)", re.IGNORECASE)
def something_like(message, term):
	query = "%s near 220 Portage Ave, Winnipeg, MB" % (term)
	the_place = get_recommendation(query)
	if the_place != None:
		if the_place.rating != None and the_place.rating != "":
			message.send("Try eating at %s, it has a rating of %.1f/5.0 :star: and is about %s away" % (unidecode(the_place.name), float(the_place.rating), get_time_estimate_from_work(the_place.formatted_address)) )
		else:
			message.send("Try eating at %s. It has no rating :confused: It is about %s away" % ( unidecode(the_place.name), get_time_estimate_from_work(the_place.formatted_address) ) )
	else:
		message.send("Uh oh something went wrong. Maybe I hit my daily request limit?")

@listen_to("where is that.*|where$|where's that", re.IGNORECASE)
@respond_to("where is that.*|where$|Where's that", re.IGNORECASE)
def get_location(message):
	if latest_recommendation != None:
		place_photo = ""
		if len(latest_recommendation.photos) > 0:
			latest_recommendation.photos[0].get(maxheight=500, maxwidth=500)
			place_photo = latest_recommendation.photos[0].url

		map_img = "https://maps.googleapis.com/maps/api/staticmap?size=500x500&markers=color:green%%7Clabel:W%%7C49.8947876,-97.1392768&markers=color:blue%%7C%s,%s" % (latest_recommendation.geo_location['lat'], latest_recommendation.geo_location['lng'])

		message.send("It's located at %s \n%s \n%s" %(latest_recommendation.vicinity, place_photo, map_img) )
	else:
		message.reply("Sorry I'm not sure where you're talking about.")

@listen_to('thank.*', re.IGNORECASE)
@respond_to("thank.*", re.IGNORECASE)
def welcome(message):
	message.send("You're welcome! I'm glad to help! :thumbsup:")

@respond_to('^hi|^hello', re.IGNORECASE)
def hello(message):
	message.send('Hello, I recommend food')

@respond_to('friend.*', re.IGNORECASE)
def friendship(message):
	message.reply("I'll be your friend!")

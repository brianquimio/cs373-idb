#!/usr/local/bin/python

#--------
# Imports
#--------

from static.other.locations import *
from static.other.stats import *
from Secrets import *
import json
import time


#--------------------------------
# Get all states as a json object
#--------------------------------

def write_states(places, state_filter=None):
	"""
	places: a Locations() object from the locations module
	state_filter: an optional list of stateCodes (2 char postal code) to filter states

	queries all of the states in US from trulia
	returns a json objects containing name, code, lat, long for each state
	"""

	states = places.get_states()

	if state_filter:
		states = [state for state in states if state['stateCode'] in state_filter]

	return states

#---------------------------------------------------------
# Get all cities for each state and insert into state JSON
#---------------------------------------------------------

def write_cities(places, state, city_filter=None):
	"""
	places: a Locations() object from the locations module
	locations: a json object containing 50 US states

	queries all of the cities within a specific state
	returns a modified json object containing the states with cities for the specified state
	"""

	# Make a call to trulia for a list of OrderedDicts of cities
	cities = places.get_cities_in_state(state['stateCode'])

	# Apply city filter to the 
	if city_filter:
		cities = [city for city in cities if city['name'] in city_filter]

	# add foreign key to JSON for the state
	for city in cities:
		city['stateCode'] = state['stateCode']

	# Return the modified states JSON object that now contains cities
	return cities


#------------------------------------------------------------------
# Get all neighborhoods for each city and insert into a JSON object
#------------------------------------------------------------------

def write_neighborhoods(places, city):
	"""
	places: a Locations() object from the locations module
	locations: a json object containing 50 US states
	states: an optional list of states to subset the entire list
	cities: an optional list of cities to subset the entire list

	queries all of the neighborhood within each city in a list of states
	returns a modified json object containing the states with cities for the specified state
	"""

	# Make a call to trulia for a list of OrderedDicts of cities
	neighborhoods = places.get_neighborhoods_in_city(city['name'],city['stateCode'])
	neighborhoods = [neighborhood for neighborhood in neighborhoods]

	# Add foreign keys
	for neighborhood in neighborhoods:
		neighborhood['stateCode'] = city['stateCode']
		neighborhood['city'] = city['cityId']


	return neighborhoods


#-------------------------
# Get stats for each state
#-------------------------

def write_state_stats(state, stats):
	"""
	stats: a TruliaStats() object from the stats module
	state: an OrderedDict containing state information

	returns a modified JSON object that contains stats for each state in provided input
	"""

	state_stats = stats.get_state_stats(state['stateCode'], start=date.today()-timedelta(days=30), type="listings")
	print(state_stats)

	return state_stats

#------------------------
# Get stats for each city
#------------------------

def write_city_stats(city, stats):
	"""
	city: an OrderedDict containing city information
	state: an OrderedDict containing state information
	stats: a TruliaStats() object from the stats module

	returns a modified JSON object that contains stats for each state in provided input
	"""

	city_stats = stats.get_city_stats(city['name'], city['stateCode'], start=date.today()-timedelta(days=30), type="listings")

	return city_stats

#--------------------------------
# Get stats for each neighborhood
#--------------------------------

def write_neighborhood_stats(neighborhood, stats):
	"""
	city: an OrderedDict containing city information
	state: an OrderedDict containing state information
	stats: a TruliaStats() object from the stats module

	returns a modified JSON object that contains stats for each state in provided input
	"""

	neighborhood_stats = stats.get_neighborhood_stats(neighborhood['id'], start=date.today()-timedelta(days=30), type="listings")

	# return json.loads(json.dumps(neighborhood_stats))
	return neighborhood_stats


#-----
# Main
#-----

if __name__ == '__main__':

	#---------------------------------------
	# Contruct Trulia API Extraction Objects
	#---------------------------------------

	places = Locations(truliaKey)
	stats = TruliaStats(truliaKey)

	# Specify a subset of States and cities
	state_filter = ['CA','TX','NY','WA']
	city_filter = ['Dallas', 'Houston', 'Austin', 'San Francisco', 'San Jose', 'Redwood City', 'Palo Alto', 'Mountain View', 'South San Francisco', 'San Mateo', 'Seattle', 'Bellevue', 'Redmond', 'Renton', 'Issaquah', 'New York City', 'Long Beach', 'Yonkers']


	# Query for all states from Trulia (applying filter)
	states = write_states(places, state_filter)
	states_json = json.loads(json.dumps(states))
	time.sleep(1)

	# Query for the listing stats for each state
	# state_stats = {}
	# for state in states:
	# 	state_stats[state['stateCode']] = write_state_stats(state, stats)
	# 	time.sleep(1)
	# state_stats_json = json.loads(json.dumps(state_stats))

	# Query for each city in specified states (applying filter)
	cities = []
	for state in states:
		cities += write_cities(places, state, city_filter)
		time.sleep(1)
	cities_json = json.loads(json.dumps(cities))

	# Query for the listing stats for each city
	# city_stats = {}
	# for city in cities:
	# 	city_stats[city['cityId']] = write_city_stats(city, stats)
	# 	time.sleep(1)
	# city_stats_json = json.loads(json.dumps(city_stats))

	# Query for neighborhood in all cities
	neighborhoods = []
	for city in cities:
		neighborhoods += write_neighborhoods(places, city)
		time.sleep(1)
	neighborhoods_json = json.loads(json.dumps(neighborhoods))

	# Query for the listing stats for each neighborhood
	neighborhood_stats = {}
	for neighborhood in neighborhoods:
		neighborhood_stats[neighborhood['id']] = write_neighborhood_stats(neighborhood, stats)
		time.sleep(1)
	neighborhood_stats_json = json.loads(json.dumps(neighborhood_stats))

#--------------------------------------
# Write States and State Stats to files
#--------------------------------------

	# file = open('states.json', 'a')
	# file.write('"states": ' + str(states_json))
	# file.close

	# file = open('state_stats.json', 'a')
	# file.write('"stateStats": [' + str(state_stats_json) + "]")
	# file.close

#-----------------------------------
# Write City and City Stats to files
#-----------------------------------

	# file = open('cities.json', 'a')
	# file.write('"cities":' + str(cities_json))
	# file.close

	# file = open('city_stats.json', 'a')
	# file.write(str(city_stats_json))
	# file.close

#---------------------------------------------------
# Write Neighborhood and Neighborhood Stats to files
#---------------------------------------------------

	# file = open('neighborhoods.json', 'a')
	# file.write('neighborhoods: [' + str(neighborhoods_json) + ']')
	# file.close

	file = open('neighborhood_stats.json', 'a')
	file.write(str(neighborhood_stats_json))
	file.close





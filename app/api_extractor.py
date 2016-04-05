#!/usr/local/bin/python

#--------
# Imports
#--------

from static.other.locations import *
from static.other.stats import *
from Secrets import *
import json
import time


#---------------------------------------
# Contruct Trulia API Extraction Objects
#---------------------------------------

places = Locations(truliaKey)
stats = TruliaStats(truliaKey)


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

	# states = json.loads(json.dumps(states))

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

	# check if caller specified a subset of cities and filter if so

	# Parse the list and convert it to JSON
	# cities = json.loads(json.dumps(cities))

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

	# Parse the list and convert it to JSON
	# neighborhoods = json.loads(json.dumps(neighborhoods))

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

	state_stats = stats.get_state_stats(state['stateCode'], start=date.today()-timedelta(years=2), type="listings")

	# return json.loads(json.dumps(state_stats))
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

	city_stats = stats.get_city_stats(city['name'], city['stateCode'], start=date.today()-timedelta(years=2), type="listings")

	# return json.loads(json.dumps(city_stats))
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

	neighborhood_stats = stats.get_neighborhoood_stats(neighborhood['neighborhoodId'], start=date.today()-timedelta(years=2), type="listings")

	# return json.loads(json.dumps(neighborhood_stats))
	return neighborhood_stats


#-----
# Main
#-----

if __name__ == '__main__':

	# Specify a subset of States and cities
	state_filter = ['CA','TX','NY','WA']
	city_filter = ['Dallas', 'Fort Worth', 'Houston', 'San Antonio', 'Austin', 'San Francisco', 'San Jose', 'Redwood City', 'Palo Alto', 'Mountain View', 'Cupertino', 'Sunnyvale', 'Los Gatos', 'Milpitas', 'Fremont', 'Menlo Park', 'South San Francisco', 'San Mateo', 'Seattle', 'Bellevue', 'Redmond', 'Renton', 'Newcastle', 'Mercer Island', 'Bainbridge Island', 'Sammamish', 'Issaquah', 'Bothell', 'New York City', 'Long Beach', 'Yonkers', 'Glen Cove']

	# Query for all states from Trulia (applying filter)
	states = write_states(places, state_filter)
	states_json = json.loads(json.dumps(states))
	time.sleep(31)

	# Query for each city in specified states (applying filter)
	cities = []
	print("States :" + str(states))
	for state in states:
		cities += write_cities(places, state, city_filter)
		print("writing city: " + str(cities[-1]))
		time.sleep(31)
	cities_json = json.loads(json.dumps(cities))

	# Query for neighborhood in all cities
	neighborhoods = []
	print("Cities: " + str(cities))
	for city in cities:
		test = write_neighborhoods(places, city)
		if len(test) > 0:
			time.sleep(31)
			neighborhoods += test
			print("writing neighborhood: " + str(neighborhoods[-1]))
	neighborhoods_json = json.loads(json.dumps(neighborhoods))

	# Query for the listing stats for each state
	state_stats = []
	for state in states:
		state_stats += write_state_stats(state, stats)
		time.sleep(31)
	state_stats_json = json.loads(json.dumps(state_stats))

	# Query for the listing stats for each city
	city_stats = []
	for city in cities:
		city_stats += write_city_stats(city, stats)
		time.sleep(31)
	city_stats_json = json.loads(json.dumps(city_stats))

	# Query for the listing stats for each neighborhood
	neighborhood_stats = []
	for neighborhood in neighborhoods:
		neighborhood_stats += write_neighborhood_stats(neighborhood, stats)
		time.sleep(31)


#--------------------------------------
# Write States and State Stats to files
#--------------------------------------

	file = open('states.json', 'a')
	file.write(str(states_json))
	file.close

	file = open('state_stats.json', 'a')
	file.write(str(states_stats_json))
	file.close

#-----------------------------------
# Write City and City Stats to files
#-----------------------------------

	file = open('cities.json', 'a')
	file.write(str(cities_json))
	file.close

	file = open('city_stats.json', 'a')
	file.write(str(city_stats_json))
	file.close

#---------------------------------------------------
# Write Neighborhood and Neighborhood Stats to files
#---------------------------------------------------

	file = open('neighborhoods.json', 'a')
	file.write(str(neighborhoods_json))
	file.close

	file = open('neighborhood_stats.json', 'a')
	file.write(str(neighborhood_stats_json))
	file.close





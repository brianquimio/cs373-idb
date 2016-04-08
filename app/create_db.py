#!/usr/local/bin/python

#--------
# Imports
#--------

from db import db
from models import State, StateStats, City, CityStats, Neighborhood, NeighborhoodStats
import json


def init_states(states_file):
	"""
	Insert data for states pulled from trulia API
	"""

	states_json = json.loads(states_file)

	for state in states_json["states"]:
		s = State(state['stateCode'], state['name'], state['latitude'], state['longitude'])
		db.session.add(s)
		db.session.commit()

def init_state_stats(state_stats_file):
	"""
	Insert data for state stats pulled from trulia API
	"""

	state_stats_json = json.loads(state_stats_file)
	state_codes = state_stats_json['stateStats'].keys()

	for code in state_codes:
		for week in state_stats_json['stateStats'][code]['listingStat']:
			week_of = week['weekEndingDate']
			for subcat in state_stats_json['stateStats'][code]['listingStat']['listingPrice']['subcategory']:
				num_properties = subcat['numberOfProperties']
				med_listing_price = int(subcat['medianListingPrice'])
				avg_listing_price = int(subcat['averageListingPrice'])
				property_type = subcat['type']

				stats = StateStats(week_of, property_type, num_properties, med_listing_price, avg_listing_price, code)
				
				db.session.add(stats)
				db.session.commit()


def init_cities(cities_file):
	"""
	Insert data for cities pulled from trulia API
	"""

	cities_json = json.loads(cities_file)

	for city in cities_json["states"]:
		s = City(city['cityId'], city['name'], city['stateCode'], city['latitude'], city['longitude'])
		db.session.add(s)
		db.session.commit()

def init_city_stats(city_stats_file):
	"""
	Insert data for city stats pulled from trulia API
	"""
	city_stats_json = json.loads(city_stats_file)
	city_codes = city_stats_json['cityStats'].keys()

	for code in city_codes:
		for week in city_stats_json['cityStats'][code]['listingStat']:
			week_of = week['weekEndingDate']
			for subcat in city_stats_json['cityStats'][code]['listingStat']['listingPrice']['subcategory']:
				num_properties = subcat['numberOfProperties']
				med_listing_price = int(subcat['medianListingPrice'])
				avg_listing_price = int(subcat['averageListingPrice'])
				property_type = subcat['type']

				stats = CityStats(week_of, code, property_type, num_properties, avg_listing_price, med_listing_price)
				
				db.session.add(stats)
				db.session.commit()

def init_neighborhoods(neighborhood_file):
	"""
	Insert data for neighborhoods pulled from trulia API
	"""
	neighborhoods_json = json.loads(neighborhood_file)

	for neighborhood in neighborhoods_json["neighborhoods"]:
		s = Neighborhood(neighborhood['id'], neighborhood['name'], neighborhood['stateCode'], neighborhood['city'])
		db.session.add(s)
		db.session.commit()

def init_neighborhood_stats(neighborhood_stats_file):
	"""
	Insert data for neighborhood stats from trulia API
	"""
	neighborhood_stats_json = json.loads(neighborhood_stats_file)
	neighborhood_codes = neighborhood_stats_json['neighborhoodStats'].keys()

	for code in neighborhood_codes:
		for week in neighborhood_stats_json['neighborhoodStats'][code]['listingStat']:
			week_of = week['weekEndingDate']
			for subcat in neighborhood_stats_json['cityStats'][code]['listingStat']['listingPrice']['subcategory']:
				num_properties = subcat['numberOfProperties']
				med_listing_price = int(subcat['medianListingPrice'])
				avg_listing_price = int(subcat['averageListingPrice'])
				property_type = subcat['type']

				stats = NeighborhoodStats(week_of, code, property_type, num_properties, med_listing_price, avg_listing_price)
				
				db.session.add(stats)
				db.session.commit()

def init_db():
	"""
	initialize the database for virtual-address.space
	"""

	db.drop_all()
	db.create_all()

	# Init states
	with open('states.json') as states:
		init_states(json.loads(states))

	# Init state stats
	with open('state_stats.json') as state_stats:
		init_state_stats(json.loads(state_stats))

	# Init cities
	with open('cities.json') as cities:
		init_cities(json.loads(cities))

	# Init city stats
	with open('city_stats.json') as city_stats:
		init_city_stats(json.loads(city_stats))

	# Init neighborhoods
	with open('neighborhoods.json') as neighborhoods:
		init_neighborhoods(json.loads(neighborhoods))

	# Init neighborhood stats
	with open('neighborhood_stats.json') as neighborhood_stats:
		init_neighborhood_stats(json.loads(neighborhood_stats))





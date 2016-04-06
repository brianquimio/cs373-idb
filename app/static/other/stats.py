#!/usr/local/bin/python


# -------
# Imports
# -------

import requests, xmltodict, datetime
from datetime import timedelta, date


# ---------------------------------
# Object for statistics from Trulia
# ---------------------------------


class TruliaStats(object):
    """
    retrieves stats data from the Trulia API and returns it as an OrderedDict
    """

    def __init__(self, apikey):
        self.apikey = apikey
        self.url = "http://api.trulia.com/webservices.php"


    # -------------------
	# Function decorators
	# -------------------

    def get_stats(f):
        """
        function decorator that returns the results for trulia stats api calls
        """
        def g(*args, **kwargs):
            xml = requests.get(args[0].url, params=f(*args, **kwargs))
            results = xmltodict.parse(xml.content)
            stats = results["TruliaWebServices"]["response"]["TruliaStats"]["listingStats"]
            return stats
        return g


    # -------------
	# Class methods
	# -------------

    @get_stats
    def get_city_stats(self, city, state, start=date.today()-timedelta(days=30), end=date.today(), type="all"):
        """
        city is string value for name of city
        state is two character postal code
        start is start date of data set
        end is end data of data set
        type can be 'all', 'traffic', or 'listings' 
        returns an OrderedDict of stats for specified city/state
        """

        parameters = {
            "library": "TruliaStats",
            "function": "getCityStats",
            "city": city,
            "state": state,
            "startDate": start,
            "endDate": end,
            "statType": type,
            "apikey": self.apikey
        }

        return parameters


    @get_stats
    def get_county_stats(self, county, state, start=date.today()-timedelta(days=30), end=date.today(), type="all"):
        """
        county is string name of county
        state is two character postal code
        start is start date of data set
        end is end data of data set
        type can be 'all', 'traffic', or 'listings' 
        returns OrderedDict of stats for specified county/state
        """

        parameters = {
            "library": "TruliaStats",
            "function": "getCountyStats",
            "county": county,
            "state": state,
            "startDate": start,
            "endDate": end,
            "statType": type,
            "apikey": self.apikey
        }

        return parameters

    @get_stats
    def get_neighborhood_stats(self, neighborhood_id, start=date.today()-timedelta(days=30), end=date.today(), type="all"):
        """
        neighborhood_id is unique integer value for trulia neighborhood
        start is start date of data set
        end is end data of data set
        type can be 'all', 'traffic', or 'listings' 
        returns an OrderedDict of stats for specified neighborhood
        """

        parameters = {
            "library": "TruliaStats",
            "function": "getNeighborhoodStats",
            "neighborhoodId": neighborhood_id,
            "startDate": start,
            "endDate": end,
            "statType": type,
            "apikey": self.apikey
        }

        return parameters

    @get_stats
    def get_state_stats(self, state, start=date.today()-timedelta(days=30), end=date.today(), type="all"):
        """
        state is two character postal code
        start is start date of data set
        end is end data of data set
        type can be 'all', 'traffic', or 'listings' 
        Returns OrderedDict of stats for specified state
        """

        parameters = {
            "library": "TruliaStats",
            "function": "getStateStats",
            "state": state,
            "startDate": start,
            "endDate": end,
            "statType": type,
            "apikey": self.apikey
        }

        return parameters

    @get_stats
    def get_zip_data(self, zipcode, start=date.today()-timedelta(days=30), end=date.today(), type="all"):
        """
        zipcode is 5 digit integer zip code
        start is start date of data set
        end is end data of data set
        type can be 'all', 'traffic', or 'listings' 
        returns OrderedDict of stats for specified zipcode
        """

        parameters = {
            "library": "TruliaStats",
            "function": "getZipCodeStats",
            "zipCode": zipcode,
            "startDate": start,
            "endDate": end,
            "statType": type,
            "apikey": self.apikey
        }

        return parameters
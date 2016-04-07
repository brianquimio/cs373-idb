#!/usr/local/bin/python


# -------
# Imports
# -------

import requests, xmltodict


# ----------------
# Location classes
# ----------------

class Locations(object):
    """
    retrieves location data from the Trulia API and returns it as an OrderedDict
    """

    def __init__(self, apikey):
        self.apikey = apikey
        self.url = "http://api.trulia.com/webservices.php"
        self.aggregation = ""


    # -------------------
    # Method decorators
    # -------------------

    def get_results(f):
        def g(*args, **kwargs):

            try:
                xml = requests.get(args[0].url, params=f(*args, **kwargs))
                results = xmltodict.parse(xml.content)
                retval = results["TruliaWebServices"]["response"]["LocationInfo"][args[0].aggregation]
                return retval
            except KeyError as e:
                retval = []
                return retval

        return g


    # -------------
    # Class methods
    # -------------

    @get_results
    def get_cities_in_state(self, state):
        """
        state is two character postal code
        returns OrderedDict of all cities in specified state
        """

        self.aggregation = "city"
        parameters = {
            "library": "LocationInfo",
            "function": "getCitiesInState",
            "state": state,
            "apikey": self.apikey
        }

        return parameters


    @get_results
    def get_counties_in_state(self, state):
        """
        state is two character postal code
        returns OrderedDict of all counties in specified state
        """

        self.aggregation = "county"
        parameters = {
            "library": "LocationInfo",
            "function": "getCountiesInState",
            "state": state,
            "apikey": self.apikey
        }

        return parameters

    @get_results
    def get_neighborhoods_in_city(self, city, state):
        """
        city is string of city name
        state is two character postal code
        returns OrderedDict of all neighborhoods in specified city
        """

        self.aggregation = "neighborhood"
        parameters = {
            "library": "LocationInfo",
            "function": "getNeighborhoodsInCity",
            "city": city,
            "state": state,
            "apikey": self.apikey
        }

        return parameters

    @get_results
    def get_states(self):
        """
        returns OrderedDict of all states in the US
        """

        self.aggregation = "state"
        parameters = {
            "library": "LocationInfo",
            "function": "getStates",
            "apikey": self.apikey
        }

        return parameters

    @get_results
    def get_zip_codes_in_state(self, state):
        """
        state is two character postal code
        returns OrderedDict of all zipcodes in specified state
        """

        self.aggregation = "zipCode"
        parameters = {
            "library": "LocationInfo",
            "function": "getZipCodesInState",
            "state": state,
            "apikey": self.apikey
        }

        return parameters
#!/usr/local/bin/python


# -------
# Imports
# -------

import requests, jsontodict, datetime

class Parks(object):

	"""
    retrieves park data from the ACTIVE Campground API and returns it as an OrderedDict
    """

    def __init__ (self, apikey):
    self.apikey = apikey
    self.url = "http://api.amp.active.com/camping/campgrounds?"


    #requested information to be returned in json, but online calls say "This XML file does not appear to have any style information associated with it."
    #wiil need to test to see which information is being returned. 
    def get_parks(f):
        def g(n):

            xml = requests.get(url, params=parameters)
            results = xmltodict.parse(xml.content)
            retval = results[""]["response"]["LocationInfo"]

        return retval

    @get_parks
    def get_state_parks(self, pstate):
        """
        state is two character  code
        returns an OrderedDict of stats for specified city/state
        """

        url = "http://api.trulia.com/webservices.php"
        parameters = {
            "pstate": pstate,
            "apikey": self.apikey
        }

        return parameters
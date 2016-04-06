#!/usr/local/bin/python


# -------
# Imports
# -------

import requests, xmltodict, datetime

class Parks(object):

	"""
	retrieves park data from the ACTIVE Campground API and returns it as an OrderedDict
	"""

	def __init__ (self, apikey):
		self.apikey = apikey
		self.url = "http://api.amp.active.com/camping/campgrounds"

	#requested information to be returned in json, but online calls say "This XML file does not appear to have any style information associated with it."
	#wiil need to test to see which information is being returned. 

	def get_state_parks(self, pstate):
		"""
		state is two character code
		returns an OrderedDict of stats about the park
		"""

		parameters = {
			"pstate": pstate,
			"api_key": self.apikey
		}

		xml = requests.get(self.url, params=parameters)
		results = xmltodict.parse(xml.content)
		print(results)
		retval = results["resultset"]["result"][0]["@facilityName"]
		print(retval)

		return retval
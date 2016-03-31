# -------
# Imports
# -------

from unittest       import main, TestCase
from stats          import TruliaStats

# ------
# set-up
# ------

data = TruliaStats('nctn3tmtxydytsqj6bmzjzrg')

# -----
# Stats
# -----

class TestStats(TestCase):

    # -----
    # State
    # -----

    def test_state_stats_1(self):
        state = "Texas"
        stats = data.get_state_stats(state = 'TX')
        self.assertEqual(state, stats['location']['stateName'])

    def test_state_stats_2(self):
        state = "California"
        stats = data.get_state_stats(state = 'CA')
        self.assertEqual(state, stats['location']['stateName'])

    def test_state_stats_3(self):
        state = "New York"
        stats = data.get_state_stats(state = 'NY')
        self.assertEqual(state, stats['location']['stateName'])

    # ------
    # county
    # ------

    def test_county_stats_1(self):
        county = "Travis"
        stats = data.get_county_stats(county = 'Travis', state = 'TX')
        self.assertEqual(county, stats['location']['county'])

    def test_county_stats_2(self):
        county = "Harris"
        stats = data.get_county_stats(county = 'Harris', state = 'TX')
        self.assertEqual(county, stats['location']['county'])

    # ----
    # city
    # ----

    def test_city_stats_1(self):
        city = "Austin"
        stats = data.get_city_stats(city = 'Austin', state = 'TX')
        self.assertEqual(city, stats['location']['city'])

    def test_city_stats_2(self):
        city = "New York City"
        stats = data.get_city_stats(city = 'New York City', state = 'NY')
        self.assertEqual(city, stats['location']['city'])

    # -------
    # zipcode
    # -------

    def test_zip_data_1(self):
        zipcode = '78705' 
        stats = data.get_zip_data(zipcode = 78705)
        self.assertEqual(zipcode, stats['location']['zipCode'])

    # ------------
    # neighborhood
    # ------------

    def test_neighborhood_stats_1(self):
        neighborhood = "Abbott Loop"
        stats = data.get_neighborhood_stats(neighborhood_id = 1)
        self.assertEqual(neighborhood, stats['location']['neighborhoodName'])

# ----
# Main
# ----

if __name__ == '__main__' :
    main()
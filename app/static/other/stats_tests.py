# -------------------------------
# Written by Steven Zhu
# Virtual_Address IDB
# Copyright (C) 2016 pshh jk
# -------------------------------

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
        stats = data.get_state_stats(state = 'TX')
        self.assertTrue(stats['location']['stateName'] is not None)

    def test_state_stats_2(self):
        state = "California"
        stats = data.get_state_stats(state = 'CA')
        self.assertEqual(state, stats['location']['stateName'])

    def test_state_stats_3(self):
        state = "New York"
        stats = data.get_state_stats(state = 'NY')
        self.assertEqual('15500000', stats['listingStats']['listingStat'][0]['listingPrice']['subcategory'][14]['medianListingPrice'])

    # ------
    # county
    # ------

    def test_county_stats_1(self):
        stats = data.get_county_stats(county = 'Travis', state = 'TX')
        self.assertTrue(stats['location']['county'] is not None)

    def test_county_stats_2(self):
        county = "Harris"
        stats = data.get_county_stats(county = 'Harris', state = 'TX')
        self.assertEqual(county, stats['location']['county'])

    def test_county_stats_3(self):
        stats = data.get_county_stats(county = 'Santa Clara', state = 'CA', start = '2016-03-01', end = '2016-03-31')
        self.assertEqual('843', stats['listingStats']['listingStat'][0]['listingPrice']['subcategory'][0]['numberOfProperties'])


    # ----
    # city
    # ----

    def test_city_stats_1(self):
        city = "Austin"
        stats = data.get_city_stats(city = 'Austin', state = 'TX', start = '2016-03-01', end = '2016-03-31', type = 'listings')
        self.assertEqual('1722', stats['listingStats']['listingStat'][0]['listingPrice']['subcategory'][0]['numberOfProperties'])

    def test_city_stats_2(self):
        city = "Austin"
        stats = data.get_city_stats(city = 'Austin', state = 'TX', start = '2016-03-01', end = '2016-03-31', type = 'listings')
        self.assertEqual('35', stats['listingStats']['listingStat'][0]['listingPrice']['subcategory'][1]['numberOfProperties'])

    def test_city_stats_3(self):
        city = "Austin"
        stats = data.get_city_stats(city = 'Austin', state = 'TX', start = '2016-03-01', end = '2016-03-31', type = 'listings')
        self.assertEqual('430297', stats['listingStats']['listingStat'][0]['listingPrice']['subcategory'][2]['averageListingPrice'])

    # -------
    # zipcode
    # -------

    def test_zip_data_1(self):
        stats = data.get_zip_data(zipcode = 78705)
        self.assertTrue(stats['location']['zipCode'] is not None)

    def test_zip_data_2(self):
        zipcode = '78705' 
        stats = data.get_zip_data(zipcode = 78705)
        self.assertEqual(zipcode, stats['location']['zipCode'])

    def test_zip_data_3(self):
        zipcode = '75633' 
        stats = data.get_zip_data(zipcode = 75633)
        self.assertEqual(zipcode, stats['location']['zipCode'])

    # ------------
    # neighborhood
    # ------------

    def test_neighborhood_stats_1(self):
        stats = data.get_neighborhood_stats(neighborhood_id = 1)
        self.assertTrue(stats['location']['neighborhoodName'] is not None)

    def test_neighborhood_stats_2(self):
        neighborhood = "Abbott Loop"
        stats = data.get_neighborhood_stats(neighborhood_id = 1)
        self.assertEqual(neighborhood, stats['location']['neighborhoodName'])

    #------------
    # stress test
    #------------

    def test_stress(self):
        stats = data.get_neighborhood_stats(neighborhood_id = 1, start = '2010-01-01', end = '2016-03-31', type = 'listings')
        self.assertTrue(stats is not None)



# ----
# Main
# ----

if __name__ == '__main__' :
    main()
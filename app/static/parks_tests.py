# -------------------------------
# Written by Steven Zhu
# Virtual_Address IDB
# Copyright (C) 2016 pshh jk
# -------------------------------

# -------
# Imports
# -------

from unittest       import main, TestCase
from parks          import Parks

# ------
# set-up
# ------

data = Parks('8ht7msbmzmvdv6xatyw6twu9')

# -----
# Parks
# -----

class TestParks(TestCase):

    # ---------------
    # get_state_parks
    # ---------------

    def test_get_state_parks(self):
        parks = data.get_state_parks(pstate = 'NY')
        self.assertTrue(parks is not None)

    def test_get_state_parks(self):
        parks = data.get_state_parks(pstate = 'TX')
        self.assertTrue(parks['Big Bend'] is not None)


    #------------
    # stress test
    #------------

    def test_for_stress(self):
        states = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'Fl','GA',
                'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')
        for s in states :
            parks = data.get_state_parks(pstate = s)
            self.assertTrue(parks is not None)


# ----
# Main
# ----

if __name__ == '__main__' :
    main()
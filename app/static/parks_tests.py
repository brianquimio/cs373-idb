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

    def test_get_state_parks_1(self):
        parks = data.get_state_parks(pstate = 'NY')
        self.assertTrue(parks is not None)

    def test_get_state_parks_2(self):
        parks = data.get_state_parks(pstate = 'TX')
        self.assertTrue('AIRPORT PARK' in parks)

# ----
# Main
# ----

if __name__ == '__main__' :
    main()
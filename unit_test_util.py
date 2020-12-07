#This file tests the database operations
from Homer_db import Homer_db 
from Subscription import Subscription
import unittest

db = Homer_db()
subsc = Subscription()

class HomerUtilTest(unittest.TestCase):

    def cov_into_date(self):
        # check if converted date format is correct
        self.assertEqual(0, 0, "count should be zero")

if __name__ == '__main__':
    unittest.main()
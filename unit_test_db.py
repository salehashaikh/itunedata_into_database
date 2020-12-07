#This file tests the database operations
from Homer_db import Homer_db 
from Subscription import Subscription
from homer_test import insert_data
import unittest

db = Homer_db()
subsc = Subscription()

class HomerdbTest(unittest.TestCase):

    def test_select(self):
        # When database table is empty, it should return zero
        subsc.delete_table(db)
        self.assertEqual(subsc.get_records_count(db) , 0, "count should be zero")

    def test_create_table(self):
        # call create table method
        # Fetch records and note count of rows - it should be zero
        subsc.create_table(db)
        self.assertEqual(subsc.get_records_count(db) , 0, "count should be zero")

    def test_insert(self):
        # Delete exisitng table, call create new table method
        # Insert records
        # Fetch all rows count and it should match to inputed data numbers
        subsc.create_table(db)
        insert_data(db, subsc, "data.json")
        self.assertEqual(subsc.get_records_count(db) , 5, "count should be five")
    
    def test_delete_table(self):
        # Delete table using its method
        # fetch rows count and it should be zero
        subsc.delete_table(db)
        self.assertEqual(subsc.get_records_count(db) , 0, "count should be zero")

    def test_select_count(self):
        # delete table and insert data in it
        # get the count and it should match with local json file data
        subsc.create_table(db)
        insert_data(db, subsc, "data.json")
        self.assertEqual(subsc.get_subsc_count(db, "Active Trial") , 0, "count should be zero")

if __name__ == '__main__':
    unittest.main()

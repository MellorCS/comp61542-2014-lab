__author__ = 'panos'
import unittest
from os import path
from comp61542.database import database

class getResultsOfSearch(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_get_results_of_search_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "publications_small_sample.xml")))
        data = db.get_results_of_search_author("sean")
        print data
        self.assertEqual(len)



if __name__ == "__main__":
 unittest.main()

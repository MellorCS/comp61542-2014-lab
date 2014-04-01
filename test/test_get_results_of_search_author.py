__author__ = 'panos'
__author__ = 'panos'
import unittest
from os import path
from comp61542.database import database

class getResultsOfSearchAuthor(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_get_results_of_search_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint2test.xml")))
        data = db.get_results_of_search_name_author("Sam")
        sortedData = db.get_results_of_search_author("Sam",data)
        self.assertEqual(sortedData[0],"Sam Alice",
            "incorrect sorted result")
        self.assertEqual(sortedData[1],"Sam Brian",
            "incorrect sorted result")





if __name__ == "__main__":
 unittest.main()

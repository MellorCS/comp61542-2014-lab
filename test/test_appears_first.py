import unittest
from os import path
from comp61542.statistics.appears_first import author_appears_first
from comp61542.database import database
__author__ = 'zoe'

class AppearsFirst(unittest.TestCase):

    def setUp(self):
        pass

    def test_appear_first_is_zero_for_empty_dataset(self):
           self.assertEqual(author_appears_first([]), 0)

    def temp(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
            "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
            "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
            "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
            "incorrect number of authors for conference papers")

if __name__ == "__main__":
 unittest.main()
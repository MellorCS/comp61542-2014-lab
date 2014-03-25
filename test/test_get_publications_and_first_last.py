__author__ = 'panos'
import unittest
from os import path

from comp61542.database import database
__author__ = 'zoe'

class AppearsFirst(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")



    def test_get_publications_and_first_last(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "publications_small_sample.xml")))
        header, data = db.get_publications_and_first_last()
        print data[2]
        self.assertEqual(len(header),len(data[0]),
            "header and data column size doesn't match.")
        self.assertEqual(data[2][1],1,
            "incorrect number of conference papers.")
        self.assertEqual(data[2][2],0,
            "incorrect number of journals.")
        self.assertEqual(data[2][3],0,
            "incorrect number of books.")
        self.assertEqual(data[2][4],0,
            "incorrect number of book chapters.")
        self.assertEqual(data[2][5],0,
            "incorrect number of times appeared first in a publicatio.n")
        self.assertEqual(data[2][6],0,
            "incorrect number of times appeared last in a publication.")
        self.assertEqual(data[2][7],3,
            "incorrect number of co-authors.")
        self.assertEqual(data[2][8],1,
            "incorrect number of total publications.")



if __name__ == "__main__":
 unittest.main()
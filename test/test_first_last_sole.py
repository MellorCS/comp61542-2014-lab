import unittest
from os import path

from comp61542.database import database
__author__ = 'panos'

class FirstLastSole(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")


    def test_get_first_last_sole(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        header, data = db.get_first_last_sole(4)
        print data
        self.assertEqual(len(header),len(data[0]),
            "header and data have different length. ")
        self.assertEqual(len(data),len(db.authors),
            "incorrect number of authors")
        self.assertEqual(data[0][3],1,
            "incorrect number of times an author appears as a sole author")
        self.assertEqual(data[0][1],2,
            "incorrect number of times an author appears first")
        self.assertEqual(data[2][2],2,
            "incorrect number of times an author appears last")


if __name__ == "__main__":
 unittest.main()
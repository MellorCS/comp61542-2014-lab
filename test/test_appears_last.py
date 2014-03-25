__author__ = 'fuhao'
import unittest
from os import path
import comp61542
from comp61542.database import database

class TestAppearsLast(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")



    def test_authors_who_appear_last(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "publications_small_sample.xml")))
        header, data = db.get_authors_who_appear_last()
        print data[1]
        self.assertEqual(len(header), len(data[0]),
            "header and data column size doesn't match")
        self.assertEqual(len(data), 14,
            "incorrect number of authors")
        self.assertEqual(data[1][1],1,
            "incorrect number of times appeared first in conference papers")
        self.assertEqual(data[1][2],0,
            "incorrect number of times appeared first in journals")
        self.assertEqual(data[1][3],0,
            "incorrect number of times appeared first in books")
        self.assertEqual(data[1][4],0,
            "incorrect number of times appeared first in book chapters")
        self.assertEqual(data[1][5],1,
            "incorrect number of times appeared first in total")
if __name__ == '__main__':
    unittest.main()
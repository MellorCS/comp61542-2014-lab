__author__ = 'panos'
__author__ = 'panos'
import unittest
from os import path
from comp61542.database import database

class getAuthorStats(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_get_author_statistics(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        db.get_author_statistics("AUTHOR1")






if __name__ == "__main__":
 unittest.main()

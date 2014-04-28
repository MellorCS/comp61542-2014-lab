from os import path
import unittest

from comp61542.database import database

class TestApp(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")


    def test_detect_whether_author_exist(self):
        db=database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        exist=db.detect_whether_the_author_exists("AUTHOR2")
        self.assertEqual(exist,1)

if __name__ == "__main__":
 unittest.main()
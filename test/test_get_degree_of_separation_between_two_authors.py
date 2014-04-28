__author__ = 'panos'
import unittest
from os import path

from comp61542.database import database


class getDegreeOfSeparation(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_get_degree_of_separation_between_two_authors(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "publications_small_sample.xml")))
        data = db.get_degree_of_separation_between_two_authors("Bechhofer Sean","Horan Bernard")
        self.assertEqual(data,0,
             "Incorrect degree of separation between authors who collaborated directly")
        data = db.get_degree_of_separation_between_two_authors("Lopez Rodrigo","Ceri Stefano")
        self.assertEqual(data,'X',
             "Incorrect degree of separation between authors who did not collaborate at all")


if __name__ == "__main__":
 unittest.main()


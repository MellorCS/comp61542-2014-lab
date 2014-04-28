__author__ = 'panos'
import unittest
from os import path

from comp61542.database import database



class getNetworkData(unittest.TestCase):

    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_get_network_data(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "publications_small_sample.xml")))
        graph = db.get_network_data()
        print graph


if __name__ == "__main__":
 unittest.main()

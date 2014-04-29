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

        self.assertEqual(len(graph[0]),14,
            "Incorrect number of vertices in the network graph")
        self.assertEqual(len(graph[1]),23,
            "Incorrect number of vertices in the network graph")
        self.assertTrue((1,3) in graph[1],
            "Incorrect graph created")
        self.assertTrue((0,3) in graph[1],
            "Incorrect graph created")
if __name__ == "__main__":
 unittest.main()

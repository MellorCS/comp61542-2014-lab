import unittest
from comp61542.statistics.appears_first import author_appears_first

__author__ = 'zoe'

class AppearsFirst(unittest.TestCase):

    def setUp(self):
        pass

    def test_appear_first_is_zero_for_empty_dataset(self):
           self.assertEqual(author_appears_first([]), 0)



if __name__ == "__main__":
 unittest.main()
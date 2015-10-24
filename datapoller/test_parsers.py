from datapoller.parsers import *
from testdata import *

import unittest
import os

class TestParsers(unittest.TestCase):
    def test_parse_nowcast(self):
        data, time = parse_nowcast(open(os.path.join('testdata', 'aurora-nowcast-map.txt')))
        self.assertEqual(data, NOWCAST_DATA)
        self.assertEqual(time, NOWCAST_TIME)

if __name__ == '__main__':
    unittest.main()


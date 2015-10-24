from datapoller.parsers import *
from testdata import *

import unittest
import os


class TestParsers(unittest.TestCase):
    def test_parse_nowcast(self):
        nowcast = list(parse_nowcast(open(os.path.join('testdata/', 'aurora-nowcast-map.txt'))))
        self.assertEqual(list(nowcast), NOWCAST_DATA)

if __name__ == '__main__':
    unittest.main()


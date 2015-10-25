from datapoller.parsers import *
from testdata import *

import unittest
import os

class TestParsers(unittest.TestCase):
    def test_parse_nowcast(self):
        data, time = parse_nowcast(open(os.path.join('..', 'testdata', 'aurora-nowcast-map.txt')))
        self.assertEqual(data, NOWCAST_DATA)
        self.assertEqual(time, NOWCAST_TIME)

    def test_parse_threeday(self):
        forecasts = parse_three_day_forecast(open(os.path.join('..', 'testdata', '3-day-forecast.txt')))
        self.assertEqual(forecasts, THREEDAY_FORECASTS)

if __name__ == '__main__':
    unittest.main()


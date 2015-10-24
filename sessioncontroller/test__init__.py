from utils import lat_lon_to_cell, LAT_BLOCKS, LON_BLOCKS

import unittest


class TestGlobalMethods(unittest.TestCase):
    def test_lat_lon_to_cell(self):
        self.assertEqual(lat_lon_to_cell(90.0, -180.0), 0)
        self.assertEqual(lat_lon_to_cell(0, 0), LAT_BLOCKS * LON_BLOCKS / 2)
        self.assertEqual(lat_lon_to_cell(-90, 180.0), LAT_BLOCKS * LON_BLOCKS)

if __name__ == '__main__':
    unittest.main()

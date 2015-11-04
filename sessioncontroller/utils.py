# coding=utf-8
from datapoller.settings import THRESHOLD_FOR_KP

LON_BLOCKS = 1024
LAT_BLOCKS = 512

def lat_lon_to_cell(lat, lon):
    """
    Converts (lat, lon) to linear cell index, based on a 1024 x 512 grid.
    Latitude ranges between -90.0 (south pole) and +90.0 (north pole), longitude is between -180.0 and +180.0.
    """
    return int((lat + 90) * LAT_BLOCKS / 180.0) * (LON_BLOCKS) \
    + int((lon + 180) * LON_BLOCKS / 360.0)


def get_kp_level(lat):
    """
    # 0 	G0 	66.5° or higher 	Very low
    # 1 	G0 	64.5° 	Low
    # 2 	G0 	62.4° 	Low
    # 3 	G0 	60.4° 	Unsettled
    # 4 	G0 	58.3° 	Active
    # 5 	G1 	56.3° 	Minor storm 	1700 per cycle (900 days per cycle)
    # 6 	G2 	54.2° 	Moderate storm 	600 per cycle (360 days per cycle)
    # 7 	G3 	52.2° 	Strong storm 	200 per cycle (130 days per cycle)
    # 8 	G4 	50.1° 	Severe storm 	100 per cycle (60 days per cycle)
    # 9 	G5 	48.1° or lower
    :param lat:
    :return:
    """
    kpTable = [66.5, 64.5, 62.4, 60.4, 58.3, 56.3, 54.2, 52.2, 50.1, 48.1]
    i = 0
    for latTable in kpTable:
        if abs(lat) >= latTable:
            return i
        i += 1
    return 10


def is_level_interesting_for_kp(level, kp):
    return level >= THRESHOLD_FOR_KP[kp]

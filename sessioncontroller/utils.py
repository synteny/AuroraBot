LON_BLOCKS = 1024
LAT_BLOCKS = 512

def lat_lon_to_cell(lat, lon):
    """
    Converts (lat, lon) to linear cell index, based on a 1024 x 512 grid.
    Latitude ranges between -90.0 (south pole) and +90.0 (north pole), longitude is between -180.0 and +180.0.
    """
    return int((lat + 90) * LAT_BLOCKS / 180.0) * (LON_BLOCKS) \
    + int((int(lon) if int(lon) >= 0 else (360 - int(lon))) * LAT_BLOCKS / 360.0)
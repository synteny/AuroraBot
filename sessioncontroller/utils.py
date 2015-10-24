LON_BLOCKS = 1096
LAT_BLOCKS = 512


# converts (lat, lon) to linear cell index, based on a 1096 x 512 grid
def lat_lon_to_cell(lat, lon):
    return int((90.0 - lat) * LAT_BLOCKS / 180.0) * (LON_BLOCKS - 1) + int((lon + 180.0) * LAT_BLOCKS / 360.0)
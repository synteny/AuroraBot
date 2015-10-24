"""
Parses the immediate aurora forecast.
http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt
"""
def parse_nowcast(text):
    for line in text:
        sline = line.strip()
        if sline and not sline.startswith('#'):
            for p in sline.split():
                yield int(p)
        else:
            print(sline)

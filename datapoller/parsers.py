import re
from datetime import datetime

"""
Parses the immediate aurora forecast.
http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt
"""
def parse_nowcast(text):
    time = datetime.max  # forecast time remains far in the future if time not found in the file
    data = []
    for i, line in enumerate(text):
        if(i > 527):
            print line[:10]
        sline = line.strip()
        if sline:
            if not sline.startswith('#'):
                for p in sline.split():
                    data.append(int(p) if p != 'n/a' else 0)
            else:
                m = re.search('^# Product Valid At: (.*)', sline)
                if m:
                    time = datetime.strptime(m.group(1), '%Y-%m-%d %H:%M')
    return data, time
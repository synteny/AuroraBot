import re
import itertools
from datetime import datetime


""" Parses the immediate aurora forecast.
    http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt """
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


""" Parses the three-day global Kp index forecast.
    http://services.swpc.noaa.gov/text/3-day-forecast.txt """
def parse_three_day_forecast(text):
    lines = itertools.imap(lambda l: l.strip(), text)

    def fetch_line(iter, matcher):
        cont = itertools.dropwhile(lambda l: not matcher(l), iter)
        return cont, cont.next()

    def parse_date(str, format):
        return datetime.strptime(str, format)

    def parse_forecast(str, dates):
        m = re.search('(\d{2})-(\d{2})UT\s+(\d)(?:\s+\(G[1-5]\))?\s+(\d)(?:\s+\(G[1-5]\))?\s+(\d)(?:\s+\(G[1-5]\))?', str)
        h, _, Kp1, Kp2, Kp3 = [m.group(i) for i in range(1, 6)]
        for kp, date in zip([Kp1, Kp2, Kp3], dates):
            yield (date.replace(hour=int(h)), int(kp))

    lines, issue_time = fetch_line(lines, lambda l: l.startswith(':Issued: '))
    issue_time = parse_date(issue_time[len(':Issued: '):].strip(), '%Y %b %d %H%M %Z')

    lines, _ = fetch_line(lines, lambda l: l.startswith('NOAA Kp index breakdown'))

    lines, dates_line = fetch_line(lines, lambda l: l)  # first nonempty

    ms = re.finditer('\w{3} \d+', dates_line)
    dates = [parse_date(m.group(0), '%b %d').replace(year=issue_time.year) for m in ms]

    return [f for ln in itertools.takewhile(lambda l: len(l) > 0, lines) for f in parse_forecast(ln, dates)]
#!/usr/bin/env python

import urllib2
from lxml import html
from datetime import datetime, tzinfo
import time
import re
import sqlite3

teams_encoded = [ "Red Team", "Blue Team", "Pink Team", "Green Team", "Purple Team" ]

start_date = datetime(2014, 6, 19)

conn = sqlite3.connect("scores.db")

def load_archive(day):
    enc = urllib2.urlopen("http://store.steampowered.com/promotion/summer2014teams/?day=" + str(day)).read()
    dom = html.fromstring(enc)
    teams_absolute = {}
    for element in dom.xpath("//div[@class='team_score_detail']"):
        team_enc = element.xpath("div[@class='team_score_detail_header']/text()")[0]
        team_id = teams_encoded.index(str(team_enc).strip())
        delta_by_stamp = {}
        for point in element.xpath("div[@class='detail_graph_ctn']/div[@class='detail_graph_positive']/div[@class='graph_element']/@data-store-tooltip"):
            delta_by_stamp[point[:point.index(" ")]] = int(re.sub(r"[^0-9]", r"", point[point.index(" "):]))

        # Using the negative values seems to mismatch the values on the site
        #for point in element.xpath("div[@class='detail_graph_ctn']/div[@class='detail_graph_negative']/div[@class='graph_element']/@data-store-tooltip"):
            # let's just assume we have a positive there too so it already exists
            #delta_by_stamp[point[:point.index(" ")]] -= int(re.sub(r"[^0-9]", r"", point[point.index(" "):]))

        delta_by_time = {}
        for k in delta_by_stamp.keys():
            date_parsed = datetime.strptime(k, "%I:%M%p")
            hour = date_parsed.hour
            if hour < 10:
                hour += 24
            hour += 9
            date = datetime(2014, 6, 19 + day + hour / 24, hour % 24, date_parsed.minute)
            delta_by_time[date] = delta_by_stamp[k]
        absolute = {}
        total = 0
        for date in sorted(delta_by_time):
            total += delta_by_time[date]
            absolute[date] = total
        for date in absolute:
            if not date in teams_absolute:
                teams_absolute[date] = [(), (), (), (), ()]
            teams_absolute[date][team_id] = absolute[date]
    for date in sorted(teams_absolute):
        v = teams_absolute[date]
        if () in v:
            continue
        utime = long(time.mktime(date.timetuple()))
        print str(utime) + "\t" + str(date) + "\t" + str(v)
        conn.execute("INSERT OR IGNORE INTO scores (time, red, blue, pink, green, purple) VALUES (?, ?, ?, ?, ?, ?)", 
                    (utime, v[0], v[1], v[2], v[3], v[4]))
    conn.commit()

for i in range(0, 6):
    load_archive(i)
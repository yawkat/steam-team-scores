#!/usr/bin/env python

import json
import urllib2
import time
import sqlite3
import sys

def get_current_scores():
    d = json.load(urllib2.urlopen("http://store.steampowered.com/promotion/summer2014teamscoreajax"))
    arr = []
    for i in range(1, 6):
        arr.append(d[str(i)])
    return arr

conn = sqlite3.connect("scores.db")
interval = 5

conn.execute("CREATE TABLE IF NOT EXISTS scores "
    + "(time INTEGER PRIMARY KEY, red INT, blue INT, pink INT, green INT, purple INT)")

while True:
    t = time.time()

    try:
        scores = get_current_scores()
        int_time = int(t)
        conn.execute("INSERT INTO scores VALUES (?, ?, ?, ?, ?, ?)", [int_time, scores[0], scores[1], scores[2], scores[3], scores[4]])
        conn.commit()
    except:
        print sys.exc_info()[0]

    took = time.time() - t
    print "Run complete, took %s seconds" % took
    remaining = interval - took
    if remaining > 0:
        time.sleep(remaining)
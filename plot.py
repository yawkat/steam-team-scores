#!/usr/bin/env python

import time
import sqlite3
import os
from os import path
import json

conn = sqlite3.connect("scores.db")

def plot_span(output_file, from_time, to_time):
    tmp_data_file = ".tmp.dat"
    tmp_image_file = ".tmp.png"

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scores WHERE time >= %s AND time < %s AND red != 0 ORDER BY time" % (from_time, to_time))
    entries = cursor.fetchall()

    with open(tmp_data_file, "w") as tmp_file:
        for entry in entries:
            tmp_file.write("%s\t%s\t%s\t%s\t%s\t%s\n" % entry)

    os.system("gnuplot -e \"ifile='%s'; ofile='%s'\" plot.gp" % (tmp_data_file, tmp_image_file))
    os.remove(tmp_data_file)
    if not path.exists(path.dirname(output_file)):
        os.makedirs(path.dirname(output_file))
    if path.exists(output_file):
        os.remove(output_file)
    os.rename(tmp_image_file, output_file)

def find_minima():
    minima_point_threshold = 20000
    minima_time_threshold = 10 * 60 * 60

    cursor = conn.cursor()
    cursor.execute("SELECT time FROM scores WHERE red < %s AND red != 0 ORDER BY time" % minima_point_threshold)
    entries = cursor.fetchall()
    
    last_time = 0
    for entry in entries:
        time = entry[0]
        if time - last_time > minima_point_threshold:
            yield time
        last_time = time

def update_index(minima):
    index = []
    i = 1
    for minimum in minima:
        index.append({ "start_time": minimum, "image_id": i, "latest": i == len(minima) })
        i += 1
    with open("visual/index.json", "w") as index_file:
        json.dump(index, index_file)

filename_for_day = lambda day: path.join("visual", "days", str(day) + ".png")
minima = list(find_minima())

first_missing = 0
while path.exists(filename_for_day(first_missing)):
    first_missing += 1
for i in range(max(0, first_missing - 1), len(minima)):
    if i == len(minima) - 1:
        end = time.time() * 2
    else:
        end = minima[i + 1]
    plot_span(filename_for_day(i + 1), minima[i], end)

latest = filename_for_day("latest")
if path.exists(latest):
    os.unlink(latest)
os.symlink(path.abspath(filename_for_day(len(minima))), latest)

update_index(minima)

#!/usr/bin/env python

import time
import sqlite3
import os
from os import path

conn = sqlite3.connect("scores.db")

def plot_span(output_file, from_time, to_time):
    tmp_data_file = ".tmp.dat"
    tmp_image_file = ".tmp.svg"

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scores WHERE time >= %s AND time <= %s" % (from_time, to_time))
    entries = cursor.fetchall()

    with open(tmp_data_file, "w") as tmp_file:
        for entry in entries:
            tmp_file.write("%s\t%s\t%s\t%s\t%s\t%s\n" % entry)

    os.system("gnuplot -e \"ifile='%s'; ofile='%s'\" plot.gp" % (tmp_data_file, tmp_image_file))
    os.remove(tmp_data_file)
    os.makedirs(path.dirname(output_file))
    if path.exists(output_file):
        os.remove(output_file)
    os.rename(tmp_image_file, output_file)

def find_minima():
    minima_point_threshold = 5000
    minima_time_threshold = 60 * 60

    cursor = conn.cursor()
    cursor.execute("SELECT time FROM scores WHERE red < %s" % minima_point_threshold)
    entries = cursor.fetchall()
    
    last_time = 0
    for entry in entries:
        time = entry[0]
        if time - last_time > minima_point_threshold:
            yield time
        last_time = time

filename_for_day = lambda day: path.join("visual", "days", str(day) + ".svg")
minima = list(find_minima())
plot_span(filename_for_day(len(minima)), minima[-1], time.time() * 2)
if not path.exists(filename_for_day(len(minima))) and len(minima) > 1:
    plot_span(filename_for_day(len(minima) - 1), minima[-2], minima[-1])

latest = filename_for_day("latest")
if path.exists(latest):
    os.unlink(latest)
os.symlink(path.abspath(filename_for_day(len(minima))), latest)

#!/usr/bin/env python

# Extract 2 columns from a csv and plot it in matplotlib

def usage():
    print "Usage: heatmap.py x-axis-column y-axis-column"
    print 'Example usage: ./heaptmap.py hack_distance.csv 1 2'

import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) < 4:
    usage()

filename, x_col, y_col = sys.argv[1:4]

fileData = np.genfromtxt(filename, delimiter=',')

x = []
y = []
for row in fileData:
    x_val = row[int(x_col)]
    y_val = row[int(y_col)]
    if not (x_val > -74.8375 and x_val < -73.1209 and y_val > 40.3225 and y_val < 41.0721):
        continue 
    x.append(x_val)
    y.append(y_val)

heatmap, xedges, yedges = np.histogram2d(x, y, bins=500)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap, extent=extent)
plt.show()

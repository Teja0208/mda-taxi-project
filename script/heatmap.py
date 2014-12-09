#!/usr/bin/env python

# Extract 2 columns from a csv and plot it in matplotlib

def usage():
    print "Usage: heatmap.py x-axis-column y-axis-column nbins"
    print 'Example usage: ./heaptmap.py hack_distance.csv 1 2 500'

import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) < 5:
    usage()

filename, x_col, y_col, nbins = sys.argv[1:5]

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

#heatmap, xedges, yedges = np.histogram2d(x, y, bins=int(nbins))
#extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#
#plt.clf()
#plt.imshow(heatmap, extent=extent)
#plt.show()


import heatmap
pts = []
for a,b in zip(x,y):
    pts.append((x, y))

print "Processing %d points..." % len(pts)

hm = heatmap.Heatmap()
img = hm.heatmap(pts)
img.save("classic.png")

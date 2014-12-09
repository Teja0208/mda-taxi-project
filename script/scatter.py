#!/usr/bin/env python

# Extract 2 columns from a csv and plot it in matplotlib

def usage():
    print "Usage: scatter.py x-axis-column y-axis-column [x-axis-label] [y-axis-label]"
    print 'Example usage: ./scatter.py hack_distance.csv 1 2 "Number of Trips" "Average Distance"'

import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) < 4:
    usage()

filename, x_col, y_col = sys.argv[1:4]

try:
  x_lbl = sys.argv[4]
except IndexError:
  x_lbl = "x axis"

try:
  y_lbl = sys.argv[5]
except IndexError:
  y_lbl = "y axis"

fileData = np.genfromtxt(filename, delimiter=',')

x = []
y = []
for row in fileData:
    x.append(row[int(x_col)])
    y.append(row[int(y_col)])

plt.scatter(x, y)
plt.xlabel(x_lbl)
plt.ylabel(y_lbl)
plt.show()


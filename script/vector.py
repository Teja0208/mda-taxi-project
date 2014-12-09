#!/usr/bin/env python

# Extract 2 columns from a csv and plot it in matplotlib

def usage():
    print "Usage: vector.py x1-col y1-col x2-col y2-col"
    print 'Example usage: ./vector.py hack_distance.csv 1 2 3 4'

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
fig, ax = plt.subplots()

n_args = 6
if len(sys.argv) < n_args:
    usage()

filename, x1_col, y1_col, x2_col, y2_col = sys.argv[1:n_args]

fileData = np.genfromtxt(filename, delimiter=',')

xss = []
yss = []
for row in fileData:
    xss.append([row[int(x1_col)], row[int(x2_col)]])
    yss.append([row[int(y1_col)], row[int(y2_col)]])

# http://calebmadrigal.com/draw-lines-with-matplotlib/
fig.set_size_inches(6,6)          # Make graph square

for xs, ys in zip(xss, yss):
  ax.add_line(lines.Line2D(xs, ys, linewidth=1, color='blue'))

plt.plot()
plt.show()

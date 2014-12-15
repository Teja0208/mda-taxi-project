import numpy as np
from matplotlib import pyplot as plt
import csv
import pdb
from matplotlib import colors as colors
import sys

pickup_xs, pickup_ys, dropoff_xs, dropoff_ys = [], [], [], []

#make commandline later:
# filename = 'trips_from_lazy_drivers_cleaned.csv'
# filename = 'trips_from_lazy_drivers_frequent.csv'
filename = 'mets_2013_query_results-20141212-233549.csv'

DISTANCE_TO_POINTS_FACTOR = 10000.0 #units: points/lat-lon-degree
#so if we want say 10 spots per block. a block is about .002 degrees lat long
# so do 10 = factor*(.002) and solve for factor yields 5000
BINS = 100
OFFSET = 0
DEBUG_1 = False
DEBUG_2 = False

if DEBUG_1:
    DISTANCE_TO_POINTS_FACTOR = 1000.
    BINS = 20

if DEBUG_2: #for lots of points but chaning bins
    DISTANCE_TO_POINTS_FACTOR = 10.
    BINS = 200

# nycBounds = [[-74.05,-73.9],[40.67,40.85]] #no laguardia
nycBounds = [[-74.05,-73.85],[40.67,40.85]] #with laguardia

nycBounds[0][0] += OFFSET
nycBounds[0][1] += OFFSET



firstIndex, seondIndex, thirdIndex, fourthIndex = range(4)

with open(filename) as opened:
    readerObj = csv.reader(opened)
    init = False
    for line in readerObj:
        if not init:
            init = True
            continue
        pickup_xs.append(float(line[firstIndex]) + OFFSET)
        pickup_ys.append(float(line[seondIndex]))

        dropoff_xs.append(float(line[thirdIndex]) + OFFSET)
        dropoff_ys.append(float(line[fourthIndex]))

# xsFull = xs
# ysFull = ys
count = 0
xsFull = []
ysFull = []

for startX, startY, endX, endY in zip(pickup_xs, pickup_ys, dropoff_xs, dropoff_ys):
    count += 1
    xsFull.append(startX)
    ysFull.append(startY)

heatmap, xedge, yedge = np.histogram2d(xsFull, ysFull, bins=BINS, range=nycBounds)

heatmapCopy = heatmap.copy()

heatmap = heatmap.transpose()

print 'max, min, med, mean:'
maxI = np.max(np.max(heatmap))
minI = np.min(np.min(heatmap))
medI = np.median(np.median(heatmap))
meanI = np.mean(np.mean(heatmap))
print maxI, minI, medI, meanI

nonZeroBinVals = []
for i in xrange(len(heatmap)):
    for val in heatmap[i]:
        if val > .0000001:
            nonZeroBinVals.append(val)
specialMedian = np.median(nonZeroBinVals)
print 'special median:'
print specialMedian

# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal')
plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', vmin=minI, vmax=maxI/5)
# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', norm=colors.BoundaryNorm([ele for ele in np.linspace(specialMedian, maxI, 10)], ncolors=256, clip = False))
# plt.imshow(heatmap, extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]])
# plt.imshow(heatmap, aspect='equal')

plt.show()

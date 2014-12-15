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
# filename = 'mets_2013_query_results-20141212-233549.csv'
ITER_DEPTH = 50000
DIVIDE_BY_FACTOR=300.
DISTANCE_TO_POINTS_FACTOR = 10000.0 #units: points/lat-lon-degree
#so if we want say 10 spots per block. a block is about .002 degrees lat long
# so do 10 = factor*(.002) and solve for factor yields 5000
BINS = 1000
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



if len(sys.argv) == 5:
    firstIndex, seondIndex, thirdIndex, fourthIndex = sys.argv[1:]
elif len(sys.argv) == 6:
    filename, firstIndex, seondIndex, thirdIndex, fourthIndex = sys.argv[1:]
else:
    firstIndex, seondIndex, thirdIndex, fourthIndex = range(4)

firstIndex, seondIndex, thirdIndex, fourthIndex =int(firstIndex), int(seondIndex), int(thirdIndex), int(fourthIndex)
 

with open(filename) as opened:
    readerObj = csv.reader(opened)
    counter_line = 0
    for line in readerObj:
        counter_line+=1
        if counter_line == 1:
            continue
        if counter_line > ITER_DEPTH:
            continue
        pickup_xs.append(float(line[firstIndex])/DIVIDE_BY_FACTOR)
        pickup_ys.append(float(line[seondIndex])/DIVIDE_BY_FACTOR)

        dropoff_xs.append(float(line[thirdIndex])/DIVIDE_BY_FACTOR)
        dropoff_ys.append(float(line[fourthIndex])/DIVIDE_BY_FACTOR)

# xsFull = xs
# ysFull = ys
count = 0
xsFull = []
ysFull = []
print 'here1',
print len(dropoff_ys), len(dropoff_xs), len(pickup_xs), len(pickup_ys)
for startX, startY, endX, endY in zip(pickup_xs, pickup_ys, dropoff_xs, dropoff_ys):
    count += 1
    deltaY = endY - startY 
    deltaX = endX - startX

    distance = np.sqrt(deltaX*deltaX + deltaY*deltaY)
    # if distance > 1:
    #     continue
    #FILTER OUT THE REALLY SHORT ZERO MOVEMENT TRIPS
    if distance < .001:
        continue

    numPointsInSegment = distance * DISTANCE_TO_POINTS_FACTOR

    xsFull.extend([curSubSegmentPartialVal for curSubSegmentPartialVal in np.linspace(startX, endX, numPointsInSegment)])
    ysFull.extend([curSubSegmentPartialVal for curSubSegmentPartialVal in np.linspace(startY, endY, numPointsInSegment)])

# quit()
print 'here2'
heatmap, xedge, yedge = np.histogram2d(xsFull, ysFull, bins=BINS, range=nycBounds)
if DEBUG_1:
    print xedge
    print yedge
    print xedge[1]-xedge[0], xedge[10]-xedge[9]
    print yedge[1]-yedge[0], yedge[10]-yedge[9]

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

print 'here3'
# #replace top vals w 0
# CUTOFF = maxI/4
# heatmap[heatmap > CUTOFF] = 0.0

# COLORMAP = 'jet'
# COLORMAP = 'prism'
COLORMAP = 'BuRd'

# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal')
# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', cmap=COLORMAP, norm=colors.Normalize(vmin=minI,vmax=maxI,clip=False))
plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', cmap=COLORMAP, vmin=minI, vmax=maxI)
# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', norm=colors.BoundaryNorm([ele for ele in np.linspace(specialMedian, maxI, 10)], ncolors=256, clip = False))
# plt.imshow(heatmap, extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]])
# plt.imshow(heatmap, aspect='equal')

# figgy = plt.gcf()
# figgy.savefig('test_save_fig.png', dpi=1020 )
plt.show()



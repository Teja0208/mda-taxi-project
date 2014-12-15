
#most recent call looked like:
# python routes_heatmap_weighted.py routes_top2000_1000factor.csv 0 1 2 3

import numpy as np
from matplotlib import pyplot as plt
import csv
import pdb
from matplotlib import colors as colors
import sys
import math
from scipy import ndimage
import datetime

pickup_xs, pickup_ys, dropoff_xs, dropoff_ys = [], [], [], []

#make commandline later:
# filename = 'trips_from_lazy_drivers_cleaned.csv'
# filename = 'trips_from_lazy_drivers_frequent.csv'
# filename = 'mets_2013_query_results-20141212-233549.csv'
ITER_DEPTH = 50000
DISTANCE_TO_POINTS_FACTOR = 10000.0 #units: points/lat-lon-degree
#so if we want say 10 spots per block. a block is about .002 degrees lat long
# so do 10 = factor*(.002) and solve for factor yields 5000
BINS = 1000




############# modify for file and for high rez boxing and/or current sql file
DISTANCE_TO_POINTS_FACTOR = 100000.0
BINS = 10000
DIVIDE_BY_FACTOR=1000.#300.



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


if len(sys.argv) == 2:
    filename = sys.argv[-1]
    firstIndex, seondIndex, thirdIndex, fourthIndex = range(4)
elif len(sys.argv) == 5:
    firstIndex, seondIndex, thirdIndex, fourthIndex = sys.argv[1:]
elif len(sys.argv) == 6:
    filename, firstIndex, seondIndex, thirdIndex, fourthIndex = sys.argv[1:]
else:
    firstIndex, seondIndex, thirdIndex, fourthIndex = range(4)

firstIndex, seondIndex, thirdIndex, fourthIndex =int(firstIndex), int(seondIndex), int(thirdIndex), int(fourthIndex)
 


def bin_1d(x, index, granularity):
    missedBy = (x - index) % granularity
    return x - missedBy
def bin_2d(x, y, x_ind, y_ind, x_gran, y_gran=None):
    """returns tuple binned"""
    if y_gran is None:
        y_gran = x_gran
    return (bin_1d(x, x_ind, x_gran), bin_1d(y, y_ind, y_gran))












count_that_trip = []

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

        count_that_trip.append(int(line[fourthIndex+1]))

print count_that_trip[:50]
# xsFull = xs
# ysFull = ys
count = 0
xsFull = []
ysFull = []
print 'here1',
print len(dropoff_ys), len(dropoff_xs), len(pickup_xs), len(pickup_ys)

xSpread = nycBounds[0][1] - nycBounds[0][0]
ySpread = nycBounds[1][1] - nycBounds[1][0]
xBinGranularity = float(xSpread)/BINS
yBinGranularity = float(ySpread)/BINS

trackingHash = {}

for startX, startY, endX, endY, curTripCount in zip(pickup_xs, pickup_ys, dropoff_xs, dropoff_ys, count_that_trip):
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

    curXPointsInterpList = [curSubSegmentPartialVal for curSubSegmentPartialVal in np.linspace(startX, endX, numPointsInSegment)]
    curYPointsInterpList = [curSubSegmentPartialVal for curSubSegmentPartialVal in np.linspace(startY, endY, numPointsInSegment)]

    for curX, curY in zip(curXPointsInterpList, curYPointsInterpList):
        binnedTuple = bin_2d(curX, curY, nycBounds[0][0], nycBounds[1][0], xBinGranularity, yBinGranularity)

        try:
            trackingHash[binnedTuple].append(curTripCount)
        except KeyError:
            trackingHash[binnedTuple] = []
            trackingHash[binnedTuple].append(curTripCount)


#now we have hte 'sparse' plot (scatter of points that happen to represent lines)
#now we can make a simple 2d sparse without the lists by just selectin max from each list

def xyToPixelIJ(x,y):
    iii = math.floor((x - nycBounds[0][0])/xBinGranularity)
    jjj = math.floor((y - nycBounds[1][0])/yBinGranularity)
    return (iii, jjj)

pixels = np.zeros([BINS, BINS])

#add the HIGHEST VAL from each tuple (lat-long pair) to the according bin in pixels

for curTuple in trackingHash.keys():
    maxIntensity = max(trackingHash[curTuple])
    curX, curY = curTuple
    ii, jj = xyToPixelIJ(curX, curY)
    try:
        pixels[ii,jj] = float(maxIntensity)
    except IndexError:
        #so we're trying to plot a point that is out of our nycBounds
        pass

pixels = pixels.transpose() #i had mixed up lat and long

print 'max, min, med, mean:'
maxI = np.max(np.max(pixels))
minI = np.min(np.min(pixels))
medI = np.median(np.median(pixels))
meanI = np.mean(np.mean(pixels))
print maxI, minI, medI, meanI

smoothed = ndimage.filters.gaussian_filter(pixels, 6, mode='nearest')

toShow = smoothed

COLORMAP = 'Purples'
COLORMAP = 'jet'
COLORMAP = 'PuRd'
COLORMAP = 'spectral'
plt.imshow(toShow, origin='bottom',cmap=COLORMAP)
figgy=plt.gcf()
figgy.savefig('figure_top200_whatever'+str(datetime.datetime.now())+'.png', dpi=500)
# plt.show()

sys.exit()

































nonZeroBinVals = []
for i in xrange(len(pixels)):
    for val in pixels[i]:
        if val > .0000001:
            nonZeroBinVals.append(val)
specialMedian = np.median(nonZeroBinVals)
print 'special median:'
print specialMedian




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
COLORMAP = 'Purples'

# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal')
# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', cmap=COLORMAP, norm=colors.Normalize(vmin=minI,vmax=maxI,clip=False))
plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', cmap=COLORMAP, vmin=minI, vmax=maxI/10)
# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', norm=colors.BoundaryNorm([ele for ele in np.linspace(specialMedian, maxI, 10)], ncolors=256, clip = False))
# plt.imshow(heatmap, extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]])
# plt.imshow(heatmap, aspect='equal')

# figgy = plt.gcf()
# figgy.savefig('test_save_fig.png', dpi=1020 )
plt.show()

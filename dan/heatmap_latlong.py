import numpy as np
from matplotlib import pyplot as plt
import csv
import pdb
from matplotlib import colors as colors
import sys

pickup_xs, pickup_ys, dropoff_xs, dropoff_ys = [], [], [], []


DISTANCE_TO_POINTS_FACTOR = 10000.0 #units: points/lat-lon-degree
#so if we want say 10 spots per block. a block is about .002 degrees lat long
# so do 10 = factor*(.002) and solve for factor yields 5000
BINS = 2000
OFFSET = 0
DEBUG_1 = False
DEBUG_2 = True

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


#make commandline later:
# filename = 'trips_from_lazy_drivers_cleaned.csv'
filename = 'trips_from_lazy_drivers_frequent.csv'
firstIndex = -4
seondIndex = -3
thirdIndex = -2
fourthIndex = -1

with open(filename) as opened:
    readerObj = csv.reader(opened)
    for line in readerObj:
        pickup_xs.append(float(line[firstIndex]) + OFFSET)
        pickup_ys.append(float(line[seondIndex]))

        dropoff_xs.append(float(line[thirdIndex]) + OFFSET)
        dropoff_ys.append(float(line[fourthIndex]))


def bin_1d(x, index, granularity):
    missedBy = (x - index) % granularity
    return x - missedBy

def bin_2d(x, y, x_ind, y_ind, x_gran, y_gran=None):
    """returns tuple binned"""
    if y_gran is None:
        y_gran = x_gran
    return (bin_1d(x, x_ind, x_gran), bin_1d(y, y_ind, y_gran))

xSpread = nycBounds[0][1] - nycBounds[0][0]
ySpread = nycBounds[1][1] - nycBounds[1][0]
xBinGranularity = float(xSpread)/BINS
yBinGranularity = float(ySpread)/BINS

#generate the hashmap of the routes:
routeHash = {}
for startX, startY, endX, endY in zip(pickup_xs, pickup_ys, dropoff_xs, dropoff_ys):
    
    binnedStartTuple = bin_2d(startX, startY, nycBounds[0][0], nycBounds[1][0], xBinGranularity, yBinGranularity)
    binnedEndTuple = bin_2d(endX, endY, nycBounds[0][0], nycBounds[1][0], xBinGranularity, yBinGranularity)

    try:
        routeHash[(binnedStartTuple, binnedEndTuple)] += 1
    except KeyError:
        routeHash[(binnedStartTuple, binnedEndTuple)] = 1



routeTuples = [(curKey, routeHash[curKey]) for curKey in routeHash.keys()] #first thing makes new tuple w 4 things kinda
sortedRouteTuples = sorted(routeTuples, key=lambda x: x[-1], reverse=True)

sortedRouteTuplesNoStationary = [ele for ele in sortedRouteTuples if ele[0][0][0]-ele[0][1][0]>.00000001]

TOP_X = 10
# print sortedRouteTuples[:TOP_X]
print sortedRouteTuplesNoStationary[:TOP_X]
# for curTuple in sortedRouteTuples[:TOP_X]:
for curTuple in sortedRouteTuplesNoStationary[:TOP_X]:
    tupleTuple = curTuple[0]
    # print curTuple
    # print tupleTuple
    xList = [tupleTuple[0][0], tupleTuple[1][0]]
    yList = [tupleTuple[0][1], tupleTuple[1][1]]
    plt.plot(xList, yList)

plt.show()












sys.exit()

# xsFull = xs
# ysFull = ys
count = 0
xsFull = []
ysFull = []
for startX, startY, endX, endY in zip(pickup_xs, pickup_ys, dropoff_xs, dropoff_ys):
    count += 1
    deltaY = endY - startY 
    deltaX = endX - startX

    distance = np.sqrt(deltaX*deltaX + deltaY*deltaY)

    #debug_1ging
    # if count < 50:
    #     print distance

    numPointsInSegment = distance * DISTANCE_TO_POINTS_FACTOR

    xsFull.extend([curSubSegmentPartialVal for curSubSegmentPartialVal in np.linspace(startX, endX, numPointsInSegment)])
    ysFull.extend([curSubSegmentPartialVal for curSubSegmentPartialVal in np.linspace(startY, endY, numPointsInSegment)])

# quit()

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

plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal')
# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', vmin=maxI/2.0, vmax=maxI)
# plt.imshow(heatmap, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', norm=colors.BoundaryNorm([ele for ele in np.linspace(specialMedian, maxI, 10)], ncolors=256, clip = False))
# plt.imshow(heatmap, extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]])
# plt.imshow(heatmap, aspect='equal')

plt.show()
pdb.set_trace()

print heatmap.shape
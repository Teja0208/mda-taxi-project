#make a heatmap for route vectors, where each pixel's value is the value of the
#most popular route through that point

import numpy as np
from matplotlib import pyplot as plt
import csv
import pdb
from matplotlib import colors as colors
import sys
import math
from scipy import ndimage
import datetime


# nycBounds = [[-74.05,-73.9],[40.67,40.85]] #no laguardia
nycBounds = [[-74.05,-73.85],[40.67,40.85]] #with laguardia
ITER_DEPTH = 200 #max number of routes to view
BINS = 1000
DIVIDE_BY_FACTOR=1.#300.
TRANSPOSE_LAT_LONG = True
COLORMAP = 'spectral'
LINE_DENSITY_FACTOR = 1


if len(sys.argv) == 7:
    filename, firstIndex, seondIndex, thirdIndex, fourthIndex, fifthIndex = sys.argv[1:]
elif len(sys.argv) == 2:
    filename = sys.argv[-1]
    firstIndex, seondIndex, thirdIndex, fourthIndex, fifthIndex = range(5)
else:
    raise IOError("must specify filename")

firstIndex, seondIndex, thirdIndex, fourthIndex, fifthIndex = int(firstIndex), int(seondIndex), int(thirdIndex), int(fourthIndex), int(fifthIndex)


def bin_1d(x, index, granularity):
    missedBy = (x - index) % granularity
    return x - missedBy
def bin_2d(x, y, x_ind, y_ind, x_gran, y_gran=None):
    """returns tuple binned"""
    if y_gran is None:
        y_gran = x_gran
    return (bin_1d(x, x_ind, x_gran), bin_1d(y, y_ind, y_gran))



#load file data into memory:
pickup_xs, pickup_ys, dropoff_xs, dropoff_ys = [], [], [], []
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

        count_that_trip.append(int(line[fifthIndex]))

dataSpreadMetric = sum([max(pickup_xs)-min(pickup_xs), max(pickup_ys)-min(pickup_ys)])/2. #rough just use pickup will give basicaly spread
distanceToNumPointsInterpFactor =  LINE_DENSITY_FACTOR * BINS / dataSpreadMetric


count = 0
xsFull = []
ysFull = []
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
    #FILTER OUT THE REALLY SHORT ZERO MOVEMENT TRIPS
    if distance < .001:
        continue

    numPointsInSegment = distance * distanceToNumPointsInterpFactor
    print numPointsInSegment

    curXPointsInterpList = [curSubSegmentPartialVal for curSubSegmentPartialVal in np.linspace(startX, endX, numPointsInSegment)]
    curYPointsInterpList = [curSubSegmentPartialVal for curSubSegmentPartialVal in np.linspace(startY, endY, numPointsInSegment)]

    for curX, curY in zip(curXPointsInterpList, curYPointsInterpList):
        binnedTuple = bin_2d(curX, curY, nycBounds[0][0], nycBounds[1][0], xBinGranularity, yBinGranularity)

        try:
            trackingHash[binnedTuple].append(curTripCount)
        except KeyError:
            trackingHash[binnedTuple] = []
            trackingHash[binnedTuple].append(curTripCount)


#now we have the 'sparse' plot (scatter of points that happen to represent lines, each point a LL)
#now we can make a simple 2d sparse without the lists by just selectin max from each list

def xyToPixelIJ(x,y):
    """convert data coordinates to pixel indices"""
    iii = math.floor((x - nycBounds[0][0])/xBinGranularity)
    jjj = math.floor((y - nycBounds[1][0])/yBinGranularity)
    return (iii, jjj)

pixels = np.zeros([BINS, BINS])
#todo add flexibility for non square arrays
#add the HIGHEST VAL from each tuple (lat-long pair) to the according bin in pixels

for curTuple in trackingHash.keys():
    maxIntensity = max(trackingHash[curTuple])
    curX, curY = curTuple
    ii, jj = xyToPixelIJ(curX, curY)
    print ii,
    print jj
    try:
        pixels[ii,jj] = float(maxIntensity)
    except IndexError:
        #so we're trying to plot a point that is out of our nycBounds
        pass

if TRANSPOSE_LAT_LONG:
    pixels = pixels.transpose()

maxI = np.max(np.max(pixels))

smoothed = ndimage.filters.gaussian_filter(pixels, 6, mode='nearest')

toShow = smoothed
import pdb;pdb.set_trace()
plt.imshow(toShow, origin='bottom',cmap=COLORMAP)
figgy=plt.gcf()
# figgy.savefig('figure_top200_whatever'+str(datetime.datetime.now())+'.png', dpi=500)
plt.show()

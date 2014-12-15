import numpy as np
from matplotlib import pyplot as plt
import csv
import pdb
from matplotlib import colors as colors
import sys


# nycBounds = [[-74.05,-73.9],[40.67,40.85]] #no laguardia
nycBounds = [[-74.05,-73.85],[40.67,40.85]] #with laguardia

#make commandline later:
# filename = 'teja_groupby1.csv'
# filename = 'test_dan'
filename = 'routes_top2000_1000factor.csv'
firstIndex = 0
seondIndex = 1
thirdIndex = 2
fourthIndex = 3
fifthIndex = 4
FACTOR = 1000.
pickup_xs, pickup_ys, dropoff_xs, dropoff_ys = [], [], [], []
tripCounts = []

with open(filename) as opened:
    readerObj = csv.reader(opened)
    for line in readerObj:
        pickup_xs.append(float(line[firstIndex])/FACTOR)
        pickup_ys.append(float(line[seondIndex])/FACTOR)

        dropoff_xs.append(float(line[thirdIndex])/FACTOR)
        dropoff_ys.append(float(line[fourthIndex])/FACTOR)

        tripCounts.append(int(line[fifthIndex]))

allAsTuples = []
for startX, startY, endX, endY, numTrips in zip(pickup_xs, pickup_ys, dropoff_xs, dropoff_ys, tripCounts):
    allAsTuples.append((startX, startY, endX, endY, numTrips))

allSorted = sorted(allAsTuples, key=lambda x: x[-1], reverse=True)
maxCount = allSorted[1][-1]
GRAPH_LIMIT = 20
MAX_LINE_WIDTH = 20

print 'max count:',
print maxCount

for curTuple in allSorted[:GRAPH_LIMIT]:
    if 0 not in curTuple:
        deltaX = curTuple[0]-curTuple[2]
        deltaY = curTuple[1]-curTuple[3]
        distance = np.sqrt(deltaX*deltaX + deltaY*deltaY)
        # if distance < .000000001:
        #     continue
        #else
        print curTuple,
        print distance
        # plt.plot([curTuple[0], curTuple[2]],[curTuple[1],curTuple[3]], linewidth=MAX_LINE_WIDTH*float(curTuple[-1])/maxCount)
        plt.plot([curTuple[0], curTuple[2]],[curTuple[1],curTuple[3]], linewidth=5)

plt.show()





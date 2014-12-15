import numpy as np
from matplotlib import pyplot as plt
import csv
import pdb
from matplotlib import colors as colors
import sys

filename = 'results-20141212-211526.csv'

if len(sys.argv) == 2:
    firstIndex = sys.argv[0]
    seondIndex = sys.argv[1]
else:
    firstIndex = 0
    seondIndex = 1


counts = []
dists = []

with open(filename) as opened:
    readerObj = csv.reader(opened)
 
    lines = 0
    for line in readerObj:
        lines +=1
        if lines == 1:
            continue

        curCount = float(line[firstIndex])
        curDist = float(line[seondIndex])/100.

        if curDist > 4.5:
            continue
        counts.append(curCount)
        dists.append(curDist)

# plt.plot(dists, counts)
plt.bar(dists, counts, width=.01)

plt.title('Average Lifetime Driver Trip Distance vs\nNumber of Drivers with that Average\n(Only Includes Drivers with over 500 Lifetime Trips)')
plt.xlabel('Average Lifetime Driver Trip Distance (miles)')
plt.ylabel('Number of Drivers with that Average (absolute)')

# heatmap, xedge, yedge = np.histogram([counts, dists])

# plt.imshow(heatmap)
plt.show()

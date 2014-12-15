import numpy as np
from matplotlib import pyplot as plt
import csv
import pdb
from matplotlib import colors as colors
import sys
from scipy.stats import kde
from scipy import ndimage
import pickle

BINS = 2000
# nycBounds = [[-74.05,-73.9],[40.67,40.85]] #no laguardia
# nycBounds = [[-74.05,-73.85],[40.67,40.85]] #with laguardia
nycBounds = [[-74.05,-73.85],[40.67,40.885]] #with bx


#make commandline later:
# filename = 'trips_from_lazy_drivers_cleaned.csv'
# filename = 'trips_from_lazy_drivers_frequent.csv'

# print sys.argv
# sys.exit()

if len(sys.argv) == 4:
    filename, firstIndex, seondIndex = sys.argv[1:]
elif len(sys.argv) == 2:
    filename = sys.argv[1]
elif len(sys.argv) == 5:
    filename, firstIndex, seondIndex, BINS = sys.argv[1:]
else:
    firstIndex = -2
    seondIndex = -1

firstIndex = int(firstIndex)
seondIndex = int(seondIndex)
BINS = int(BINS)

xs, ys = [], []

with open(filename) as opened:
    readerObj = csv.reader(opened)
    index = 0
    for line in readerObj:
        if index == 0:
            index += 1
            continue
        xs.append(float(line[firstIndex]))
        ys.append(float(line[seondIndex]))

xsFull = xs
ysFull = ys

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

# heatmapSmooth = kde.gaussian_kde(heatmap)
heatmapSmooth = ndimage.filters.gaussian_filter(heatmap, 10, mode='nearest')

pickle.dump(heatmapSmooth, open("pickled_smooth_" + filename[:-5], 'wb'))

# toShowMatrix = heatmap
toShowMatrix = heatmapSmooth
COLORMAP='PuRd'
# plt.imshow(toShowMatrix, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal')
plt.imshow(toShowMatrix, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', vmin=0, vmax=maxI/300, cmap=COLORMAP)
# plt.imshow(toShowMatrix, origin='lower', extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]], aspect='equal', norm=colors.BoundaryNorm([ele for ele in np.linspace(specialMedian, maxI, 10)], ncolors=256, clip = False))
# plt.imshow(toShowMatrix, extent=[xedge[0], xedge[-1], yedge[0],yedge[-1]])
# plt.imshow(toShowMatrix, aspect='equal')

plt.show()
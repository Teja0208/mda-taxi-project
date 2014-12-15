import numpy as np
from matplotlib import pyplot as plt
import csv
import pdb
from matplotlib import colors as colors
import sys
from scipy.stats import kde
from scipy import ndimage
import pickle
import matplotlib.patches as mpatches


if len(sys.argv)==3:
    p1, p2 = sys.argv[1:]
else:
    raise IOError("usage \'python compare_heatmaps.py pickle_filename_1 pickle_filename_2")

heat1 = pickle.load(open(p1, 'rb'))
heat2 = pickle.load(open(p2, 'rb'))

heat1 = heat1/np.max(np.max(heat1)) #normalize against hottest
heat2 = heat2/np.max(np.max(heat2))

difference = heat2-heat1

#compute diff stats for plotting use
maxI = np.max(np.max(difference))
minI = np.min(np.min(difference))
medI = np.median(np.median(difference))
meanI = np.mean(np.mean(difference))

#do math to ensure that the background (0) ends up being in the middle of 
# vmin and vmax (just requires that vmin===vmax )



VMAX = maxI/6
COLORMAP='RdBu'#'BrBG'
difference = difference * -1#to make colormap blue == yankees red==mets
plt.imshow(difference, origin='bottom',cmap=COLORMAP, vmin=-1*VMAX, vmax=VMAX)
plt.title('Ridership Difference (2013 Season)\nYankees Pickups Heatmap minus Mets Pickups Heatmap')

metsLegend = mpatches.Patch(color='red', label='More Mets')
yankeesLegend = mpatches.Patch(color='blue', label='More Yankees')
plt.legend([yankeesLegend, metsLegend], ['More Yankees', 'More Mets'])
plt.axis('off')
plt.show()

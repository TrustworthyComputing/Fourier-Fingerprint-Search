#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import sys
import string

benchmark = 'class'
mydpi = 600
pltsize = (9, 3.2)


data = {
    'class_naive' : {
        '2_slices' : [0.67, 0.97, 0.83, 0.78, 0.66, 0.96, 0.83, 0.87, 0.97, 0.94, 0.66, 0.85, 0.99, 0.74, 0.72, 0.66, 0.72, 0.99, 0.66, 0.75, 0.98, 0.90, 0.73, 0.98],
        '4_slices' : [0.44, 0.76, 0.76, 0.83, 0.45, 0.78, 0.42, 0.63, 0.71, 0.80, 0.36, 0.50, 0.69, 0.54, 0.59, 0.52, 0.45, 0.64, 0.36, 0.51, 0.76, 0.71, 0.70, 0.55],
    },
    'class_neighborhoods' : {
        '2_slices' : [0.68, 1.00, 1.00, 1.00, 0.69, 1.00, 0.91, 0.93, 1.00, 1.00, 0.76, 0.93, 1.00, 0.91, 0.94, 0.71, 0.97, 1.00, 0.76, 0.97, 1.00, 1.00, 0.88, 1.00],
        '4_slices' : [0.48, 0.99, 0.99, 1.00, 0.65, 1.00, 0.71, 0.91, 0.97, 0.99, 0.58, 0.72, 0.94, 0.91, 0.88, 0.77, 0.77, 0.94, 0.58, 0.94, 0.98, 0.99, 0.99, 0.75],
    }
}

x_axis_labels = [
    'Bearings',
    'Bolts',
    'Brackets',
    'Bushing Liners',
    'Bushing',
    'Collets',
    'Gasket',
    'Grommets',
    'Headless Screws',
    'Hex Screws',
    'Keyway Shaft',
    'Machine Key',
    'Nuts',
    'O Rings',
    'Pipe Fittings',
    'Pipe Joints',
    'Pipes',
    'Rollers',
    'Rotary Shaft',
    'Shaft Collar',
    'Slotted Screws',
    'Socket Screws',
    'Thumb Screws',
    'Washers'
]

data8b_naive = data[benchmark+"_naive"]['2_slices']
data16b_naive = data[benchmark+"_naive"]['4_slices']

data8b_neighborhoods = data[benchmark+"_neighborhoods"]['2_slices']
data16b_neighborhoods = data[benchmark+"_neighborhoods"]['4_slices']


N = len(data8b_neighborhoods)
index = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots(figsize=pltsize)

ax.margins(0.01, 0.01)

rects1_neighborhoods = ax.bar(index-width/2, data8b_neighborhoods, width, color='#69ceff', hatch='xxxx', edgecolor='black', linewidth=1)
rects2_neighborhoods = ax.bar(index+width/2, data16b_neighborhoods, width, color='#bdbdbd', hatch='....', edgecolor='black', linewidth=1)

rects1_naive = ax.bar(index-width/2, data8b_naive, width, color='#69ceff', edgecolor='black', linewidth=1)
rects2_naive = ax.bar(index+width/2, data16b_naive, width, color='#bdbdbd', edgecolor='black', linewidth=1)


# ax.set_yscale('log')
ax.set_ylim([0, 1.05])
ax.set_yticks(np.arange(0, 1.05, step=0.2))
ax.set_ylabel('FEI index', fontsize=12)
ax.set_xticks(index)
ax.set_xlabel('FabWave Class', fontsize=12)
ax.set_xticklabels(x_axis_labels, rotation='90')

ax.tick_params(axis='both', which='major', labelsize=10)

ax.legend((rects1_naive[0], rects2_naive[0], rects1_neighborhoods[0], rects2_neighborhoods[0]), ['Naive 2 slices', 'Naive 4 slices', 'Neighborhoods 2 slices', 'Neighborhoods 4 slices'], fontsize=10, ncol=4, bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower center')
# ax.legend((rects1_naive[0], rects2_naive[0], rects1_neighborhoods[0], rects2_neighborhoods[0]), ['Naive 2 slices', 'Naive 4 slices', 'Neighborhoods 2 slices', 'Neighborhoods 4 slices'], fontsize=9, ncol=4, loc='lower center', framealpha=0.9)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%2.1f' % (height), ha='center', va='bottom', fontsize=9)


# autolabel(rects1_neighborhoods)
# autolabel(rects2_neighborhoods)

# plt.show()

plt.tight_layout()
plt.savefig("../images/fei.png", dpi=mydpi, bbox_inches="tight", pad_inches=0.03)

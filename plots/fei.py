#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import sys
import string

benchmark = 'class'
mydpi = 600
pltsize = (9, 3.2)


data = {
    'class_fine_grained' : {
        '2_slices' : [0.864, 0.966, 0.973, 0.871, 0.842, 0.881, 0.85, 0.793, 0.945, 0.956, 0.783, 0.84, 0.847, 0.856, 0.863, 0.861, 0.854, 0.793, 0.711, 0.819, 0.865, 0.956, 0.851, 0.842],
        '6_slices' : [0.489, 0.829, 0.914, 0.829, 0.589, 0.776, 0.654, 0.613, 0.802, 0.85, 0.408, 0.913, 0.726, 0.672, 0.758, 0.655, 0.684, 0.627, 0.408, 0.574, 0.651, 0.847, 0.684, 0.615],
    },

    'class_neighborhoods' : {
        '2_slices' : [0.913, 1.0, 1.00, 0.982, 0.891, 0.969, 0.889, 0.824, 0.992, 1.00, 0.798, 0.858, 0.927, 0.93, 0.936, 0.896, 0.934, 0.833, 0.705, 0.92, 0.9, 1.0, 0.891, 0.894],
        '6_slices' : [0.594, 0.964, 0.994, 0.992, 0.828, 0.994, 0.843, 0.887, 0.972, 0.994, 0.577, 0.982, 0.951, 0.93, 0.963, 0.922, 0.941, 0.923, 0.56, 0.898, 0.863, 0.997, 0.918, 0.798],
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

data8b_fine_grained = data[benchmark+"_fine_grained"]['2_slices']
data16b_fine_grained = data[benchmark+"_fine_grained"]['6_slices']

data8b_neighborhoods = data[benchmark+"_neighborhoods"]['2_slices']
data16b_neighborhoods = data[benchmark+"_neighborhoods"]['6_slices']


N = len(data8b_neighborhoods)
index = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots(figsize=pltsize)

ax.margins(0.01, 0.01)

rects1_neighborhoods = ax.bar(index-width/2, data8b_neighborhoods, width, color='#69ceff', hatch='xxxx', edgecolor='black', linewidth=1)
rects2_neighborhoods = ax.bar(index+width/2, data16b_neighborhoods, width, color='#bdbdbd', hatch='....', edgecolor='black', linewidth=1)

rects1_fine_grained = ax.bar(index-width/2, data8b_fine_grained, width, color='#69ceff', edgecolor='black', linewidth=1)
rects2_fine_grained = ax.bar(index+width/2, data16b_fine_grained, width, color='#bdbdbd', edgecolor='black', linewidth=1)


# ax.set_yscale('log')
ax.set_ylim([0, 1.05])
ax.set_yticks(np.arange(0, 1.05, step=0.2))
ax.set_ylabel('FEI index', fontsize=11)
ax.set_xticks(index)
ax.set_xlabel('FabWave Class', fontsize=11)
ax.set_xticklabels(x_axis_labels, rotation='90')

ax.tick_params(axis='both', which='major', labelsize=9)

ax.legend((rects1_fine_grained[0], rects2_fine_grained[0], rects1_neighborhoods[0], rects2_neighborhoods[0]), ['Fine-grained 2 slices', 'Fine-grained 6 slices', 'Neighborhoods 2 slices', 'Neighborhoods 6 slices'], fontsize=9, ncol=4, bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower center')
# ax.legend((rects1_fine_grained[0], rects2_fine_grained[0], rects1_neighborhoods[0], rects2_neighborhoods[0]), ['fine_grained 2 slices', 'fine_grained 4 slices', 'Neighborhoods 2 slices', 'Neighborhoods 4 slices'], fontsize=9, ncol=4, loc='lower center', framealpha=0.9)

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%2.1f' % (height), ha='center', va='bottom', fontsize=9)


# autolabel(rects1_neighborhoods)
# autolabel(rects2_neighborhoods)

# plt.show()

plt.tight_layout()
plt.savefig("../images/fei.png", dpi=mydpi, bbox_inches="tight", pad_inches=0.03)

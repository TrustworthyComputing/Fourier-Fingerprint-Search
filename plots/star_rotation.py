import numpy as np
import matplotlib.pyplot as plt
import sys

mydpi = 300

pltsize = (7, 3)

naive_accuracy = [ 0.93, 0.92, 0.905, 0.89]
neighborhoods_accuracy = [ 0.95, 0.94, 0.91, 0.9]
Time      =   [ 267.63, 149.43, 106.59, 89.75 ]

N = len(naive_accuracy)
index = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(figsize=pltsize)
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

ax.set_xticks(index)
ax.set_xlabel('Rotation degrees', fontsize=13)
ax.set_xticklabels(['$5^{\circ}$', '$10^{\circ}$', '$15^{\circ}$', '$20^{\circ}$'], fontsize=11)

ax.tick_params(axis='both', which='major', labelsize=11)
ax.tick_params(axis='both', which='minor', labelsize=11)

l1 = ax.plot(index, naive_accuracy, linestyle='solid', color='black', markerfacecolor='#076794', marker='^', linewidth=1, markersize=8)
l2 = ax.plot(index, neighborhoods_accuracy, linestyle='solid', color='black', markerfacecolor='#14b4ff', marker='D', linewidth=1, markersize=8)

# ax.set_ylim([0.5, 3])
ax.set_ylabel('Accuracy', fontsize=13)

l3 = ax2.plot(index, Time, linestyle='solid', color='black', markerfacecolor='xkcd:grey', marker='s', linewidth=1, markersize=8)
ax2.set_ylabel('Time (sec.)', fontsize=13)
# ax2.set_yscale('log')

ax2.tick_params(axis='both', which='major', labelsize=11)
ax2.tick_params(axis='both', which='minor', labelsize=11)
ax2.set_ylim([50, 300])


ax.legend((l1[0], l2[0], l3[0]), ['Naive', 'Neighborhoods', 'Time'], fontsize=11, ncol=1, loc='upper right')


plt.tight_layout()
plt.savefig('../images/star_rotation_exp.png', dpi=mydpi, bbox_inches='tight', pad_inches=0.03)

import numpy as np
import matplotlib.pyplot as plt
import sys

mydpi = 300

pltsize = (7, 3)

# Keyway_Shaft

naive_accuracy          = [ 1.0, 1.0, 1.0, 1.0, 0.92]
neighborhoods_accuracy  = [ 0.76, 0.59, 0.51, 0.50, 0.24]

Time      =   [ None, None, 1017.6, None, 197.02 ]


N = len(naive_accuracy)
index = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(figsize=pltsize)
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

ax.set_xticks(index)
ax.set_xlabel('Rotation degrees', fontsize=13)
ax.set_xticklabels(['$5^{\circ}$', '$10^{\circ}$', '$15^{\circ}$', '$20^{\circ}$', 'No rotation'], fontsize=11)

ax.tick_params(axis='both', which='major', labelsize=11)
ax.tick_params(axis='both', which='minor', labelsize=11)

l1 = ax.plot(index, naive_accuracy, linestyle='solid', color='black', markerfacecolor='#076794', marker='^', linewidth=1, markersize=8)
l2 = ax.plot(index, neighborhoods_accuracy, linestyle='solid', color='black', markerfacecolor='#14b4ff', marker='D', linewidth=1, markersize=8)

# ax.set_ylim([0.5, 3])
ax.set_ylabel('Top-1 Accuracy', fontsize=13)

l3 = ax2.plot(index, Time, linestyle='solid', color='black', markerfacecolor='#bdbdbd', marker='s', linewidth=1, markersize=8)
ax2.set_ylabel('Time (sec.)', fontsize=13)
# ax2.set_yscale('log')

ax2.tick_params(axis='both', which='major', labelsize=11)
ax2.tick_params(axis='both', which='minor', labelsize=11)
# ax2.set_ylim([50, 300])


# ax.legend((l1[0], l2[0], l3[0]), ['Naive', 'Neighborhoods', 'Time'], fontsize=11, ncol=1, loc='upper right')

ax.legend((l1[0], l2[0], l3[0]), ['Naive', 'Neighborhoods', 'Time'], fontsize=11, ncol=3, bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower center')


plt.tight_layout()
plt.savefig('../images/star_rotation_exp.png', dpi=mydpi, bbox_inches='tight', pad_inches=0.03)

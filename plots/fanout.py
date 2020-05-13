import numpy as np
import matplotlib.pyplot as plt
import sys

mydpi = 300

pltsize = (7, 3)

# TOP 3 accuracy
fine_grained_accuracy = [ 0.893, 0.947, 0.893, 0.92, 0.916 ]
neighborhoods_accuracy = [ 0.83, 0.867, 0.813, 0.84, 0.882 ]
Time = [ 1.11, 1.15, 1.15, 1.18, 1.21]

N = len(neighborhoods_accuracy)
index = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(figsize=pltsize)
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

ax.set_xticks(index)
ax.set_xlabel('Fan-out value', fontsize=13)
ax.set_xticklabels(['$5$', '$10$', '$15$', '$20$', '$25$'], fontsize=11)

ax.tick_params(axis='both', which='major', labelsize=11)
ax.tick_params(axis='both', which='minor', labelsize=11)

l1 = ax.plot(index, fine_grained_accuracy, linestyle='solid', color='black', markerfacecolor='#076794', marker='^', linewidth=1, markersize=8)
l2 = ax.plot(index, neighborhoods_accuracy, linestyle='solid', color='black', markerfacecolor='#14b4ff', marker='D', linewidth=1, markersize=8)

ax.set_ylabel('Accuracy', fontsize=13)
ax.set_ylim([0.8, 1])

l3 = ax2.plot(index, Time, linestyle='solid', color='black', markerfacecolor='xkcd:grey', marker='s', linewidth=1, markersize=8)
ax2.set_ylabel('Time (sec.)', fontsize=13)
# ax2.set_yscale('log')

ax2.tick_params(axis='both', which='major', labelsize=11)
ax2.tick_params(axis='both', which='minor', labelsize=11)
# ax2.set_ylim([25, 200])


ax.legend((l1[0], l2[0], l3[0]), ['Fine-grained', 'Neighborhoods', 'Average time per file'], fontsize=11, ncol=3, bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower center')



plt.tight_layout()
plt.savefig('../images/fanout.png', dpi=mydpi, bbox_inches='tight', pad_inches=0.03)

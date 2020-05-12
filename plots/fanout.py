import numpy as np
import matplotlib.pyplot as plt
import sys

mydpi = 300

pltsize = (7, 3)

naive_accuracy = [.94, .94, .947, .933 ]
neighborhoods_accuracy = [.787, .767, .803, .816]
Time = [ 39.11, 48.99, 70.05, 100]

N = len(neighborhoods_accuracy)
index = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(figsize=pltsize)
# ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

ax.set_xticks(index)
ax.set_xlabel('Fan-out value', fontsize=13)
ax.set_xticklabels(['$10$', '$15$', '$20$', '$25$'], fontsize=11)

ax.tick_params(axis='both', which='major', labelsize=11)
ax.tick_params(axis='both', which='minor', labelsize=11)

l1 = ax.plot(index, naive_accuracy, linestyle='solid', color='black', markerfacecolor='#076794', marker='^', linewidth=1, markersize=8)
l2 = ax.plot(index, neighborhoods_accuracy, linestyle='solid', color='black', markerfacecolor='#14b4ff', marker='D', linewidth=1, markersize=8)

ax.set_ylabel('Accuracy', fontsize=13)
# ax.set_ylim([0.5, 0.9])

# l3 = ax2.plot(index, Time, linestyle='solid', color='black', markerfacecolor='xkcd:grey', marker='s', linewidth=1, markersize=8)
# ax2.set_ylabel('Time (sec.)', fontsize=13)
# # ax2.set_yscale('log')
#
# ax2.tick_params(axis='both', which='major', labelsize=11)
# ax2.tick_params(axis='both', which='minor', labelsize=11)
# ax2.set_ylim([25, 200])


ax.legend((l1[0], l2[0]), ['Naive', 'Neighborhoods'], fontsize=11, ncol=1, loc='center left')
# ax.legend((l1[0], l2[0]), ['Naive', 'Neighborhoods'], fontsize=11, ncol=2, bbox_to_anchor=(0, 1.02, 1, 0.2), loc='lower center')


plt.tight_layout()
plt.savefig('../images/fanout.png', dpi=mydpi, bbox_inches='tight', pad_inches=0.03)

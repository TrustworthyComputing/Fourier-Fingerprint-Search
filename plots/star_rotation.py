import numpy as np
import matplotlib.pyplot as plt
import sys

"""
Top-5 accuracy

Trained the database with original dataset, query with rotated from all 3 axes.
"""

# With all rotated
# Class : new_partial_exp/rot-z-y-x-Brackets_slices4_fanout10_minsig5.txt
# 	Total queries            : 52
# 	Accuracy (naive)         : 0.85
# 	Accuracy (neighborhoods) : 0.65

# rot 30
# Total accuracy (naive)         : 0.885
# Total accuracy (neighborhoods) : 0.808
# 167.06s user 34.11s system 224% cpu 1:29.41 total
# 1.90 sec per file

# rot 20
# Total accuracy (naive)         : 0.942
# Total accuracy (neighborhoods) : 0.962
# 219.62s user 45.22s system 235% cpu 1:52.24 total
# 2.15 sec per file

# rot 10
# Total accuracy (naive)         : 1.0
# Total accuracy (neighborhoods) : 1.0
# 381.31s user 75.39s system 242% cpu 3:08.61 total
# 3.6153846153846154

mydpi = 300

pltsize = (7, 3)

naive_accuracy = [ 0.85, 0.885, 0.942, 1 ]
neighborhoods_accuracy = [ 0.65, 0.808, 0.962, 1 ]
Time = [ 0.51 , 1.9, 2.15, 3.61 ]

N = len(naive_accuracy)
index = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(figsize=pltsize)
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

ax.set_xticks(index)
ax.set_xlabel('Number of slices using star rotation', fontsize=13)
ax.set_xticklabels(['$0$', '$12$', '$18$', '$36$'], fontsize=11)

ax.tick_params(axis='both', which='major', labelsize=11)
ax.tick_params(axis='both', which='minor', labelsize=11)

l2 = ax.plot(index, neighborhoods_accuracy, linestyle='solid', color='black', markerfacecolor='#14b4ff', marker='D', linewidth=1, markersize=8)
l1 = ax.plot(index, naive_accuracy, linestyle='solid', color='black', markerfacecolor='#076794', marker='^', linewidth=1, markersize=8)

ax.set_ylim([0.58, 1.02])
ax.set_ylabel('Accuracy', fontsize=13)

l3 = ax2.plot(index, Time, linestyle='solid', color='black', markerfacecolor='xkcd:grey', marker='s', linewidth=1, markersize=8)
ax2.set_ylabel('Time (sec.)', fontsize=13)
# ax2.set_yscale('log')

ax2.tick_params(axis='both', which='major', labelsize=11)
ax2.tick_params(axis='both', which='minor', labelsize=11)
ax2.set_ylim([0, 4])


ax.legend((l1[0], l2[0], l3[0]), ['Fine-grained', 'Neighborhoods', 'Average time per model'], fontsize=11, ncol=1, loc='lower right')


plt.tight_layout()
plt.savefig('../images/star_rotation_exp.png', dpi=mydpi, bbox_inches='tight', pad_inches=0.03)

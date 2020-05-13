import numpy as np
import matplotlib.pyplot as plt
import sys

mydpi = 300

pltsize = (7, 3)

# TOP 5 - 4 slices - fanout 10
fine_grained_accuracy = [ 0.963, 0.915, 0.86, 0.823 ]
neighborhoods_accuracy = [ 0.914, 0.886, 0.845, 0.804 ]

N = len(neighborhoods_accuracy)
index = np.arange(N)  # the x locations for the groups

fig, ax = plt.subplots(figsize=pltsize)

ax.set_xticks(index)
ax.set_xlabel('Rotation axis', fontsize=13)
ax.set_xticklabels(['No rotation', '$x$', '$x$ and $y$', '$x$, $y$ and $z$'], fontsize=11)

ax.tick_params(axis='both', which='major', labelsize=11)
ax.tick_params(axis='both', which='minor', labelsize=11)

l1 = ax.plot(index, fine_grained_accuracy, linestyle='solid', color='black', markerfacecolor='#076794', marker='^', linewidth=1, markersize=8)
l2 = ax.plot(index, neighborhoods_accuracy, linestyle='solid', color='black', markerfacecolor='#14b4ff', marker='D', linewidth=1, markersize=8)

ax.set_ylabel('Accuracy', fontsize=13)
ax.set_ylim([0.79, 1.01])


ax.legend((l1[0], l2[0]), ['Fine-grained', 'Neighborhoods'], fontsize=11, ncol=3, loc='upper right')



plt.tight_layout()
plt.savefig('../images/modified_stl.png', dpi=mydpi, bbox_inches='tight', pad_inches=0.03)

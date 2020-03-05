import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import mpl_toolkits.mplot3d.art3d as art3d


fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='3d')

p = Circle((50, 50), 30, color='#758a72', fill=True)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=0, zdir="z")

p = Circle((50, 50), 40, color='#a2bd9f', fill=True)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=50, zdir="z")

p = Circle((50, 50), 30, color='#b8d6b4', fill=True)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=100, zdir="z")

ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 100)

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

# plt.show()
plt.savefig('slices.eps', format='eps', transparent=True)

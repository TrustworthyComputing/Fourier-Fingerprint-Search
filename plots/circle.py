import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import mpl_toolkits.mplot3d.art3d as art3d


fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='3d')

# blue hex colors: #14b4ff #008ed1 #076794
# green hex colors: #b8d6b4 #a2bd9f #758a72

p = Circle((50, 50), 30, color='#14b4ff', fill=True)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=100, zdir="z")

p = Circle((50, 50), 40, color='#008ed1', fill=True)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=50, zdir="z")

p = Circle((50, 50), 30, color='#076794', fill=True)
ax.add_patch(p)
art3d.pathpatch_2d_to_3d(p, z=0, zdir="z")

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

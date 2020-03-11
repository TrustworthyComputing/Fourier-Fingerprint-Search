import matplotlib.pyplot as plt
import numpy as np
import sys
import pyfftw
from mpl_toolkits.mplot3d import Axes3D

# grid = np.fromfile(sys.argv[1], dtype=float, count=-1, sep=" ", offset=0).reshape(1000,1000)
grid = np.fromfile('slice_data.txt', dtype=float, sep=" ").reshape(1000,1000)

grid_fft = np.abs(pyfftw.interfaces.numpy_fft.fft2(grid))
ny, nx = grid_fft.shape
x = np.linspace(0, 1, nx)
y = np.linspace(0, 1, ny)
xv, yv = np.meshgrid(x, y)
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
grid3d = ax.plot_surface(xv, yv, grid_fft, cmap='Blues', linewidth=0)
# grid3d=ax.plot_surface(xv,yv,grid_fft, cmap='GnBu', linewidth=0)

ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 9)

ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

# plt.show()

plt.savefig('fft.eps', format='eps', transparent=True)


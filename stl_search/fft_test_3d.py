import pyfftw
import numpy
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

c = numpy.empty([2048, 3])
a = pyfftw.byte_align(c)
i = 0
while i < 2048:
    a[i][0] = random.uniform(-1,1)
    a[i][1] = random.uniform(-5,5)
    a[i][2] = random.uniform(-1,1)
    i = i + 1

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(2048):
    ax.scatter(a[i][0], a[i][1], a[i][2])

plt.show()
fig.clear()
plt.close(fig)
b = pyfftw.interfaces.numpy_fft.fftn(a)
c = numpy.absolute(b)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(2048):
    ax.scatter(c[i][0], c[i][1], c[i][2])
plt.show()

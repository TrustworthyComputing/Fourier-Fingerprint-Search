import os
import sys
import argparse
import pyfftw
import math
import numpy as np
from scipy.signal import find_peaks
from scipy.spatial import distance
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from operator import itemgetter, attrgetter
from enum import Enum

class Axis(Enum):
    X = 1
    Y = 2
    Z = 3

def parseArgs():
    parser = argparse.ArgumentParser(description='STL compression')
    parser.add_argument('--stl', help='path to STL file (.stl)', required=True)
    parser.add_argument('--slices', help='Number of slices', required=False)
    args = parser.parse_args()
    stl_input = args.stl
    if not args.stl.endswith(".stl"):
        print("STL file should end with '.stl' extension.")
        exit(-1)
    if not os.path.isfile(args.stl):
        print("Input file '" + args.stl + "' does not exist.")
        exit(-2)
    slices = 10
    if args.slices is not None:
        slices = args.slices
    return stl_input, int(slices)

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def print_point(self):
        print(str(self.x) + ' \t ' + str(self.y) + ' \t ' + str(self.z))

def plot(array):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(array)):
        ax.scatter(array[i][0], array[i][1], array[i][2])
    plt.show()
    
def fft_3d(array):
    return np.absolute(pyfftw.interfaces.numpy_fft.fftn(array))

def stl_to_points_array(fileName):
    stl = open(fileName, "r")
    # Parse STL and save it to array
    points = []
    for line in stl:
        if "vertex" in line:
            i = 0
            tokens = line.split()
            p = Point(float(tokens[1]), float(tokens[2]), float(tokens[3]))
            points.append(p)
    stl.close()
    return points

# Points array tp numpy array
def points_array_to_numpy_array(points):
    c = np.empty([len(points), 3], dtype='f')
    array = pyfftw.byte_align(c)
    i = 0
    for p in points:
        array[i][0] = p.x
        array[i][1] = p.y
        array[i][2] = p.z
        i += 1
    return array

def sort_by_axis(axis, points):
    if axis == Axis.X:
        return sorted(points, key=lambda point: point.x)
    elif axis == Axis.Y:
        return sorted(points, key=lambda point: point.y)
    elif axis == Axis.Z:
        return sorted(points, key=lambda point: point.z)
    else:
        print("No such axis.")

def slice_and_fft(points, num_of_slices):
    points = sort_by_axis(Axis.X, points)
    min_val = points[0].x
    axis_range = abs(points[-1].x - min_val)
    # print('Min: ' + str(points[0].x))
    # print('Max: ' + str(points[-1].x))
    slice_range = axis_range / num_of_slices
    slices = [[] for i in range(num_of_slices+1)]
    # print('axis_range: ' + str(axis_range))
    # print('slice_range: ' + str(slice_range))
    for p in points:
        slice_idx = math.floor(p.x / slice_range) - math.floor(min_val / slice_range)
        # print(p.x, ' -> ', slice_idx)
        
        slices[slice_idx].append(p)

    # fft_array = [[] for i in range(num_of_slices+1)]
    fft_array = []
    i = 0
    for axis_slice in slices:
        if len(axis_slice) == 0:
            continue
        fft_array.append(fft_3d(points_array_to_numpy_array(axis_slice)))
        i += 1

    return fft_array

# Driver function
def main():
    stl_input, num_of_slices = parseArgs()
    print('Number of slices: ' + str(num_of_slices))

    points = stl_to_points_array(stl_input)

    fft_array = slice_and_fft(points, num_of_slices)

    peak_array = []
    for slice_idx in range(len(fft_array)):
        print(fft_array[slice_idx])
        
        z_vals = []
        i = 0
        for v in fft_array[slice_idx]:
            z_vals.append(v[2]) # get z value
            i += 1
        max_z = max(z_vals)
        
        peaks, properties = find_peaks(z_vals, height=max_z/10)
        peak_array.append(peaks)
        
        # print('peaks: ', end='')
        # print(peaks)
        # for p in peaks:
            # print(z_vals[p])
        
    # p1 = peaks[0]
    # p2 = peaks[1]
    # print('distance: ' + str(distance.euclidean(fft_array[slice_idx][p1], fft_array[slice_idx][p2])))
    
    return


if __name__ == "__main__":
    main()

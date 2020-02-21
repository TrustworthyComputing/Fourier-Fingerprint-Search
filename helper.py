import os
import argparse
import heapq
from enum import Enum

class Axis(Enum):
    X = 1
    Y = 2
    Z = 3
    
class Point:
    def __init__(self, token):
        self.x = float(token[1])
        self.y = float(token[2])
        self.z = float(token[3])

    def print_point(self):
        print(str(self.x) + ' \t ' + str(self.y) + ' \t ' + str(self.z))

'''
Parse arguments and perform checks.
'''
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

'''
Sort the list for the given axis
'''
def sort_by_axis(axis, points):
    if axis == Axis.X:
        return sorted(points, key=lambda point: point.x)
    elif axis == Axis.Y:
        return sorted(points, key=lambda point: point.y)
    elif axis == Axis.Z:
        return sorted(points, key=lambda point: point.z)
    else:
        print("No such axis.")

'''
Find min, max and range for the given axis
'''
def find_max_min_range(points_array, axis):
    if axis == Axis.X:
        max_x = max(p.x for p in points_array)
        min_x = min(p.x for p in points_array)
        range_x = max_x - min_x
        return max_x, min_x, range_x
    elif axis == Axis.Y:
        max_y = max(p.y for p in points_array)
        min_y = min(p.y for p in points_array)
        range_y = max_y - min_y
        return max_y, min_y, range_y
    elif axis == Axis.Z:
        max_z = max(p.z for p in points_array)
        min_z = min(p.z for p in points_array)
        range_z = max_z - min_z
        return max_z, min_z, range_z

'''
Return the nth largest of a list
'''
def nth_largest(n, lst):
    return heapq.nlargest(n, lst)[-1]

def quantizer(num, accuracy=0.02):
    factor = 1.0 / accuracy
    return round(num*factor)/factor

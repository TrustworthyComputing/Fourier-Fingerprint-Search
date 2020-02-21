import sys
import pyfftw
import math
import numpy as np
from helper import *

'''
The size of the grid that all shapes will scale to.
'''
GRID_SIZE = 1000

'''
Degree to which a fingerprint can be paired with its neighbors -- higher will cause more fingerprints, but potentially better accuracy.
'''
DEFAULT_FAN_VALUE = 15

'''
If True, will sort peaks temporally for fingerprinting; not sorting will cut down number of fingerprints, but potentially affect performance.
'''
PEAK_SORT = True


'''
* Open fileName STL file
* Parse the points
* Return array of 3D points  
'''
def stl_to_points_array(fileName):
    stl = open(fileName, "r")
    points_array = []
    triangle = []
    points_count = 0
    in_triangle = False
    for line in stl:
        if "vertex" in line and in_triangle:
            points_count +=1
            tokens = line.split()
            p = Point(tokens)
            triangle.append(p)
        elif "outer loop" in line:
            in_triangle = True
        elif "endloop" in line:
            in_triangle = False
            assert(points_count == 3)
            points_count = 0
# TODO: interpolate
            for p in triangle:
                points_array.append(p)
            triangle = []
    stl.close()
    return points_array

'''
Determine scale factor and update all points. 
'''
def scale_points(points_array, grid_size=1000):
    # Find scale factor
    max_x, min_x, range_x = find_max_min_range(points_array, Axis.X)
    max_y, min_y, range_y = find_max_min_range(points_array, Axis.Y)
    max_z, min_z, range_z = find_max_min_range(points_array, Axis.Z)
    scale_factor = float(grid_size-1) / max(range_x, range_y, range_z)
    # Update points
    for i in range(len(points_array)):
        points_array[i].x = int(scale_factor * (points_array[i].x - min_x) )
        points_array[i].y = int(scale_factor * (points_array[i].y - min_y) )
        points_array[i].z = int(scale_factor * (points_array[i].z - min_z) )
    return points_array


'''
Generate the fingerprint of a STL file and store it in the hash table.
    stl_file        : STL input file name.
    num_of_slices   : Number of slices to split the STL file to.
'''
def fingerprint(stl_file, num_of_slices):
    # Parse STL and interpolate points
    points_array = stl_to_points_array(stl_file)
    
    # Scale points
    scaled_points_array = scale_points(points_array)

    # Sort by Z axis
    scaled_points_array = sort_by_axis(Axis.Z, scaled_points_array)
    
    # For each slice 
    points_per_slice = math.ceil(len(scaled_points_array)/num_of_slices)
    for i in range(num_of_slices):
        
        # Put points on the grid 
        grid = np.zeros((GRID_SIZE, GRID_SIZE))
        for j in range(points_per_slice):
            
            idx = (i*points_per_slice) + j
            if (idx >= len(scaled_points_array)):
                break
            p = scaled_points_array[idx]
            grid[p.x][p.y] = 1
        
        # FTT



'''
Driver function
'''
def main():
    stl_file, num_of_slices = parseArgs()
    fingerprint(stl_file, num_of_slices)
    

if __name__ == "__main__":
    main()

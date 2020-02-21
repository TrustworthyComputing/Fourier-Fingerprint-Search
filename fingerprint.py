import sys
import pyfftw
import math
import numpy as np
from helper import *
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion

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
The number of peaks to keep after filtering out.
'''
DEFAULT_NUM_OF_PEAKS = 10


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
* Takes a grid and detect the peaks using the local maximum filter.
* Returns a boolean mask of the peaks (i.e. 1 when the pixel's value is the neighborhood maximum, 0 otherwise)
'''
def detect_peaks(grid):
    # define an 8-connected neighborhood
    neighborhood = generate_binary_structure(2, 2)

    # apply the local maximum filter; all pixel of maximal value in their neighborhood are set to 1
    local_max = (maximum_filter(grid, footprint=neighborhood) == grid)
    # local_max is a mask that contains the peaks we are looking for, but also the background. In order to isolate the peaks we must remove the background from the mask.

    # we create the mask of the background
    background = (grid == 0)

    # a little technicality: we must erode the background in order to successfully subtract it form local_max, otherwise a line will appear along the background border (artifact of the local maximum filter)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # we obtain the final mask, containing only peaks, by removing the background from the local_max mask (xor operation)
    detected_peaks = local_max ^ eroded_background
    return detected_peaks


'''
Generate the fingerprint of a STL file and store it in the hash table.
    stl_file            : STL input file name.
    num_of_slices       : Number of slices to split the STL file to
    num_of_peaks_to_keep: Number of peaks to keep after filtering the rest out
    fan_value           : Degree to which a fingerprint can be paired with its neighbors
'''
def fingerprint(stl_file, num_of_slices, num_of_peaks_to_keep=DEFAULT_NUM_OF_PEAKS, fan_value=DEFAULT_FAN_VALUE):
    # Parse STL and interpolate points
    points_array = stl_to_points_array(stl_file)
    
    # Scale points
    scaled_points_array = scale_points(points_array, GRID_SIZE)

    # Sort by Z axis
    scaled_points_array = sort_by_axis(Axis.Z, scaled_points_array)
    
    maxima_list = []
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
        grid_fft = np.abs( pyfftw.interfaces.numpy_fft.fft2(grid) )
        
        # Find peaks
        detected_peaks = detect_peaks(grid_fft)
        magnitudes = grid_fft[detected_peaks]
        j_arr, i_arr = np.where(detected_peaks)
        
        # Find minimum magnitude with respect to the number of peaks to keep
        min_magnitude = nth_largest(num_of_peaks_to_keep, magnitudes)
        
        # filter peaks
        magnitudes = magnitudes.flatten()
        peaks = zip(i_arr, j_arr, magnitudes)
        peaks_filtered = filter(lambda x: x[2]>min_magnitude, peaks) # freq, time, mag
        
        # get indices for frequency x and frequency y
        frequency_x_idx = []
        frequency_y_idx = []
        for x in peaks_filtered:
            frequency_x_idx.append(x[1])
            frequency_y_idx.append(x[0])
        local_maxima = zip(frequency_x_idx, frequency_y_idx, [i for k in range(len(frequency_y_idx))])
        
        maxima_list += local_maxima
    
    # Generate hashes    
    return generate_hashes(maxima_list, fan_value)


'''
Generate Hashes
'''
def generate_hashes(peaks_list, fan_value=DEFAULT_FAN_VALUE):
    for ml in peaks_list:
        print(ml)
    
    # # For each list of peaks (slice)
    # for i in range(len(peaks_list) - 1):
    #     # Select Anchor (For each peak)
    #     for j in range(len(peaks_list[i])):
    #         # For the next fan_value peaks
    #         for k in range(1, fan_value):
    # 
    #             # Check if we are at the last fan_value peaks
    #             if (k) < len(peaks_list[i + 1]):
    # 
    #                 freq1 = peaks_list[j][IDX_FREQ_I]
    #                 freq2 = peaks_list[j + k][IDX_FREQ_I]
    #                 t1 = peaks_list[j][IDX_TIME_J]
    #                 t2 = peaks_list[j + k][IDX_TIME_J]
    #                 t_delta = t2 - t1
        
    # for i in range(len(peaks_list)):
    #     for j in range(1, fan_value):
    #         if (i + j) < len(peaks_list):
    #             if t_delta >= MIN_HASH_TIME_DELTA and t_delta <= MAX_HASH_TIME_DELTA:
    #                 h = hashlib.sha1("%s|%s|%s" % (str(freq1), str(freq2), str(t_delta)))
    #                 yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], t1)
    
'''
Driver function
'''
def main():
    stl_file, num_of_slices = parseArgs()
    fingerprint(stl_file, num_of_slices, DEFAULT_NUM_OF_PEAKS, DEFAULT_FAN_VALUE)
    

if __name__ == "__main__":
    main()

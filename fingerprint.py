import sys
import pyfftw
import math
import numpy as np
import copy
import hashlib
import helper
import multiprocessing as mp
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion


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
            points_count += 1
            tokens = line.split()
            p = helper.Point(tokens)
            triangle.append(p)
        elif "outer loop" in line:
            in_triangle = True
        elif "endloop" in line:
            in_triangle = False
            assert (points_count == 3)
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
    max_x, min_x, range_x = helper.find_max_min_range(points_array, helper.Axis.X)
    max_y, min_y, range_y = helper.find_max_min_range(points_array, helper.Axis.Y)
    max_z, min_z, range_z = helper.find_max_min_range(points_array, helper.Axis.Z)
    scale_factor = float(grid_size - 1) / max(range_x, range_y, range_z)
    # Update points
    for i in range(len(points_array)):
        points_array[i].x = int(scale_factor * (points_array[i].x - min_x))
        points_array[i].y = int(scale_factor * (points_array[i].y - min_y))
        points_array[i].z = int(scale_factor * (points_array[i].z - min_z))
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
* Generate slices, apply FFT and generate the hashes for a given axis.
* The three axes can be run in parallel.
'''
def parallel_slice_fft_and_hash(axis, points_array, num_of_peaks_to_keep, num_of_slices, fan_value, queue, rotation):
    # Find peaks
    maxima_list = slice_and_fft(axis, points_array, num_of_peaks_to_keep, num_of_slices, rotation)

    # If debug, log the peaks list length
    helper.log('\nlen(maxima_list_' + str(axis) + '): ' + str(len(maxima_list)))

    # Generate hashes
    signatures = generate_hashes(maxima_list, fan_value)

    # Add hashes to the results
    queue.put(signatures)


'''
Slice the array of points, calculate FFT and find the peaks.
Return a list of peaks.
'''
def slice_and_fft(axis, points_array, num_of_peaks_to_keep, num_of_slices, rotation):
    maxima_list = []

    # Sort by axis
    scaled_points_array = helper.sort_by_axis(axis, copy.deepcopy(points_array))

    # For each slice
    points_per_slice = math.ceil(len(scaled_points_array) / num_of_slices)
    for i in range(num_of_slices):

        # Put points on the grid
        grid = np.zeros((helper.GRID_SIZE, helper.GRID_SIZE))
        for j in range(points_per_slice):

            idx = (i * points_per_slice) + j
            if (idx >= len(scaled_points_array)):
                break
            p = scaled_points_array[idx]
            grid[p.x][p.y] = 1

        if rotation:
            for r in range(3):
                grid = helper.rot90(grid)
                # FTT
                grid_fft = np.abs(pyfftw.interfaces.numpy_fft.fft2(grid))

                # Find peaks
                detected_peaks = detect_peaks(grid_fft)
                magnitudes = grid_fft[detected_peaks]
                j_arr, i_arr = np.where(detected_peaks)

                # Find minimum magnitude with respect to the number of peaks to keep
                min_magnitude = helper.nth_largest(num_of_peaks_to_keep, magnitudes)
                # If a slice does not have any peaks, continue
                if min_magnitude is None:
                    continue

                # filter peaks
                magnitudes = magnitudes.flatten()
                peaks = zip(i_arr, j_arr, magnitudes)
                peaks_filtered = filter(lambda x: x[2] > min_magnitude, peaks)  # freq, time, mag

                # get indices for frequency x and frequency y
                frequency_x_idx = []
                frequency_y_idx = []
                for x in peaks_filtered:
                    frequency_x_idx.append(x[1])
                    frequency_y_idx.append(x[0])
                local_maxima = zip(frequency_x_idx, frequency_y_idx, [i for k in range(len(frequency_y_idx))])

                maxima_list += local_maxima

        else:
            # FTT
            grid_fft = np.abs(pyfftw.interfaces.numpy_fft.fft2(grid))

            # Find peaks
            detected_peaks = detect_peaks(grid_fft)
            magnitudes = grid_fft[detected_peaks]
            j_arr, i_arr = np.where(detected_peaks)

            # Find minimum magnitude with respect to the number of peaks to keep
            min_magnitude = helper.nth_largest(num_of_peaks_to_keep, magnitudes)
            # If a slice does not have any peaks, continue
            if min_magnitude is None:
                continue

            # filter peaks
            magnitudes = magnitudes.flatten()
            peaks = zip(i_arr, j_arr, magnitudes)
            peaks_filtered = filter(lambda x: x[2] > min_magnitude, peaks)  # freq, time, mag

            # get indices for frequency x and frequency y
            frequency_x_idx = []
            frequency_y_idx = []
            for x in peaks_filtered:
                frequency_x_idx.append(x[1])
                frequency_y_idx.append(x[0])
            local_maxima = zip(frequency_x_idx, frequency_y_idx, [i for k in range(len(frequency_y_idx))])

            maxima_list += local_maxima
    return maxima_list


'''
Generate Hashes: returns a list of sha1 digests and anchor slice numbers
'''
def generate_hashes(peaks_list, fan_value):
    signatures = []
    # Use each point as an anchor
    for i in range(len(peaks_list) - fan_value):
        anchor = peaks_list[i]
        # For the next fan_value points
        for j in range(i + 1, min(i + 1 + fan_value, len(peaks_list))):
            # Generate signatue
            target = peaks_list[j]
            dist_wrt_z = target[2] - anchor[2]
            hash_input = str(anchor[0]) + str(anchor[1]) + str(target[0]) + str(target[1]) + str(dist_wrt_z)
            sha = hashlib.sha1()
            sha.update(hash_input.encode())
            # append signature to the fingerprint of the file
            key = sha.digest()
            slice_num = anchor[2]
            signatures.append( (key, slice_num) )
    return signatures


'''
Generate the fingerprint of a STL file and store it in the hash table.
    stl_file            : STL input file name.
    num_of_slices       : Number of slices to split the STL file to
    num_of_peaks_to_keep: Number of peaks to keep after filtering the rest out
    fan_value           : Degree to which a fingerprint can be paired with its neighbors
'''
def fingerprint(stl_file, num_of_slices, num_of_peaks_to_keep, fan_value, rotation):
    # Parse STL and interpolate points
    points_array = stl_to_points_array(stl_file)

    # Scale points
    scaled_points_array = scale_points(points_array, helper.GRID_SIZE)

    # Find the signatures for each axis in parallel
    queue = mp.Queue()
    processes = []
    for axis in helper.Axis:
        p = mp.Process(target=parallel_slice_fft_and_hash, args=(axis, scaled_points_array, num_of_peaks_to_keep, num_of_slices, fan_value, queue, False))
        processes.append(p)
        p.start()
        if rotation:
            p = mp.Process(target=parallel_slice_fft_and_hash, args=(axis, scaled_points_array, num_of_peaks_to_keep, num_of_slices, fan_value, queue, True))
            processes.append(p)
            p.start()

    # Retrieve the signatures
    signatures = []
    while 1:
        running = any(p.is_alive() for p in processes)
        while not queue.empty():
            partial_results = queue.get()
            signatures += partial_results
        if not running:
            break

    # Join the processes
    for p in processes:
        p.join()

    helper.log('len(signatures): ' + str(len(signatures)))

    if len(signatures) == 0:
        print()
        helper.error('No signatures generated. Try either decreasing the fan-value or increasing the number of slices.')
        exit(-1)

    # Return the list of hashes
    return signatures

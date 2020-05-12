import pyfftw
import math
import numpy as np
import copy
import helper as _hp
import multiprocessing as mp
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion


def stl_to_points_array(filename, interp):
    """
    Open filename STL file, parse the points and return an array of 3D points.
    If interp flag is true, use interpolation to add more points.
    """
    stl = open(filename, "r")
    points_array = set()
    triangle = []
    points_count = 0
    in_triangle = False
    for line in stl:
        if "vertex" in line and in_triangle:
            points_count += 1
            tokens = line.split()
            p = _hp.Point(tokens)
            triangle.append(p)
        elif "outer loop" in line:
            in_triangle = True
        elif "endloop" in line:
            in_triangle = False
            assert (points_count == 3)
            points_count = 0
            for p in triangle:
                points_array.add(p)
            # interpolate
            if (interp):
                prev_center = _hp.Point(['vertex', -100000.0, -100000.0, -100000.0])
                while (1):
                    center = _hp.tri_centroid([triangle[0], triangle[1], triangle[2]])
                    point_1 = _hp.tri_centroid([center, triangle[0], triangle[1]])
                    point_2 = _hp.tri_centroid([center, triangle[0], triangle[2]])
                    point_3 = _hp.tri_centroid([center, triangle[1], triangle[2]])
                    triangle = [point_1, point_2, point_3]
                    for p in triangle:
                        points_array.add(copy.deepcopy(p))
                    points_array.add(center)
                    if prev_center.x == center.x and prev_center.y == center.y and prev_center.z == center.z:
                        break
                    prev_center = center
            triangle = []
    stl.close()
    return list(points_array)


def scale_points(points_array, grid_size=1000):
    """
    Determine scale factor and update all points.
    """
    # Find scale factor
    max_x, min_x, range_x = _hp.find_max_min_range(points_array, _hp.Axis.X)
    max_y, min_y, range_y = _hp.find_max_min_range(points_array, _hp.Axis.Y)
    max_z, min_z, range_z = _hp.find_max_min_range(points_array, _hp.Axis.Z)
    scale_factor = float(grid_size - 1) / max(range_x, range_y, range_z)
    # Update points
    for i in range(len(points_array)):
        points_array[i].x = int(scale_factor * (points_array[i].x - min_x))
        points_array[i].y = int(scale_factor * (points_array[i].y - min_y))
        points_array[i].z = int(scale_factor * (points_array[i].z - min_z))
    return points_array


def detect_peaks(grid):
    """
    Takes a grid and detect the peaks using the local maximum filter.
    Returns a boolean mask of the peaks (i.e. 1 when the pixel's value is the neighborhood maximum, 0 otherwise)
    """
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


def parallel_slice_fft_and_hash(axis, points_array, num_of_peaks_to_keep, num_of_slices, fan_value, neighborhood_dict, rot90_times, star_degree):
    """
    Generate slices, apply FFT and generate the hashes for a given axis.
    The three axes can be run in parallel.
    The return value (signatures list) is added to a synchronized queue.
    """
    # Find peaks
    maxima_list = slice_and_fft(axis, points_array, num_of_peaks_to_keep, num_of_slices, rot90_times, star_degree)
    # If debug, log the peaks list length
    _hp.log('\nlen(maxima_list_' + str(axis) + '): ' + str(len(maxima_list)))
    # Generate hashes
    neighborhood = generate_hashes(maxima_list, axis, fan_value)
    # Add hashes to the results
    neighborhood_dict.update(neighborhood)


def slice_and_fft(axis, points_array, num_of_peaks_to_keep, num_of_slices, rot90_times, star_degree):
    """
    Slice the array of points, calculate FFT and find the peaks.
    Return a list of peaks.
    """
    maxima_list = []
    num_star_slices = 0
    # Sort by axis
    scaled_points_array = _hp.sort_by_axis(axis, copy.deepcopy(points_array))
    # For each slice
    points_per_slice = math.ceil(len(scaled_points_array) / num_of_slices)

    rot_slice_masks = []
    rot_slice_grids = []
    if star_degree:
        num_star_slices = int(180/star_degree)
        rot_slice_masks = _hp.build_line_equations(star_degree, num_star_slices)
        rot_slice_grids = np.zeros((num_star_slices, _hp.GRID_SIZE, _hp.GRID_SIZE))

    for i in range(num_of_slices + num_star_slices):
        # Put points on the grid
        grid = np.zeros((_hp.GRID_SIZE, _hp.GRID_SIZE))
        for j in range(points_per_slice):
            idx = (i * points_per_slice) + j
            if idx >= len(scaled_points_array):
                break
            p = scaled_points_array[idx]
            px, py = p.get_adjacent_axis_data(axis)
            grid[px][py] = 1

            # build rotational slices
            if star_degree:
                for k in range(num_star_slices):
                    if rot_slice_masks[k][px][py] == 1:
                        starx, stary = p.get_star_rot_axis_data(axis)
                        rot_slice_grids[k][starx][stary] = 1

        # If rotation flag is passed rotate three times for each axis
        for r in range(rot90_times):
            grid = _hp.rot90(grid)

        if i >= num_of_slices:
            grid = rot_slice_grids[i - num_of_slices]

        # FTT
        grid_fft = np.abs(pyfftw.interfaces.numpy_fft.fft2(grid))
        # Find peaks
        detected_peaks = detect_peaks(grid_fft)
        magnitudes = grid_fft[detected_peaks]
        j_arr, i_arr = np.where(detected_peaks)
        # Find minimum magnitude with respect to the number of peaks to keep
        min_magnitude = _hp.nth_largest(num_of_peaks_to_keep, magnitudes)
        # If a slice does not have any peaks, continue
        if min_magnitude is None:
            continue
        # filter peaks
        peaks = zip(i_arr, j_arr, magnitudes)
        peaks_filtered = filter(lambda peak: peak[2] > min_magnitude, peaks)  # (freq_x, freq_y, mag)
        # get indices for frequency x and frequency y
        frequency_x_idx = []
        frequency_y_idx = []
        for triple in peaks_filtered:
            frequency_x_idx.append(triple[0])
            frequency_y_idx.append(triple[1])
        local_maxima = zip(frequency_x_idx, frequency_y_idx, [i for _ in range(len(frequency_y_idx))])
        maxima_list += local_maxima

    return maxima_list


def generate_hashes(peaks_list, axis, fan_value):
    """
    Generate Hashes: returns a list of sha1 digests and anchor slice numbers
    peaks_list: [ (frequency_x, frequency_y, slice_no) ]
    """
    neighborhood = {}
    # Use each point as an anchor
    for i in range(len(peaks_list) - fan_value):
        anchor = peaks_list[i]
        # Generate anchor ID based on
        anchor_id = (anchor[0], anchor[1], anchor[2], axis.value)
        neighborhood[anchor_id] = []
        # For the next fan_value points
        for j in range(i + 1, min(i + 1 + fan_value, len(peaks_list))):
            # Generate signature
            target = peaks_list[j]
            dist_wrt_z = target[2] - anchor[2]
            hash_input = str(anchor[0]) + str(anchor[1]) + str(target[0]) + str(target[1]) + str(dist_wrt_z) + str(axis.value)
            # hash_input = str(anchor[0]) + str(anchor[1]) + str(target[0]) + str(target[1]) + str(anchor[2]) + str(target[2]) + str(axis.value) # Absolute hash input. Partial matches would be limited.
            h = _hp.sha1_hash(hash_input.encode())
            # append signature to the fingerprint of the file
            neighborhood[anchor_id].append(h)
    return neighborhood


def fingerprint(stl_file, num_of_slices, num_of_peaks_to_keep, fan_value, rotation, interp, star_rotate):
    """
    Generate the fingerprint of a STL file and store it in the hash table.
    stl_file            : STL input file name.
    num_of_slices       : Number of slices to split the STL file to
    num_of_peaks_to_keep: Number of peaks to keep after filtering the rest out
    fan_value           : Degree to which a fingerprint can be paired with its neighbors
    """
    # Parse STL and interpolate points
    points_array = stl_to_points_array(stl_file, interp)
    # Scale points
    scaled_points_array = scale_points(points_array, _hp.GRID_SIZE)
    # Find the signatures for each axis in parallel
    neighborhood_dict = mp.Manager().dict()
    processes = []
    for axis in _hp.Axis:
        total_rotations = 1
        if rotation:
            total_rotations = 4
        for rot90_times in range(total_rotations):
            # parallel_slice_fft_and_hash( axis, scaled_points_array, num_of_peaks_to_keep, num_of_slices, fan_value, neighborhood_dict, rot90_times, star_rotate )
            p = mp.Process(target=parallel_slice_fft_and_hash, args=(axis, scaled_points_array, num_of_peaks_to_keep, num_of_slices, fan_value, neighborhood_dict, rot90_times, star_rotate))
            processes.append(p)
            p.start()
    # Join the processes
    for p in processes:
        p.join()
    neighborhoods = neighborhood_dict
    _hp.log('len(neighborhoods): ' + str(len(neighborhoods)))
    if len(neighborhoods) == 0:
        print()
        _hp.error('No signatures generated. Try either decreasing the fan-value or increasing the number of slices.')
    # Return the list of hashes
    return neighborhoods

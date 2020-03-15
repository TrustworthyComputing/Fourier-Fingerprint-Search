import os
import argparse
import heapq
import copy
import hashlib
import numpy as np
from enum import Enum
from glob import glob
from colorama import Fore, Style

'''
Debug flag.
'''
DEBUG = False

'''
Verbose flag for various print messages.
'''
VERBOSE = False

'''
The maximum number of matches to return
'''
NUMBER_OF_MATCHES = 5

'''
Degree to which a fingerprint can be paired with its neighbors -- higher will cause more fingerprints, but potentially better accuracy.
'''
FAN_VALUE = 10

'''
The number of slices to split our shape to.
'''
NUM_OF_SLICES = 10

'''
The number of peaks to keep after filtering out.
'''
NUM_OF_PEAKS = 10

'''
The size of the grid that all shapes will scale to.
'''
GRID_SIZE = 1000

'''
Rotation flag.
'''
ROTATE = False

'''
Interp flag.
'''
INTERP = False

'''
Flag to print accuracy including collisions.
'''
PRINT_COLLISIONS = False

'''
Flag to print accuracy using the neighborhoods approach.
'''
NEIGHBORHOODS = False

'''
Min number of signatures to match within a neighborhood.
'''
MIN_SIGNATURES_TO_MATCH = 2

'''
Number of bytes of the hash output
'''
HASH_DIGEST_SIZE = 20


class Axis(Enum):
    '''
    A class to represent the three axes.
    '''
    X = 1
    Y = 2
    Z = 3


class Point:
    '''
    A class to store points.
    '''
    def __init__(self, token):
        self.x = float(token[1])
        self.y = float(token[2])
        self.z = float(token[3])

    def print_point(self):
        print(str(self.x) + ' \t ' + str(self.y) + ' \t ' + str(self.z))

def tri_centroid(triangle):
    '''
    Find the center of a triangle
    '''
    x = 0.0
    y = 0.0
    z = 0.0
    for point in triangle:
        x += point.x
        y += point.y
        z += point.z

    return Point(['vertex', quantizer(x / 3), quantizer(y / 3), quantizer(z / 3)])


def log(s):
    '''
    If DEBUG flag is specified, print log messages.
    '''
    if DEBUG:
        print(Fore.YELLOW + str(s) + Style.RESET_ALL)


def error(s):
    '''
    Print red the error messages.
    '''
    print(Fore.RED + '> ' + str(s) + Style.RESET_ALL)


def file_or_dir_path(filepath):
    '''
    Check if a path is a file or a directory
    '''
    if os.path.isfile(filepath) or os.path.isdir(filepath):
        return filepath
    else:
        raise NotAFileOrDirectoryError(filepath)


def is_stl(filepath):
    '''
    Check if a given file ends with .stl (or .STL) extension
    '''
    ends_with_stl = filepath.endswith('.stl') or filepath.endswith('.STL')
    if not ends_with_stl:
        error('Omitting file ' + filepath + '. Does not end with .stl extension.')
        return False
    return True


def is_binary(filepath):
    '''
    Check if a given file is binary or ASCII
    '''
    try: # Try open file in text mode. If fail then file is non-text (binary)
        with open(filepath, 'tr') as check_file:
            check_file.read()
            return False
    except:
        error('Omitting file ' + filepath + '. It is a binary STL.')
        return True


def parseArgs():
    '''
    Parse arguments and perform checks.
    '''
    parser = argparse.ArgumentParser(description='STL compression')
    parser.add_argument('--stl', help='Path to STL files (.stl) or directory.', type=file_or_dir_path, nargs='+', required=True)
    parser.add_argument('--mode', type=str.lower, choices=['learn', 'search'], help='Learn (l) or Search (s) mode.', required=True)
    parser.add_argument('--matches_num', help='Maximum number of matches to return.', required=False)
    parser.add_argument('--slices', help='Number of slices.', required=False)
    parser.add_argument('--fanout', help='Degree to which a fingerprint can be paired with its neighbors.', required=False)
    parser.add_argument('--peaks_num', help='The number of peaks to keep after filtering out.', required=False)
    parser.add_argument('--grid_size', help='The size of the grid that all shapes will scale to.', required=False)
    parser.add_argument('--rotate', help='Enable rotation.', action='store_true', required=False)
    parser.add_argument('--destroyDB', help='Destroy the database.', action='store_true', required=False)
    parser.add_argument('--verbose', help='Enable verbose mode.', action='store_true', required=False)
    parser.add_argument('--interp', help='Enable interpolation.', action='store_true', required=False)
    parser.add_argument('--debug', help='Enable debug mode.', action='store_true', required=False)
    parser.add_argument('--neighborhoods', help='Print matches using the neighborhood approach.', action='store_true', required=False)
    parser.add_argument('--print_collisions', help='Print matches with collisions.', action='store_true', required=False)
    args = parser.parse_args()
    
    # Get list of files recursively
    stl_inputs = []
    for filepath in args.stl:
        # if it is a dir, get files recursively
        if os.path.isdir(filepath):
            stl_inputs += [f for f in glob(filepath + '/**', recursive=True) if os.path.isfile(f)]
        # if it is a file, append it to the list of files
        else:
            stl_inputs.append(filepath)
    # Check that all files end with .stl
    stl_inputs = [filepath for filepath in stl_inputs if is_stl(filepath) and not is_binary(filepath)]
        
    global DEBUG
    global VERBOSE
    global NUMBER_OF_MATCHES
    global FAN_VALUE
    global NUM_OF_SLICES
    global NUM_OF_PEAKS
    global GRID_SIZE
    global ROTATE
    global INTERP
    global PRINT_COLLISIONS
    global NEIGHBORHOODS

    DEBUG = args.debug
    ROTATE = args.rotate
    INTERP = args.interp
    VERBOSE = args.verbose
    PRINT_COLLISIONS = args.print_collisions
    NEIGHBORHOODS = args.neighborhoods
    if args.matches_num is not None:
        NUMBER_OF_MATCHES = int(args.matches_num)
    if args.fanout is not None:
        FAN_VALUE = int(args.fanout)
    if args.slices is not None:
        NUM_OF_SLICES = int(args.slices)
    if args.peaks_num is not None:
        NUM_OF_PEAKS = int(args.peaks_num)
    if args.grid_size is not None:
        GRID_SIZE = int(args.grid_size)
    return stl_inputs, args.mode, args.destroyDB


def rot90(points_grid):
    '''
    Rotate the grid clockwise by 90 degrees
    '''
    return np.rot90(points_grid, 1, (0,1))


def sort_by_axis(axis, points):
    '''
    Sort the list for the given axis
    '''
    if axis == Axis.X:
        return sorted(points, key=lambda point: point.x)
    elif axis == Axis.Y:
        return sorted(points, key=lambda point: point.y)
    elif axis == Axis.Z:
        return sorted(points, key=lambda point: point.z)
    else:
        print('No such axis.')


def find_max_min_range(points_array, axis):
    '''
    Find min, max and range for the given axis
    '''
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


def sha1_hash(bytes):
    '''
    Compute the SHA-1 hash of a byte stream. 
    '''
    sha = hashlib.sha1()
    sha.update(bytes)
    return sha.digest()


def sha1_hash_lst(byte_lst):
    '''
    Compute the SHA-1 hash of a list with byte streams.
    '''
    sha = hashlib.sha1()
    for l in byte_lst:
        sha.update(l)
    return sha.digest()


def nth_largest(n, lst):
    '''
    Return the nth largest of a list
    '''
    if len(lst) == 0:
        return None
    return heapq.nlargest(n, lst)[-1]


def quantizer(num, accuracy=0.02):
    factor = 1.0 / accuracy
    return round(num*factor)/factor


def print_lst_of_tuples(lst):
    if len(lst) == 0:
        print('0')
    else:
        print()
    for l in lst:
        match = l[0]
        accuracy = l[1]
        print('\t' + match + '\t:\t' + str(round(accuracy, 3)))

'''
The maximum number of matches to return
'''
NUMBER_OF_MATCHES = 5

'''
The size of the grid that all shapes will scale to.
'''
GRID_SIZE = 1000

'''
Degree to which a fingerprint can be paired with its neighbors -- higher will cause more fingerprints, but potentially better accuracy.
'''
DEFAULT_FAN_VALUE = 10

'''
If True, will sort peaks temporally for fingerprinting; not sorting will cut down number of fingerprints, but potentially affect performance.
'''
PEAK_SORT = True

'''
The number of peaks to keep after filtering out.
'''
DEFAULT_NUM_OF_PEAKS = 10

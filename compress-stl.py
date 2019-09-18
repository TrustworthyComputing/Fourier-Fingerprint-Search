#!/usr/bin/env python

stl_input = '3d-models/boat-ascii.stl'
stl_output = stl_input[:-4] + '.cstl'

ifp = open(stl_input, mode='r')
ofp = open(stl_output, mode='w')
for line in ifp:
    tokens = line.split()
    if len(tokens) >= 3:
        str = ' '.join(tokens[-3:])
        # print(str)
        ofp.write(str)

ifp.close()
ofp.close()


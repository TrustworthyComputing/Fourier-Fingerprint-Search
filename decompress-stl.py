#!/usr/bin/env python

import os
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='STL decompression')
    parser.add_argument('--cstl', help='path to decompressed STL file (.cstl)', required=False)
    parser.add_argument('--out', help='path to custom output STL file (.stl)', required=False)
    args = parser.parse_args()
    stl_input = args.cstl
    if args.cstl is None:
        stl_input = '3d-models/boat-ascii.cstl'
    else:
        if not args.cstl.endswith(".cstl"):
            print("Compreesed STL file should end with '.cstl' extension.")
            exit(-1)
        if not os.path.isfile(args.cstl):
            print("Input file '" + args.cstl + "' does not exist.")
            exit(-2)
    if args.out is None:
        stl_output = stl_input[:-5] + '_1.stl'
    return stl_input, stl_output


def decompress(stl_input, stl_output):
    ifp = open(stl_input, mode='r')
    ofp = open(stl_output, mode='w')
    ofp.write('solid OpenSCAD_Model\n')
    tokens = ifp.readlines()[0].split() # read file and split by spaces
    i = 0
    while i < len(tokens):
        ofp.write('  facet normal ')
        ofp.write(tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2] + '\n')
        i += 3
        ofp.write('    outer loop\n')
        for _ in range(3):
            ofp.write('      vertex ' + tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2] + '\n')
            i += 3
        ofp.write('    endloop\n')
        ofp.write('  endfacet\n')
    ofp.write('endsolid OpenSCAD_Model\n')
    
    # if len(tokens) >= 3:
    #     str = ' '.join(tokens[-3:])
            # print(str)
            # ofp.write(str)
    ifp.close()
    ofp.close()


if __name__== "__main__":
    stl_input, stl_output = parseArgs()
    decompress(stl_input, stl_output)
    print('Output saved to ' + stl_output)
    
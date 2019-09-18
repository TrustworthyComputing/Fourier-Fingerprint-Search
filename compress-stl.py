#!/usr/bin/env python

import os
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='STL compression')
    parser.add_argument('--stl', help='path to STL file (.stl)', required=False)
    parser.add_argument('--out', help='path to custom output CSTL file (.cstl)', required=False)
    args = parser.parse_args()
    stl_input = args.stl
    if args.stl is None:
        stl_input = '3d-models/boat-ascii.stl'
    else:
        if not args.stl.endswith(".stl"):
            print("STL file should end with '.stl' extension.")
            exit(-1)
        if not os.path.isfile(args.stl):
            print("Input file '" + args.stl + "' does not exist.")
            exit(-2)
    if args.out is None:
        stl_output = stl_input[:-4] + '.cstl'
    return stl_input, stl_output


def compress(stl_input, stl_output):
    ifp = open(stl_input, mode='r')
    ofp = open(stl_output, mode='w')
    for line in ifp:
        tokens = line.split()
        if len(tokens) >= 3:
            str = ' '.join(tokens[-3:])
            ofp.write(str+' ')
    ifp.close()
    ofp.close()


if __name__== "__main__":
    stl_input, stl_output = parseArgs()
    compress(stl_input, stl_output)
    print('Output saved to ' + stl_output)

    
from enum import Enum

class Axis(Enum):
    X = 1
    Y = 2
    Z = 3

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
    
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def print_point(self):
        print(str(self.x) + ' \t ' + str(self.y) + ' \t ' + str(self.z))

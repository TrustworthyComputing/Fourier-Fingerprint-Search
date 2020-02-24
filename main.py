import plyvel
from fingerprint import *
from helper import *

def main():
    # parse arguments
    stl_file, num_of_slices = parseArgs()
    
    # create database
    db = plyvel.DB('./avocado_db', create_if_missing=True)
    
    # generate fingerprint of the file
    fingerprint(stl_file, db, num_of_slices, DEFAULT_NUM_OF_PEAKS,DEFAULT_FAN_VALUE)
    
    # close the database
    db.close()


if __name__ == "__main__":
    main()
import plyvel
from fingerprint import *
from helper import *


def addSignaturesToDB(db, signatures, filename):
    for sig in signatures:
        val = str(sig[1]) + ' ' + filename
        db.put(sig[0], val.encode())


def searchSignaturesInDB(db, signatures):
    matched_files = {}
    similarity = 0
    i = 0
    for sig in signatures:
        val = db.get(sig[0])
        if val is None:
            continue
        val = val.decode("utf-8").split()
        slice_no = val[0]
        filename = val[1]
        # Count occurences
        if filename in matched_files:
            matched_files[filename] += 1
        else:
            matched_files[filename] = 1
    # Bring first the ones that matched the most
    sorted(matched_files.items(), key=lambda x: x[1], reverse=True)
    # return percentages
    for k, v in matched_files.items():
        matched_files[k] /= len(signatures)
    return matched_files



def main():
    # parse arguments
    stl_file, mode, num_of_slices = parseArgs()
    
    # open (or create) database
    db = plyvel.DB('./avocado_db', create_if_missing=True)
    
    # generate fingerprint of the file
    print('Generating fingerprint of ' + stl_file + '\n')
    signatures = fingerprint(stl_file, num_of_slices, DEFAULT_NUM_OF_PEAKS, DEFAULT_FAN_VALUE)
    
    # Add fingerprint to database
    if mode == 'learn':
        print('Updating database with ' + stl_file + '\n')
        
        addSignaturesToDB(db, signatures, stl_file)
    
        print('Done')

    # Search in database for potential matches
    else: # mode == 'search':
        print('Searching in the database for STL files that are similar to ' + stl_file + '\n')
        
        matched_files = searchSignaturesInDB(db, signatures)
        print(matched_files)
    
    # close the database
    db.close()


if __name__ == "__main__":
    main()
import plyvel
from fingerprint import *
from helper import *


def addSignaturesToDB(db, signatures, filename):
    for sig in signatures:
        hash = sig[0]
        slice_no = str(sig[1])
        new_value = slice_no + ' ' + filename
    
        # Check if the hash exist and append them
        prev_values = db.get(hash)
        
        # If this is the first occurence of this hash
        if prev_values is None:
            db.put(hash, new_value.encode())
            log(new_value)
        
        # If we have seen this hash previously, check if it's from a different file
        else:
            # Get the list of [ slice_no_1, filename_1, slice_no_2, filename_2, ... ]
            prev_values = prev_values.decode("utf-8").split()
            already_exists = False
            for prev_slice, prev_fname in zip(prev_values[::2], prev_values[1::2]):
                if prev_fname == filename and prev_slice == slice_no:
                    already_exists = True
                    break
            if already_exists:
                continue # to the next signature
            prev_values.append(slice_no)
            prev_values.append(filename)
            str_value = ' '.join([str(el) for el in prev_values])
            log(str_value)
            db.put(sig[0], str_value.encode())


def searchSignaturesInDB(db, signatures):
    matched_files = {}
    similarity = 0
    i = 0
    for sig in signatures:
        val = db.get(sig[0])
        if val is None:
            continue
        # Get the list of [ slice_no_1, filename_1, slice_no_2, filename_2, ... ]
        val = val.decode("utf-8").split()
        for slice_no, filename in zip(val[::2], val[1::2]):
            
            # Check if this is a collision from another slice
            # if str(slice_no) == str(sig[1]):
                # Count occurences
            if filename in matched_files:
                matched_files[filename] += 1
            else:
                matched_files[filename] = 1
    # Bring first the ones that matched the most
    sorted(matched_files.items(), key=lambda x: x[1], reverse=True)
    # return percentages
    # for k, v in matched_files.items():
        # matched_files[k] /= len(signatures)
    return matched_files



def main():
    # parse arguments
    stl_file, mode, num_of_slices, destroyDB = parseArgs()
    
    if destroyDB:
        plyvel.destroy_db('./avocado_db')
    
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
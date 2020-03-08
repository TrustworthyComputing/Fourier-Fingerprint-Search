import helper
import plyvel
import hashlib

'''
Open database_name database. Create it if does not exist. 
'''
def openDatabase(database_name):
    db = plyvel.DB(database_name, create_if_missing=True)
    signatures_db = db.prefixed_db(b'sig')
    neighbors_db = db.prefixed_db(b'nbr')
    sig_to_nbr_db = db.prefixed_db(b'sit_nbr')
    return db, signatures_db, neighbors_db, sig_to_nbr_db


'''
Close database.
'''
def closeDatabase(db):
    db.close()


'''
Delete database_name database.
'''
def destroyDatabase(database_name):
    plyvel.destroy_db(database_name)


'''
Add list of signatures to database.

* signatures_db   : < signature_hash  : [ slice_no, filename ] >
* neighbors_db    : < anchor_hash     : [ signature_hash_from_same_anchor ] >
* sig_to_nbr_db   : < signature_hash  : [ anchor_hash ] >
'''
def addSignaturesToDB(signatures_db, neighbors_db, sig_to_nbr_db, signatures, neighborhoods, filename):
    # Add the neighborhoods to DB
    for anchor, hashes_lst in neighborhoods.items():
        # Compute the SHA1 hash of the anchor 
        sha = hashlib.sha1()
        for hash in hashes_lst:
            sha.update(hash)
        anchor_hash = sha.digest()

        # Add < signature_hash : anchor_hash > pairs to sig_to_nbr_db
        for hash in hashes_lst:
            # Check for collisions
            anchors = sig_to_nbr_db.get(hash)
            if anchors is None:
                sig_to_nbr_db.put(hash, anchor_hash)
            else:
                # Split bytestream to hashes array 
                anchors_lst = [ anchors[i * helper.HASH_DIGEST_SIZE:(i + 1) * helper.HASH_DIGEST_SIZE] for i in range((len(anchors) + helper.HASH_DIGEST_SIZE - 1) // helper.HASH_DIGEST_SIZE ) ]
                # Check if this anchor already exists for this signature
                already_exists = False
                for a in anchors_lst:
                    if a == anchor_hash:
                        already_exists = True
                        break
                if already_exists:
                    continue # to the next signature
                sig_to_nbr_db.put(hash, anchors + anchor_hash)
        
        # helper.log(str(anchor) + ' --> ' + str(len(hashes_lst)))

        # Store neighborhood
        hashes_lst_byte_str = ''.encode().join(hashes_lst)
        neighbors_db.put(anchor_hash, hashes_lst_byte_str)


    # Add the signatures
    for sig in signatures:
        hash = sig[0]
        slice_no = str(sig[1])
        new_value = slice_no + ' ' + filename
        
        # Check if the hash exist and append them
        prev_values = signatures_db.get(hash)
        
        # If this is the first occurence of this hash
        if prev_values is None:
            signatures_db.put(hash, anchor_hash + new_value.encode())
        
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
            signatures_db.put(sig[0], str_value.encode())
        

'''
Search in database given a list of signatures. Return top NUMBER_OF_MATCHES mathced files.
'''
def searchSignaturesInDB(db, signatures):
    matched_files = {}
    similarity = 0
    i = 0
    for sig in signatures:
        hash = sig[0]
        val = db.get(hash)
        if val is None:
            continue

        # Get the list of [ slice_no_1, filename_1, slice_no_2, filename_2, ... ]
        val = val.decode("utf-8").split()
        for slice_no, filename in zip(val[::2], val[1::2]):

            # If this is the first hash for that filename create a new inner dict
            if filename not in matched_files:
                matched_files[filename] = {}
                matched_files[filename]['total'] = 1

            # Count occurences
            if hash not in matched_files[filename]:
                matched_files[filename][hash] = 1
            else:
                matched_files[filename][hash] += 1
            matched_files[filename]['total'] += 1

    # Bring first the files that have the most unique matches
    unique_matches_sorted = sorted(matched_files.items(), key=lambda x: len(x[1]), reverse=True)
    with_collisions_matches_sorted = sorted(matched_files.items(), key=lambda x: x[1]['total'], reverse=True)
    '''
    unique_matches_sorted = [
        ('file_a', {'h1': 5, 'h4': 5, 'h3': 5, 'h2': 5, 'h6': 5}),
        ('file_b', {'h8': 5})
    ]
    '''
    unique_matches = {}
    collision_matches = {}
    for i in range(min(helper.NUMBER_OF_MATCHES, len(unique_matches_sorted))):
        unique_matches[unique_matches_sorted[i][0]] = (len(unique_matches_sorted[i][1]) - 1) / len(signatures)
        collision_matches[with_collisions_matches_sorted[i][0]] = with_collisions_matches_sorted[i][1]['total'] / len(signatures)
        
    return unique_matches, collision_matches


import helper as _hp
import plyvel
import hashlib


class Database:
    '''
    Key-Value storage.
    
    Schema:
    +-------------------+-------------------+
    | Key               | Value             |
    +-------------------+-------------------+
    | signature_hash    | [ file_name ]     |
    +-------------------+-------------------+
    
    Neighborhoods:
    +-----------+-------------------------------+
    | Key       | Value                         |
    +-----------+-------------------------------+
    | Anchor_id | [ signature_from_anchor_id ]  |
    +-----------+-------------------------------+
    '''
    

    def __init__(self, database_name):
        '''
        Open database_name database. Create it if does not exist. 
        '''
        self.database_name = database_name
        self.db = plyvel.DB(database_name, create_if_missing=True)
        # Generate 2 prefixed databases
        self.filenames_db = self.db.prefixed_db(b'filenames')
        self.signatures_db = self.db.prefixed_db(b'signatures')


    def close_db(self):
        '''
        Close the database.
        '''
        self.db.close()


    def add_signatures(self, neighborhoods, filename):
        '''
        Add list of signatures to database. Each signature points to a list of filenames. Refer to schema.
        '''
        # Generate SHA1 hash of filename
        sha = hashlib.sha1()
        sha.update(filename.encode())
        filename_hash = sha.digest()
        # Store filename hash in the filenames prefixed database
        self.filenames_db.put(filename_hash, filename.encode())
        # Iterate over all signatures of the file
        for _, hashes_lst in neighborhoods.items():
            for sig in hashes_lst:
                # Check if the hash exist and append them
                filehashes_lst = self.signatures_db.get(sig)
                # If this is the first occurence of this hash
                if filehashes_lst is None:
                    self.signatures_db.put(sig, filename_hash)
                # If we have seen this hash previously, check if it's from a different file
                else:
                    # Get the list of filenames. Split by HASH_DIGEST_SIZE bytes.
                    filehashes_lst = [ filehashes_lst[i * _hp.HASH_DIGEST_SIZE:(i + 1) * _hp.HASH_DIGEST_SIZE] for i in range((len(filehashes_lst) + _hp.HASH_DIGEST_SIZE - 1) // _hp.HASH_DIGEST_SIZE ) ]

                    already_exists = False
                    for fh in filehashes_lst:
                        if fh == filename_hash:
                            already_exists = True
                            break    
                    if already_exists:
                        continue # to the next signature
                    filehashes_lst.append(filename_hash)
                    str_value = ''.join([str(el) for el in filehashes_lst])
                    self.signatures_db.put(sig, str_value.encode())


    def search_signatures(self, neighborhoods):
        '''
        Search in database given a list of signatures. Return top NUMBER_OF_MATCHES mathced files.
        '''
        matched_files = {}
        total_signatures = 0
        # Iterate over all signatures of the file
        for _, hashes_lst in neighborhoods.items():
            for sig in hashes_lst:
                filehashes_lst = self.signatures_db.get(sig)
                if filehashes_lst is None:
                    continue
                # Get the list of filenames. Split by HASH_DIGEST_SIZE bytes.
                filehashes_lst = [ filehashes_lst[i * _hp.HASH_DIGEST_SIZE:(i + 1) * _hp.HASH_DIGEST_SIZE] for i in range((len(filehashes_lst) + _hp.HASH_DIGEST_SIZE - 1) // _hp.HASH_DIGEST_SIZE ) ]
                
                for filename_hash in filehashes_lst:
                    filename = self.filenames_db.get(filename_hash).decode("utf-8")
                    # If this is the first hash for that filename create a new inner dict
                    if filename not in matched_files:
                        matched_files[filename] = {}
                        matched_files[filename]['total'] = 1
                    # Count occurences
                    if sig not in matched_files[filename]:
                        matched_files[filename][sig] = 1
                    else:
                        matched_files[filename][sig] += 1
                    matched_files[filename]['total'] += 1
                total_signatures += 1
        # Bring first the files that have the most unique matches
        unique_matches_sorted = sorted(matched_files.items(), key=lambda x: len(x[1]), reverse=True)
        with_collisions_matches_sorted = sorted(matched_files.items(), key=lambda x: x[1]['total'], reverse=True)
        unique_matches = {}
        collision_matches = {}
        for i in range(min(_hp.NUMBER_OF_MATCHES, len(unique_matches_sorted))):
            unique_matches[unique_matches_sorted[i][0]] = (len(unique_matches_sorted[i][1]) - 1) / total_signatures
            collision_matches[with_collisions_matches_sorted[i][0]] = with_collisions_matches_sorted[i][1]['total'] / total_signatures
        return unique_matches, collision_matches


def destroy_db(database_name):
    '''
    Delete database_name database.
    '''
    plyvel.destroy_db(database_name)

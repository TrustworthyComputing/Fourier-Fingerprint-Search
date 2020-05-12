import helper as _hp
import plyvel

class Database:
    """
    Key-Value storage.

    Schema:
    1) Signatures DB:
        +-------------------+-------------------+
        | Key               | Value             |
        +-------------------+-------------------+
        | signature_hash    | [ filename_hash ] |
        +-------------------+-------------------+
    2) Anchors DB:
        +-------------------+-------------------+
        | Key               | Value             |
        +-------------------+-------------------+
        | signature_hash    | [ anchor_hash ]   |
        +-------------------+-------------------+
    3) Filenames DB:
        // maybe change the key to filecontents hash
        +-------------------+-------------------+
        | Key               | Value             |
        +-------------------+-------------------+
        | filename_hash     | filename          |
        +-------------------+-------------------+

    Neighborhoods:
    +-----------+-------------------------------+
    | Key       | Value                         |
    +-----------+-------------------------------+
    | Anchor_id | [ signature_from_anchor_id ]  |
    +-----------+-------------------------------+
    """


    def __init__(self, database_name):
        """
        Open database_name database. Create it if does not exist.
        """
        self.database_name = database_name
        self.db = plyvel.DB(database_name, create_if_missing=True)
        # Generate prefixed databases
        self.signatures_db = self.db.prefixed_db(b'signatures')
        self.anchors_db = self.db.prefixed_db(b'anchors')
        self.filenames_db = self.db.prefixed_db(b'filenames')


    def close_db(self):
        """
        Close the database.
        """
        self.db.close()


    def add_signatures(self, neighborhoods, filename):
        """
        Add list of signatures to database. Each signature points to a list of file names. Refer to schema.
        """
        # Generate SHA1 hash of filename
        filename_hash = _hp.sha1_hash(filename.encode())
        # Store filename hash in the filenames prefixed database
        self.filenames_db.put(filename_hash, filename.encode())
        # Iterate over all signatures of the file
        for _, hashes_lst in neighborhoods.items():
            # Compute the anchor hash based on the signatures it has
            anchor_hash = _hp.sha1_hash_lst(hashes_lst)
            for sig in hashes_lst:
                # Get the list of filename hashes
                filehashes_lst = self.signatures_db.get(sig)
                # If this is the first occurrence of this hash
                if filehashes_lst is None:
                    self.signatures_db.put(sig, filename_hash)
                    self.anchors_db.put(sig, anchor_hash)
                else: # If we have seen this hash previously, check if it's from a different file
                    self.signatures_db.put(sig, filehashes_lst+filename_hash)
                    self.anchors_db.put(sig, self.anchors_db.get(sig) + anchor_hash)


    def search_signatures(self, neighborhoods):
        """
        Search in database given a list of signatures. Return top NUMBER_OF_MATCHES mathced files.
        """
        matched_files = {}
        total_signatures = 0
        # Iterate over all signatures of the file
        for _, hashes_lst in neighborhoods.items():
            for sig in hashes_lst:
                filehashes_lst = self.signatures_db.get(sig)
                if filehashes_lst is None:
                    continue
                anchor_hashes_lst = self.anchors_db.get(sig)
                # Get the list of filenames. Split by HASH_DIGEST_SIZE bytes.
                filehashes_lst = [ filehashes_lst[i * _hp.HASH_DIGEST_SIZE:(i + 1) * _hp.HASH_DIGEST_SIZE] for i in range((len(filehashes_lst) + _hp.HASH_DIGEST_SIZE - 1) // _hp.HASH_DIGEST_SIZE ) ]
                # Get the list of anchor hashes that . Split by HASH_DIGEST_SIZE bytes.
                anchor_hashes_lst = [ anchor_hashes_lst[i * _hp.HASH_DIGEST_SIZE:(i + 1) * _hp.HASH_DIGEST_SIZE] for i in range((len(anchor_hashes_lst) + _hp.HASH_DIGEST_SIZE - 1) // _hp.HASH_DIGEST_SIZE ) ]
                # for filename_hash in filehashes_lst:
                for i in range(len(filehashes_lst)):
                    filename_hash = filehashes_lst[i]
                    filename = self.filenames_db.get(filename_hash).decode("utf-8")
                    anchor_hash = anchor_hashes_lst[i]
                    # If this is the first hash for that filename create a new inner dict
                    if filename not in matched_files:
                        matched_files[filename] = {}
                        matched_files[filename]['total'] = 1
                    # Count occurences
                    if anchor_hash not in matched_files[filename]:
                        matched_files[filename][anchor_hash] = []
                        # matched_files[filename]['anchors_matched'] = 0

# FIXME: For benchmarking, remove later
                        matched_files[filename]['anchors_matched'] = {}
                        for min_sigs in range(_hp.MIN_SIGNATURES_TO_MATCH, _hp.FAN_VALUE+1, _hp.MIN_SIGNATURES_TO_MATCH):
                            matched_files[filename]['anchors_matched'][min_sigs] = 0

                    matched_files[filename][anchor_hash].append(sig)
                    matched_files[filename]['total'] += 1
                total_signatures += 1
        # Check how many signatures and neighborhoods matched
        anchor_matches = {}
        signatures_matches = {}
        signatures_dict = {}
        for filename, anchors in matched_files.items():
            signatures_dict[filename] = {}
            signatures_dict[filename]['total'] = matched_files[filename]['total']
            # for each anchor and the hashes in its neighborhood
            for anch, sigs in anchors.items():
                # Skip the counters
                if anch == 'anchors_matched' or anch == 'total':
                    continue
                # if len(sigs) >= _hp.MIN_SIGNATURES_TO_MATCH:
                #     matched_files[filename]['anchors_matched'] += 1

# FIXME: For benchmarking, remove later
                for min_sigs in range(_hp.MIN_SIGNATURES_TO_MATCH, _hp.FAN_VALUE+1, _hp.MIN_SIGNATURES_TO_MATCH):
                    if len(sigs) >= min_sigs:
                        matched_files[filename]['anchors_matched'][min_sigs] += 1

                for s in sigs:
                    signatures_dict[filename][s] = 1
            # anchor_matches[filename] = anchors['anchors_matched'] / len(neighborhoods)

# FIXME: For benchmarking, remove later
            anchor_matches[filename] = {}
            for min_sigs in range(_hp.MIN_SIGNATURES_TO_MATCH, _hp.FAN_VALUE+1, _hp.MIN_SIGNATURES_TO_MATCH):
                anchor_matches[filename][min_sigs] = anchors['anchors_matched'][min_sigs] / len(neighborhoods)

            signatures_matches[filename] = (len(signatures_dict[filename]) - 2) / total_signatures
        # # Find top-K matches with 2 different criteria.
        # anchor_matches = sorted(anchor_matches.items(), key=lambda x: x[1], reverse=True)[:_hp.NUMBER_OF_MATCHES]
        signatures_matches = sorted(signatures_matches.items(), key=lambda x: x[1], reverse=True)[:_hp.NUMBER_OF_MATCHES]
        # # return lists of tuples
        # _hp.normalize(anchor_matches)
        # return anchor_matches, signatures_matches
# FIXME: For benchmarking, remove later
        nbr_matches_min_sigs = {}

        for min_sigs in range(_hp.MIN_SIGNATURES_TO_MATCH, _hp.FAN_VALUE+1, _hp.MIN_SIGNATURES_TO_MATCH):

            # new_dict = dict([(value, key) for key, value in old_dict.items()])

            nbr_matches_min_sigs[min_sigs] = dict([(key, value[min_sigs]) for key, value in anchor_matches.items()])
            nbr_matches_min_sigs[min_sigs] = sorted(nbr_matches_min_sigs[min_sigs].items(), key=lambda x: x[1], reverse=True)[:_hp.NUMBER_OF_MATCHES]

        return nbr_matches_min_sigs, signatures_matches


def destroy_db(database_name):
    """
    Delete database_name database.
    """
    print('Database destroyed')
    plyvel.destroy_db(database_name)

import helper
import plyvel


class Database:
    '''
    Key-Value storage.
    
    Schema:
    +-------------------+-------------------+
    | Key               | Value             |
    +-------------------+-------------------+
    | signature_hash    | [ file_name ]     |
    +-------------------+-------------------+
    '''
    

    def __init__(self, database_name):
        '''
        Open database_name database. Create it if does not exist. 
        '''
        self.database_name = database_name
        self.db = plyvel.DB(database_name, create_if_missing=True)


    def close_db(self):
        '''
        Close the database.
        '''
        self.db.close()


    def add_signatures(self, signatures, filename):
        '''
        Add list of signatures to database. Each signature points to a list of filenames. Refer to schema.
        '''
        for sig in signatures:
            # Check if the hash exist and append them
            prev_values = self.db.get(sig)
            # If this is the first occurence of this hash
            if prev_values is None:
                self.db.put(sig, filename.encode())
            # If we have seen this hash previously, check if it's from a different file
            else:
                # Get the list of filenames
                prev_values = prev_values.decode("utf-8").split()
                already_exists = False
                for prev_fname in prev_values:
                    if prev_fname == filename:
                        already_exists = True
                        break    
                if already_exists:
                    continue # to the next signature
                prev_values.append(filename)
                str_value = ' '.join([str(el) for el in prev_values])
                self.db.put(sig, str_value.encode())


    def search_signatures(self, signatures):
        '''
        Search in database given a list of signatures. Return top NUMBER_OF_MATCHES mathced files.
        '''
        matched_files = {}
        similarity = 0
        i = 0
        for sig in signatures:
            val = self.db.get(sig)
            if val is None:
                continue
            # Get the list of filenames
            val = val.decode("utf-8").split()
            for filename in val:
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


def destroy_db(database_name):
    '''
    Delete database_name database.
    '''
    plyvel.destroy_db(database_name)

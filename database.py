import os
import helper
import dataset
import hashlib


'''
Open database_name database. Create it if does not exist. 
'''
def openDatabase(database_name):
    db = dataset.connect('sqlite:///' + database_name)
    return db


'''
Delete database_name database.
'''
def destroyDatabase(database_name):
    try:
        os.remove(database_name)
    except:
        helper.error('Error while deleting directory ' + database_name)


'''
Add list of signatures to database.

Signatures Table:
[id, signature hash, filename, anchor hash]
['id', 'sig', 'fname', 'anch']
'''
def addSignaturesToDB(db, neighborhoods, filename):
    signatures_table = db['signatures']
    
    # For each anchor
    for anchor, hashes_lst in neighborhoods.items():
        # Compute the SHA1 hash of the anchor based on the signatures it contains
        sha = hashlib.sha1()
        for hash in hashes_lst:
            sha.update(hash)
        anchor_hash = sha.digest()

        # Add all the signature hashes in DB along with the anchor_hash
        for hash in hashes_lst:
            # signatures_table.insert(dict(sig=hash, fname=filename, anch=anchor_hash))
            signatures_table.upsert(dict(sig=hash, fname=filename, anch=anchor_hash), ['sig', 'fname', 'anch'])
        
        # helper.log(str(anchor) + ' --> ' + str(len(hashes_lst)))
    

'''
Search in database given a list of signatures. 
Consider a matched anchor if at least two of the hashes of the same neighborhood match. 
Return top NUMBER_OF_MATCHES mathced files.
'''
def searchSignaturesInDB(db, signatures, neighborhoods):
    signatures_table = db['signatures']
    
    # dict of < matched_files : < anchor : [ hash ] > >
    matched_files = {}
    
    # for each signature
    for sig in signatures:
        sig = sig[0]
        
        all_records = signatures_table.find(sig=sig)
        
        # For each record that has the same signature hash
        for rec in all_records:
            # Retrieve filename and anchor fields
            filename = rec['fname']
            anchor_hash = rec['anch']
        
            # If this is the first hash for that filename create a new inner dict
            if filename not in matched_files:
                matched_files[filename] = {}

            # Count occurences
            if anchor_hash not in matched_files[filename]:
                matched_files[filename][anchor_hash] = []
                matched_files[filename]['anchors_matched'] = 0
            matched_files[filename][anchor_hash].append(sig)

    # Check how many neighborhoods matched
    for filename, anchors in matched_files.items():
        # for each anchor and the hashes in its neighborhood
        for anch, sigs in anchors.items():
            # Skip the counter
            if anch == 'anchors_matched':
                continue
            
            if len(sigs) >= helper.MIN_SIGNATURES_TO_MATCH:
                matched_files[filename]['anchors_matched'] += 1
    
    # Find Top K matches
    best_matches = {}
    total_possible_matches = len(neighborhoods)
    for filename, anchors in matched_files.items():
        best_matches[filename] = anchors['anchors_matched'] / total_possible_matches
    # Bring first the files that have the most unique matches
    best_matches = sorted(best_matches.items(), key=lambda x: x[1], reverse=True)
    top_k_best_matches = {}
    for i in range(min(helper.NUMBER_OF_MATCHES, len(best_matches))):
        top_k_best_matches[best_matches[i][0]] = best_matches[i][1]
    
    return top_k_best_matches


import plyvel
import json
from fingerprint import *
from helper import *

#metadata = {'stl_id': 5, 'offset': 10}

def main():
    stl_file, num_of_slices = parseArgs()
    db = plyvel.DB('./avocado_db', create_if_missing=True)
    # key = b"c22b5f9178342609428d6f51b2c5af4c0bde6a42"
    # db.put(key, bytes(json.dumps(metadata).encode()))
    # metadict = json.loads(db.get(key))
    fingerprint(stl_file, db, num_of_slices, DEFAULT_NUM_OF_PEAKS,DEFAULT_FAN_VALUE)
    db.close()


if __name__ == "__main__":
    main()
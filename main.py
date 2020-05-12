import helper as _hp
import database as _db
import fingerprint as _fp
import sys
from tqdm import tqdm

def main():
    # parse arguments
    dir_name, stl_files, mode, destroyDB = _hp.parseArgs()

    # Delete database if the flag is set
    if destroyDB:
        _db.destroy_db('./avocado_db')
        if mode == 'search':
            sys.exit(0)

    # Open (or create) database
    db = _db.Database('./avocado_db')

    if _hp.VERBOSE:
        print('Generating fingerprint of', stl_files, 'with:',
        '\n\tNumber of matches to return :', str(_hp.NUMBER_OF_MATCHES),
        '\n\tFan value :', str(_hp.FAN_VALUE),
        '\n\tNumber of slices :', str(_hp.NUM_OF_SLICES),
        '\n\tNumber of peaks :', str(_hp.NUM_OF_PEAKS),
        '\n\tGrid size :', str(_hp.GRID_SIZE),
        '\n\tRotate flag :', str(_hp.ROTATE),
        '\n\tStar rotate :', str(_hp.STAR_ROTATE),
        '\n\tInterpolation flag :', str(_hp.INTERP),
        '\n\tMin number of signatures to match within a neighborhood :', str(_hp.MIN_SIGNATURES_TO_MATCH),
        '\n')

    # Disable progress bar if only one
    disable_tqdm = False
    if len(stl_files) < 2:
        disable_tqdm = True

    files = {}
    for min_sigs in range(_hp.MIN_SIGNATURES_TO_MATCH, _hp.FAN_VALUE+1, _hp.MIN_SIGNATURES_TO_MATCH):
        files[min_sigs] = open(dir_name + '_slices'+str(_hp.NUM_OF_SLICES) + '_fanout'+str(_hp.FAN_VALUE) + '_minsig' + str(min_sigs) + '.txt', 'w')

    # For each file
    # for stl_file in tqdm(stl_files, ncols=100, bar_format='[{n_fmt}/{total_fmt}] {l_bar}{bar}|', disable=disable_tqdm):
    for stl_file in stl_files:
        # generate fingerprint of the file
        neighborhoods = _fp.fingerprint(stl_file, _hp.NUM_OF_SLICES, _hp.NUM_OF_PEAKS, _hp.FAN_VALUE, _hp.ROTATE, _hp.INTERP, _hp.STAR_ROTATE)

        # Add fingerprint to database
        if mode == 'learn':
            db.add_signatures(neighborhoods, stl_file)
        # Search in database for potential matches
        else: # mode == 'search':
            # anchor_matches, signatures_matches = db.search_signatures(neighborhoods)

            nbr_matches_min_sigs, signatures_matches = db.search_signatures(neighborhoods)

            for min_sigs in range(_hp.MIN_SIGNATURES_TO_MATCH, _hp.FAN_VALUE+1, _hp.MIN_SIGNATURES_TO_MATCH):
                anchor_matches = nbr_matches_min_sigs[min_sigs]
                matches = None
                if _hp.PRINT_NAIVE:
                    print('\nFiles matched with ' + stl_file + ' using the number of signatures : ', end='', file=files[min_sigs])
                    matches = signatures_matches
                    _hp.print_lst_of_tuples(matches, files[min_sigs])
                    print(file=files[min_sigs])

                if _hp.NEIGHBORHOODS:
                    print('\nFiles matched with ' + stl_file + ' using the number of neighborhoods : ', end='', file=files[min_sigs])
                    matches = anchor_matches
                    _hp.print_lst_of_tuples(matches, files[min_sigs])
                    print(file=files[min_sigs])


    # Close the database
    db.close_db()

if __name__ == "__main__":
    main()

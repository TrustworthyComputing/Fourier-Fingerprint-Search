import helper as _hp
import database as _db
import fingerprint as _fp
from tqdm import tqdm

def main():
    # parse arguments
    stl_files, mode, destroyDB = _hp.parseArgs()

    # Delete database if the flag is set
    if destroyDB:
        _db.destroy_db('./avocado_db')
    
    # Open (or create) database
    db = _db.Database('./avocado_db')

    if _hp.VERBOSE:
        print('Generating fingerprint of', stl_files, 'with:',
        '\n\tNumber of matches :', str(_hp.NUMBER_OF_MATCHES),
        '\n\tFan value :', str(_hp.FAN_VALUE),
        '\n\tNumber of slices :', str(_hp.NUM_OF_SLICES),
        '\n\tNumber of peaks :', str(_hp.NUM_OF_PEAKS),
        '\n\tGrid size :', str(_hp.GRID_SIZE),
        '\n')

    # Disable progress bar if only one
    disable_tqdm = False
    if len(stl_files) < 2:
        disable_tqdm = True

    # For each file
    for stl_file in tqdm(stl_files, ncols=100, bar_format='[{n_fmt}/{total_fmt}] {l_bar}{bar}|', disable=disable_tqdm):
        # generate fingerprint of the file
        neighborhoods = _fp.fingerprint(stl_file, _hp.NUM_OF_SLICES, _hp.NUM_OF_PEAKS, _hp.FAN_VALUE, _hp.ROTATE, _hp.INTERP)

        # Add fingerprint to database
        if mode == 'learn':
            db.add_signatures(neighborhoods, stl_file)
        # Search in database for potential matches
        else: # mode == 'search':
            unique_matches, collision_matches = db.search_signatures(neighborhoods)
            print('\nFiles matched with ' + stl_file + ' : ', end='')
            _hp.print_matches(unique_matches)
            if _hp.PRINT_COLLISIONS:
                print('\nFiles matched with ' + stl_file + ' with collisions : ', end='')
                _hp.print_matches(collision_matches)
                print()
            print()

    # Close the database
    db.close_db()


if __name__ == "__main__":
    main()

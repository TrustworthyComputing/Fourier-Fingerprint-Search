import fingerprint
import helper
import database
from tqdm import tqdm

def main():
    # parse arguments
    stl_files, mode, destroyDB = helper.parseArgs()

    # Delete database if the flag is set
    if destroyDB:
        database.destroyDatabase('avocado.db')

    # open (or create) database
    db = database.openDatabase('avocado.db')

    if helper.VERBOSE:
        print('Generating fingerprint of', stl_files, 'with:',
        '\n\tNumber of matches :', str(helper.NUMBER_OF_MATCHES),
        '\n\tFan value :', str(helper.FAN_VALUE),
        '\n\tNumber of slices :', str(helper.NUM_OF_SLICES),
        '\n\tNumber of peaks :', str(helper.NUM_OF_PEAKS),
        '\n\tGrid size :', str(helper.GRID_SIZE),
        '\n')

    # Disable progress bar if only one
    disable_tqdm = False
    if len(stl_files) < 2:
        disable_tqdm = True

    # For each file
    for stl_file in tqdm(stl_files, ncols=100, bar_format='[{n_fmt}/{total_fmt}] {l_bar}{bar}|', disable=disable_tqdm):

        # generate fingerprint of the file
        signatures, neighborhoods = fingerprint.fingerprint(stl_file, helper.NUM_OF_SLICES, helper.NUM_OF_PEAKS, helper.FAN_VALUE, helper.ROTATE)

        # Add fingerprint to database
        if mode == 'learn':
            database.addSignaturesToDB(db, neighborhoods, stl_file)

        # Search in database for potential matches
        else: # mode == 'search':
            best_matches = database.searchSignaturesInDB(db, signatures, neighborhoods)
            print('\nFiles matched with ' + stl_file + ' : ', end='')
            helper.print_matches(best_matches)
            print()


if __name__ == "__main__":
    main()

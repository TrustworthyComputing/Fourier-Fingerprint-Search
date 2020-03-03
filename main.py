import fingerprint
import helper
import database


def main():
    # parse arguments
    stl_file, mode, destroyDB = helper.parseArgs()
    
    # Delete database if the flag is set
    if destroyDB:
        database.destroyDatabase('./avocado_db')
    
    # open (or create) database
    db = database.openDatabase('./avocado_db')
    
    if helper.VERBOSE:
        print('Generating fingerprint of ' + stl_file + ' with:' +
        '\n\tNumber of matches : ' + str(helper.NUMBER_OF_MATCHES) +
        '\n\tFan value : ' + str(helper.FAN_VALUE) +
        '\n\tNumber of slices : ' + str(helper.NUM_OF_SLICES) +
        '\n\tNumber of peaks : ' + str(helper.NUM_OF_PEAKS) +
        '\n\tGrid size : ' + str(helper.GRID_SIZE) +
        '\n')
    
    # generate fingerprint of the file
    signatures = fingerprint.fingerprint(stl_file, helper.NUM_OF_SLICES, helper.NUM_OF_PEAKS, helper.FAN_VALUE)
    
    # Add fingerprint to database
    if mode == 'learn':
        print('Updating database with ' + stl_file + '\n')
        
        database.addSignaturesToDB(db, signatures, stl_file)
    
        print('Done')

    # Search in database for potential matches
    else: # mode == 'search':
        print('Searching in the database for STL files that are similar to ' + stl_file + '\n')
        
        unique_matches, collision_matches = database.searchSignaturesInDB(db, signatures)
        print('Files matched: ', end = '')
        print(unique_matches)
        print('Files matched with collisions: ', end = '')
        print(collision_matches)
    
    # close the database
    database.closeDatabase(db)
    


if __name__ == "__main__":
    main()

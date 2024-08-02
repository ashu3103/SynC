import sys
import os
from constants import *
from database import *
from log import *

def manipulateDB(path, dbData, mimeType, parent_inode):
    stat_info = os.stat(path)
    for record in dbData:
        if ( stat_info.st_ino==record[DBSCHEME['inode']] and stat_info.st_atime!=record[DBSCHEME['last_modified']] ):
            # Update the records
            updateDataByInode(tuple=(str(stat_info.st_ino), parent_inode, "", "", path.split('/')[-1], mimeType, path, stat_info.st_ctime, 'modify'), inode=str(stat_info.st_ino))
            return
        
    # # Create new records
    insertData(tuple=(str(stat_info.st_ino), parent_inode, "", "", path.split('/')[-1], mimeType, path, stat_info.st_ctime, 'create'))

def traceDirectory(rootPath, dbData, parent_inode):
    manipulateDB(rootPath, dbData, "", parent_inode)
    
    with os.scandir(rootPath) as itr:
        for entry in itr:
            if entry.name.startswith("."):
                continue
            if(entry.is_dir()):
                traceDirectory(entry.path, dbData, str(os.stat(rootPath).st_ino))
                continue

            # Operations for file
            manipulateDB(entry.path, dbData, str(os.stat(rootPath).st_ino))


if __name__ == "__main__":
    # Initialize logger
    configureLogger('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = initiateLogging(name=__name__)

    # initialize the database
    initializeDB()
    logger.info(f'Database has been initialized at {DATABASE_PATH}')

    # track the files of the directory provided in argument
    trackDirectory = sys.argv[1]

    # check whether valid directory or not
    if (not os.path.exists(trackDirectory)):
        logger.error(f'The provided path {trackDirectory} doesn\'t exist')
        exit(1)
    
    # Check which one of the inodes are changed
    dbData = fetchAllFileData()
    print(dbData)

    traceDirectory(trackDirectory, dbData, "")




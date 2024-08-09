import sys
import os
from constants import *
from database import *
from log import *
from mimetype import *
from utils import *
from gdata import *


def manipulateDB(path: str, fileDict: dict, mimeType: str, parent_inode: str):
    stat_info = os.stat(path)
    # Create new records
    if (not fileDict.get(str(stat_info.st_ino))):
        logger.info(f'Create new file {path} with inode {stat_info.st_ino}')
        insertData(tuple=(str(stat_info.st_ino), parent_inode, "", "", path.split('/')[-1], mimeType, path, stat_info.st_ctime, 'create'))
        return
    # Update the changed record
    if (fileDict[str(stat_info.st_ino)].getLastModified() != stat_info.st_ctime):
        logger.info(f'Modify file {path} with inode {stat_info.st_ino}')
        updateDataByInode(tuple=(str(stat_info.st_ino), parent_inode, "", "", path.split('/')[-1], mimeType, path, stat_info.st_ctime, 'modify', str(stat_info.st_ino)))
        return

def traceDirectory(rootPath, fileDict, parent_inode):
    manipulateDB(rootPath, fileDict, getMimetype(rootPath), parent_inode)
    
    with os.scandir(rootPath) as itr:
        for entry in itr:
            if entry.name.startswith("."):
                continue
            if(entry.is_dir()):
                traceDirectory(entry.path, fileDict, str(os.stat(rootPath).st_ino))
                continue

            # Operations for file
            manipulateDB(entry.path, fileDict, getMimetype(entry.path), str(os.stat(rootPath).st_ino))

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
    dbData = fetchAllFileData() # can be cached
    fileDict = createInodeMap(dbData)
    logger.info("Successfully created file dictionary")

    traceDirectory(trackDirectory, fileDict, str(os.stat(trackDirectory).st_ino))
    dbData = fetchAllFileData()

    print(dbData)

    # Sync Data
    logger.info("Syncing data")
    g = GSession()
    g.initializeSession(dbData)
    g.syncDrive(g.root)

    dbData = fetchAllFileData()
    print(dbData)

import sqlite3
from constants import *

# DBSCHEME = {
#     "inode": 1,
#     "parent_inode": 2,
#     "id": 3,
#     "parent_id": 4,
#     "name": 5,
#     "mimeType": 6,
#     "path": 7,
#     "created_at": 8, 
#     "last_modified": 9,
#     "status": 10
# }

class fileSchema:
    def __init__(self, fileList) -> None:
        self.inode = fileList[0]
        self.parent_inode = fileList[1]
        self.id = fileList[2]
        self.parent_id = fileList[3]
        self.name = fileList[4]
        self.mimeType = fileList[5]
        self.path = fileList[6]
        self.created_at = fileList[7]
        self.last_modified = fileList[8]
        self.status = fileList[9]

    def getInode(self) -> str:
        return self.inode
    
    def getLastModified(self) -> str:
        return self.last_modified

def initializeDB():
    try :
        dbconn = sqlite3.connect(DATABASE_PATH)
        dbcurs = dbconn.cursor()
        dbcurs.execute("SELECT * FROM file")
        dbconn.close()
    except sqlite3.OperationalError :
        open(DATABASE_PATH,'w').close()
        dbconn = sqlite3.connect(DATABASE_PATH)
        dbcurs = dbconn.cursor()
        dbcurs.execute("""
        CREATE TABLE file (
                inode VARCHAR(36) NOT NULL, 
                parent_inode VARCHAR(36) NOT NULL,
                id VARCHAR(36) NOT NULL, 
                parent_id VARCHAR(36) DEFAULT 'root' NOT NULL,
                name VARCHAR(100) NOT NULL, 
                mimeType VARCHAR(36)  DEFAUlT 'application/text' NOT NULL,
                path VARCHAR(100) NOT NULL, 
                created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
                last_modified DATETIME DEFAULT (CURRENT_TIMESTAMP),
                status VARCHAR(100) DEFAULT 'create' NOT NULL, 
                PRIMARY KEY (inode)
        );
        """)
        dbconn.commit()
        dbconn.close()

def fetchAllFileData():
    dbconn = sqlite3.connect(DATABASE_PATH)
    dbcurs = dbconn.cursor()
    data = dbcurs.execute("SELECT * FROM file").fetchall()
    dbconn.close()
    return data

def insertData(tuple):
    dbconn = sqlite3.connect(DATABASE_PATH)
    dbcurs = dbconn.cursor()
    dbcurs.execute("""
            INSERT INTO file(inode,parent_inode,id,
            parent_id,name,mimeType,path,last_modified,status) VALUES (?,?,?,?,?,?,?,?,?) 
            """, tuple)
    dbconn.commit()
    dbconn.close()

def updateDataByInode(tuple):
    dbconn = sqlite3.connect(DATABASE_PATH)
    dbcurs = dbconn.cursor()
    dbcurs.execute("""
            UPDATE file SET inode = ?, parent_id = ?, id = ?, parent_id = ?,
            name = ?, mimeType = ?, path = ?, last_modified = ?, status = ? WHERE inode = ? 
            """, tuple)
    dbconn.commit()
    dbconn.close()
    
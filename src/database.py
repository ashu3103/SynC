import sqlite3
from constants import *

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
            name = ?, mimeType = ?, path = ?, last_modified = ?, status = ? WHERE id = ? 
            """, tuple)
    dbconn.commit()
    dbconn.close()
    
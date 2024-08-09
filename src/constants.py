import os

APP_PATH = os.path.dirname(os.getcwd())
DATABASE_PATH = os.path.join(APP_PATH, "instance/database.db")
DBSCHEME = {
    "inode": 0,
    "parent_inode": 1,
    "id": 2,
    "parent_id": 3,
    "name": 4,
    "mimeType": 5,
    "path": 6,
    "created_at": 7, 
    "last_modified": 8,
    "status": 9
}
import os

APP_PATH = os.path.dirname(os.getcwd())
DATABASE_PATH = os.path.join(APP_PATH, "instance/database.db")
DBSCHEME = {
    "inode": 1,
    "parent_inode": 2,
    "id": 3,
    "parent_id": 4,
    "name": 5,
    "mimeType": 6,
    "path": 7,
    "created_at": 8, 
    "last_modified": 9,
    "status": 10
}
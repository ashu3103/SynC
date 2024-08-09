from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.settings import *
from pydrive.auth import *
from constants import *
from utils import *
import os


class GSession:
    gauth = None
    drive = None
    root = None
    fileDict = None
    fileGraph = None

    def __init__(self) -> None:
        self.gauth = None

    def getGoogleAuth(self) -> None:
        gauth = GoogleAuth()
        gauth.LoadClientConfigFile(client_config_file=f'{APP_PATH}/client_secrets.json')
        gauth.LocalWebserverAuth()
        self.gauth = gauth
    
    def getDrive(self) -> None:
        if (self.gauth):
            self.drive = GoogleDrive(self.gauth)
        else:
            raise Exception("Please authenticate with the google servers first")
    
    def initializeSession(self, dbData: list) -> None:
        self.getGoogleAuth()
        self.getDrive()

        [self.fileDict, [self.root, self.fileGraph]] = buildGraphAndInodeMap(dbData)

    def createNewFile(self, inode, title, mimeType, parent_id, path):
        file = None
        if parent_id:
            file = self.drive.CreateFile({'title': title, 'mimeType': mimeType, 'parents': [{'id': parent_id}]})
        else:
            file = self.drive.CreateFile({'title': title, 'mimeType': mimeType})

        if mimeType != "application/vnd.google-apps.folder":
            file.SetContentFile(path)
            
        file.Upload()
        print('title: %s, id: %s' % (file['title'], file['id']))
        # Change database
        updateIdByInode((file["id"], parent_id, 'in-sync',inode))
        return file["id"]

    def syncDrive(self, node, parent_id=None):
        # Recursively check the status and do required things
        fileSchema = self.fileDict[node]

        if (fileSchema.getStatus() == 'create'):
            parent_id = self.createNewFile(fileSchema.getInode(), fileSchema.getName(), fileSchema.getMime(), parent_id, fileSchema.getPath())

        if (not self.fileGraph.get(node)):
            return

        for child in self.fileGraph[node]:
            self.syncDrive(child, parent_id)


    def initializeDriveDatabase(self, folder_name) -> None:
        # Search for the name of the file in 'root'
        if (self.drive):
            file_list = self.drive.ListFile({'q': "'root' in parents and trashed = false"}).GetList()
            for file in file_list:
                if (folder_name == file['title']):
                    # Save into database the id and folder_name
                    id = file['id']
                    print(f'{folder_name} - {id}')
                    return

        # Create a file of name=folder_name and mimeType='application/vnd'
        folder = self.drive.CreateFile({'title':folder_name, 'mimeType':'application/vnd.google-apps.folder'})
        folder.Upload()
        print('title: %s, id: %s' % (folder['title'], folder['id']))
        file = self.drive.CreateFile({'title': 'example.jpg', 'parents': [{'id': folder['id']}], 'mimeType': 'image/jpeg'})
        file.SetContentFile('1.jpg')
        file.Upload()
        print('title: %s, id: %s' % (file['title'], file['id']))

    def fetchDriveData(self) -> None:
        if (self.drive):
            file_list = self.drive.ListFile({'q': "'1zFBULfKpCfuWDa-0BtEkbIugj1ZvZ5R4' in parents and trashed = false"}).GetList()
            for file1 in file_list:
                print('title: %s, id: %s' % (file1['title'], file1['id']))






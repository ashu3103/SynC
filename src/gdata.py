from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.settings import *
from pydrive.auth import *
from constants import *
import os


class GData:
    gauth = None
    drive = None

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
        file = self.drive.CreateFile({'title': 'example.txt', 'parents': [{'id': folder['id']}]})
        file.SetContentString('This is an example file content')
        file.Upload()
        print('title: %s, id: %s' % (file['title'], file['id']))

    def fetchDriveData(self) -> None:
        if (self.drive):
            file_list = self.drive.ListFile({'q': "'1zFBULfKpCfuWDa-0BtEkbIugj1ZvZ5R4' in parents and trashed = false"}).GetList()
            for file1 in file_list:
                print('title: %s, id: %s' % (file1['title'], file1['id']))




g1 = GData()
g1.getGoogleAuth()
g1.getDrive()
# g1.fetchDriveData()
g1.initializeDriveDatabase('Librarys')




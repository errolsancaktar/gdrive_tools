import os.path

from google.oauth2 import service_account
from googleapiclient.discovery import build

# ## Load ENV Vars ##
# load_dotenv()

credsFile = "automation.json"


class gDrive:
    def __init__(self, credsFile):
        self.get_creds(credsFile=credsFile)
        print()

    def get_creds(self, credsFile):
        credentials = service_account.Credentials.from_service_account_file(
            credsFile)

        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform',
             'https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/driveinstance'])
        try:
            self.driveService = build('drive', 'v3', credentials=credentials)
            return True
        except:
            return False

    def get_drives(self):
        sharedDrives = self.driveService.drives().list().execute()
        driveList = sharedDrives.get('drives', [])
        try:

            drives = [{'name': item['name'], 'id': item['id']}
                      for item in driveList]
            return drives

        except:
            print("drivelist error")
            return None

    def get_files(self, driveId=None):

        try:
            if driveId:
                rawFiles = self.driveService.files().list(driveId=driveId, corpora='drive',
                                                          includeItemsFromAllDrives=True, supportsAllDrives=True).execute()
            else:
                rawFiles = self.driveService.files().list().execute()
            files = [{'name': item['name'],
                      'fileId': item['id'], 'mimeType': item['mimeType']} for item in rawFiles.get('files', [])]

            return files

        except:
            print("error")
            return None

    def create_folder(self, driveId, folderName, parentFolder=None):

        folderInfo = {
            'name': folderName,
            'parents': [driveId] if parentFolder is None else [parentFolder],
            'mimeType': 'application/vnd.google-apps.folder'

        }

        try:
            response = self.driveService.files().create(
                body=folderInfo, supportsAllDrives=True).execute()
            return response

        except:
            print("error")
            return None


def main():
    driveInstance = gDrive(credsFile=credsFile)
    print(driveInstance.get_drives())
    # print(driveInstance.get_files('0ADqFplRc8Em5Uk9PVA'))
    # print(driveInstance.get_files())
    print(driveInstance.create_folder(
        folderName='orig', driveId='0ADqFplRc8Em5Uk9PVA'))


if __name__ == "__main__":
    main()

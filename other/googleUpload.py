from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Opens a browser for authentication
drive = GoogleDrive(gauth)

# Path to the file you want to upload
file_path = "export\\202503100008.xlsx"

# Google Drive folder ID where the file should be uploaded
folder_id = "1zeQZDb-GTK3YKLeTx55LGr-nzBtFPj3b"

# Create and upload the file
file = drive.CreateFile({"title": "uploaded_file.xlsx", "parents": [{"id": folder_id}]})
file.SetContentFile(file_path)
file.Upload()

print("File uploaded successfully!")

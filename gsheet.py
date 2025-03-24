from __future__ import print_function
import os.path
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from PySide6.QtWidgets import QMessageBox
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1AYkXXV-19N2gaFVKmtCusqtPyjFTIQF8gFbUXNI_duA'
SAMPLE_RANGE_NAME = 'weightdata'

class googlesheet:
  def readText(self):
      items = []
      with open('test.txt','r') as f:
          lines = f.readlines()
          for item in lines:
              items.append([item.replace('\n','')])
          f.close()
          print(items)
          return items

  def connect_sheet(self):
      creds = None
      if os.path.exists('token.json'):
          creds = Credentials.from_authorized_user_file('token.json', SCOPES)
      # If there are no (valid) credentials available, let the user log in.
      if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
              creds.refresh(Request())
          else:
              flow = InstalledAppFlow.from_client_secrets_file(
                  'GoogleSheetAPI.json', SCOPES)
              creds = flow.run_local_server(port=3000)
          # Save the credentials for the next run
          with open('token.json', 'w') as token:
              token.write(creds.to_json())
      return creds
  
  def UpdateSheet(self,creds,valueData):
    try:
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        # valueData = [[1],[2],[3],[4],[5],[6]]   # sample data
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME,valueInputOption="USER_ENTERED",body={"values":valueData}).execute()
        # print(result)
        dlg = QMessageBox()
        dlg.setWindowTitle("อัปโหลดข้อมูล")
        dlg.setText("อัปโหลดข้อมูลสำเร็จ\n")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.exec()  

    except HttpError as err:
        dlg = QMessageBox()
        dlg.setWindowTitle("ผิดพลาด")
        dlg.setText("อัฟโหลดข้อมูลผิดพลาด \nโปรดตรวจสอบการเชื่อมต่ออินเตอร์เน็ต\nและลองทดสอบใหม่อีกครั้ง")
        dlg.setStandardButtons(QMessageBox.Ok)
        dlg.exec()   
  
def main():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    gSheet = googlesheet()
    creds = gSheet.connect_sheet()
    gSheet.UpdateSheet(creds)

    

if __name__ == '__main__':
    main()
    #getApiData()
from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'Python prjkts/keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1ei1HqFYdk9yvBEfld15DuG_f3WrQPbtPKhQvDu-AUz4'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A1:F14").execute()

print(result)

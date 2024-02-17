from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def writeToGoogleSheets(spreadsheet_id, sheet_name, sheet_range, data):
    service = build("sheets", "v4", credentials=credentials)
    body = {
        'values': data
    }
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=sheet_name + '!' + sheet_range, valueInputOption='RAW', body=body).execute()
    print(f'{result.get("updatedCells")} cells updated in {sheet_name}!{sheet_range}')


    
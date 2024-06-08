import os
import firebase_admin
from firebase_admin import credentials, firestore
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime
import pytz

# Initialize Firestore
cred = credentials.Certificate('firebase_credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Google Sheets API Setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google_service_account.json'
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = os.environ['SPREADSHEET_ID']

# Function to fetch data and update Google Sheet
def backup_firestore():
    users_ref = db.collection('users')
    users = users_ref.stream()

    registrations_ref = db.collection('registrations')
    current_month = datetime.now().month
    current_year = datetime.now().year

    data = []
    for user in users:
        user_data = user.to_dict()
        email = user_data.get('email')
        room_number = user_data.get('room_number')
        display_name = user_data.get('display_name')
        building_number = user_data.get('building_number')

        lunch_count = registrations_ref.where('email', '==', email).where('mealTime', '==', 'lunch').where('month', '==', current_month).where('year', '==', current_year).stream()
        dinner_count = registrations_ref.where('email', '==', email).where('mealTime', '==', 'dinner').where('month', '==', current_month).where('year', '==', current_year).stream()
        
        lunch_total = sum(1 for _ in lunch_count)
        dinner_total = sum(1 for _ in dinner_count)
        meal_total = lunch_total + dinner_total
        data.append([email, room_number, display_name, building_number, lunch_total, dinner_total, meal_total])

    # Create new sheet with current date
    IST = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(IST)
    sheet_suffix = "lunch" if current_time.hour < 12 else "dinner"
    sheet_title = f"{current_time.strftime('%d/%m/%Y')} {sheet_suffix}"

    sheet_body = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': sheet_title
                }
            }
        }]
    }

    service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=sheet_body).execute()

    # Update new sheet with data
    range_name = f'{sheet_title}!A1'
    body = {
        'values': [['Email', 'Room Number', 'Display Name', 'Building Number', 'Lunch Total', 'Dinner Total', 'Meal Total']] + data
    }
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption='RAW', body=body).execute()

if __name__ == '__main__':
    backup_firestore()

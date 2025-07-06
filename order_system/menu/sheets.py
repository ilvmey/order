import json
import os
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

credentials_json = os.getenv('GOOGLE_CREDENTIALS')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds_dict = json.loads(credentials_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

def get_wb():
    return client.open('點餐表單')


# def append_order_to_sheet(data):
#     sheet = get_sheet()
#     sheet.append_row([data['name'], data['item'], data['quantity']])


def get_restaurant_names():
    wb = get_wb()
    work_sheets = wb.worksheets()
    return [ws.title for ws in work_sheets if ws.title != '訂單']

def get_sheet_by_name(name):
    wb = get_wb()
    work_sheets = wb.worksheets()
    for ws in work_sheets:
        if ws.title == name:
            return ws

def append_order_to_sheet_by_restaurant(data, restaurant_name):
    sheet = client.open('點餐表單').worksheet(restaurant_name)
    sheet.append_row([data['name'], data['item'], data['quantity'], datetime.now().isoformat()])

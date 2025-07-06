import json
import os
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('點餐表單').sheet1
    return sheet


def append_order_to_sheet(data):
    sheet = get_sheet()
    sheet.append_row([data['name'], data['item'], data['quantity']])


def get_restaurant_names():
    # 使用你原本的憑證初始化
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('點餐表單')  # 總表名
    worksheets = sheet.worksheets()
    return [ws.title for ws in worksheets]

def append_order_to_sheet_by_restaurant(data, restaurant_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('點餐表單').worksheet(restaurant_name)
    sheet.append_row([data['name'], data['item'], data['quantity'], datetime.now().isoformat()])

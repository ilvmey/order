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


def get_order_log_sheet():
    return client.open("點餐表單").worksheet("訂單")

def write_orders_to_sheet(orders):
    sheet = get_order_log_sheet()
    # sheet.clear()
    values = [[seat, meal, price] for seat, meal, price in orders]
    sheet.append_rows(values, value_input_option="USER_ENTERED")

def read_orders_from_sheet():
    sheet = get_order_log_sheet()
    all_data = sheet.get_all_values()

    orders = []
    for row in all_data:
        if len(row) >= 3:
            seat, meal, price = row[0], row[1], row[2]
            try:
                price = int(price)
            except:
                price = 0
            orders.append((seat, meal, price))
    return orders
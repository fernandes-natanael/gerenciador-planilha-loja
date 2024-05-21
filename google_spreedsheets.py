import datetime
import os
import gspread
from credentials import *
from settings import *


def get_client():
    creds = get_credentials()
    return gspread.authorize(creds)

def get_workspace():
    client = get_client()
    return client.open_by_key(os.getenv("SHEETS_ID"))

def get_worksheets(workspace: gspread.spreadsheet.Spreadsheet):
    return [workspace.worksheet(name) for name in data_sheets]

def update_worksheet(worksheet, content):
    data = content.values.tolist()
    worksheet.clear()
    worksheet.append_rows([content.columns.values.tolist()] + data)
    worksheet.append_row([f"Atualizado em: {datetime.datetime.today().strftime('%d/%m/%Y %H:%M:%S')}"])


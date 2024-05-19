import os
import gspread
from credentials import *


def get_client():
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    ]
    creds = get_credentials()
    return gspread.authorize(creds)

def get_workspace():
    client = get_client()
    
    return client.open_by_key(os.getenv("SHEETS_ID"))
import os
from google.oauth2.service_account import Credentials

def get_credentials():
  scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    ]
  
  return Credentials.from_service_account_file("credentials.json", scopes=scopes)
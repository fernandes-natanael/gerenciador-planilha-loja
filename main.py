import gspread
from google.oauth2.service_account import Credentials
from data_manipulation import *
from dotenv import load_dotenv
import os
import pandas as pd
from settings import *
from collections import defaultdict


load_dotenv()

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

creds = Credentials.from_service_account_info({
  "type": os.getenv("SERVICE_ACCOUNT_TYPE"),
  "project_id": os.getenv("PROJECT_ID"),
  "private_key_id": os.getenv("PRIVATE_KEY_ID"),
  "private_key": os.getenv("PRIVATE_KEY"),
  "client_email": os.getenv("CLIENT_EMAIL"),
  "client_id": os.getenv("CLIENT_ID"),
  "auth_uri": os.getenv("AUTH_URI"),
  "token_uri": os.getenv("TOKEN_URI"),
  "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_CERT_URL"),
  "client_x509_cert_url": os.getenv("CLIENT_CERT_URL")
}, scopes=scopes)

client = gspread.authorize(creds)

workspace = client.open_by_key(os.getenv("SHEETS_ID"))

input_sheet = workspace.sheet1 # sheet where all data are save
goals_sheet = workspace.get_worksheet(1) # sheet where all goals 
processed_data_sheet = workspace.get_worksheet(2)

sells = input_sheet.get_all_records()
goals = goals_sheet.get_all_records()


inputs_df = pd.DataFrame(sells)
inputs_df[sell_date_col] = pd.to_datetime(inputs_df[sell_date_col], format='%d/%m/%Y')
inputs_df[sell_date_col] = inputs_df[sell_date_col].dt.date
inputs_df[sell_price_col] = pd.to_numeric(inputs_df[sell_price_col])

week_first, week_last = get_week_info()
month_first, month_last = get_month_info()
year_first, year_last = get_year_info()

inputs_df_this_week = inputs_df[(inputs_df[sell_date_col] >= week_first) & (inputs_df[sell_date_col] <= week_last)]
inputs_df_this_month = inputs_df[(inputs_df[sell_date_col] >= month_first) & (inputs_df[sell_date_col] <= month_last)] 
inputs_df_this_year = inputs_df[(inputs_df[sell_date_col] >= year_first) & (inputs_df[sell_date_col] <= year_last)]

def sum_sells(dataframe, period):
    dataframe = dataframe.groupby(seller_col)[sell_price_col].sum()
    dataframe = dataframe.reset_index()
    dataframe = dataframe.rename(columns={sell_price_col:period})
    return dataframe
    
weekly_sales = sum_sells(inputs_df_this_week, week_value_col)
monthly_sales = sum_sells(inputs_df_this_month, month_value_col)
yearly_sales = sum_sells(inputs_df_this_year, year_value_col)

goals_df = pd.DataFrame(goals)
goals_df[goal_col] = pd.to_numeric(goals_df[goal_col])

goals_df[sells_per_day_col] = goals_df[goal_col] / (goals_df[work_days_col]*4)
goals_df[sells_per_week_col] = goals_df[goal_col] / 4
goals_df[percent_sells_per_goal_col] = (monthly_sales[month_value_col] / goals_df[goal_col])*100
goals_df.drop(columns=[seller_col, work_days_col], inplace=True)

goals_df.rename(columns={goal_col:'Meta Atual', sells_per_day_col:'Meta por dia', sells_per_week_col:'Meta por semana'}, inplace=True)

print(goals_df)
combined_sales = pd.concat([weekly_sales, monthly_sales[month_value_col], yearly_sales[year_value_col], goals_df], axis=1)
print(combined_sales)

data = combined_sales.values.tolist()
processed_data_sheet.clear()
processed_data_sheet.update([combined_sales.columns.values.tolist()] + data)

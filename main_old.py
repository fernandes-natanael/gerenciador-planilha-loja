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
processed_data_sheet = workspace.get_worksheet(1)


sells = input_sheet.get_all_records()


df = pd.DataFrame(sells)
df[sell_date_col] = pd.to_datetime(df[sell_date_col], format='%d/%m/%Y')
df[sell_date_col] = df[sell_date_col].dt.date
df[sell_price_col] = pd.to_numeric(df[sell_price_col])

week_first, week_last = get_week_info()
month_first, month_last = get_month_info()
year_first, year_last = get_year_info()

df_this_week = df[(df[sell_date_col] >= week_first) & (df[sell_date_col] <= week_last)]
df_this_month = df[(df[sell_date_col] >= month_first) & (df[sell_date_col] <= month_last)] 
df_this_year = df[(df[sell_date_col] >= year_first) & (df[sell_date_col] <= year_last)]

df_this_week.reset_index(inplace=True)
weekly_sales = df_this_week.groupby(seller_col).sum()[sell_price_col]
# monthly_sales = df_this_month.groupby(sell_date_col)[seller_col].sum()[sell_price_col]
# yearly_sales = df_this_year.groupby(sell_date_col)[seller_col].sum()[sell_price_col]
print(weekly_sales)
salesmans = []



# for seller in df['Vendedor(a)'].unique():
#     weekly_total = weekly_sales.get(seller, 0)
#     monthly_total = monthly_sales.get(seller, 0)
#     yearly_total = yearly_sales.get(seller, 0)
#     salesmans.append({'Vendedor(a)': seller, 'Total vendido(Semana)': weekly_total, 'Total vendido(Mês)': monthly_total, 'Total vendido(Ano)': yearly_total})
    
print(salesmans)

# sells = sanitize(sells)

# sells_per_seller = get_sellers_info(sells)

# for seller, info in sells_per_seller.items():
#     print(f'Seller {seller}:\n\tthis_week: {info["this_week"]}\n\tthis_month: {info["this_month"]}\n\tthis_year: {info["this_year"]}')
    
# processed_data_sheet.clear()

# processed_data_sheet.append_rows([['Vendedor(a)', 'Semana', 'Mês', 'Ano']])

# # It can be better, but it works
# # And for now it will only show 2 sellers, so it's ok 
# for seller, info in sells_per_seller.items():
#     print(seller, format_price(info['this_week']), format_price(info['this_month']), format_price(info['this_year']))
#     processed_data_sheet.append_rows([[seller, format_price(info['this_week']), format_price(info['this_month']), format_price(info['this_year'])]])

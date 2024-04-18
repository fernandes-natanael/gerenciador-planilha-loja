import gspread
from google.oauth2.service_account import Credentials
from data_manipulation import *

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '1HszlIyHxuDFCYcWPmKqPQmL2JXTWSZz-8vUwN5AvR38'
workspace = client.open_by_key(sheet_id)

worksheet = workspace.sheet1 # sheet where all data are save

sells = worksheet.get_all_records()

sells = sanitize(sells)

sells_per_seller = get_sellers_info(sells)

for seller, info in sells_per_seller.items():
    print(f'Seller {seller}:\n\tthis_week: {info["this_week"]}\n\tthis_month: {info["this_month"]}\n\tthis_year: {info["this_year"]}')
    
update_workspace = workspace.get_worksheet(1)
update_workspace.clear()

update_workspace.append_rows([['Vendedor(a)', 'Semana', 'Mês', 'Ano']])
# It can be better, but it works
# And for now it will only show 2 sellers, so it's ok 
for seller, info in sells_per_seller.items():
    print(seller, format_price(info['this_week']), format_price(info['this_month']), format_price(info['this_year']))
    update_workspace.append_rows([[seller, format_price(info['this_week']), format_price(info['this_month']), format_price(info['this_year'])]])

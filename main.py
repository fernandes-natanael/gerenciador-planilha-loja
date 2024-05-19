import gspread
from google.oauth2.service_account import Credentials
from data_manipulation import *
from dotenv import load_dotenv
import pandas as pd
from settings import *
from google_spreedsheets import *
from collections import defaultdict
load_dotenv()

workspace = get_workspace()

input_sheet = workspace.get_worksheet(2) # sheet where all data are save
goals_sheet = workspace.get_worksheet(1) # sheet where all goals 
processed_data_sheet = workspace.get_worksheet(0)

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

print(goals_df)
combined_sales = pd.concat([weekly_sales, monthly_sales[month_value_col], yearly_sales[year_value_col], goals_df], axis=1)

combined_sales.rename(columns={
    goal_col:goal_treated_month_col, 
    sells_per_day_col:goal_treated_day_col, 
    sells_per_week_col:goal_treated_week_col
    }, inplace=True)


money_columns = [ week_value_col, month_value_col, year_value_col, goal_treated_day_col, goal_treated_week_col, goal_treated_month_col]

def format_money(value):
    return f'R$ {value:,.2f}'

def format_percent(value):
    return f'{value:,.2f}%'

for col in money_columns:
    combined_sales[col] = combined_sales[col].apply(format_money)

combined_sales[percent_sells_per_goal_col] = combined_sales[percent_sells_per_goal_col].apply(format_percent)	

print(combined_sales)

data = combined_sales.values.tolist()
processed_data_sheet.clear()
processed_data_sheet.update([combined_sales.columns.values.tolist()] + data)

from dotenv import load_dotenv
from log import logger
from settings import *
from google_spreedsheets import *
from pandas_manipulation import *
from utils import *
load_dotenv()

import os


workspace = get_workspace()
[processed_data_sheet, goals_sheet, data_sheet, temp_sheet] = get_worksheets(workspace)
logger(get_worksheets(workspace)) 

data_df = format_data_sheet(data_sheet.get_all_records())
logger(data_df)

goals_df = format_goals_sheet(goals_sheet.get_all_records())

sellers_name = get_sellers_name(goals_df)
logger(sellers_name)

data_df_this_week = get_data_in_period(data_df, *get_week_info())
data_df_this_month = get_data_in_period(data_df, *get_month_info())
data_df_this_year = get_data_in_period(data_df, *get_year_info())

logger(data_df_this_week, data_df_this_month, data_df_this_year)
    
weekly_sales = sum_sells(data_df_this_week, week_value_col, sellers_name)
monthly_sales = sum_sells(data_df_this_month, month_value_col, sellers_name)
yearly_sales = sum_sells(data_df_this_year, year_value_col, sellers_name)

logger("Sales per week, month and year", weekly_sales, monthly_sales, yearly_sales)

goals_df[sells_per_day_col] = goals_df[goal_col] / (goals_df[work_days_col]*4)
goals_df[sells_per_week_col] = goals_df[goal_col] / 4
goals_df[percent_sells_per_goal_col] = (monthly_sales[month_value_col] / goals_df[goal_col])*100

logger(goals_df)

combined_sales = formating_results(weekly_sales, monthly_sales, yearly_sales, goals_df)	

logger("Final sales", combined_sales)

update_worksheet(temp_sheet, combined_sales)
update_worksheet(processed_data_sheet, combined_sales)
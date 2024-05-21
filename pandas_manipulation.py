import pandas as pd
from formatation import format_money, format_percent
from log import logger
from settings import *

def format_data_sheet(data):
    data_df = pd.DataFrame(data)
    if data_df.empty:
        exit(0)
    data_df[col_date_sell] = pd.to_datetime(data_df[col_date_sell], format='%d/%m/%Y')
    data_df[col_date_sell] = data_df[col_date_sell].dt.date
    data_df[sell_price_col] = pd.to_numeric(data_df[sell_price_col])
    return data_df

def format_goals_sheet(data):
    goals_df = pd.DataFrame(data)
    if goals_df.empty:
        exit(0)
    goals_df[goal_col] = pd.to_numeric(goals_df[goal_col])
    goals_df[goal_col] = goals_df[goal_col].fillna(0)
    goals_df[work_days_col] = goals_df[work_days_col].fillna(1)
    return goals_df

def get_data_in_period(data, start, end):
    return data[(data[col_date_sell] >= start) & (data[col_date_sell] <= end)]

def get_sellers_name(data):
    names: pd.DataFrame = data[col_seller_name].copy()
    return names

def sum_sells(dataframe, period, sellers):
    
    dataframe = dataframe.groupby(col_seller_name)[sell_price_col].sum()
    dataframe = dataframe.reset_index()
    dataframe = dataframe.rename(columns={sell_price_col:period})
    dataframe = pd.merge(sellers, dataframe, on=col_seller_name, how='left').fillna({period: 0})
    return dataframe

def formating_results(weekly_sales, monthly_sales, yearly_sales, goals_df):
    combined_sales = pd.concat([
    weekly_sales,
    monthly_sales[month_value_col],
    yearly_sales[year_value_col],
    goals_df[goal_col],
    goals_df[sells_per_day_col],
    goals_df[sells_per_week_col],
    goals_df[percent_sells_per_goal_col]
    ], axis=1)

    logger(combined_sales)
    
    combined_sales.rename(columns={
        goal_col:goal_treated_month_col, 
        sells_per_day_col:goal_treated_day_col, 
        sells_per_week_col:goal_treated_week_col
        }, inplace=True)
    
    money_columns = [ week_value_col, month_value_col, year_value_col, goal_treated_day_col, goal_treated_week_col, goal_treated_month_col]
    
    for col in money_columns:
        combined_sales[col] = combined_sales[col].apply(format_money)
    
    combined_sales[percent_sells_per_goal_col] = combined_sales[percent_sells_per_goal_col].apply(format_percent)
    return combined_sales
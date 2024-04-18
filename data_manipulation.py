from collections import defaultdict
from datetime import datetime
from settings import *
from numba import njit

from utils import *

def format_price(valor):
    decimal = str(valor % 100)
    valor = str(valor // 100)
    return  valor + "." + decimal

# @njit
def sanitize_price(price):
    price = str(price)
    if  not '.' in price:
        return int(price.replace('.', ''))*100
    qnt_decimal = len(price) - price.index('.') - 1
    if qnt_decimal > 2:
        return int(price.replace('.', '')[:2-qnt_decimal])
    if qnt_decimal == 1:
        return int((price + '0').replace('.', ''))
    
    return int(price.replace('.', ''))

# @njit
def sanitize(data):
    for sell in data:   
        sell[sell_price_col] = sanitize_price(sell[sell_price_col])                
        sell[sell_date_col] = datetime.strptime(sell[sell_date_col], '%d/%m/%Y').date()
    return data

def get_total_sells(sells):
    total_sells = defaultdict(int)

    for sell in sells:
        seller = sell[seller_col]
        total_sell_day = sell[sell_price_col]
        if not total_sells[seller]:
            total_sells[seller] = 0
        total_sells[seller] += total_sell_day 
    return total_sells

def get_sellers_info(sells):
    week_first, week_last = get_week_info()
    month_first, month_last = get_month_info()
    year_first, year_last = get_year_info()
    
    sells_per_seller = defaultdict(lambda: defaultdict(int))
    
    for sell in sells:
        seller = sell[seller_col]
        total_sell_day = sell[sell_price_col]
        
        if week_first <= sell[sell_date_col] <= week_last:
            sells_per_seller[seller]['this_week'] += total_sell_day
        
        if month_first <= sell[sell_date_col] <= month_last:
            sells_per_seller[seller]['this_month'] += total_sell_day
        
        if year_first <= sell[sell_date_col] <= year_last:
            sells_per_seller[seller]['this_year'] += total_sell_day
            
    return sells_per_seller
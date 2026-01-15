import akshare as ak
import pandas as pd
import inspect
import openpyxl as pyxl
import json
from pathlib import Path
from constants import TIMESTAMP_LOG_PATH


# plan
# First check Json database for matching stock
# Second populate by searching based off of name - if multiple matches - either interrupt and ask or match by some other factor (price)
# Get currente prices for each

# df = ak.stock_zh_a_spot(symbol='sz300648')
# df.to_json('test.json', orient='records', force_ascii=False)

# df_read = pd.read_json('raw_akshare_stocks.json', orient='records')
# df_read.to_json('indented.json', orient='records', force_ascii=False, indent=2)


#TESTING INDVIDUAL STOCKS

# test_stock = ak.stock_individual_info_em("300648", timeout=5)
# test_stock.to_json(Path('Reference/test_stock1.json'), orient='records', force_ascii=False, indent=2)
# test_stock2 = ak.stock_individual_spot_xq("SZ300648")
# test_stock2.to_json(Path('Reference/test_stock4.json'), orient='records', force_ascii=False, indent=2)

# result3 = ak.stock_individual_basic_info_xq("SZ300648", timeout=10) # Not useful - just manager / initial listing data
# result3.to_json(Path('Reference/test_stock3.json'), orient='records', force_ascii=False, indent=2)

# stock_dict3 = result3.set_index('item')['value'].to_dict()
# print(stock_dict3)


# result2= ak.stock_individual_spot_xq("SZ300648")
# stock_dict2 = result2.set_index('item')['value'].to_dict()

# print(stock_dict2)

# exchange = 'sh'
# stock_code = '600460'

# result = ak.stock_individual_spot_xq(f"{exchange.upper()}{stock_code}", timeout=5)
# stock_dict = result.set_index('item')['value'].to_dict()

# print(stock_dict)



# with open('test_stock.json', 'r', encoding='utf-8') as file:
#     read_json = json.load(file)
# with open('stock_individual_info_dm_result.json', 'w', encoding='utf-8') as file:
#     json.dump(read_json, file, indent=2, ensure_ascii=False)

# pre_df = pd.read_json(Path('Reference/stock_individual_info_em_result.json'), orient='records')
# print(pre_df.set_index('item')['value'].to_dict())



# test_stock_name1 = "华润微"
# test_stock_name2 = "星云股份"

# stock_df = pd.read_json('indented.json', orient='records')

# stock_match1 = stock_df[stock_df["名称"].str[-6:] == "华润微"]
# stock_match2 = stock_df[stock_df["名称"].str[-6:] == "星云股份"]

# print(stock_match1.iloc[0]['最新价']) #53.3



# GETTING NUMBER FROM STOCK NAME
# test_stock_1 = ["300648", "星云股份"]
# test_stock_2 = ["688396", "华润微"]
# stock_df = pd.read_json('indented.json', orient='records')

# match1 = stock_df[stock_df["名称"] == test_stock_1[1]]
# if len(match1) == 1:
#     print(match1.iloc[0])
#     print(match1.iloc[0]["代码"])
# elif len(match1) > 1:
#     print("ERROR MORE THAN ONE MATCH")
# else:
#     print("ERROR NO MATCHES")
    


# READING EXCEL DOC
# wb = pyxl.open('短线记录.xlsx')
# ws = wb['持仓总表']

# cell = ws.cell(1, 1)
# print(type(cell))
# print(cell.value)

# print(ws.dimensions)

# Checking cache for 

# def search_stocks(stock_name):
#     with open("indented.json", "r", encoding='utf-8') as file:
#         all_stocks = json.load(file)
#     matching_stocks = list(filter(lambda x: x["名称"] == stock_name, all_stocks))
#     if len(matching_stocks) == 0:
#         raise LookupError(f"No matching stocks with stock name {stock_name} found.")
#     if len(matching_stocks) > 1:
#         raise LookupError(f"More than one match for stock {stock_name} found")
#     return matching_stocks[0]
    

# with open("stock_cache.json", "r", encoding='utf-8') as file:
#     stock_cache = json.load(file)
# for row in ws.iter_rows(min_row=2):
#     stock_name = row[1].value
#     if stock_name is None or stock_name == "汇总":
#         break
#     print(stock_name)
#     if stock_name in stock_cache:
#         print(f"{stock_name} found")
#     else:
#         found_stock = search_stocks(stock_name)
#         stock_cache[stock_name] = {"name": stock_name, "code": found_stock["代码"][-6:], "exchange": found_stock["代码"][:2]}
# with open("stock_cache.json", 'w', encoding='utf-8') as file:
#     json.dump(stock_cache, file, indent=2, ensure_ascii=False)
    



#wb.save(filepath)


# from config import Config
# config = Config("config.json")
# xlsx_path = Path(config.xlsx_filename())
# backup_path = xlsx_path.with_stem(f"{xlsx_path.stem}_backup")
# print(backup_path)


# test_config = Config()
# test_dict = test_config.get_config()
# print(test_dict["文件名"])
# print(test_config.get_xlsx_filename())
# print(test_config.get_current_price_column())
# print(test_config.get_should_update_prices())
# print(type(test_config.get_should_update_prices()))


# from datetime import datetime, timedelta
# from time import sleep
## ==== Test timestamp file ====

# FORMAT = "%Y-%m-%d %H:%M:%S"
# now = datetime.now().strftime(FORMAT)
# sleep(5)
# now_read = datetime.strptime(now, FORMAT)
# diff = datetime.now() - now_read
# print(diff.seconds)
# print(diff.total_seconds())

# from timestamps import Timestamps

# timestamp = Timestamps(TIMESTAMP_LOG_PATH)
# print(timestamp.get_a_stocks_hour_diff())
    
# Any issue with writing with current time before attempting the call? - As long as this read write doesn't fail - should be fine - should be fine either way?

a_path = Path(r'C:\Users\MyPC\AppData\Local\Programs\Python\Python314\Lib\site-packages\akshare\file_fold\*')
print(a_path)
print(a_path.cwd())
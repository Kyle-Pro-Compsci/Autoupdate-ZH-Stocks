import sys
from config import Config
import openpyxl as pyxl
from pathlib import Path
import json
import stock_utils
from utils import setup_logger
from constants import CONFIG_PATH, CACHE_PATH, STOCK_LIB_PATH, TIMESTAMP_LOG_PATH
import logging
from time import sleep
import random
from timestamps import Timestamps


config = Config(CONFIG_PATH)

ENDCELLS = [
    "",
    "汇总",
    "合计",
    None
]

# Do it separately or include it in the main iteration and check for if the database was successfully queried? How to split? Maybe keep separate to avoid the sleep timer
def update_current_prices_group(wb: pyxl.Workbook, all_stocks, file_index):
    
    holdings_sheet = wb[config.sheet_name()]
    for row in holdings_sheet.iter_rows(min_row=config.starting_row(file_index)):
        price_cell = row[config.current_price_column(file_index) - 1]
        stock_name = row[config.stock_name_column(file_index) - 1].value
        
        if holdings_sheet.row_dimensions[price_cell.row].hidden:
            logging.debug(f"Skipping hidden row {price_cell.row}, stock name:{stock_name}")
            continue
        
        if stock_name is None or stock_name in ENDCELLS:
            logging.info("到达股票列表末尾") #Reached end of stock list.
            break
        try:
            found_stock = stock_utils.search_stocks(stock_name, all_stocks)
        except LookupError as e:
            logging.error(e)
            logging.info(f"未找到与 {stock_name} 匹配的股票") #Failed to find match for {stock_name}
            price_cell.value = "ERROR"
            continue
        except Exception as e:
            logging.error(e)
            logging.info(f"Unexpected error for {stock_name}")
            price_cell.value = "ERROR"
            continue
        
        #Update cache
        with open(CACHE_PATH, 'r', encoding='utf-8') as file:
            stock_cache = json.load(file)
        code = found_stock["代码"][-6:]
        exchange = found_stock["代码"][:2]
        logging.debug(f"Updating stock cache with {stock_name}, {code}, {exchange}")
        stock_cache[stock_name] = {"name": stock_name, "code": code, "exchange": exchange}
        stock_utils.update_stock_cache(CACHE_PATH, stock_cache)
        
        logging.info(f"{stock_name} 现价更新为{found_stock['最新价']}") #Updating stock with price {found_stock['最新价']}
        price_cell.value = found_stock['最新价']
        

def update_current_prices_individual(wb: pyxl.Workbook, file_index):
    logging.info("正在逐条更新股票现价")
    holdings_sheet = wb[config.sheet_name(file_index)]
    
    with open(CACHE_PATH, 'r', encoding='utf-8') as file:
        stock_cache = json.load(file)
    
    
    for row in holdings_sheet.iter_rows(min_row=config.starting_row(file_index)):
        name_cell = row[config.stock_name_column(file_index) - 1]
        stock_name = name_cell.value
        
        if holdings_sheet.row_dimensions[name_cell.row].hidden:
            logging.debug(f"Skipping hidden row {name_cell.row}, stock_name:{stock_name}")
            continue
        
        if stock_name is None or stock_name in ENDCELLS:
            logging.info("到达股票列表末尾") #Reached end of stock list.
            break
        
        if stock_name in stock_cache:
            code = stock_cache[stock_name]["code"]
            exchange = stock_cache[stock_name]["exchange"]
        else:
            try:
                with open(STOCK_LIB_PATH, "r", encoding='utf-8') as file:
                    all_stocks = json.load(file)
                found_stock = stock_utils.search_stocks(stock_name, all_stocks)
                code = found_stock["代码"][-6:]
                exchange = found_stock["代码"][:2]
                #update stock cache
                logging.debug(f"Updating stock cache with {stock_name}, {code}, {exchange}")
                stock_cache[stock_name] = {"name": stock_name, "code": code, "exchange": exchange}
                stock_utils.update_stock_cache(CACHE_PATH, stock_cache)
            except LookupError as e:
                logging.error(e)
                code = "ERROR"
            except Exception as e:
                logging.critical(f"Unexpected error when searching for stocks with {stock_name}")
                logging.critical(e)
                code = "ERROR"
            
        if code == "ERROR":
            price = "ERROR"
        else:
            price = stock_utils.get_price_from_code(code, exchange)
        row[config.current_price_column(file_index) - 1].value = price
        sleep(random.uniform(3,6))


def update_current_prices(wb: pyxl.Workbook, all_stocks, file_index):
    if all_stocks is not None:
        try:
            update_current_prices_group(wb, all_stocks, file_index)
        except Exception as e:
            logging.error(e)
            logging.info("批量查询失败")
            update_current_prices_individual(wb, file_index)
    else:
        update_current_prices_individual(wb, file_index)


def save_excel_workbook(wb: pyxl.Workbook, path):
    logging.info("正在更新文件") #Updating file
    try:
        wb.save(path)
    except PermissionError as e:
        logging.error("权限错误: 请确保xlsx文件可写入") #Permission error: make sure the xlsx file has write permissions
        logging.error(e)
        updated_filepath = path.with_stem(f"{path.stem}_更新")
        logging.info(f"正在保存至新文件: {updated_filepath}") #Saving to new file instead:
        wb.save(updated_filepath)
    except Exception as e:
        logging.error(e)
        logging.info("保存xlsx时发生未知错误 - 更新失败.") #Unknown error when saving xlsx - update failed.


def main():
    #Create and save backup of xlsx file before modifying?
    # Read excel file
    logging.info("开始。。。") # Starting...
    
    #TODO: Operating on multiple excel files, if successfully done a group query use it for all files
    
    timestamps = Timestamps(TIMESTAMP_LOG_PATH)
    
    all_stocks = None
    if config.should_update_prices():
        if timestamps.get_a_stocks_hour_diff() > 12:
            try:
                timestamps.set_a_stocks_time()
                all_stocks = stock_utils.query_all_a_stocks()
            except Exception as e:
                logging.error("获取所有的A股失败")
                pass
        else:
            logging.info(f"上一批量查询：{int(timestamps.get_a_stocks_hour_diff()*10)/10} 小时之前")
            logging.info("上次批量查询时间太近了")

    for index, file in enumerate(config.file_list()):
        xlsx_path = Path(config.xlsx_filename(index))
        logging.info(f"正在打开表格文件 {xlsx_path}") #Opening excel file
        wb = pyxl.open(xlsx_path, read_only=False)
    
        backup_path = xlsx_path.with_stem(f"{xlsx_path.stem}_备份")
        logging.info(f"正在将表格文件备份为 {backup_path}") # Backing up excel file as
        wb.save(backup_path)
    
        if config.should_update_prices():
            update_current_prices(wb, all_stocks, index) #TODO: THIS - update to use 
    
        save_excel_workbook(wb, xlsx_path)
    
    logging.info("完成.") #Execution finished.
    sleep(5)


if __name__ == "__main__":
    setup_logger()
    try:
        sys.exit(main())
    except Exception as e:
        logging.critical(e)
        sleep(10)
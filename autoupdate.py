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
def update_current_prices_group(wb: pyxl.Workbook):
    logging.info("Attempting to fetch all stocks")
    try:
        database_dict = stock_utils.query_all_a_stocks()
    except LookupError as e:
        logging.error(e)
        raise Exception(e)
    
    logging.info("Successfully queried all stocks")
    # If doesn't exit - create history/log json of last opened date, last time rate limited, etc.
    
    holdings_sheet = wb[config.holdings_sheet_name]
    for row in holdings_sheet.iter_rows(min_row=config.holdings_starting_row):
        price_cell = row[config.holdings_current_price_column - 1]
        
        if holdings_sheet.row_dimensions[price_cell.row].hidden:
            logging.debug(f"Skipping hidden row {stock_name.row} with value {stock_name}")
            continue
        
        stock_name = row[config.holdings_stock_name_column - 1].value
        if stock_name is None or stock_name in ENDCELLS:
            logging.info("Reached end of stock list.")
            break
        try:
            found_stock = stock_utils.search_stocks(stock_name, database_dict)
        except LookupError as e:
            logging.error(e)
            logging.info(f"Failed to find match for {stock_name}")
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
        
        logging.info(f"Updating stock {stock_name} with price {found_stock['最新价']}")
        price_cell.value = found_stock['最新价']
        

def update_current_prices_individual(wb: pyxl.Workbook):
    holdings_sheet = wb[config.holdings_sheet_name]
    
    with open(CACHE_PATH, 'r', encoding='utf-8') as file:
        stock_cache = json.load(file)
    
    
    for row in holdings_sheet.iter_rows(min_row=config.holdings_starting_row):
        stock_name = row[config.holdings_stock_name_column - 1].value
        
        if holdings_sheet.row_dimensions[stock_name.row].hidden:
            logging.debug(f"Skipping hidden row {stock_name.row} with value {stock_name}")
            continue
        
        if stock_name is None or stock_name in ENDCELLS:
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
        row [config.holdings_current_price_column - 1].value = price
        sleep(random.uniform(3,6))


def update_current_prices(wb: pyxl.Workbook):
    #Check if can do group - else do individual
    timestamps = Timestamps(TIMESTAMP_LOG_PATH)
    if timestamps.get_a_stocks_hour_diff() > 12:
        try:
            timestamps.set_a_stocks_time()
            logging.debug("Set current time for a_stocks")
            update_current_prices_group(wb)
        except Exception as e:
            logging.error(e)
            logging.info("Group query failed - attempting individual stock queries")
            update_current_prices_individual(wb)
    else:
        logging.info("Group query too recent")
        update_current_prices_individual(wb)


def main():
    #Create and save backup of xlsx file before modifying?
    # Read excel file
    logging.info("Starting...") #开始。。。
    xlsx_path = Path(config.xlsx_filename)
    logging.info(f"Opening excel file {xlsx_path}") #正在打开表格文件
    wb = pyxl.open(xlsx_path, read_only=False)
    
    backup_path = xlsx_path.with_stem(f"{xlsx_path.stem}_backup")
    logging.info(f"Backing up excel file as {backup_path}") #
    wb.save(backup_path)
    
    if config.should_update_prices:
        update_current_prices(wb)
    
    logging.info("Updating file")
    try:
        wb.save(xlsx_path)
    except PermissionError as e:
        logging.error("Permission error: make sure the xlsx file has write permissions")
        logging.error(e)
        updated_filepath = xlsx_path.with_stem(f"{xlsx_path.stem}_updated")
        logging.info(f"Saving to new file instead: {updated_filepath}")
        wb.save(updated_filepath)
    except Exception as e:
        logging.error(e)
        logging.info("Unknown error when saving xlsx - update failed.")
    logging.info("Execution finished.")


if __name__ == "__main__":
    setup_logger()
    try:
        sys.exit(main())
    except Exception as e:
        logging.critical(e)
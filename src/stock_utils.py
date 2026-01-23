import json
import akshare as ak
import logging
from constants import STOCK_LIB_PATH

def search_stocks(stock_name, json_data):
    matching_stocks = list(filter(lambda x: x["名称"] == stock_name, json_data))
    if len(matching_stocks) == 0:
        logging.error(f"未找到与股票名称 '{stock_name}' 匹配的股票.") #No matching stocks with stock name {} found.
        raise LookupError(f"No matching stocks with stock name {stock_name} found.")
    if len(matching_stocks) > 1:
        logging.error(f"More than one match for stock {stock_name} found")
        raise LookupError(f"More than one match for stock {stock_name} found")
    return matching_stocks[0]


def update_stock_cache(cache_path, new_stock_cache):
    with open(cache_path, 'w', encoding='utf-8') as file:
        json.dump(new_stock_cache, file, ensure_ascii=False)


def query_all_a_stocks():
    logging.info("正在获取所有的A股")
    df = ak.stock_zh_a_spot() #SinaFinance
    logging.info("获取成功")
    df.to_json(STOCK_LIB_PATH, orient='records', indent=2, force_ascii=False)
    return df.to_dict(orient='records')


def run_stock_individual_info_em(stock_code):
    logging.debug(f"Attempting to run ak.stock_individual_info_em({stock_code}, timeout=5)")
    result = ak.stock_individual_info_em(stock_code, timeout=5)
    stock_dict = result.set_index('item')['value'].to_dict() # result initially is a pd item value format
    logging.info(f"收到股票{stock_code}: {stock_dict['股票简称']}, 现价为{stock_dict['最新']}") #Received stock... and its current price
    price = stock_dict['最新']
    return price
    

def run_stock_individual_spot_xq(stock_code: str, exchange: str):
    logging.error("Running stock_individual_spot_xq instead.")
    logging.debug(f"Attempting to run ak.stock_individual_spot_xq({exchange.upper()}{stock_code}, timeout=5)")
    result = ak.stock_individual_spot_xq(f"{exchange.upper()}{stock_code}", timeout=5)
    stock_dict = result.set_index('item')['value'].to_dict()
    logging.info(f"收到股票{stock_code}: {stock_dict['名称']},现价为{stock_dict['现价']} from backup xq function")
    price = stock_dict['现价']
    return price


def get_price_from_code(stock_code:str, exchange:str):
    # Can try both methods - if error try the other
    try:
        price = run_stock_individual_info_em(stock_code)
    except Exception as e:
        logging.error("stock_individal_info_em error:")
        logging.error(e)
        try:
            price = run_stock_individual_spot_xq(stock_code, exchange)
        except Exception as e:
            logging.error("stock_individual_spot_xq error:")
            logging.error(e)
            logging.error(f"Stock code: {stock_code} failed.")
            price = '失败'
    return price
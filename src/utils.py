from constants import CONFIG_PATH
from config import Config
import logging
import datetime
config = Config(CONFIG_PATH)

def log(text):
    if config.verbose:
        print(text)
        
def test_print(text):
    print(text)
    
def setup_logger():
    LOG_NAME = 'history.log'
    
    with open(LOG_NAME, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Run started at: {datetime.datetime.now()}\n")
        f.write(f"{'='*60}\n\n")
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG) # root logger filters out logs before it's sent to the handlers - set to lowest level
    
    console_handler = logging.StreamHandler()
    if config.verbose:
        console_handler.setLevel(logging.INFO)
    else:
        console_handler.setLevel(logging.WARNING)
        
    file_handler = logging.FileHandler(LOG_NAME, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    console_formatter = logging.Formatter('%(message)s')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)
    
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
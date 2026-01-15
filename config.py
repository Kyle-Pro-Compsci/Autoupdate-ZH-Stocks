from pathlib import Path
import json

class Config:
    
    default_values = {
        "文件名": "短线记录.xlsx",
        "表名称": "持仓总表", 
        "价格列": 3,
        "起始行": 2,

        "重新价格": True
    }
    
    def __init__(self, path = "config.json"):
        self.config_path = path
        self.config_values = self.load_config(path)

    
    def load_config(self, config_path):
        if not Path(config_path).exists():
            return self.default_values
        else:
            with open(Path(config_path), 'r', encoding='utf-8') as f:
                return json.load(f)
            
    def get_config(self):
        return self.config_values
    
    @property
    def xlsx_filename(self):
        return self.config_values["文件名"]
    
    @property
    def holdings_sheet_name(self):
        return self.config_values["持仓表名称"]
    
    @property
    def holdings_current_price_column(self):
        return self.config_values["持仓表_价格列"]
    
    @property
    def holdings_stock_name_column(self):
        return self.config_values["持仓表_股票名称列"]
    
    @property
    def holdings_starting_row(self):
        return self.config_values["持仓表_起始行"]
    
    @property
    def should_update_prices(self):
        return self.config_values["重新价格"]
    
    @property
    def verbose(self):
        return self.config_values["说明模式"]
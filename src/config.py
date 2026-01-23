from pathlib import Path
import json

# TODO: Update to singleton pattern when implemented GUI and editable config data
class Config:
    
    default_values = {
    "文件列表":
        [
            {
            "文件名": "短线记录2.xlsx",
            "目标工作表名称": "持仓总表",
            "价格列": 7,
            "股票名称列": 2,
            "起始行": 3
            },
            {
            "文件名": "1月19日 持 仓 汇 总.xlsx",
            "目标工作表名称": "公司持仓汇总表",
            "价格列": 7,
            "股票名称列": 2,
            "起始行": 3
            }
        ],
        "重新价格": True,
        "说明模式": True
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
    
    def file_count(self):
        return len(self.config_values["文件列表"])
    
    def file_list(self):
        return self.config_values["文件列表"]
    
    def xlsx_filename(self, file_index: int):
        return self.config_values["文件列表"][file_index]["文件名"]
    
    def sheet_name(self, file_index: int):
        return self.config_values["文件列表"][file_index]["目标工作表名称"]
    
    def current_price_column(self, file_index: int):
        return self.config_values["文件列表"][file_index]["现价列"]
    
    def stock_name_column(self, file_index: int):
        return self.config_values["文件列表"][file_index]["股票名称列"]
    
    def starting_row(self, file_index: int):
        return self.config_values["文件列表"][file_index]["起始行"]
    
    def should_update_prices(self):
        return self.config_values["重新价格"]
    
    def verbose(self):
        return self.config_values["说明模式"]
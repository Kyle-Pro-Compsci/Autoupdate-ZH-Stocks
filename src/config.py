from pathlib import Path
import json
import copy

# Used in 
class Config:
    config_values = None

    def __init__(self, data_dict):
        self.config_values = data_dict
    
    def load_config(self):
        config_path = Path("config.json")
        self.path = config_path
        if not config_path.exists():
            print(f"Path {config_path} does not exist, using blank")
            self.config_values = self.blank_config()
        else:
            with open(Path(config_path), 'r', encoding='utf-8') as f:
                self.config_values = json.load(f)
    
    def save_config(self):
        with open(Path("config.json"), 'w', encoding='utf-8') as f:
            json.dump(self.get_config(), f, ensure_ascii=False, indent=2)
            
    def add_file(self, file_dict):
        self.file_list().append(file_dict)
    
    def delete_file(self, index):
        if index >= len(self.file_list()):
            print("Out of bounds just go crash ig")
        self.file_list().pop(index)
        
    # ==== GETTERS ====
    def get_config(self):
        return self.config_values
    
    def file_count(self) -> int:
        return len(self.config_values["文件列表"])
    
    def file_list(self) -> list:
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
    
    def should_update_prices(self) -> bool:
        return self.config_values["重新价格"]
    
    def verbose(self) -> bool:
        return self.config_values["说明模式"]
    
    # ====Setters====
    
    def set_verbose(self, new_value: bool):
        self.config_values["说明模式"] = new_value 
    
    def set_should_update_prices(self, new_value:bool): 
        self.config_values["重新价格"] = new_value
            
    def set_file_value(self, index, key, new_value):
        self.file_list()[index][key] = new_value
        
    # ====Other====
    def blank_file(self):
        blank_values = {
            "文件名": "Untitled",
            "目标工作表名称": "",
            "价格列": 0,
            "股票名称列": 0,
            "起始行": 0
        }
        return blank_values
    
    def blank_config(self):
        return {
            "文件列表": [self.blank_file()],
            "重新价格": True,
            "说明模式": True
        }
        
    def deep_copy(self):
        return copy.deepcopy(self.config_values)
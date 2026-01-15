import json
from datetime import datetime
import logging

class Timestamps:
    TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
    FORMAT_KEY = 'read_format'
    A_STOCKS_KEY = 'a_stocks_recent_call'
    
    DEFAULT_JSON = {FORMAT_KEY : TIMESTAMP_FORMAT}
    
    def __init__(self, path = "timestamps_log.json"):
        self.path = path
        self.timestamps_json = self.DEFAULT_JSON
        try:    
            with open(path, "r", encoding='utf-8') as file:
                try:
                    self.timestamps_json = json.load(file)
                except json.decoder.JSONDecodeError:
                    return
            # have a READ_FORMAT in the json dict
        except FileNotFoundError as e:
            logging.debug("No timestamp file found - creating a new one")
            with open(path, "w", encoding='utf-8') as file:
                json.dump(self.DEFAULT_JSON, file, indent=2, ensure_ascii=False)
                return
    
    
    def _update_json_file(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(self.timestamps_json, file, indent=2, ensure_ascii=False)
    
    
    def set_a_stocks_time(self):
        self.timestamps_json[self.A_STOCKS_KEY] = datetime.now().strftime(self.TIMESTAMP_FORMAT)
        self.timestamps_json[self.FORMAT_KEY] = self.TIMESTAMP_FORMAT
        self._update_json_file()
        
    
    def get_a_stocks_hour_diff(self):
        if self.FORMAT_KEY in self.timestamps_json:
            format = self.timestamps_json[self.FORMAT_KEY]
        else:
            format = self.TIMESTAMP_FORMAT
        
        if self.A_STOCKS_KEY in self.timestamps_json:
            try:
                old_time = datetime.strptime(self.timestamps_json[self.A_STOCKS_KEY], format)
            except Exception as e:
                logging.critical("Error with getting datetime from json - check format")
                logging.critical(e)
                return 0
            diff = datetime.now() - old_time
            return diff.total_seconds() / 3600
        else:
            return 500
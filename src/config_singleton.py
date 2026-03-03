from pathlib import Path
from config import Config

#Used in the GUI during editing
class ConfigSingleton(Config):
    _instance = None
    
    def __new__(cls): # cls is Config
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        
        return cls._instance

    def __init__(self):
        if self._instance is None:
            super().__init__(self.config_values)
    
    def create_instance(self):
        return Config(self.deep_copy())
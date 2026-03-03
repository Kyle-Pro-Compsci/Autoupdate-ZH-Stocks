from PySide6.QtCore import QObject, Signal, Slot
from autoupdate import Autoupdater
from config import Config
from time import sleep

class ProcessWorker(QObject):
    started = Signal()
    finished = Signal()
    error = Signal(str)
    
    config = None
    
    def set_config(self, config: Config):
        self.config = config
    
    @Slot(dict)
    def run_worker_process(self):
        if self.config is None:
                print("ProcessWorker: config is still None")
                self.error.emit("No config sent")
                return
        self.started.emit()
        try:
            autoupdater = Autoupdater(self.config)
            autoupdater.run()
        except Exception as e:
            print(f"Hit exception {e}")
            self.error.emit(str(e))
        self.finished.emit()
        
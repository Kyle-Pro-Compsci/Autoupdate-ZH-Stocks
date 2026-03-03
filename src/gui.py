import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Slot, QThread
from gui_modules.tab_manager import TabManager
from config_singleton import ConfigSingleton
from gui_modules.worker import ProcessWorker

class WindowInterior(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigSingleton()
        
        layout = QVBoxLayout()
        tab_bar = TabManager(self)
        layout.addWidget(tab_bar)
        self.setLayout(layout)
        
        bottom_section = QWidget()
        bottom_layout = QVBoxLayout()
        bottom_section.setContentsMargins(10, 5, 10, 5)
        layout.addWidget(bottom_section)
        bottom_section.setLayout(bottom_layout)
        
        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start_pressed)
        
        self.bottom_message = QLabel("")
        bottom_layout.addWidget(self.start_button)
        bottom_layout.addWidget(self.bottom_message)
        
        self.setWindowTitle("TestGUI")
        self.setMinimumSize(700, 500)
    
    def run_process(self):
        # Disable button
        self.start_button.setEnabled(False)
        
        self.thread = QThread()
        self.worker = ProcessWorker()
        self.worker.set_config(self.config.create_instance())
        
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run_worker_process)
        
        self.worker.started.connect(self.set_started_message)
        self.worker.finished.connect(lambda: self.start_button.setEnabled(True))
        self.worker.finished.connect(self.set_finished_message)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.worker.error.connect(self.set_error_message)
        
        self.thread.start()
    
    @Slot()
    def start_pressed(self):
        self.run_process()
        
    @Slot(str)
    def set_error_message(self, error):
        self.bottom_message.setText(error)
        self.bottom_message.setStyleSheet("color: red")
        
    @Slot(str)
    def set_started_message(self):
        self.bottom_message.setText("Processing...")
        self.bottom_message.setStyleSheet("color: orange")
        
    @Slot()
    def set_finished_message(self):
        self.bottom_message.setText("Process successfully completed")
        self.bottom_message.setStyleSheet("color: green") 
               

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Autoupdate")
        
        window_interior = WindowInterior(self)
        self.setCentralWidget(window_interior)
        

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    main_window = MainWindow()
    main_window.show()
    # Run the main Qt loop
    sys.exit(app.exec())
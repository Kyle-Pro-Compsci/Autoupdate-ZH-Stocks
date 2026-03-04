from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QPushButton
from PySide6.QtCore import Slot, Qt
from config_singleton import ConfigSingleton

class HomeTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigSingleton()
        
        layout = QVBoxLayout()
        
        row_section = QWidget()
        row_section_layout = QFormLayout()
        
        #UPDATE PRICE ROW
        price_checkbox = QCheckBox()
        price_checkbox.setChecked(self.config.should_update_prices())
        price_checkbox.checkStateChanged.connect(self.price_checkbox_pressed)
        row_section_layout.addRow("重新价格", price_checkbox)
        
        verbose_checkbox = QCheckBox()
        verbose_checkbox.setChecked(self.config.verbose())
        verbose_checkbox.checkStateChanged.connect(self.verbose_checkbox_pressed)
        row_section_layout.addRow("说明模式", verbose_checkbox)
        row_section.setLayout(row_section_layout)
        
        layout.addWidget(row_section)
        
        save_button = QPushButton("保存") #配置文件
        save_button.clicked.connect(self.save_pressed)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
        
    @Slot(Qt.CheckState)
    def price_checkbox_pressed(self, new_state):
        if new_state is Qt.CheckState.Checked:
            print("price checked")
            state_bool = True
        elif new_state is Qt.CheckState.Unchecked:
            print("price unchecked")
            state_bool = False
        elif new_state is Qt.CheckState.PartiallyChecked:
            print("HUH??? Partially checked???")
            state_bool = True
        self.config.set_should_update_prices(state_bool)
    
    @Slot(Qt.CheckState)
    def verbose_checkbox_pressed(self, new_state):
        if new_state is Qt.CheckState.Checked:
            print("verbose checked")
            state_bool = True
        elif new_state is Qt.CheckState.Unchecked:
            print("verbose unchecked")
            state_bool = False
        elif new_state is Qt.CheckState.PartiallyChecked:
            print("HUH??? Partially checked???")
            state_bool = True
        self.config.set_verbose(state_bool)
                 
    @Slot()
    def save_pressed(self):
        self.config.save_config()
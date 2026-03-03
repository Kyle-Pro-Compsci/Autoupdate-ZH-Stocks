from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QSpinBox, QCheckBox, QTabBar
from PySide6.QtCore import Slot, Qt
from config_singleton import ConfigSingleton
from gui_modules.gui_constants import PREFIX_TAB_COUNT

NAME_KEY = "文件名"

class FileTab(QWidget):
    def __init__(self, file_info, index, parent:QTabBar):
        super().__init__(parent)
        self.config = ConfigSingleton()
        self.index = index
        self.parent_tab_bar = parent
        self.name = "Untitled"
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
        for key in file_info.keys():
            if key == NAME_KEY:
                self.name = file_info[key]
            self.add_row(key, file_info[key])
    
    
    def add_row(self, key, data):
        if isinstance(data, str):
            line = QLineEdit(data)
            # line.textEdited.connect(lambda text: self.line_edited(text, key))
            line.editingFinished.connect(lambda: self.line_edited(line.text(), key)) # SHOULD be ok - double check if edit went through
            self.layout.addRow(key, line)
        if isinstance(data, int):
            spinbox = QSpinBox(value=data, minimum=0)
            spinbox.editingFinished.connect(lambda: self.spinbox_edited(spinbox.value(), key))
            self.layout.addRow(key, spinbox)
        if isinstance(data, bool):
            checkbox = QCheckBox()
            checkbox.setChecked(data)
            checkbox.checkStateChanged.connect(lambda state: self.checkbox_edited(state, key))
            self.layout.addRow(key, checkbox)
        #else treat as string maybe?
        
    def set_new_index(self, index):
        # print(f"Setting index from {self.index} to {index}")
        self.index = index
    
    def get_name(self):
        return self.name
    
    def set_name_in_parent(self):
        # print(f"Setting name in parent for index {self.index + 1}, and name {self.name}")
        self.parent_tab_bar.setTabText(self.index + PREFIX_TAB_COUNT, self.name)
        
    @Slot() #str for textEdited
    def line_edited(self, new_text, key):
        # print(f"{key}: {new_text}")
        if key == NAME_KEY:
            self.name = new_text
            # self.parent_tab_bar.setTabText(self.parent_tab_bar.currentIndex(), new_text)
            self.set_name_in_parent()
        # print(f"Current index of line editing: {self.index}")
        self.config.set_file_value(self.index, key, new_text)
    
    @Slot()
    def spinbox_edited(self, new_num, key):
        # print(f"{key}: {new_num}")
        self.config.set_file_value(self.index, key, new_num)
    
    @Slot()
    def checkbox_edited(self, new_state: Qt.CheckSate, key):
        if new_state is Qt.CheckState.Checked:
            state_bool = True
        elif new_state is Qt.CheckState.Unchecked:
            state_bool = False
        elif new_state is Qt.CheckState.PartiallyChecked:
            print("HUH??? Partially checked???")
        self.config.set_file_value(self.index, key, state_bool)
        # print(f"{key}: {state_bool}")
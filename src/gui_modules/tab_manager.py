from PySide6.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QTabBar
from PySide6.QtCore import Slot, Qt
from config_singleton import ConfigSingleton
from gui_modules.home_tab import HomeTab
from gui_modules.file_tab import FileTab
from gui_modules.gui_constants import PREFIX_TAB_COUNT


class TabManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0 ,0)
        tabs = TabSection(self)
        layout.addWidget(tabs)
        
        self.setLayout(layout)
        

class TabSection(QTabWidget):
    def __init__(self, parent:TabManager=None):
        super().__init__(parent)
        self.config = ConfigSingleton()
        self.tab_manager_parent = parent
        
        add_tab_button = QPushButton("+")
        add_tab_button.clicked.connect(self.on_add_tab_pressed)
        self.setCornerWidget(add_tab_button, Qt.Corner.TopRightCorner)
        
        self.home_tab = self.set_home_tab()        
        self.tabBar().setTabsClosable(True)
        self.addTab(self.home_tab, "Home")
        self.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
        self.tabBar().setTabTextColor(0, "darkGreen")
        
        self.tabCloseRequested.connect(self.close_tab)
        self.tabBar().tabCloseRequested.connect(self.close_tab)
        
        self.file_tabs = [] # PLAN: indexes in this list and in config should automatically match - no need to track separately
        
        # Prefill config pages
        for index, file_info in enumerate(self.config.file_list()):
            file_tab = FileTab(file_info, index, parent=self)
            self.file_tabs.append(file_tab)
            self.addTab(file_tab, file_tab.get_name())
                
        
    @Slot(None)
    def on_add_tab_pressed(self):
        self.add_blank_file_tab()
    
    
    def add_blank_file_tab(self): #TODO
        new_file = self.config.blank_file()
        file_tab = FileTab(new_file, len(self.file_tabs), parent=self)
        self.file_tabs.append(file_tab)
        self.addTab(file_tab, "new tab")
        #Edit config
        self.config.add_file(new_file)
        
        
    @Slot(int)
    def close_tab(self, index):
        # Home tab should be non closable
        if index < PREFIX_TAB_COUNT:
           print("Panic - trying to close non file tabs") 
        
        self.removeTab(index)
        self.config.delete_file(index - PREFIX_TAB_COUNT)
        self.file_tabs.pop(index - PREFIX_TAB_COUNT)
        for index, tab in enumerate(self.file_tabs):
            tab.set_new_index(index)
    
    def set_home_tab(self):
        return HomeTab()
    
from ctypes.wintypes import HBITMAP
from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget,QTabWidget,QFormLayout,QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox, QComboBox,
    QListWidget,QListWidgetItem, QScrollBar, QMessageBox, QTreeView
)
from PyQt6.QtCore import Qt

from views.passwordReqTab import PasswordReqTab
from views.changePasswordTab import ChangePasswordTab
from views.changeSudoers import ChangeSudoers
from views.iptablesTab import IPTables
from views.ServicesTab import DisableServices



class HardenPage(QWidget):
    
    def __init__(self):
        super(HardenPage,self).__init__()
        
        # Layout
        self.layout = QGridLayout(self)

        # Scrollbar
        list_widget = QListWidget()
        list_widget.setMaximumWidth(180)

        # Scrollbar List
        passReqTab = QListWidgetItem("Password Requirements")
        changePassTab = QListWidgetItem("Change Password")
        changeSudoers = QListWidgetItem("Change Sudoers")
        disableServices = QListWidgetItem("Disable Services")
        iptables = QListWidgetItem("IPTables")
        self.current_tab = PasswordReqTab()

        list_widget.addItem(passReqTab)
        list_widget.addItem(changePassTab)
        list_widget.addItem(changeSudoers)
        list_widget.addItem(disableServices)
        list_widget.addItem(iptables)
        list_widget.itemClicked.connect(self.change_tab)
        
        # Scrollbar formatting
        scroll_bar = QScrollBar(self)
        list_widget.setVerticalScrollBar(scroll_bar)
        self.layout.addWidget(list_widget, 0, 0)
        self.layout.addWidget(self.current_tab, 0, 1)

        self.setLayout(self.layout)
    
    # Function for changing between different menus
    def change_tab(self, item):
        self.current_tab.close()
        match item.text():
            case "Password Requirements":                
                self.current_tab = PasswordReqTab()
            case "Change Password":
                self.current_tab = ChangePasswordTab()                
            case "Change Sudoers":                
                self.current_tab = ChangeSudoers()                
            case "Disable Services":                
                self.current_tab = DisableServices()                
            case "IPTables":                
                self.current_tab = IPTables()                
        self.layout.addWidget(self.current_tab, 0, 1)

#TODO Add better Styling to password requirements
# - Better Text Area
# - Smaller Buttons
# - Closer labels
#





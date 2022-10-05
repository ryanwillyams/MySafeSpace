from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget,QTabWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox,
    QListWidget,QListWidgetItem, QScrollBar
)
from PyQt6.QtCore import Qt

# TODO Find a way to import this function outside of this file
import sys 
sys.path.append("..")
from functions import listUsers
from passwdReq import passwdExpirConfig, passwdReqs
from change_passwds import passwdChange

"""
Options for harden tab
1. Change password requirements
2. Change password for user(s)
3. Change sudoers
4. Configure SSH
5. Disable services
6. View logs

"""
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


class PasswordReqTab(QWidget):
    def __init__(self):
        super(PasswordReqTab,self).__init__()
        main_layout = QGridLayout(self)
        
        ##
        # Maximum days before password change
        self.max_day_label = QLabel('&Maximum number of days before changing password', self)
        self.max_day = QSpinBox(self)
        self.max_day_label.setBuddy(self.max_day)

        self.max_day.setRange(1,99999)
        self.max_day.setMaximumSize(80,32)
        self.max_day.setValue(90)

        main_layout.addWidget(self.max_day_label, 0, 0)
        main_layout.addWidget(self.max_day, 0, 1)

        #Minimum days before password change
        self.min_day_label = QLabel('&Minimum number of days before changing password', self)
        self.min_day = QSpinBox(self)
        self.min_day_label.setBuddy(self.min_day)

        self.min_day.setRange(1,99999)
        self.min_day.setMaximumSize(80,32)
        self.min_day.setValue(30)

        main_layout.addWidget(self.min_day_label, 1, 0)
        main_layout.addWidget(self.min_day, 1, 1)

        # Warning before password change
        self.warning_label = QLabel('&Number of days before warning is given to change passsword', self)
        self.warning = QSpinBox(self)
        self.warning_label.setBuddy(self.warning)

        self.warning.setRange(1,31)
        self.warning.setMaximumSize(48,32)
        self.warning.setValue(7)

        main_layout.addWidget(self.warning_label, 2, 0)
        main_layout.addWidget(self.warning, 2, 1)
        
        #Initalize Minimum Characters
        self.minCharLabel = QLabel('&Minimum password length', self)
        self.min_chars = QSpinBox(self)
        self.minCharLabel.setBuddy(self.min_chars)

        self.min_chars.setRange(4,32)
        self.min_chars.setMaximumSize(48,32)
        self.min_chars.setValue(12)

        main_layout.addWidget(self.minCharLabel, 3, 0)
        main_layout.addWidget(self.min_chars, 3, 1)

        # Initalize Password History
        self.passHist = QLabel('Number of previous passwords remembered', self)
        self.pass_remember = QSpinBox(self)
        self.passHist.setBuddy(self.pass_remember)

        self.pass_remember.setRange(1,10)
        self.pass_remember.setMaximumSize(48,32)
        self.pass_remember.setValue(5)

        main_layout.addWidget(self.passHist, 4, 0)
        main_layout.addWidget(self.pass_remember, 4, 1)

        ##
        # Intialize Checked buttons
        self.check_buttons = []
        self.need_upper_case = QCheckBox("Upper Case")
        self.need_lower_case = QCheckBox("Lower Case")
        self.need_digits = QCheckBox("Digits")
        self.need_special_chars = QCheckBox("Special Characters")
        
        self.check_buttons.append(self.need_upper_case)
        self.check_buttons.append(self.need_lower_case)
        self.check_buttons.append(self.need_digits)
        self.check_buttons.append(self.need_special_chars)

        self.need_upper_case.setChecked(True)
        self.need_lower_case.setChecked(True)
        self.need_digits.setChecked(True)
        self.need_special_chars.setChecked(True)

        index = 5
        for button in self.check_buttons:
            main_layout.addWidget(button, index, 0)
            index += 1
        ##
        # Initialize Buttons
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear")
        self.submit_button = QPushButton("Submit", clicked=self.submit_password_req_changes)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)

        bottom_buttons = QWidget()
        bottom_buttons.setLayout(button_layout)
        
        main_layout.addWidget(bottom_buttons)
        self.setLayout(main_layout)

    def submit_password_req_changes(self):
        # Update password requirements config file '/etc/pam.d/common-password'
        passwdReqs(self.min_chars.text(), self.need_upper_case.isChecked(), 
                   self.need_lower_case.isChecked(), self.need_digits.isChecked(),
                   self.need_special_chars.isChecked(), self.pass_remember.text())
        
        # Update password expiration config file '/etc/login.defs'
        passwdExpirConfig(self.max_day.text(), self.min_day.text(), self.warning.text())

CHANGE_PASSWORD_STYLE = """

"""
class ChangePasswordTab(QWidget):
    def __init__(self):
        super(ChangePasswordTab,self).__init__()

        # Layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title
        title_card = QLabel("Choose Users to reset password")
        main_layout.addWidget(title_card)

        # List all normal users on device
        self.user_list_display = QListWidget()
        main_layout.addWidget(self.user_list_display)

        # Text box for new password
        self.newPasswdLabel = QLabel("New password: ")
        main_layout.addWidget(self.newPasswdLabel)
        self.newPasswd = QLineEdit(self)
        main_layout.addWidget(self.newPasswd)

        # Submit buttom
        self.submit_button = QPushButton("Submit", clicked=self.changeCheckedUsers)
        main_layout.addWidget(self.submit_button)
        self.setLayout(main_layout)

        # Retrieve list of users
        users_list = listUsers()
        for user in users_list:
            item = QListWidgetItem(user)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.user_list_display.addItem(item)

    # Function to change selected users
    def changeCheckedUsers(self):
        checkedUsers = []
        for index in range(self.user_list_display.count()):
            if self.user_list_display.item(index).checkState() == Qt.CheckState.Checked:
                checkedUsers.append(self.user_list_display.item(index).text())

        passwdChange(self.newPasswd.text(), checkedUsers)

class ChangeSudoers(QWidget):
    def __init__(self):
        super(ChangeSudoers,self).__init__()

class DisableServices(QWidget):
    def __init__(self):
        super(DisableServices,self).__init__()

class IPTables(QWidget):
    def __init__(self):
        super(IPTables,self).__init__()
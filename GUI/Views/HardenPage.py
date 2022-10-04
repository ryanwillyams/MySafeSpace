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
from passwdReq import passwdReqs
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
        
        layout = QVBoxLayout()

        tabs = QTabWidget()
        # list_widget = QListWidget()
        # list_widget.setGeometry()
        tabs.setTabPosition(QTabWidget.TabPosition.West)

        # Initialize tabs
        passReqTab = PasswordReqTab()
        changePassTab = ChangePasswordTab()
        changeSudoers = ChangeSudoers()
        disableServices = DisableServices()
        iptables = IPTables()
        # passReqTab = QListWidgetItem("Password Requirements")
        # changePassTab = QListWidgetItem("Change Password")
        # changeSudoers = QListWidgetItem("Change Sudoers")
        # disableServices = QListWidgetItem("Disable Services")
        # iptables = QListWidgetItem("IPTables")


        tabs.addTab(passReqTab,"Password Requirements")
        tabs.addTab(changePassTab,"Change Password")
        tabs.addTab(changeSudoers, "Change Sudoers")
        tabs.addTab(disableServices, "Disable Services")
        tabs.addTab(iptables, "IPTables")
        # list_widget.addItem(passReqTab)
        # list_widget.addItem(changePassTab)
        # list_widget.addItem(changeSudoers)
        # list_widget.addItem(disableServices)
        # list_widget.addItem(iptables)
        # list_widget.itemClicked.connect(PasswordReqTab.__init__)
        
        layout.addWidget(tabs)
        # scroll_bar = QScrollBar(self)
        # list_widget.setVerticalScrollBar(scroll_bar)
        # layout.addWidget(list_widget)

        self.setLayout(layout)

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
        #Initalize Minimum Characters
        self.minCharLabel = QLabel('&Minimum password length', self)
        self.min_chars = QSpinBox(self)
        self.minCharLabel.setBuddy(self.min_chars)

        self.min_chars.setRange(4,32)
        self.min_chars.setMaximumSize(64,32)

        main_layout.addWidget(self.minCharLabel, 0, 0)
        main_layout.addWidget(self.min_chars, 0, 1)

        # Initalize Password History
        self.passHist = QLabel('Number of previous passwords remembered', self)
        self.pass_remember = QSpinBox(self)
        self.passHist.setBuddy(self.pass_remember)

        self.pass_remember.setRange(1,32)
        self.pass_remember.setMaximumSize(64,32)

        main_layout.addWidget(self.passHist, 1, 0)
        main_layout.addWidget(self.pass_remember, 1, 1)

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

        index = 2
        for button in self.check_buttons:
            button.stateChanged.connect(self.is_text_area_valid)
            main_layout.addWidget(button, index, 0)
            index += 1
        ##
        # Initialize Buttons
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear")
        self.submit_button = QPushButton("Submit")

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)

        bottom_buttons = QWidget()
        bottom_buttons.setLayout(button_layout)
        
        main_layout.addWidget(bottom_buttons)
        self.setLayout(main_layout)

        self.submit_button.clicked.connect(lambda: passwdReqs(self.min_chars.text(), 
                    self.need_upper_case.isChecked(), self.need_lower_case.isChecked(), 
                    self.need_digits.isChecked(), self.need_special_chars.isChecked(), 
                    self.pass_remember.text()))
    

    def text_was_edited(self):
        
        self.current_password_text = self.main_text_edit_area.text()
        # print(self.current_password_text)


    def is_text_area_valid(self):
        # Check checkboxes
        print("Checking Text")
        states = [button for button in self.check_buttons if button == Qt.CheckState.Checked]

    def clear_button(self):
        pass

    def submit_button(self):
        # TODO add the submit button
        pass

    
        

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
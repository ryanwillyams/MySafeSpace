from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget,QTabWidget,QFormLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox,
    QListWidget,QListWidgetItem
)
from PyQt6.QtCore import Qt

# TODO Find a way to import this function outside of this file
import sys 
sys.path.append("..") 

from functions import listUsers
from passwdReq import passwdReqs

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
        tabs.setTabPosition(QTabWidget.TabPosition.West)

        # Initialize tabs
        passReqTab = PasswordReqTab()
        changePassTab = ChangePasswordTab()
        changeSudoers = ChangeSudoers()


        tabs.addTab(passReqTab,"Password Requirements")
        tabs.addTab(changePassTab,"Change Password")
        tabs.addTab(changeSudoers, "Change Sudoers")
        
        layout.addWidget(tabs)
        self.setLayout(layout)

#TODO Add better Styling to password requirements
# - Better Text Area
# - Smaller Buttons
# - Closer labels
#


class PasswordReqTab(QWidget):
    def __init__(self):
        super(PasswordReqTab,self).__init__()
        main_layout = QFormLayout()
        
        title_label = QLabel('Set Password Requirements Here')
        # title_label.setProperty("Title_Font_Size",True)
        # title_label.setFont(title_font_size)

        # Adjust font size of Label
        # Yes this is the best way to do it
        tlf = title_label.font()
        tlf.setPointSize(30)
        title_label.setFont(tlf)
        
        title_label.setFixedHeight(40)
        main_layout.addWidget(title_label)
        
        
        
        # ##
        # # Initialize Text Area
        # label_text_edit = QLabel('Try your password here')
        # self.current_password_text = ''

        # self.main_text_edit_area = QLineEdit()
        # self.main_text_edit_area.textChanged.connect(self.text_was_edited)
        # main_layout.addWidget(label_text_edit)
        # main_layout.addWidget(self.main_text_edit_area)
        
        ##
        #Initalize Minimum Characters
        
        self.min_chars = QSpinBox()
        self.min_chars.setRange(4,32)
        self.min_chars.setMaximumSize(64,32)
        main_layout.addWidget(self.min_chars)

        self.pass_remember = QSpinBox()
        self.pass_remember.setRange(1,32)
        self.pass_remember.setMaximumSize(64,32)
        main_layout.addWidget(self.pass_remember)

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

        for button in self.check_buttons:
            button.stateChanged.connect(self.is_text_area_valid)
            main_layout.addWidget(button)

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

        ##
        # Initialize button connections
        self.clear_button.clicked.connect(self.clear_button_action)
        self.submit_button.clicked.connect(self.submit_button_action)
    

    def text_was_edited(self):
        self.current_password_text = self.main_text_edit_area.text()
        # print(self.current_password_text)


    def is_text_area_valid(self):
        # Check checkboxes
        print("Checking Text")
        states = [button for button in self.check_buttons if button.isChecked()]

    def clear_button_action(self):
        for button in self.check_buttons:
            button.setCheckState(Qt.CheckState.Unchecked)

    def submit_button_action(self):
        passwdReqs(self.min_chars.text(), 
                    self.need_upper_case.isChecked(), self.need_lower_case.isChecked(), 
                    self.need_digits.isChecked(), self.need_special_chars.isChecked(), 
                    self.pass_remember.text())


class ChangePasswordTab(QWidget):
    def __init__(self):
        super(ChangePasswordTab,self).__init__()
        main_layout = QVBoxLayout()
        
        title_card = QLabel("Choose Users to reset password")

        main_layout.addWidget(title_card)
        self.user_list_display = QListWidget()

        users_list = listUsers()
        check_box_users = []

        for user in users_list:
            check_box_users.append(QListWidgetItem(user))
            check_box_users[-1].setCheckState(Qt.CheckState.Unchecked)
            self.user_list_display.addItem(check_box_users[-1])


        main_layout.addWidget(self.user_list_display)
        self.submit_button = QPushButton("Submit")
        main_layout.addWidget(self.submit_button)
        self.setLayout(main_layout)


class ChangeSudoers(QWidget):
    def __init__(self):
        super(ChangeSudoers,self).__init__()

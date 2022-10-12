from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget,QTabWidget,QFormLayout,QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox, QComboBox,
    QListWidget,QListWidgetItem, QScrollBar, QMessageBox
)
from PyQt6.QtCore import Qt

from scripts.passwdReq import passwdExpirConfig, passwdReqs

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

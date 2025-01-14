
from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt

from scripts.passwdReq import (getMaxDays, getMinDays, getWarnDays, 
        getMinPasswdLen, getPasswdsRemember, getReqUpper, getReqLower, 
        getReqDigit, getReqOther, writeToCommon_Password, changeMaxDays,
        changeMinDays, changeWarnDays, fetchRequirements)


class PasswordReqTab(QWidget):
    def __init__(self):
        super(PasswordReqTab, self).__init__()
        # Declare layouts
        outer_layout = QVBoxLayout()
        top_layout = QFormLayout()
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Define Top layout
        fetchRequirements()

        self.max_day = QSpinBox(self)
        self.max_day.setRange(1, 99999)
        self.max_day.setMaximumSize(80, 32)
        self.max_day.setValue(getMaxDays())

        self.min_day = QSpinBox(self)
        self.min_day.setRange(1, 99999)
        self.min_day.setMaximumSize(80, 32)
        self.min_day.setValue(getMinDays())

        self.warning = QSpinBox(self)
        self.warning.setRange(1, 31)
        self.warning.setMaximumSize(48, 32)
        self.warning.setValue(getWarnDays())

        self.min_chars = QSpinBox(self)
        self.min_chars.setRange(4, 32)
        self.min_chars.setMaximumSize(48, 32)
        self.min_chars.setValue(getMinPasswdLen())

        self.pass_remember = QSpinBox(self)
        self.pass_remember.setRange(1, 10)
        self.pass_remember.setMaximumSize(48, 32)
        self.pass_remember.setValue(getPasswdsRemember())

        self.need_upper_case = QCheckBox("Upper Case")
        self.need_lower_case = QCheckBox("Lower Case")
        self.need_digits = QCheckBox("Digits")
        self.need_special_chars = QCheckBox("Special Characters")

        self.need_upper_case.setChecked(getReqUpper())
        self.need_lower_case.setChecked(getReqLower())
        self.need_digits.setChecked(getReqDigit())
        self.need_special_chars.setChecked(getReqOther())

        # Add Widgets to Top layout
        top_layout.addRow(
            QLabel('Maximum number of days before changing password'), self.max_day)
        top_layout.addRow(
            QLabel('Minimum number of days before changing password'), self.min_day)
        top_layout.addRow(QLabel(
            'Number of days before warning is given to change passsword'), self.warning)
        top_layout.addRow(QLabel('Minimum password length'), self.min_chars)
        top_layout.addRow(
            QLabel('Number of previous passwords remembered'), self.pass_remember)
        top_layout.addRow(self.need_upper_case)
        top_layout.addRow(self.need_lower_case)
        top_layout.addRow(self.need_digits)
        top_layout.addRow(self.need_special_chars)

        # Define Btn layout
        self.apply_btn = QPushButton(
            "Apply", clicked=self.submit_password_req_changes)

        btn_layout.addWidget(self.apply_btn)

        # Add sublayouts to main layout
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(btn_layout)

        # Set window's main layout
        self.setLayout(outer_layout)

    def submit_password_req_changes(self):
        # Update password expiration config file '/etc/login.defs'
        changeMaxDays(self.max_day.text())
        changeMinDays(self.min_day.text())
        changeWarnDays(self.warning.text())
        
        # Update password requirements config file '/etc/pam.d/common-password'
        writeToCommon_Password(self.min_chars.text(), self.pass_remember.text(), 
                   self.need_upper_case.isChecked(), self.need_lower_case.isChecked(), 
                   self.need_digits.isChecked(), self.need_special_chars.isChecked())

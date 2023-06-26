from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox,
    QPushButton, QLineEdit, QListWidget, 
    QListWidgetItem, QFormLayout
)
from PyQt6.QtCore import Qt

from scripts.functions import listUsers, list_sudoers, list_nonsudoers
from scripts.change_passwds import passwdChange
import controller.controller as c

class ChangePasswordTab(QWidget):
    def __init__(self):
        super(ChangePasswordTab, self).__init__()

        # Layout
        main_layout = QVBoxLayout()
        pass_layout = QFormLayout()
        # second_pass_layout = QHBoxLayout()

        # Title
        title_card = QLabel("Choose Users to reset password")
        main_layout.addWidget(title_card)

        # List all normal users on device
        self.user_list_display = QListWidget()
        main_layout.addWidget(self.user_list_display)

        # Retrieve list of users
        users_list = listUsers()
        for user in users_list:
            item = QListWidgetItem(user)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable |
                          Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.user_list_display.addItem(item)

        # Text box for new password
        # self.newPasswdLabel = QLabel("New password: ")
        # main_layout.addWidget(self.newPasswdLabel)
        # self.newPasswd = QLineEdit(self)
        # self.newPasswd.setEchoMode(QLineEdit.EchoMode.Password)
        # main_layout.addWidget(self.newPasswd)

        
        # Form for new password
        self.new_pass_textbox = QLineEdit(self)
        self.new_pass_textbox.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_pass_textbox = QLineEdit(self)
        self.confirm_pass_textbox.setEchoMode(QLineEdit.EchoMode.Password)

        pass_layout.addRow(QLabel("New Password: "), self.new_pass_textbox)
        pass_layout.addRow(QLabel("Confirm Password: "), self.confirm_pass_textbox)        

        # Submit button
        self.submit_button = QPushButton(
            "Submit", clicked=self.changeCheckedUsers)

        # Add sublayouts to main layout
        main_layout.addLayout(pass_layout)
        main_layout.addWidget(self.submit_button)

        # Set windows main layout
        self.setLayout(main_layout)

    # Function to change selected users
    def changeCheckedUsers(self):
        checkedUsers = []
        for index in range(self.user_list_display.count()):
            if self.user_list_display.item(index).checkState() == Qt.CheckState.Checked:
                checkedUsers.append(self.user_list_display.item(index).text())

        # passwdChange(self.newPasswd.text(), checkedUsers)
        if self.new_pass_textbox.text() == self.confirm_pass_textbox.text():
            c.changePass(self.confirm_pass_textbox.text(), checkedUsers)
            for index in range(self.user_list_display.count()):
                self.user_list_display.item(index).setCheckState(Qt.CheckState.Unchecked)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error Invalid Password")
            msg.setText("Passwords do not match. Try again.")
            msg.exec()
        
        self.new_pass_textbox.clear()
        self.confirm_pass_textbox.clear()

class PopDialog(QWidget):
    pass


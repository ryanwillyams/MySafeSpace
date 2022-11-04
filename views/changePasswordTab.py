from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget,  QVBoxLayout, QLabel, 
    QPushButton, QLineEdit, QListWidget, 
    QListWidgetItem
)
from PyQt6.QtCore import Qt

from scripts.functions import listUsers, list_sudoers, list_nonsudoers
from scripts.change_passwds import passwdChange


class ChangePasswordTab(QWidget):
    def __init__(self):
        super(ChangePasswordTab, self).__init__()

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
        self.submit_button = QPushButton(
            "Submit", clicked=self.changeCheckedUsers)
        main_layout.addWidget(self.submit_button)
        self.setLayout(main_layout)

        # Retrieve list of users
        users_list = listUsers()
        for user in users_list:
            item = QListWidgetItem(user)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable |
                          Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.user_list_display.addItem(item)

    # Function to change selected users
    def changeCheckedUsers(self):
        checkedUsers = []
        for index in range(self.user_list_display.count()):
            if self.user_list_display.item(index).checkState() == Qt.CheckState.Checked:
                checkedUsers.append(self.user_list_display.item(index).text())

        passwdChange(self.newPasswd.text(), checkedUsers)

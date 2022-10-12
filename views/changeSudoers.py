from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget,QTabWidget,QFormLayout,QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox, QComboBox,
    QListWidget,QListWidgetItem, QScrollBar, QMessageBox
)
from PyQt6.QtCore import Qt

from scripts.functions import listUsers, list_sudoers, list_nonsudoers
from scripts.sudo_priv import addSudo, removeSudo

class ChangeSudoers(QWidget):
    def __init__(self):
        super(ChangeSudoers,self).__init__()
        # Declare layouts
        outer_layout = QVBoxLayout()
        top_layout = QGridLayout()
        bottom_layout = QHBoxLayout()

        # Sudoer label and list
        sudoer_label = QLabel("Sudoers")
        self.sudoer_list_display = QListWidget()
        sudoer_list = list_sudoers()
        for sudoer in sudoer_list:
            item = QListWidgetItem(sudoer)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.sudoer_list_display.addItem(item)

        # Add sudo Widgets into layout
        top_layout.addWidget(sudoer_label, 0, 0)
        top_layout.addWidget(self.sudoer_list_display, 1, 0)

        # Normal User label and list
        normal_users_label = QLabel("Normal Users")
        self.normal_user_list_display = QListWidget()
        normal_user_list = list_nonsudoers()
        for user in normal_user_list:
            item = QListWidgetItem(user)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.normal_user_list_display.addItem(item)

        # Add normal user widgets into layout
        top_layout.addWidget(normal_users_label, 0, 1)
        top_layout.addWidget(self.normal_user_list_display, 1, 1)

        # Submit button
        submit_button = QPushButton("Submit", clicked=self.changeCheckedUsers)
        bottom_layout.addWidget(submit_button)

        # Add sublayouts to main layout
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(bottom_layout)

        # Set window's main layout
        self.setLayout(outer_layout)

    # Changes users between sudo and normal users
    def changeCheckedUsers(self):
        # Fetch all checked sudoers and remove from sudo group
        checked_sudoers = []
        for index in range(self.sudoer_list_display.count()):
            if self.sudoer_list_display.item(index).checkState() == Qt.CheckState.Checked:
                checked_sudoers.append(self.sudoer_list_display.item(index).text())

        removeSudo(checked_sudoers)

        # Fetch all checked normal users and add to sudo group
        checked_normals = []
        for index in range(self.normal_user_list_display.count()):
            if self.normal_user_list_display.item(index).checkState() == Qt.CheckState.Checked:
                checked_normals.append(self.normal_user_list_display.item(index).text())

        addSudo(checked_normals)

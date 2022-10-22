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
        middle_layout = QVBoxLayout()

        # Sudoer label and list
        sudoer_label = QLabel("Sudoers")
        self.sudoer_list_display = QListWidget()

        # Add sudo Widgets into layout
        top_layout.addWidget(sudoer_label, 0, 0)
        top_layout.addWidget(self.sudoer_list_display, 1, 0)

        # Normal User label and list
        normal_users_label = QLabel("Normal Users")
        self.normal_user_list_display = QListWidget()

        # Add normal user widgets into layout
        top_layout.addWidget(normal_users_label, 0, 2)
        top_layout.addWidget(self.normal_user_list_display, 1, 2)

        # Populate Lists
        self.updateDisplayLists()
        
        # Change buttons
        sudo_to_normal = QPushButton(">>", clicked=self.changeSudoToNormal)
        normal_to_sudo = QPushButton("<<", clicked=self.changeNormalToSudo)

        # Add to VBoxlayout
        middle_layout.addWidget(sudo_to_normal)
        middle_layout.addWidget(normal_to_sudo)

        # Create a Wrapper for the layout
        button_wrapper = QWidget()
        button_wrapper.setLayout(middle_layout)
        top_layout.addWidget(button_wrapper,1,1)

        # Add sublayouts to main layout
        outer_layout.addLayout(top_layout)

        # Set window's main layout
        self.setLayout(outer_layout)

    # Changes users between sudo and normal users
    def changeSudoToNormal(self):
        # Fetch all checked sudoers and remove from sudo group
        checked_sudoers = []
        for index in range(self.sudoer_list_display.count()):
            if self.sudoer_list_display.item(index).checkState() == Qt.CheckState.Checked:
                checked_sudoers.append(self.sudoer_list_display.item(index).text())
        
        # Only called if there were checked values
        if checked_sudoers:
            removeSudo(checked_sudoers)
            self.updateDisplayLists()

    def changeNormalToSudo(self):
        # Fetch all checked normal users and add to sudo group
        checked_normals = []
        for index in range(self.normal_user_list_display.count()):
            if self.normal_user_list_display.item(index).checkState() == Qt.CheckState.Checked:
                checked_normals.append(self.normal_user_list_display.item(index).text())
        # Only called if there were checked values
        if checked_normals:
            addSudo(checked_normals)
            self.updateDisplayLists()


    def updateDisplayLists(self):

        # Sudo User lists
        self.sudoer_list_display.clear()
        sudoer_list = list_sudoers()
        for sudoer in sudoer_list:
            item = UserListItem(sudoer)
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.sudoer_list_display.addItem(item)

        # Normal User list
        self.normal_user_list_display.clear()
        normal_user_list = list_nonsudoers()
        for user in normal_user_list:
            item = UserListItem(user)
            self.normal_user_list_display.addItem(item)


class UserListItem(QListWidgetItem):
    def __init__(self,*args,**kwargs):
        super(QListWidgetItem,self).__init__(*args,**kwargs)
        self.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        self.setCheckState(Qt.CheckState.Unchecked)
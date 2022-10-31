from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QFormLayout, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QSpinBox, QComboBox,
    QListWidget, QListWidgetItem, QScrollBar, QMessageBox, QTreeView
)
from PyQt6.QtCore import Qt

from views.passwordReqTab import PasswordReqTab
from views.changePasswordTab import ChangePasswordTab
from views.changeSudoers import ChangeSudoers
from views.iptablesTab import IPTables
from views.ServicesTab import DisableServices


class HardenMainPage(QWidget):
    def __init__(self):
        super(HardenMainPage,  self).__init__()

        # Declare layout
        self.layout = QHBoxLayout()

        self.uiFront = UIFront()
        self.uiCustomize = UICustomize()
        self.uiLogs = UILogs()
        self.uiFront.btn_customize.clicked.connect(self.customizeView)
        self.uiFront.btn_logs.clicked.connect(self.logView)
        self.uiCustomize.btn_back.clicked.connect(self.frontView)
        self.uiLogs.btn_back.clicked.connect(self.frontView)

        self.layout.addWidget(self.uiFront)
        self.layout.addWidget(self.uiCustomize)
        self.layout.addWidget(self.uiLogs)
        self.uiCustomize.hide()
        self.uiLogs.hide()

        self.setLayout(self.layout)

    def customizeView(self):
        self.uiFront.hide()
        self.uiCustomize.show()

    def logView(self):
        self.uiFront.hide()
        self.uiLogs.refreshLogs()
        self.uiLogs.show()

    def frontView(self):
        self.uiCustomize.hide()
        self.uiLogs.hide()
        self.uiFront.show()

class UIFront(QWidget):
    def __init__(self):
        super(UIFront, self).__init__()


        # Declare layouts
        outer_layout = QVBoxLayout()
        preset_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()

        # Define preset layout
        preset_high = QWidget()
        preset_high.setMaximumSize(200, 300)
        preset_high.setStyleSheet("background-color: #353535")

        preset_med = QWidget()
        preset_med.setMaximumSize(200, 300)
        preset_med.setStyleSheet("background-color: #353535")

        preset_low = QWidget()
        preset_low.setMaximumSize(200, 300)
        preset_low.setStyleSheet("background-color: #353535")

        preset_layout.addWidget(preset_high)
        preset_layout.addWidget(preset_med)
        preset_layout.addWidget(preset_low)

        # Define btn layout
        self.btn_customize = QPushButton("Customize")
        self.btn_customize.setMaximumSize(100, 25)

        self.btn_logs = QPushButton("Logs")
        self.btn_logs.setMaximumSize(100, 25)

        btn_layout.addWidget(self.btn_customize)
        btn_layout.addWidget(self.btn_logs)

        # Add sublayouts to main layout
        outer_layout.addLayout(preset_layout)
        outer_layout.addLayout(btn_layout)

        # Set main window layout
        self.setLayout(outer_layout)

class UICustomize(QWidget):
    def __init__(self):
        super(UICustomize, self).__init__()

        # Declare layouts
        outer_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        self.layout = QGridLayout()

        # Define top layout
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.btn_back = QPushButton("Back")
        self.btn_back.setMaximumSize(75, 25)

        top_layout.addWidget(self.btn_back)


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

        # Add sub layouts to outer layout
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(self.layout)

        self.setLayout(outer_layout)

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

class UILogs(QWidget):
    def __init__(self):
        super(UILogs, self).__init__()

        # Declare layouts
        self.outer_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # Define top layout
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.btn_back = QPushButton("Back")
        
        top_layout.addWidget(self.btn_back)

        # Define logs views
        self.logs = QListWidget()
        try:
            for line in reversed(list(open('changelog.txt'))):
                self.logs.addItem(line.rstrip())
        except:
            f = open('changelog.txt', 'x')

        # Add sublayouts to outer layout
        self.outer_layout.addLayout(top_layout)
        self.outer_layout.addWidget(self.logs)

        # Set layout to main view
        self.setLayout(self.outer_layout)

    def refreshLogs(self):
        self.logs.close()
        new_logs = QListWidget()

        for line in reversed(list(open('changelog.txt'))):
            new_logs.addItem(line.rstrip())

        self.logs = new_logs
        self.outer_layout.addWidget(self.logs)
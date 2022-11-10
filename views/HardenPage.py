from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QFormLayout, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QSpinBox, QComboBox,
    QListWidget, QListWidgetItem, QScrollBar, QMessageBox, QTreeView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

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

        # Define high preset layout
        preset_high = QWidget()
        preset_high.setMaximumSize(200, 300)
        preset_high.setStyleSheet("background-color: #353535")

        ## Label
        label_high = QLabel("High Security")
        label_high.setFont(QFont('Exo 2', 20))
        label_high.resize(200, 25)

        ## Image
        pic_preset_high = QLabel()
        pixmap = QPixmap('images/highPreset.png')
        pixmap_high = pixmap.scaledToWidth(180)
        pic_preset_high.setPixmap(pixmap_high)

        ## Layout
        high_layout = QVBoxLayout()
        high_layout.addWidget(label_high)
        high_layout.addWidget(pic_preset_high)
        high_layout.addStretch()
        preset_high.setLayout(high_layout)

        # Define medium preset layout
        preset_med = QWidget()
        preset_med.setMaximumSize(200, 300)
        preset_med.setStyleSheet("background-color: #353535")

        ## Label
        label_med = QLabel("Med Security")
        label_med.setFont(QFont('Exo 2', 20))
        label_med.resize(200, 25)

        ## Image
        pic_preset_med = QLabel()
        pixmap = QPixmap('images/medPreset.png')
        pixmap_med = pixmap.scaledToWidth(180)
        pic_preset_med.setPixmap(pixmap_med)

        ## Layout
        med_layout = QVBoxLayout()
        med_layout.addWidget(label_med)
        med_layout.addWidget(pic_preset_med)
        med_layout.addStretch()
        preset_med.setLayout(med_layout)

        # Define low preset layout
        preset_low = QWidget()
        preset_low.setMaximumSize(200, 300)
        preset_low.setStyleSheet("background-color: #353535")

        preset_layout.addWidget(preset_high)
        preset_layout.addWidget(preset_med)
        preset_layout.addWidget(preset_low)

        ## Label
        label_low = QLabel("low Security")
        label_low.setFont(QFont('Exo 2', 20))
        label_low.resize(200, 25)

        ## Image
        pic_preset_low = QLabel()
        pixmap = QPixmap('images/lowPreset.png')
        pixmap_low = pixmap.scaledToWidth(180)
        pic_preset_low.setPixmap(pixmap_low)

        ## Layout
        low_layout = QVBoxLayout()
        low_layout.addWidget(label_low)
        low_layout.addWidget(pic_preset_low)
        low_layout.addStretch()
        preset_low.setLayout(low_layout)

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
        self.bottom_layout = QHBoxLayout()

        # Define top layout
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.btn_back = QPushButton("Back")
        self.btn_back.setMaximumSize(75, 25)

        top_layout.addWidget(self.btn_back)


        # Scrollbar
        list_widget = QListWidget()
        list_widget.setMaximumWidth(180)

        # Scrollbar List
        list_passReqTab = QListWidgetItem("Password Requirements")
        list_changePassTab = QListWidgetItem("Change Password")
        list_changeSudoers = QListWidgetItem("Change Sudoers")
        list_disableServices = QListWidgetItem("Services")
        list_iptables = QListWidgetItem("IPTables")

        list_widget.addItem(list_passReqTab)
        list_widget.addItem(list_changePassTab)
        list_widget.addItem(list_changeSudoers)
        list_widget.addItem(list_disableServices)
        list_widget.addItem(list_iptables)
        list_widget.itemClicked.connect(self.change_tab)

        # Create list widgets
        self.passReqTab = PasswordReqTab()
        self.changePassTab = ChangePasswordTab()
        self.changeSudoers = ChangeSudoers()
        self.disableServices = DisableServices()
        self.iptables = IPTables()

        self.tabs = [self.passReqTab, self.changePassTab, self.changeSudoers,
                self.disableServices, self.iptables]
        self.current_tab = 0

        # Scrollbar formatting
        scroll_bar = QScrollBar(self)
        list_widget.setVerticalScrollBar(scroll_bar)
        self.bottom_layout.addWidget(list_widget)
        self.bottom_layout.addWidget(self.tabs[0])
        self.bottom_layout.addWidget(self.tabs[1])
        self.bottom_layout.addWidget(self.tabs[2])
        self.bottom_layout.addWidget(self.tabs[3])
        self.bottom_layout.addWidget(self.tabs[4])

        # Hide all widgets besides first
        self.changePassTab.hide()
        self.changeSudoers.hide()
        self.disableServices.hide()
        self.iptables.hide()

        # Add sub layouts to outer layout
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(self.bottom_layout)

        self.setLayout(outer_layout)

    # Function for changing between different menus
    def change_tab(self, item):
        match item.text():
            case "Password Requirements":
                self.tabs[self.current_tab].hide()
                self.passReqTab.show()
                self.current_tab = 0
            case "Change Password":
                self.tabs[self.current_tab].hide()
                self.changePassTab.show()
                self.current_tab = 1
            case "Change Sudoers":
                self.tabs[self.current_tab].hide()
                self.changeSudoers.show()
                self.current_tab = 2
            case "Services":
                self.tabs[self.current_tab].hide()
                self.disableServices.show()
                self.current_tab = 3
            case "IPTables":
                self.tabs[self.current_tab].hide()
                self.iptables.show()
                self.current_tab = 4

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
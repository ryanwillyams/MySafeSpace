from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget,QTabWidget,QFormLayout,QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox, QComboBox,
    QListWidget,QListWidgetItem, QScrollBar, QMessageBox
)
from PyQt6.QtCore import Qt

# TODO Find a way to import this function outside of this file
import sys 

sys.path.append("..")
from functions import listUsers, list_sudoers, list_nonsudoers
from passwdReq import passwdExpirConfig, passwdReqs
from change_passwds import passwdChange
from sudo_priv import addSudo, removeSudo
from iptables import viewRules, changeChainPolicy, addRule, removeRule

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
        
        # Layout
        self.layout = QGridLayout(self)

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

        self.setLayout(self.layout)
    
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

class DisableServices(QWidget):
    def __init__(self):
        super(DisableServices,self).__init__()

class IPTables(QWidget):
    def __init__(self):
        super(IPTables,self).__init__()

        # Declare layouts
        outer_layout = QVBoxLayout()
        rule_list = QListWidget()
        buttons_layout = QHBoxLayout()

        # Define Rule List layout
        rules = viewRules()
        for line in rules:
            item = QListWidgetItem(line)
            rule_list.addItem(item)

        scroll_bar = QScrollBar(self)
        rule_list.setVerticalScrollBar(scroll_bar)

        # Define Buttons layout
        btn_change_policy = QPushButton("Change Policies", clicked=self.chainPoliciesForm)
        btn_add_rule = QPushButton("Add Rule", clicked=self.addRuleForm)
        btn_remove_rule = QPushButton("Remove Rule", clicked=self.removeRuleForm)
        btn_clear_all = QPushButton("Clear All", clicked=self.clearAllMsg)

        buttons_layout.addWidget(btn_change_policy)
        buttons_layout.addWidget(btn_add_rule)
        buttons_layout.addWidget(btn_remove_rule)

        #Add sublayouts to main layout
        outer_layout.addWidget(rule_list)
        outer_layout.addLayout(buttons_layout)

        # Set windows main layout
        self.setLayout(outer_layout)

    # Function call to open Chain Policy Form
    def chainPoliciesForm(self):
        self.popup = ChainPoliciesForm()
        self.popup.setMinimumSize(300, 150)
        self.popup.show()

    # Function call to open Add Rule Form
    def addRuleForm(self):
        self.popup = AddRuleForm()
        self.popup.setMinimumSize(500, 150)
        self.popup.show()

    # Function call to open Remove Rule Form
    def removeRuleForm(self):
        self.popup = RemoveRuleForm()
        self.popup.setMinimumSize(250, 100)
        self.popup.show()

    def clearAllMsg(self):
        return 0

class ChainPoliciesForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Change Chain Policy")

        # Declare layout
        outer_layout = QVBoxLayout()
        form_layout = QFormLayout()
        button_layout = QHBoxLayout()

        # Define form layout
        self.input_policy = QComboBox()
        self.input_policy.addItems(["Options", "Accept", "Drop"])
        
        self.forward_policy = QComboBox()
        self.forward_policy.addItems(["Options", "Accept", "Drop"])

        self.output_policy = QComboBox()
        self.output_policy.addItems(["Options", "Accept", "Drop"])
        
        form_layout.addRow(QLabel("Input Policy"), self.input_policy)
        form_layout.addRow(QLabel("Forward Policy"), self.forward_policy)
        form_layout.addRow(QLabel("Output Policy"), self.output_policy)

        # Define Button layout
        btn_submit = QPushButton("Submit", clicked=self.changePolicy)
        button_layout.addWidget(btn_submit)

        # Add sublayouts to main layout
        outer_layout.addLayout(form_layout)
        outer_layout.addLayout(button_layout)

        # Set window's main layout
        self.setLayout(outer_layout)

    def changePolicy(self):
        # Change Input policy
        if self.input_policy.currentText() != "Options":
            changeChainPolicy("input", self.input_policy.currentText())
        # Change Forward policy
        if self.forward_policy.currentText() != "Options":
            changeChainPolicy("forward", self.forward_policy.currentText())
        # Change Output policy
        if self.output_policy.currentText() != "Options":
            changeChainPolicy("output", self.output_policy.currentText())
        self.close()

class AddRuleForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Add New Rule")

        # Declare layouts
        outer_layout = QVBoxLayout()
        form_layout = QFormLayout()
        button_layout = QHBoxLayout()

        # Define From layout
        self.chain_type = QComboBox()
        self.chain_type.addItems(["Options", "Input", "Output", "Forward"])

        self.network_type = QComboBox()
        self.network_type.addItems(["Options", "Port Number", "IP Address"])
        
        self.port_ip = QLineEdit("ex. 433 or 192.0.10.6")

        self.action = QComboBox()
        self.action.addItems(["Options", "Accept", "Drop", "Reject"])

        form_layout.addRow(QLabel("Chain Type"), self.chain_type)
        form_layout.addRow(QLabel("Network Type"), self.network_type)
        form_layout.addRow(QLabel("Port Number or IP Address"), self.port_ip)
        form_layout.addRow(QLabel("Action"), self.action)

        # Define Button layout
        btn_submit = QPushButton("Submit")
        btn_submit.clicked.connect(self.submitAction)
        button_layout.addWidget(btn_submit)

        # Add sublayouts to amin layout
        outer_layout.addLayout(form_layout)
        outer_layout.addLayout(button_layout)

        # Set window's main layout
        self.setLayout(outer_layout)

    def submitAction(self):
        result = addRule(self.chain_type.currentText(), self.network_type.currentText(), 
                self.port_ip.text(), self.action.currentText())
        if result == "No Error":
            self.close()
        # Error Message
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error Invalid Entry")
            msg.setText("One of the entries is invalid, check details for more information")
            msg.setDetailedText(result)
            # msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


class RemoveRuleForm(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Remove Rule")

        # Declare layouts
        outer_layout = QVBoxLayout()
        form_layout = QFormLayout()
        button_layout = QHBoxLayout()

        # Define form_layout
        self.chain_type = QComboBox()
        self.chain_type.addItems(["Options", "Input", "Output", "Forward"])

        self.line_number = QSpinBox()
        self.line_number.setRange(1, 999)

        form_layout.addRow(QLabel("Chain Type"), self.chain_type)
        form_layout.addRow(QLabel("Line number"), self.line_number)

        # Define button_layout
        btn_submit = QPushButton("Submit", clicked=self.submitAction)
        button_layout.addWidget(btn_submit)

        # Add sublayouts to main layout
        outer_layout.addLayout(form_layout)
        outer_layout.addLayout(button_layout)

        # Set window's main layout
        self.setLayout(outer_layout)

    def submitAction(self):
        result = removeRule(self.chain_type.currentText(), self.line_number.text())
        if result == "No Error":
            self.close()
        # Error Message
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error Invalid Entry")
            msg.setText("One of the entries is invalid, check details for more information")
            msg.setDetailedText(result)
            # msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    
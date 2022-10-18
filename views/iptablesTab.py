from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget,QTabWidget,QFormLayout,QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox, QComboBox,
    QListWidget,QListWidgetItem, QScrollBar, QMessageBox
)
from PyQt6.QtCore import Qt

from scripts.iptables import viewRules, changeChainPolicy, addRule, removeRule


class IPTables(QWidget):
    def __init__(self):
        super(IPTables,self).__init__()

        # Declare layouts
        outer_layout = QVBoxLayout()
        self.rule_list = QListWidget()
        buttons_layout = QHBoxLayout()

        # Define Rule List layout
        rules = viewRules()
        for line in rules:
            item = QListWidgetItem(line)
            self.rule_list.addItem(item)

        scroll_bar = QScrollBar(self)
        self.rule_list.setVerticalScrollBar(scroll_bar)

        # Define Buttons layout
        btn_change_policy = QPushButton("Change Policies", clicked=self.chainPoliciesForm)
        btn_add_rule = QPushButton("Add Rule", clicked=self.addRuleForm)
        btn_remove_rule = QPushButton("Remove Rule", clicked=self.removeRuleForm)
        btn_clear_all = QPushButton("Clear All", clicked=self.clearAllMsg)

        buttons_layout.addWidget(btn_change_policy)
        buttons_layout.addWidget(btn_add_rule)
        buttons_layout.addWidget(btn_remove_rule)

        #Add sublayouts to main layout
        outer_layout.addWidget(self.rule_list)
        outer_layout.addLayout(buttons_layout)

        # Set windows main layout
        self.setLayout(outer_layout)

    # Function call to open Chain Policy Form
    def chainPoliciesForm(self):
        self.popup = ChainPoliciesForm(self.updateRuleList)
        self.popup.setMinimumSize(300, 150)
        self.popup.show()

    # Function call to open Add Rule Form
    def addRuleForm(self):
        self.popup = AddRuleForm(self.updateRuleList)
        self.popup.setMinimumSize(500, 150)
        self.popup.show()

    # Function call to open Remove Rule Form
    def removeRuleForm(self):
        self.popup = RemoveRuleForm(self.updateRuleList)
        self.popup.setMinimumSize(250, 100)
        self.popup.show()

    def clearAllMsg(self):
        return 0
    
    def updateRuleList(self):
        # Call when rule list changed
        print("Updating Rule List")
        self.rule_list.clear()
        rules = viewRules()
        for line in rules:
            item = QListWidgetItem(line)
            self.rule_list.addItem(item)

class ChainPoliciesForm(QWidget):
    def __init__(self,updateRuleList):
        QWidget.__init__(self)
        self.setWindowTitle("Change Chain Policy")

        self.updateRuleList = updateRuleList

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
        
        # TODO: Create check before updating
        self.updateRuleList()
        self.close()

class AddRuleForm(QWidget):
    def __init__(self,updateRuleList):
        QWidget.__init__(self)
        self.setWindowTitle("Add New Rule")

        self.updateRuleList = updateRuleList

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
            self.updateRuleList()
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
    def __init__(self, updateRuleList):
    
        QWidget.__init__(self)
        self.setWindowTitle("Remove Rule")

        self.updateRuleList = updateRuleList
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
            self.updateRuleList()
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

    
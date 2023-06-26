from logging.handlers import QueueListener
from PyQt6.QtWidgets import (
    QWidget, QFormLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QSpinBox, QComboBox,
    QListWidget, QListWidgetItem, QScrollBar, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6 import QtGui

from scripts.iptables import resetRules
from controller.ip_tables_controller import (
    viewRules, changeChainPolicy, addRule, removeRule
)


class IPTables(QWidget):
    def __init__(self):
        super(IPTables, self).__init__()

        # Declare layouts
        outer_layout = QVBoxLayout()
        self.rule_list = QListWidget()
        buttons_layout = QHBoxLayout()

        # Make the font monospace or monospace adjacent
        list_font = self.rule_list.font()
        list_font.setFamily("Monospace")
        list_font.setStyleHint(QtGui.QFont.StyleHint.TypeWriter)
        self.rule_list.setFont(list_font)

        # Define Rule List layout
        rules = viewRules()
        for line in rules:
            item = RuleListWidgetItem(line)
            self.rule_list.addItem(item)

        scroll_bar = QScrollBar(self)
        self.rule_list.setVerticalScrollBar(scroll_bar)

        # Define Buttons layout
        btn_change_policy = QPushButton(
            "Change Policies", clicked=self.chainPoliciesForm)
        btn_add_rule = QPushButton("Add Rule", clicked=self.addRuleForm)
        btn_remove_rule = QPushButton(
            "Remove Rule", clicked=self.removeRuleForm)
        btn_clear_all = QPushButton("Clear All", clicked=self.clearAllMsg)

        buttons_layout.addWidget(btn_change_policy)
        buttons_layout.addWidget(btn_add_rule)
        buttons_layout.addWidget(btn_remove_rule)
        buttons_layout.addWidget(btn_clear_all)

        # Add sublayouts to main layout
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
        resetRules()
        self.updateRuleList()

    def updateRuleList(self):
        # Call when rule list changed
        self.rule_list.clear()
        rules = viewRules()
        for line in rules:
            item = RuleListWidgetItem(line)
            self.rule_list.addItem(item)


class RuleListWidgetItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super(QListWidgetItem, self).__init__(*args, **kwargs)

        initial_text = self.text().lstrip()
        if not initial_text or initial_text.startswith('-'):
            self._create_blank_line()
        elif initial_text.startswith('Chain'):
            self._create_title_line()
        elif initial_text.startswith('num'):
            self._create_header_line()

    def _create_blank_line(self):
        # Disables selections
        # To Enable selection use | or instead of & ~
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsSelectable)

    def _create_title_line(self):
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setBackground(QtGui.QColor(0, 0, 200))

    def _create_header_line(self):
        self.setFlags(self.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.setBackground(QtGui.QColor(0, 0, 100))


class RuleFormPopDialog(QWidget):
    # Use this Class to apply style/methods to all forms
    def __init__(self, updateRuleList):
        QWidget.__init__(self)
        self.updateRuleList = updateRuleList
        flags = Qt.WindowType.Sheet
        self.setWindowFlags(flags)


class ChainPoliciesForm(RuleFormPopDialog):
    def __init__(self, *args, **kwargs):
        RuleFormPopDialog.__init__(self, *args, **kwargs)
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

        # TODO: Create check before updating
        self.updateRuleList()

        self.close()


class AddRuleForm(RuleFormPopDialog):
    def __init__(self, *args, **kwargs):
        RuleFormPopDialog.__init__(self, *args, **kwargs)
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

        self.port_ip = QLineEdit()
        self.port_ip.setPlaceholderText("ex. 433 or 192.0.10.6")

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
            msg.setText(
                "One of the entries is invalid, check details for more information")
            msg.setDetailedText(result)
            # msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()


class RemoveRuleForm(RuleFormPopDialog):
    def __init__(self, *args, **kwargs):
        RuleFormPopDialog.__init__(self, *args, **kwargs)
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
        result = removeRule(self.chain_type.currentText(),
                            self.line_number.text())
        if result == "No Error":
            self.updateRuleList()
            self.close()
        # Error Message
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Error Invalid Entry")
            msg.setText(
                "One of the entries is invalid, check details for more information")
            msg.setDetailedText(result)
            # msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

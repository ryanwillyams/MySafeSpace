from PyQt6.QtWidgets import (
    QWidget,QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt
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
        
        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.West)

        # Initialize tabs
        passReqTab = PasswordReqTab()
        changePassTab = ChangePasswordTab()
        changeSudoers = ChangeSudoers()


        tabs.addTab(passReqTab,"Password Requirements")
        tabs.addTab(changePassTab,"Change Password")
        tabs.addTab(changeSudoers, "Change Sudoers")
        
        layout.addWidget(tabs)
        self.setLayout(layout)

#TODO Add better Styling to password requirements
# - Better Text Area
# - Smaller Buttons
# - Closer labels
#


class PasswordReqTab(QWidget):
    def __init__(self):
        super(PasswordReqTab,self).__init__()
        main_layout = QVBoxLayout()
        
        ##
        # Initialize Text Area
        label_text_edit = QLabel('Try your password here')
        self.current_password_text = ''

        self.main_text_edit_area = QLineEdit()
        self.main_text_edit_area.textChanged.connect(self.text_was_edited)
        main_layout.addWidget(label_text_edit)
        main_layout.addWidget(self.main_text_edit_area)
        
        ##
        #Initalize Minimum Characters
        self.min_chars = QSpinBox()
        self.min_chars.setRange(4,32)
        
        main_layout.addWidget(self.min_chars)

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

        for button in self.check_buttons:
            button.stateChanged.connect(self.is_text_area_valid)
            main_layout.addWidget(button)
        ##
        # Initialize Buttons
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear")
        self.submit_button = QPushButton("Submit")

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)

        bottom_buttons = QWidget()
        bottom_buttons.setLayout(button_layout)
        
        main_layout.addWidget(bottom_buttons)
        self.setLayout(main_layout)
    

    def text_was_edited(self):
        
        self.current_password_text = self.main_text_edit_area.text()
        # print(self.current_password_text)


    def is_text_area_valid(self):
        # Check checkboxes
        print("Checking Text")
        states = [button for button in self.check_buttons if button == Qt.CheckState.Checked]

        pass

    def clear_button(self):
        pass

    def submit_button(self):
        # TODO add the submit button
        pass

    
        

class ChangePasswordTab(QWidget):
    def __init__(self):
        super(ChangePasswordTab,self).__init__()


class ChangeSudoers(QWidget):
    def __init__(self):
        super(ChangeSudoers,self).__init__()

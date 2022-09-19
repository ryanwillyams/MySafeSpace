from PyQt6.QtWidgets import QWidget,QTabWidget, QVBoxLayout
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



class PasswordReqTab(QWidget):
    def __init__(self):
        super(PasswordReqTab,self).__init__()

        

class ChangePasswordTab(QWidget):
    def __init__(self):
        super(ChangePasswordTab,self).__init__()


class ChangeSudoers(QWidget):
    def __init__(self):
        super(ChangeSudoers,self).__init__()

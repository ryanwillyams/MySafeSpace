import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget

from Views.ResourcesPage import ResourcesPage
from Views.SecurePage import SecurePage
from Views.ServicesPage import ServicesPage


class MainWindow(QMainWindow):
    
    WIDTH = 600
    HEIGHT = 400

    def __init__(self):
        super(MainWindow,self).__init__()

        self.setWindowTitle("My Safe Space")
        
        self.setMinimumSize(self.WIDTH, self.HEIGHT)

        tabs = QTabWidget()
        tabs.setMovable(False)
        
        securePage = SecurePage()
        servicesPage = ServicesPage()
        resourcesPage = ResourcesPage()

        tab_views = {
            'SecurePage':securePage,
            'ServicesPage':servicesPage,
            'ResourcesPage':resourcesPage
        }

        for view_name,view in tab_views.items():
            tabs.addTab(view,view_name)

        self.setCentralWidget(tabs)

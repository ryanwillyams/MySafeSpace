import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget

from Views.ResourcesPage import ResourcesPage
from Views.HardenPage import HardenPage
from Views.ServicesPage import ServicesPage


class MainWindow(QMainWindow):
    
    # Keeps a 4:3 aspect ratio
    WIDTH = 1024
    HEIGHT = 768

    def __init__(self):
        super(MainWindow,self).__init__()

        self.setWindowTitle("My Safe Space")
        
        self.setMinimumSize(self.WIDTH, self.HEIGHT)

        tabs = QTabWidget()
        tabs.setMovable(False)
        
        hardenPage = HardenPage()
        servicesPage = ServicesPage()
        resourcesPage = ResourcesPage()

        tab_views = {
            'Harden': hardenPage,
            'Services': servicesPage,
            'Resources': resourcesPage
        }

        for view_name,view in tab_views.items():
            tabs.addTab(view,view_name)

        self.setCentralWidget(tabs)

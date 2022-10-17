from PyQt6.QtWidgets import (
    QWidget,QTabWidget,QFormLayout,QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox, QComboBox,
    QListWidget,QListWidgetItem, QScrollBar, QMessageBox, QTreeView,
    QGroupBox, QAbstractItemView, QMenu
)
from PyQt6.QtCore import (Qt, QEvent)
from PyQt6.QtGui import QStandardItemModel

from scripts.services import (getServices, startService, stopService)

class DisableServices(QWidget):
    def __init__(self):
        super(DisableServices,self).__init__()
        # Declare layouts
        outer_layout = QVBoxLayout()
        data_group_box = QGroupBox("Services")
        data_layout = QHBoxLayout()
        data_group_box.setLayout(data_layout)

        # Define data layout
        self.data_view = QTreeView()
        self.data_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.data_view.setSortingEnabled(True)

        model = self.createServiceModel(self)
        self.data_view.setModel(model)
        # Populate list
        services = getServices()
        for service in services:
            self.addService(model, service['name'], service['active'],
                            service['sub'], service['startup type'],
                            service['description'])

        data_layout.addWidget(self.data_view)

        # Add sublayouts to main layout
        outer_layout.addWidget(data_group_box)

        # Set main window layout
        self.setLayout(outer_layout)

    # Initiate service tree model
    def createServiceModel(self, parent):
        model = QStandardItemModel(0, 5)
        model.setHeaderData(0, Qt.Orientation.Horizontal, "Name")
        model.setHeaderData(1, Qt.Orientation.Horizontal, "Activity")
        model.setHeaderData(2, Qt.Orientation.Horizontal, "Status")
        model.setHeaderData(3, Qt.Orientation.Horizontal, "Startup Type")
        model.setHeaderData(4, Qt.Orientation.Horizontal, "Description")
        return model

    # Add service to list
    def addService(self, model, name, active, status, startup, descript):
        model.insertRow(0)
        model.setData(model.index(0, 0), name)
        model.setData(model.index(0, 1), active)
        model.setData(model.index(0, 2), status)
        model.setData(model.index(0, 3), startup)
        model.setData(model.index(0, 4), descript)

    # Right-click action menu
    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        start_act = context_menu.addAction("Start")
        stop_act = context_menu.addAction("Stop")
        enable_act = context_menu.addAction("Enable")
        disable_act = context_menu.addAction("Disable")
        action = context_menu.exec(self.mapToGlobal(event.pos()))
        
        service_name = self.data_view.currentIndex().siblingAtColumn(0).data()
        if action == start_act:
            startService(service_name)
        if action == stop_act:
            stopService(service_name)
        if action == enable_act:
            print(service_name)
        if action == disable_act:
            print(service_name)

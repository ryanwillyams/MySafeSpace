from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QHBoxLayout,
)

from PyQt6.QtCore import Qt

from views.systemCare import SystemCare
from views.automaticBackup import AutomaticBackup


class ServicesPage(QWidget):

    def __init__(self):
        super(ServicesPage, self).__init__()

        # Declare layout
        outer_layout = QHBoxLayout()

        # Define layout
        services = QTabWidget()
        services.setMovable(False)

        # Declare tabs
        system_care = SystemCare()
        auto_backup = AutomaticBackup()

        tab_views = {
            'System Care': system_care,
            'Automatic Backup': auto_backup
        }

        for view_name, view in tab_views.items():
            services.addTab(view, view_name)

        # Add widget to layout
        outer_layout.addWidget(services)

        # Set layout to main window
        self.setLayout(outer_layout)

from PyQt6.QtWidgets import (
    QWidget,QTabWidget,QFormLayout,QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton,QLineEdit,QCheckBox, QSpinBox, QComboBox,
    QListWidget,QListWidgetItem, QScrollBar, QMessageBox, QTreeView
)
from PyQt6.QtCore import Qt

class SystemCare(QWidget):
    def __init__(self):
        super(SystemCare,self).__init__()
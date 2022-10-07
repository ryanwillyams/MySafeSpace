from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

def get_dark_color_theme():
    palette = QPalette()
    qtgc = Qt.GlobalColor
    palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.WindowText, qtgc.white)
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, qtgc.white)
    palette.setColor(QPalette.ColorRole.ToolTipText, qtgc.white)
    palette.setColor(QPalette.ColorRole.Text, qtgc.white)
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, qtgc.white)
    palette.setColor(QPalette.ColorRole.BrightText, qtgc.red)
    palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.ColorRole.HighlightedText, qtgc.black)
    return palette
from Views.MainWindow import MainWindow
from stlye_config import get_dark_color_theme

from PyQt6.QtWidgets import QApplication,QStyle



if __name__ == '__main__':

    ##
    # Get style of application

    app = QApplication([])

    # Force the style to be the same on all OSs:
    app.setStyleSheet("Fusion")
    
    #Set a default Dark theme
    palette = get_dark_color_theme()
    app.setPalette(palette)


    window = MainWindow()
    window.show()

    app.exec()
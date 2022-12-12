import pytest

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QFileDialog

from views.MainWindow import MainWindow


new_window = MainWindow()
new_window.show()


def test_arithemtic_works():
    """Check that the computer isn't bad"""
    assert 1 + 1 == 2

def test_window_title(window):
    """Check that the window title shows as declared."""
    assert window.windowTitle() == 'My Safe Space'


# def test_window_geometry(window):
#     """Check that the window width and height are set as declared."""
#     assert window.width() == 1024
#     assert window.height() == 768

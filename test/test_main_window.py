import pytest

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QFileDialog

from views.MainWindow import MainWindow

@pytest.fixture
def window(qtbot):
    """Pass the application to the test functions via a pytest fixture."""
    new_window = MainWindow()
    qtbot.add_widget(new_window)
    new_window.show()
    return new_window


def test_window_title(window):
    """Check that the window title shows as declared."""
    assert window.windowTitle() == 'My Safe Space'


def test_window_geometry(window):
    """Check that the window width and height are set as declared."""
    assert window.width() == 1024
    assert window.height() == 768

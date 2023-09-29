import os
import sys


from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
)
from PyQt5 import uic

# from pyqtgraph import PlotWidget, plot


class PlanBAI(QMainWindow):
    def __init__(self):
        # Override
        super(PlanBAI, self).__init__()

        # Load UI
        self.load_ui()

        # Define/connect our widgets
        self.buttonBox = self.findChild(QPushButton, "exitButton")
        self.buttonBox.clicked.connect(self.exitCleanly)

        # Show the UI
        self.show()

    def load_ui(self):
        path = os.fspath(
            Path(__file__).resolve().parent / "resources/interface.ui"
        )  # NOQA: E501

        # Load UI frompath
        uic.loadUi(path, self)

    def exitCleanly(self):
        quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = PlanBAI()
    app.exec_()

import os
import sys
import time

import pyqtgraph as pg

from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
)
from PyQt5 import uic
from pyqtgraph import PlotWidget, plot


class PlanBAI(QMainWindow):
    def __init__(self):
        # Override
        super(PlanBAI, self).__init__()

        # Load UI
        self.load_ui()

        # Define/connect our widgets
        self.buttonBox = self.findChild(QPushButton, "exitButton")
        self.buttonBox.clicked.connect(self.exitCleanly)

        self.graphWidget = self.findChild(PlotWidget, "mainGraph")

        # Graph setup
        self.time = [] # Graph data
        self.temperatureReading = []
        self.humidityReading = []

        self.graphWidget.setBackground("w") # Set background color to white.

        # Add Title
        self.graphWidget.setTitle(
            "Climate Air Conditions", color="b", size="16pt"
        )

        # Add Axis Labels
        tempStyle = {"color": "#f00", "font-size": "20px"}
        humidityStyle = {"color": "#00f", "font-size": "20px"}
        self.graphWidget.setLabel("left", "Temperature (°C)", **tempStyle)
        self.graphWidget.setLabel("right", "Humidity (Rh%)", **humidityStyle)
        self.graphWidget.setLabel("bottom", "Epoch (s)", **tempStyle)

        # Add legend
        self.graphWidget.addLegend()

        # Add grid
        self.graphWidget.showGrid(x=True, y=True)

        # Setup plots
        pen = pg.mkPen(color="r")
        self.tempPlot = self.graphWidget.plot(
            self.time,
            self.temperatureReading,
            name="Temp",
            pen=pen,
            symbolSize=3,
            symbolBrush=("r"),
        )
        pen = pg.mkPen(color="b")
        self.humidityPlot = self.graphWidget.plot(
            self.time,
            self.temperatureReading,
            name="Humidity",
            pen=pen,
            symbolSize=3,
            symbolBrush=("b"),
        )

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

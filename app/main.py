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
        self.time = [1, 2, 3, 4, 5]  # Graph data
        self.temperatureReading = [1.1, 1.2, 1.3, 1.4, 1.5]
        self.humidityReading = [0.1, 0.2, 0.3, 0.4, 0.5]

        self.graphWidget.setBackground("w")  # Set background color to white.

        # Add Title
        self.graphWidget.setTitle("Climate Air Conditions", color="b", size="16pt")

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
            self.humidityReading,
            name="Humidity",
            pen=pen,
            symbolSize=3,
            symbolBrush=("b"),
        )

        # Show the UI
        self.show()

    # Loads the UI file (widgets and stuff)
    def load_ui(self):
        path = os.fspath(
            Path(__file__).resolve().parent / "resources/interface.ui"
        )  # NOQA: E501

        # Load UI frompath
        uic.loadUi(path, self)

    # Cleanly exits the program.
    def exitCleanly(self):
        quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = PlanBAI()
    app.exec_()

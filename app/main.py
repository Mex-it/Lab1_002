import os
import sys
import time
import serial

import pyqtgraph as pg

from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
)
from PyQt5.QtCore import QThread, pyqtSignal
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
        self.time = [0]  # Graph data
        self.temperatureReading = [0]
        self.humidityReading = [0]

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

        self.arduino = serial.Serial("/dev/ttyACM0", 115200, timeout=1)

        # Configure polling systems
        self.poller = Poller()
        self.poller.start()
        self.poller.update_arduino.connect(self.logRead)

        # Show the UI
        self.show()

    # Loads the UI file (widgets and stuff)
    def load_ui(self):
        path = os.fspath(
            Path(__file__).resolve().parent / "resources/interface.ui"
        )  # NOQA: E501

        # Load UI frompath
        uic.loadUi(path, self)

    def logRead(self, check_ack=True):
        """
        Reads a line and decodes it but
        also prints it out to the 'console' window.
        """

        try:
            line = str(self.arduino.readline().decode().strip("\n\r"))
            print(f"Read '{line}' as newline.")

            splitLine = line.split(",")
            if len(splitLine) > 1:
                self.time.append(self.time[-1] + 1)  # Last time + 1
                self.temperatureReading.append(float(splitLine[0]))
                self.humidityReading.append(float(splitLine[1]))
                self.show()
        except TypeError as e:
            print(f"Failed to read line! {e}")

        self.tempPlot.setData(self.time, self.temperatureReading)
        self.humidityPlot.setData(self.time, self.humidityReading)
        # self.serialLog.append(line)
        # self.serialLog.verticalScrollBar().setValue(
        #     self.serialLog.verticalScrollBar().maximum()
        # )

    # Cleanly exits the program.
    def exitCleanly(self):
        quit()


class Poller(QThread):
    # Triggers stuff tied to it, has no logic
    update_arduino = pyqtSignal()

    def run(self):
        while True:
            time.sleep(0.1)
            self.update_arduino.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = PlanBAI()
    app.exec_()

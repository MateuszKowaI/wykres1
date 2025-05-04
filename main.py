import sys
from datetime import datetime, timedelta

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class TemperaturePlot(QWidget):
    def __init__(self):
        super().__init__()
        self.hours = [datetime.now() + timedelta(hours=i) for i in range(4)]
        self.temperatures = [20, 21, 19, 22]
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Add matplotlib figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Add form layout
        form_layout = QHBoxLayout()
        self.temp_input = QLineEdit()
        self.temp_input.setPlaceholderText("Temperature (°C)")
        self.hour_input = QLineEdit()
        self.hour_input.setPlaceholderText("Hour from now (e.g., 5)")

        self.add_button = QPushButton("Add Data Point")
        self.add_button.clicked.connect(self.add_data_point)

        form_layout.addWidget(QLabel("Temp:"))
        form_layout.addWidget(self.temp_input)
        form_layout.addWidget(QLabel("Hour:"))
        form_layout.addWidget(self.hour_input)
        form_layout.addWidget(self.add_button)

        layout.addLayout(form_layout)

        # Initial plot
        self.plot_data()

    def plot_data(self):
        self.ax.clear()
        self.ax.plot(self.hours, self.temperatures, marker='o', color='blue', label='Temperature (°C)')
        self.ax.set_title("Temperature Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.tick_params(axis="x", rotation=45)
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def add_data_point(self):
        try:
            temp = float(self.temp_input.text())
            hour_offset = int(self.hour_input.text())
            time_point = datetime.now() + timedelta(hours=hour_offset)

            self.hours.append(time_point)
            self.temperatures.append(temp)

            # Sort the data by time for consistent plotting
            combined = sorted(zip(self.hours, self.temperatures), key=lambda x: x[0])
            self.hours, self.temperatures = zip(*combined)
            self.hours = list(self.hours)
            self.temperatures = list(self.temperatures)

            self.plot_data()

            # Clear inputs
            self.temp_input.clear()
            self.hour_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number for both fields.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Temperature Plot")
        self.setGeometry(100, 100, 900, 600)

        self.plot_widget = TemperaturePlot()
        self.setCentralWidget(self.plot_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

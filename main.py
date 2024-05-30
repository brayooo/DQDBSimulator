import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QFrame
from DQDBSimulator import DQDBSimulator
from RingTopology import RingTopology
from UserControls import UserControls

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('DQDB Simulator')
        self.setGeometry(100, 100, 1000, 600)  # Adjusted window size

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        # Left side for controls
        self.controls = UserControls()
        self.layout.addWidget(self.controls)

        # Add vertical line
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.line)

        # Right side for simulator and other elements
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_widget.setLayout(self.right_layout)

        # Add top right double ring topology animation
        self.ring_topology = RingTopology()
        self.right_layout.addWidget(self.ring_topology)

        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setMaximumHeight(100)

        self.simulator = DQDBSimulator(self.log_widget, self.controls.speed_slider)

        self.right_layout.addWidget(self.simulator)
        self.right_layout.addWidget(self.log_widget)

        self.layout.addWidget(self.right_widget)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

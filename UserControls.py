from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt6.QtCore import Qt

class UserControls(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Speed slider
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(10)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(50)
        self.speed_slider.setTickInterval(10)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel('Speed:'))
        slider_layout.addWidget(self.speed_slider)
        slider_widget = QWidget()
        slider_widget.setLayout(slider_layout)
        slider_widget.setMaximumHeight(50)

        self.layout.addWidget(slider_widget)

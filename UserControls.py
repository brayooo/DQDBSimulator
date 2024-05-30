from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QComboBox
from PyQt6.QtCore import Qt
class UserControls(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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

        # Start button
        self.start_button = QPushButton('Start Simulation')
        self.start_button.clicked.connect(self.main_window.start_simulation)

        # Stop button
        self.stop_button = QPushButton('Stop Simulation')
        self.stop_button.clicked.connect(self.main_window.stop_simulation)

        # Reset button
        self.reset_button = QPushButton('Reset Simulation')
        self.reset_button.clicked.connect(self.main_window.reset_simulation)

        # Custom slot selection
        self.start_node_combo = QComboBox()
        self.end_node_combo = QComboBox()
        self.bus_combo = QComboBox()
        self.bus_combo.addItem('Bus A', 'A')
        self.bus_combo.addItem('Bus B', 'B')
        for i in range(1, 6):  # Assuming 5 nodes
            self.start_node_combo.addItem(f'Node {i}', i - 1)
            self.end_node_combo.addItem(f'Node {i}', i - 1)

        self.custom_slot_button = QPushButton('Set Custom Slots')
        self.custom_slot_button.clicked.connect(self.set_custom_slots)

        custom_slot_layout = QVBoxLayout()
        custom_slot_layout.addWidget(QLabel('Start Node:'))
        custom_slot_layout.addWidget(self.start_node_combo)
        custom_slot_layout.addWidget(QLabel('End Node:'))
        custom_slot_layout.addWidget(self.end_node_combo)
        custom_slot_layout.addWidget(QLabel('Bus:'))
        custom_slot_layout.addWidget(self.bus_combo)
        custom_slot_layout.addWidget(self.custom_slot_button)
        custom_slot_widget = QWidget()
        custom_slot_widget.setLayout(custom_slot_layout)

        # Add widgets to layout
        self.layout.addWidget(slider_widget)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(custom_slot_widget)

    def set_custom_slots(self):
        start_node = self.start_node_combo.currentData()
        end_node = self.end_node_combo.currentData()
        bus = self.bus_combo.currentData()
        self.main_window.set_custom_slots(start_node, end_node, bus)

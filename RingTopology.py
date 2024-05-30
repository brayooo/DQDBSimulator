import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QTimer
import math


class RingTopology(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 200)  # Ensure the widget has a minimum size
        self.node_positions_outer = [(i, 0) for i in range(8)]  # (angle index, angle offset) for outer ring
        self.node_positions_inner = [(i, 0) for i in range(8)]  # (angle index, angle offset) for inner ring
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_positions)
        self.timer.start(100)  # Update positions every 100 ms

    def update_positions(self):
        self.node_positions_outer = [(i, (offset + 1) % 360) for i, offset in self.node_positions_outer]
        self.node_positions_inner = [(i, (offset - 1) % 360) for i, offset in self.node_positions_inner]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.fillRect(self.rect(), QColor(128, 128, 128))  # Fill the background with white color
        self.draw_ring_topology(painter)

    def draw_ring_topology(self, painter):
        center_x, center_y = self.width() // 2, self.height() // 2
        outer_radius = min(self.width(), self.height()) // 3 # Larger outer radius
        inner_radius = min(self.width(), self.height()) // 6.5 # Smaller inner radius
        painter.setPen(QPen(Qt.GlobalColor.black, 2))

        # Outer ring
        painter.drawEllipse(center_x - outer_radius, center_y - outer_radius, outer_radius * 2, outer_radius * 2)
        # Inner ring
        painter.drawEllipse(center_x - inner_radius, center_y - inner_radius, inner_radius * 2, inner_radius * 2)

        # Nodes on the outer ring
        for angle_index, angle_offset in self.node_positions_outer:
            angle = angle_index * (360 / 8) + angle_offset
            rad = angle * (math.pi / 180)
            node_x = int(center_x + outer_radius * math.cos(rad))  # Convert to int
            node_y = int(center_y + outer_radius * math.sin(rad))  # Convert to int
            painter.setBrush(QColor(0, 128, 0))  # Set color for outer nodes
            painter.drawRect(node_x - 5, node_y - 5, 10, 10)  # Draw square nodes

        # Nodes on the inner ring
        for angle_index, angle_offset in self.node_positions_inner:
            angle = angle_index * (360 / 8) + angle_offset
            rad = angle * (math.pi / 180)
            node_x = int(center_x + inner_radius * math.cos(rad))  # Convert to int
            node_y = int(center_y + inner_radius * math.sin(rad))  # Convert to int
            painter.setBrush(QColor(255, 0, 0))  # Set color for inner nodes
            painter.drawRect(node_x - 5, node_y - 5, 10, 10)  # Draw square nodes

        # Central nodes
        pentagon_radius = inner_radius // 2  # Radius for the pentagon
        pentagon_angles = [i * (360 / 5) for i in range(5)] # Angles for the pentagon nodes
        painter.setBrush(QColor(0, 0, 0))  # Set color for central nodes

        for angle in pentagon_angles:
            rad = angle * (math.pi / 180) # Convert to radians
            node_x = int(center_x + pentagon_radius * math.cos(rad) * 3.3)  # Convert to int
            node_y = int(center_y + pentagon_radius * math.sin(rad) * 3.3)  # Convert to int
            painter.drawRect(node_x - 5, node_y - 5, 20, 20) # Draw square nodes

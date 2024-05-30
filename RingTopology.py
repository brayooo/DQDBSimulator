import sys
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QTimer
import math

class RingTopology(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 200)
        self.node_positions_outer = [(i, 0) for i in range(8)]
        self.node_positions_inner = [(i, 0) for i in range(8)]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_positions)
        self.timer.start(100)  # Update positions every 100 ms

        self.topology_title = QLabel("Topología", self)
        self.topology_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topology_title.resize(self.width(), 40)
        self.topology_title.setStyleSheet("font-size: 32px; font-weight: bold;")

    def resizeEvent(self, event):
        self.topology_title.resize(self.width(), 40)
        self.topology_title.move(0, 0)

    def update_positions(self):
        self.node_positions_outer = [(i, (offset + 1) % 360) for i, offset in self.node_positions_outer]
        self.node_positions_inner = [(i, (offset - 1) % 360) for i, offset in self.node_positions_inner]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_ring_topology(painter)

    def draw_ring_topology(self, painter):
        center_x, center_y = self.width() // 2, self.height() // 1.6
        outer_radius = min(self.width(), self.height()) // 3
        inner_radius = min(self.width(), self.height()) // 6.5
        painter.setPen(QPen(Qt.GlobalColor.black, 2))

        painter.drawEllipse(center_x - outer_radius, center_y - outer_radius, outer_radius * 2, outer_radius * 2)
        painter.drawEllipse(center_x - inner_radius, center_y - inner_radius, inner_radius * 2, inner_radius * 2)

        for angle_index, angle_offset in self.node_positions_outer:
            angle = angle_index * (360 / 8) + angle_offset
            rad = angle * (math.pi / 180)
            node_x = int(center_x + outer_radius * math.cos(rad))
            node_y = int(center_y + outer_radius * math.sin(rad))
            painter.setBrush(QColor(255, 215, 0))
            painter.drawRect(node_x - 5, node_y - 5, 10, 10)

        for angle_index, angle_offset in self.node_positions_inner:
            angle = angle_index * (360 / 8) + angle_offset
            rad = angle * (math.pi / 180)
            node_x = int(center_x + inner_radius * math.cos(rad))
            node_y = int(center_y + inner_radius * math.sin(rad))
            painter.setBrush(QColor(255, 215, 0))
            painter.drawRect(node_x - 5, node_y - 5, 10, 10)
        pentagon_radius = inner_radius // 2
        pentagon_angles = [i * (360 / 5) for i in range(5)]
        painter.setBrush(QColor(0, 128, 0))
        for angle in pentagon_angles:
            rad = angle * (math.pi / 180)
            node_x = int(center_x + pentagon_radius * math.cos(rad) * 3.3)
            node_y = int(center_y + pentagon_radius * math.sin(rad) * 3.3)
            painter.drawRect(node_x - 5, node_y - 5, 20, 20)

import sys
import random
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QTextEdit, QSlider, QHBoxLayout


class DQDBSimulator(QWidget):
    MAX_SLOTS = 4  # Limiting the number of active slots

    def __init__(self, log_widget, speed_slider):
        super().__init__()
        self.nodos = [(100, 200), (200, 200), (300, 200), (400, 200), (500, 200)]
        self.node_functions = [random.choice(['send', 'receive']) for _ in self.nodos]
        self.node_status = ["Idle"] * len(self.nodos)  # Initialize node status as "Idle"
        self.bus_a = [(50, 150), (550, 150)]
        self.bus_b = [(50, 250), (550, 250)]
        self.slots = []
        self.slots_to_remove = []
        self.log_widget = log_widget
        self.speed_slider = speed_slider
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('DQDB Simulator')
        self.setGeometry(100, 100, 800, 600)  # Adjusted window size
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.spawn_slot)
        self.timer.start(5000)  # Spawn a new slot every 5 seconds

        # Connect the slider value change to update the speed of all slots
        self.speed_slider.valueChanged.connect(self.update_slot_speeds)

    def spawn_slot(self):
        if len(self.slots) < self.MAX_SLOTS:
            # Decide randomly if the slot will be in bus A or bus B
            bus = random.choice(['A', 'B'])
            if bus == 'A':
                slot = {'position': [50, 150], 'direction': 'forward', 'current_node': 0, 'bus': 'A'}
            else:
                slot = {'position': [550, 250], 'direction': 'backward', 'current_node': len(self.nodos) - 1,
                        'bus': 'B'}
            self.slots.append(slot)
            self.log_widget.append(f"New slot spawned in bus {bus}")
            # Create a timer for the new slot
            slot_timer = QTimer(self)
            slot_timer.timeout.connect(lambda s=slot: self.update_simulation(s))
            slot_timer.start(self.speed_slider.value())  # Update based on slider value
            slot['timer'] = slot_timer

    def update_simulation(self, slot):
        log_msg = ""
        if slot['bus'] == 'A':
            log_msg = self.update_slot_a(slot)
        else:
            log_msg = self.update_slot_b(slot)

        if log_msg:
            self.log_widget.append(log_msg)

        self.update()

    def update_slot_a(self, slot):
        log_msg = ""
        # Move the slot position in bus A
        if slot['direction'] == 'forward':
            if slot['position'][0] < self.nodos[slot['current_node']][0]:
                slot['position'][0] += 2
            else:
                slot['direction'] = 'down'
                log_msg = f"Slot entering node C{slot['current_node'] + 1} ({self.node_functions[slot['current_node']]})"
                self.node_status[slot['current_node']] = "Processing"
        elif slot['direction'] == 'down':
            if slot['position'][1] < self.nodos[slot['current_node']][1]:
                slot['position'][1] += 2
            else:
                if self.node_functions[slot['current_node']] == 'receive':
                    log_msg = f"Node C{slot['current_node'] + 1} is receiving the slot. Slot is removed."
                    self.slots_to_remove.append(slot)
                    slot['timer'].stop()
                    self.node_status[slot['current_node']] = "Received"
                else:
                    log_msg = f"Node C{slot['current_node'] + 1} is sending data"
                    self.node_status[slot['current_node']] = "Sending"
                slot['direction'] = 'up'
        elif slot['direction'] == 'up':
            if slot['position'][1] > self.bus_a[0][1]:
                slot['position'][1] -= 2
            else:
                slot['direction'] = 'forward'
                log_msg = f"Slot exiting node C{slot['current_node'] + 1}"
                slot['current_node'] = (slot['current_node'] + 1) % len(self.nodos)
                self.node_status[slot['current_node']] = "Idle"
                if slot['current_node'] == 0:
                    slot['position'] = [50, 150]
                else:
                    slot['position'][0] = self.nodos[slot['current_node'] - 1][0]
        return log_msg

    def update_slot_b(self, slot):
        log_msg = ""
        # Move the slot position in bus B
        if slot['direction'] == 'backward':
            if slot['position'][0] > self.nodos[slot['current_node']][0]:
                slot['position'][0] -= 2
            else:
                slot['direction'] = 'up'
                log_msg = f"Slot entering node C{slot['current_node'] + 1} ({self.node_functions[slot['current_node']]})"
                self.node_status[slot['current_node']] = "Processing"
        elif slot['direction'] == 'up':
            if slot['position'][1] > self.nodos[slot['current_node']][1]:
                slot['position'][1] -= 2
            else:
                if self.node_functions[slot['current_node']] == 'receive':
                    log_msg = f"Node C{slot['current_node'] + 1} is receiving the slot. Slot is removed."
                    self.slots_to_remove.append(slot)
                    slot['timer'].stop()
                    self.node_status[slot['current_node']] = "Received"
                else:
                    log_msg = f"Node C{slot['current_node'] + 1} is sending data"
                    self.node_status[slot['current_node']] = "Sending"
                slot['direction'] = 'down'
        elif slot['direction'] == 'down':
            if slot['position'][1] < self.bus_b[0][1]:
                slot['position'][1] += 2
            else:
                slot['direction'] = 'backward'
                log_msg = f"Slot exiting node C{slot['current_node'] + 1}"
                slot['current_node'] = (slot['current_node'] - 1 + len(self.nodos)) % len(self.nodos)
                self.node_status[slot['current_node']] = "Idle"
                if slot['current_node'] == len(self.nodos) - 1:
                    slot['position'] = [550, 250]
                else:
                    slot['position'][0] = self.nodos[slot['current_node'] + 1][0]
        return log_msg

    def update_slot_speeds(self):
        for slot in self.slots:
            slot['timer'].start(self.speed_slider.value())

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_bus(painter)
        self.draw_nodos(painter)
        self.draw_slots(painter)
        self.draw_node_status(painter)

    def draw_bus(self, painter):
        pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.drawLine(*self.bus_a[0], *self.bus_a[1])
        painter.drawLine(*self.bus_b[0], *self.bus_b[1])

    def draw_nodos(self, painter):
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(QColor(0, 128, 0))  # Dark green color
        font = QFont('Arial', 10, QFont.Weight.Bold)
        painter.setFont(font)
        for x, y in self.nodos:
            painter.drawRect(x - 20, y - 20, 40, 40)
            painter.drawText(x - 10, y, 'C{}'.format(self.nodos.index((x, y)) + 1))

    def draw_node_status(self, painter):
        font = QFont('Arial', 8)
        painter.setFont(font)
        for i, (x, y) in enumerate(self.nodos):
            painter.drawText(x - 30, y + 50, self.node_status[i])

    def draw_slots(self, painter):
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(QColor(255, 215, 0))  # Gold color
        for slot in self.slots:
            painter.drawRect(slot['position'][0] - 10, slot['position'][1] - 10, 20, 20)
            painter.drawText(slot['position'][0] - 5, slot['position'][1] + 5, 'Slot')

    def update(self):
        super().update()
        if self.slots_to_remove:
            for slot in self.slots_to_remove:
                if slot in self.slots:
                    self.slots.remove(slot)
            self.slots_to_remove.clear()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('DQDB Simulator')
        self.setGeometry(100, 100, 800, 600)  # Adjusted window size

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setMaximumHeight(150)

        speed_slider_widget = self.create_speed_slider()

        self.simulator = DQDBSimulator(self.log_widget, self.speed_slider)

        self.layout.addWidget(self.simulator)
        self.layout.addWidget(speed_slider_widget)
        self.layout.addWidget(self.log_widget)

    def create_speed_slider(self):
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

        return slider_widget


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

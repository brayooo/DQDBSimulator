import random
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtWidgets import QWidget

class DQDBSimulator(QWidget):
    MAX_SLOTS = 4  # Limiting the number of active slots

    def __init__(self, log_widget, speed_slider):
        super().__init__()
        self.nodos = [(100, 200), (200, 200), (300, 200), (400, 200), (500, 200)]
        self.node_functions = [random.choice(['send', 'receive']) for _ in self.nodos]
        self.node_status = ["Idle"] * len(self.nodos)  # Initialize node status as "Idle"
        self.node_colors = ["base"] * len(self.nodos)  # Initialize node colors as "base"
        self.bus_a = [(50, 150), (550, 150)]
        self.bus_b = [(50, 250), (550, 250)]
        self.slots = []
        self.slots_to_remove = []
        self.log_widget = log_widget
        self.speed_slider = speed_slider
        self.init_ui()

    def init_ui(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.spawn_slot)
        self.timer.start(5000)  # Spawn a new slot every 5 seconds

        # Connect the slider value change to update the speed of all slots
        self.speed_slider.valueChanged.connect(self.update_slot_speeds)

    def spawn_slot(self):
        if len(self.slots) < self.MAX_SLOTS:
            # Decide randomly if the slot will be in bus A or bus B
            bus = random.choice(['A', 'B'])
            slot_type = random.choice(['send', 'receive'])  # Randomly decide if the slot is for send or receive
            if bus == 'A':
                slot = {'position': [50, 150], 'direction': 'forward', 'current_node': 0, 'bus': 'A', 'type': slot_type, 'received': False}
            else:
                slot = {'position': [550, 250], 'direction': 'backward', 'current_node': len(self.nodos) - 1, 'bus': 'B', 'type': slot_type, 'received': False}
            self.slots.append(slot)
            self.log_widget.append(f"New {slot_type} slot spawned in bus {bus}")
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
                self.node_colors[slot['current_node']] = "processing"
        elif slot['direction'] == 'down':
            if slot['position'][1] < self.nodos[slot['current_node']][1]:
                slot['position'][1] += 2
            else:
                if self.node_functions[slot['current_node']] == 'receive' and slot['type'] == 'receive':
                    log_msg = f"Node C{slot['current_node'] + 1} is receiving the slot."
                    slot['received'] = True
                    self.node_status[slot['current_node']] = "Received"
                    self.node_colors[slot['current_node']] = "received"
                else:
                    log_msg = f"Node C{slot['current_node'] + 1} is sending data"
                    self.node_status[slot['current_node']] = "Sending"
                    self.node_colors[slot['current_node']] = "sending"
                slot['direction'] = 'up'
        elif slot['direction'] == 'up':
            if slot['position'][1] > self.bus_a[0][1]:
                slot['position'][1] -= 2
            else:
                slot['direction'] = 'forward'
                log_msg = f"Slot exiting node C{slot['current_node'] + 1}"
                slot['current_node'] = (slot['current_node'] + 1) % len(self.nodos)
                self.node_status[slot['current_node']] = "Idle"
                self.node_colors[slot['current_node']] = "base"
                if slot['current_node'] == 0 and slot.get('received'):
                    self.slots_to_remove.append(slot)
                    slot['timer'].stop()
                elif slot['current_node'] == 0:
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
                self.node_colors[slot['current_node']] = "processing"
        elif slot['direction'] == 'up':
            if slot['position'][1] > self.nodos[slot['current_node']][1]:
                slot['position'][1] -= 2
            else:
                if self.node_functions[slot['current_node']] == 'receive' and slot['type'] == 'receive':
                    log_msg = f"Node C{slot['current_node'] + 1} is receiving the slot."
                    slot['received'] = True
                    self.node_status[slot['current_node']] = "Received"
                    self.node_colors[slot['current_node']] = "received"
                else:
                    log_msg = f"Node C{slot['current_node'] + 1} is sending data"
                    self.node_status[slot['current_node']] = "Sending"
                    self.node_colors[slot['current_node']] = "sending"
                slot['direction'] = 'down'
        elif slot['direction'] == 'down':
            if slot['position'][1] < self.bus_b[0][1]:
                slot['position'][1] += 2
            else:
                slot['direction'] = 'backward'
                log_msg = f"Slot exiting node C{slot['current_node'] + 1}"
                slot['current_node'] = (slot['current_node'] - 1 + len(self.nodos)) % len(self.nodos)
                self.node_status[slot['current_node']] = "Idle"
                self.node_colors[slot['current_node']] = "base"
                if slot['current_node'] == len(self.nodos) - 1 and slot.get('received'):
                    self.slots_to_remove.append(slot)
                    slot['timer'].stop()
                elif slot['current_node'] == len(self.nodos) - 1:
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
        pen = QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.drawLine(*self.bus_a[0], *self.bus_a[1])
        painter.drawLine(*self.bus_b[0], *self.bus_b[1])

    def draw_nodos(self, painter):
        for i, (x, y) in enumerate(self.nodos):
            if self.node_colors[i] == "base":
                painter.setBrush(QColor(0, 128, 0))  # Dark green color
            elif self.node_colors[i] == "processing":
                painter.setBrush(QColor(255, 255, 0))  # Yellow for processing
            elif self.node_colors[i] == "sending":
                painter.setBrush(QColor(0, 0, 255))  # Blue for sending
            elif self.node_colors[i] == "received":
                painter.setBrush(QColor(255, 0, 0))  # Red for receiving
            painter.setPen(Qt.GlobalColor.black)
            painter.drawRect(x - 20, y - 20, 40, 40)
            painter.drawText(x - 10, y, 'C{}'.format(i + 1))

    def draw_node_status(self, painter):
        font = QFont('Arial', 8)
        painter.setFont(font)
        for i, (x, y) in enumerate(self.nodos):
            painter.drawText(x - 30, y + 50, self.node_status[i])

    def draw_slots(self, painter):
        for slot in self.slots:
            painter.setBrush(QColor(255, 215, 0))  # Gold color for all slots
            painter.setPen(Qt.GlobalColor.black)
            painter.drawRect(slot['position'][0] - 10, slot['position'][1] - 10, 20, 20)
            painter.drawText(slot['position'][0] - 5, slot['position'][1] + 5, 'Slot')

    def update(self):
        super().update()
        if self.slots_to_remove:
            for slot in self.slots_to_remove:
                if slot in self.slots:
                    self.slots.remove(slot)
            self.slots_to_remove.clear()

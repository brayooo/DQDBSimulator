import random
from PyQt6.QtCore import QTimer

class CustomSimulationLogic:
    MAX_SLOTS = 4  # Limiting the number of active slots

    def __init__(self, dqdb_simulator):
        self.simulator = dqdb_simulator
        self.custom_start_node = 0
        self.custom_end_node = 0
        self.selected_bus = 'A'
        self.timer = QTimer(self.simulator)
        self.timer.timeout.connect(self.spawn_custom_slot)

    def set_custom_parameters(self, start_node, end_node, bus):
        self.custom_start_node = start_node
        self.custom_end_node = end_node
        self.selected_bus = bus

    def start_custom_simulation(self):
        self.timer.start(5000)  # Spawn a new slot every 5 seconds

    def stop_custom_simulation(self):
        self.timer.stop()

    def spawn_custom_slot(self):
        if len(self.simulator.slots) < self.MAX_SLOTS:
            slot_type = 'send'  # Custom slots are always of type 'send'
            start_x, start_y = self.simulator.nodos[self.custom_start_node]
            end_x, end_y = self.simulator.nodos[self.custom_end_node]
            if self.selected_bus == 'A':
                slot = {
                    'position': [start_x, 150],
                    'direction': 'forward',
                    'current_node': self.custom_start_node,
                    'bus': 'A',
                    'type': slot_type,
                    'received': False,
                    'end_position': [end_x, 150]  # Endpoint on bus A
                }
            else:
                slot = {
                    'position': [start_x, 250],
                    'direction': 'backward',
                    'current_node': self.custom_start_node,
                    'bus': 'B',
                    'type': slot_type,
                    'received': False,
                    'end_position': [end_x, 250]  # Endpoint on bus B
                }
            self.simulator.slots.append(slot)
            self.simulator.log_widget.append(f"Custom slot spawned from Node {self.custom_start_node + 1} to Node {self.custom_end_node + 1} on bus {self.selected_bus}")
            # Create a timer for the new slot
            slot_timer = QTimer(self.simulator)
            slot_timer.timeout.connect(lambda s=slot: self.update_custom_simulation(s))
            slot_timer.start(self.simulator.speed_slider.value())  # Update based on slider value
            slot['timer'] = slot_timer

    def update_custom_simulation(self, slot):
        if slot['bus'] == 'A':
            log_msg = self.update_slot_a(slot)
        else:
            log_msg = self.update_slot_b(slot)

        if log_msg:
            self.simulator.log_widget.append(log_msg)

        self.simulator.update()

        if slot['current_node'] == self.custom_end_node and slot['received']:
            slot['timer'].stop()
            self.simulator.slots_to_remove.append(slot)
            self.simulator.update()

    def update_slot_a(self, slot):
        log_msg = ""
        if slot['direction'] == 'forward':
            if slot['position'][0] < self.simulator.nodos[slot['current_node']][0]:
                slot['position'][0] += 2
            else:
                slot['direction'] = 'down'
                self.simulator.node_status[slot['current_node']] = "Processing"
                self.simulator.node_colors[slot['current_node']] = "processing"
                log_msg = f"Slot entering node C{slot['current_node'] + 1} ({self.simulator.node_functions[slot['current_node']]})"
        elif slot['direction'] == 'down':
            if slot['position'][1] < self.simulator.nodos[slot['current_node']][1]:
                slot['position'][1] += 2
            else:
                slot['direction'] = 'up'
                if slot['current_node'] == self.custom_end_node:
                    if self.simulator.node_functions[slot['current_node']] == 'receive':
                        log_msg = f"Node C{slot['current_node'] + 1} received the slot."
                        slot['received'] = True
                        self.simulator.node_status[slot['current_node']] = "Received"
                        self.simulator.node_colors[slot['current_node']] = "received"
                    else:
                        log_msg = f"Node C{slot['current_node'] + 1} sent the slot."
                        self.simulator.node_status[slot['current_node']] = "Sending"
                        self.simulator.node_colors[slot['current_node']] = "sending"
                else:
                    log_msg = f"Slot passing through node C{slot['current_node'] + 1}"
                slot['direction'] = 'up'
        elif slot['direction'] == 'up':
            if slot['position'][1] > 150:
                slot['position'][1] -= 2
            else:
                slot['direction'] = 'forward'
                self.simulator.node_status[slot['current_node']] = "Idle"
                self.simulator.node_colors[slot['current_node']] = "base"
                if slot['current_node'] != self.custom_end_node:
                    slot['current_node'] += 1
                    slot['direction'] = 'forward'
        return log_msg

    def update_slot_b(self, slot):
        log_msg = ""
        if slot['direction'] == 'backward':
            if slot['position'][0] > self.simulator.nodos[slot['current_node']][0]:
                slot['position'][0] -= 2
            else:
                slot['direction'] = 'up'
                self.simulator.node_status[slot['current_node']] = "Processing"
                self.simulator.node_colors[slot['current_node']] = "processing"
                log_msg = f"Slot entering node C{slot['current_node'] + 1} ({self.simulator.node_functions[slot['current_node']]})"
        elif slot['direction'] == 'up':
            if slot['position'][1] > self.simulator.nodos[slot['current_node']][1]:
                slot['position'][1] -= 2
            else:
                slot['direction'] = 'down'
                if slot['current_node'] == self.custom_end_node:
                    if self.simulator.node_functions[slot['current_node']] == 'receive':
                        log_msg = f"Node C{slot['current_node'] + 1} received the slot."
                        slot['received'] = True
                        self.simulator.node_status[slot['current_node']] = "Received"
                        self.simulator.node_colors[slot['current_node']] = "received"
                    else:
                        log_msg = f"Node C{slot['current_node'] + 1} sent the slot."
                        self.simulator.node_status[slot['current_node']] = "Sending"
                        self.simulator.node_colors[slot['current_node']] = "sending"
                else:
                    log_msg = f"Slot passing through node C{slot['current_node'] + 1}"
                slot['direction'] = 'down'
        elif slot['direction'] == 'down':
            if slot['position'][1] < 250:
                slot['position'][1] += 2
            else:
                slot['direction'] = 'backward'
                self.simulator.node_status[slot['current_node']] = "Idle"
                self.simulator.node_colors[slot['current_node']] = "base"
                if slot['current_node'] != self.custom_end_node:
                    slot['current_node'] -= 1
                    slot['direction'] = 'backward'
        return log_msg

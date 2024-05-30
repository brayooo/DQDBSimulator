import random
from PyQt6.QtCore import QTimer

class CustomSimulationLogic:
    MAX_SLOTS = 4
    def __init__(self, dqdb_simulator):
        self.simulator = dqdb_simulator
        self.custom_start_node = 0
        self.custom_end_node = 0
        self.timer = QTimer(self.simulator)
        self.timer.timeout.connect(self.spawn_custom_slot)
        self.initialized = False

    def set_custom_parameters(self, start_node, end_node):
        self.custom_start_node = start_node
        self.custom_end_node = end_node

    def start_custom_simulation(self):
        if not self.initialized:
            self.simulator.log_widget.append(
                f"Custom slot spawned desde el Node {self.custom_start_node + 1} al Node {self.custom_end_node + 1}")
            self.initialized = True
        self.timer.start(5000)

    def stop_custom_simulation(self):
        self.timer.stop()

    def spawn_custom_slot(self):
        if len(self.simulator.slots) < self.MAX_SLOTS:
            slot_a = {
                'position': [50, 150],
                'direction': 'forward',
                'current_node': 0,
                'bus': 'A',
                'type': 'send',
                'received': False,
                'custom': True,
                'start_node': self.custom_start_node,
                'end_node': self.custom_end_node
            }

            slot_b = {
                'position': [550, 250],
                'direction': 'backward',
                'current_node': len(self.simulator.nodos) - 1,
                'bus': 'B',
                'type': 'receive',
                'received': False,
                'custom': True,
                'start_node': self.custom_end_node,
                'end_node': self.custom_start_node
            }

            self.simulator.slots.append(slot_a)
            self.simulator.slots.append(slot_b)

            # Create timers for the new slots
            slot_a_timer = QTimer(self.simulator)
            slot_a_timer.timeout.connect(lambda s=slot_a: self.update_custom_simulation(s))
            slot_a_timer.start(50)  # Update based on a fixed value
            slot_a['timer'] = slot_a_timer

            slot_b_timer = QTimer(self.simulator)
            slot_b_timer.timeout.connect(lambda s=slot_b: self.update_custom_simulation(s))
            slot_b_timer.start(50)  # Update based on a fixed value
            slot_b['timer'] = slot_b_timer

    def update_custom_simulation(self, slot):
        log_msg = self.update_slot(slot)

        if log_msg:
            self.simulator.log_widget.append(log_msg)

        self.simulator.update()

    def update_slot(self, slot):
        log_msg = ""
        if slot['bus'] == 'A':
            log_msg = self.update_slot_a(slot)
        elif slot['bus'] == 'B':
            log_msg = self.update_slot_b(slot)

        return log_msg

    def update_slot_a(self, slot):
        log_msg = ""
        if slot['direction'] == 'forward':
            if slot['position'][0] < self.simulator.nodos[slot['current_node']][0]:
                slot['position'][0] += 2
            else:
                slot['direction'] = 'down'
                if (slot['current_node'] == slot['start_node'] and slot['start_node'] < slot['end_node']) or (
                        slot['current_node'] == slot['end_node'] and slot['start_node'] < slot['end_node']):
                    self.simulator.node_status[slot['current_node']] = "Procesando"
                    self.simulator.node_colors[slot['current_node']] = "custom"
                    log_msg = f"Slot entrando en el nodo C{slot['current_node'] + 1} ({self.simulator.node_functions[slot['current_node']]})"
        elif slot['direction'] == 'down':
            if slot['position'][1] < self.simulator.nodos[slot['current_node']][1]:
                slot['position'][1] += 2
            else:
                slot['direction'] = 'up'
                if slot['current_node'] == slot['end_node'] and slot['start_node'] < slot['end_node']:
                    if self.simulator.node_functions[slot['current_node']] == 'receive':
                        log_msg = f"Node C{slot['current_node'] + 1} received the slot."
                        slot['received'] = True
                        self.simulator.node_status[slot['current_node']] = "Recibido"
                        self.simulator.node_colors[slot['current_node']] = "custom"
                    else:
                        log_msg = f"Node C{slot['current_node'] + 1} sent the slot."
                        self.simulator.node_status[slot['current_node']] = "Enviando"
                        self.simulator.node_colors[slot['current_node']] = "custom"
                else:
                    log_msg = f"Slot pasando por el nodo C{slot['current_node'] + 1}"
                slot['direction'] = 'up'
        elif slot['direction'] == 'up':
            if slot['position'][1] > 150:
                slot['position'][1] -= 2
            else:
                slot['direction'] = 'forward'
                if (slot['current_node'] == slot['start_node'] and slot['start_node'] < slot['end_node']) or (
                        slot['current_node'] == slot['end_node'] and slot['start_node'] < slot['end_node']):
                    self.simulator.node_status[slot['current_node']] = "Idle"
                    self.simulator.node_colors[slot['current_node']] = "base"
                slot['current_node'] = (slot['current_node'] + 1) % len(self.simulator.nodos)
                if slot['current_node'] == 0 and slot.get('received'):
                    self.simulator.slots_to_remove.append(slot)
                    slot['timer'].stop()
                elif slot['current_node'] == 0:
                    slot['position'][0] = 50
                else:
                    slot['position'][0] = self.simulator.nodos[slot['current_node'] - 1][0]
        return log_msg

    def update_slot_b(self, slot):
        log_msg = ""
        if slot['direction'] == 'backward':
            if slot['position'][0] > self.simulator.nodos[slot['current_node']][0]:
                slot['position'][0] -= 2
            else:
                slot['direction'] = 'up'
                if (slot['current_node'] == slot['start_node'] and slot['start_node'] < slot['end_node']) or (
                        slot['current_node'] == slot['end_node'] and slot['start_node'] < slot['end_node']):
                    self.simulator.node_status[slot['current_node']] = "Procesando"
                    self.simulator.node_colors[slot['current_node']] = "custom"
                    log_msg = f"Slot entrando en el nodo C{slot['current_node'] + 1} ({self.simulator.node_functions[slot['current_node']]})"
        elif slot['direction'] == 'up':
            if slot['position'][1] > self.simulator.nodos[slot['current_node']][1]:
                slot['position'][1] -= 2
            else:
                slot['direction'] = 'down'
                if slot['current_node'] == slot['end_node'] and slot['start_node'] < slot['end_node']:
                    if self.simulator.node_functions[slot['current_node']] == 'receive':
                        log_msg = f"Node C{slot['current_node'] + 1} received the slot."
                        slot['received'] = True
                        self.simulator.node_status[slot['current_node']] = "Recibido"
                        self.simulator.node_colors[slot['current_node']] = "custom"
                    else:
                        log_msg = f"Node C{slot['current_node'] + 1} sent the slot."
                        self.simulator.node_status[slot['current_node']] = "Enviando"
                        self.simulator.node_colors[slot['current_node']] = "custom"
                else:
                    log_msg = f"Slot pasando por el nodo C{slot['current_node'] + 1}"
                slot['direction'] = 'down'
        elif slot['direction'] == 'down':
            if slot['position'][1] < 250:
                slot['position'][1] += 2
            else:
                slot['direction'] = 'backward'
                if (slot['current_node'] == slot['start_node'] and slot['start_node'] < slot['end_node']) or (
                        slot['current_node'] == slot['end_node'] and slot['start_node'] < slot['end_node']):
                    self.simulator.node_status[slot['current_node']] = "Idle"
                    self.simulator.node_colors[slot['current_node']] = "base"
                slot['current_node'] = (slot['current_node'] - 1 + len(self.simulator.nodos)) % len(self.simulator.nodos)
                if slot['current_node'] == len(self.simulator.nodos) - 1 and slot.get('received'):
                    self.simulator.slots_to_remove.append(slot)
                    slot['timer'].stop()
                elif slot['current_node'] == len(self.simulator.nodos) - 1:
                    slot['position'][0] = 550
                else:
                    slot['position'][0] = self.simulator.nodos[slot['current_node'] + 1][0]
        return log_msg

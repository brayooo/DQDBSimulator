from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox

class UserControls(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.start_button = QPushButton('Iniciar Simulación')
        self.start_button.clicked.connect(self.main_window.start_simulation)

        self.stop_button = QPushButton('Detener Simulación')
        self.stop_button.clicked.connect(self.main_window.stop_simulation)

        self.reset_button = QPushButton('Reiniciar Simulación')
        self.reset_button.clicked.connect(self.main_window.reset_simulation)

        self.start_node_combo = QComboBox()
        self.end_node_combo = QComboBox()
        for i in range(1, 6):
            self.start_node_combo.addItem(f'Node {i}', i - 1)
            self.end_node_combo.addItem(f'Node {i}', i - 1)

        self.custom_slot_button = QPushButton('Configurar Slots Personalizados')
        self.custom_slot_button.clicked.connect(self.set_custom_slots)

        custom_slot_layout = QVBoxLayout()
        custom_slot_layout.addWidget(QLabel('Nodo Inicial:'))
        custom_slot_layout.addWidget(self.start_node_combo)
        custom_slot_layout.addWidget(QLabel('Nodo Final:'))
        custom_slot_layout.addWidget(self.end_node_combo)
        custom_slot_layout.addWidget(self.custom_slot_button)
        custom_slot_widget = QWidget()
        custom_slot_widget.setLayout(custom_slot_layout)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(custom_slot_widget)

    def set_custom_slots(self):
        start_node = self.start_node_combo.currentData()
        end_node = self.end_node_combo.currentData()
        self.main_window.set_custom_slots(start_node, end_node)

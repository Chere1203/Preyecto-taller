import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget


class Participantes(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Registro de Agenda")
        self.setFixedSize(400, 200)

        # Crear los widgets de la ventana
        self.name_label = QLabel("Nombre:")
        self.name_input = QLineEdit()
        self.Apellido_label = QLabel("Apellido:")
        self.Apellido_input = QLineEdit()
        self.save_button = QPushButton("Guardar")

        # Configuración del layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.Apellido_label)
        main_layout.addWidget(self.Apellido_input)
        main_layout.addWidget(self.save_button)

        # Configuración del widget principal
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Configuración de la acción del botón "Guardar"
        self.save_button.clicked.connect(self.save_contact)

    def save_contact(self):
        name = self.name_input.text()
        Apellido = self.Apellido_input.text()

        if name and Apellido:
            with open("agenda.txt", "a") as file:
                file.write(f"{name}: {Apellido}\n")
            self.name_input.setText("")
            self.Apellido_input.setText("")
            self.name_input.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Participantes()
    window.show()
    sys.exit(app.exec_())
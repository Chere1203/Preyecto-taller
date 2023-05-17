from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTextEdit, QMessageBox, QVBoxLayout, QWidget, QInputDialog, QListWidget, QLineEdit, QDialogButtonBox, QLabel, QDialog
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr


class ParticipantsWindow(QWidget):
    """Esta clase crean una ventana donde se puede agregar y eliminar participantes que almacena en una lista interna

    Args:
        QWidget
        QListWidget,QLineEdit,QPushButton,QPushButton
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registro de Participantes')
        self.layout = QVBoxLayout()

        self.participants_list = QListWidget()
        self.layout.addWidget(self.participants_list)

        self.input_line = QLineEdit()
        self.layout.addWidget(self.input_line)

        self.add_button = QPushButton('Agregar')
        self.add_button.clicked.connect(self.add_participant)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton('Eliminar')
        self.remove_button.clicked.connect(self.remove_participant)
        self.layout.addWidget(self.remove_button)

        self.setLayout(self.layout)

        self.participants = []  # Lista para almacenar los participantes

    def add_participant(self):
        """Funcion para agregar y almacenar en una lista los participantes agragados
        """
        participant = self.input_line.text()
        if participant:
            self.participants_list.addItem(participant)
            self.participants.append(participant)  # Agregar participante a la lista
            self.input_line.clear()

    def remove_participant(self):
        """Funcion para eliminar participantes recientemente agragados 
        """
        selected_item = self.participants_list.currentItem()
        if selected_item:
            participant = selected_item.text()
            self.participants_list.takeItem(self.participants_list.row(selected_item))
            self.participants.remove(participant)  # Eliminar participante de la lista




class AgendaWindow(QWidget):
    """Ventana de la agenda donde se pueden agregar, eliminar y editar puntos de esta

    Args:
        QWidget (_type_): _description_
        agenda_text (QTextEdit): Widget de texto para mostrar la agenda.
        apartado_input (QLineEdit): Cuadro de texto para ingresar nuevos apartados.
        add_apartado_button (QPushButton): Botón para agregar un nuevo apartado.
        punto_input (QLineEdit): Cuadro de texto para ingresar nuevos puntos.
        add_punto_button (QPushButton): Botón para agregar un nuevo punto.
        edit_punto_button (QPushButton): Botón para editar un punto existente.
        remove_punto_button (QPushButton): Botón para eliminar un punto existente.
        agenda_data (dict): Diccionario para almacenar los datos de la agenda.
    """
    def __init__(self):

        super().__init__()
        self.setWindowTitle('Registro de Agenda')
        self.layout = QVBoxLayout()

        self.agenda_text = QTextEdit()
        self.layout.addWidget(self.agenda_text)

        self.apartado_input = QLineEdit()
        self.layout.addWidget(self.apartado_input)

        self.add_apartado_button = QPushButton('Agregar Apartado')
        self.add_apartado_button.clicked.connect(self.add_apartado)
        self.layout.addWidget(self.add_apartado_button)

        self.punto_input = QLineEdit()
        self.layout.addWidget(self.punto_input)

        self.add_punto_button = QPushButton('Agregar Punto')
        self.add_punto_button.clicked.connect(self.add_punto)
        self.layout.addWidget(self.add_punto_button)

        self.edit_punto_button = QPushButton('Editar Punto')
        self.edit_punto_button.clicked.connect(self.edit_punto)
        self.layout.addWidget(self.edit_punto_button)

        self.remove_punto_button = QPushButton('Eliminar Punto')
        self.remove_punto_button.clicked.connect(self.remove_punto)
        self.layout.addWidget(self.remove_punto_button)

        self.setLayout(self.layout)

        self.agenda_data = {}

    def add_apartado(self):
        """Funcion para agregar apartado a la agenda
        """
        apartado = self.apartado_input.text()
        if apartado:
            self.agenda_data[apartado] = []
            self.update_agenda_text()
            self.apartado_input.clear()

    def add_punto(self):
        """Funcion para agregar punto en la agenda
        """
        apartado, ok = QInputDialog.getItem(self, "Seleccionar Apartado", "Apartado:", self.agenda_data.keys(), editable=False)
        if ok and apartado:
            punto = self.punto_input.text()
            if punto:
                self.agenda_data[apartado].append(punto)
                self.update_agenda_text()
                self.punto_input.clear()

    def edit_punto(self):
        """Funcion para editar punto en la agenda
        """
        apartado, ok = QInputDialog.getItem(self, "Seleccionar Apartado", "Apartado:", self.agenda_data.keys(), editable=False)
        if ok and apartado:
            puntos = self.agenda_data[apartado]
            punto, ok = QInputDialog.getItem(self, "Seleccionar Punto", "Punto:", puntos, editable=False)
            if ok and punto:
                nuevo_punto, ok = QInputDialog.getText(self, "Editar Punto", "Nuevo nombre del punto:", text=punto)
                if ok and nuevo_punto:
                    index = puntos.index(punto)
                    self.agenda_data[apartado][index] = nuevo_punto
                    self.update_agenda_text()

    def remove_punto(self):
        """Funcion que elimina un punto no deseado 
        """
        apartado, ok = QInputDialog.getItem(self, "Seleccionar Apartado", "Apartado:", self.agenda_data.keys(), editable=False)
        if ok and apartado:
            puntos = self.agenda_data[apartado]
            punto, ok = QInputDialog.getItem(self, "Seleccionar Punto", "Punto:", puntos, editable=False)
            if ok and punto:
                index = puntos.index(punto)
                self.agenda_data[apartado].pop(index)
                self.update_agenda_text()

    def update_agenda_text(self):
        """Funcion que actualiza el contenido de la agenda
        """
        self.agenda_text.clear()
        for apartado, puntos in self.agenda_data.items():
            self.agenda_text.append(f"{apartado}:")
            for punto in puntos:
                self.agenda_text.append(f"  - {punto}")

class MainWindow(QMainWindow):
    """Ventana principal del registro
    Esta clase extiende de QMainWindow y se utiliza como la ventana principal de la aplicación de registro.
    Contiene dos ventanas secundarias: ParticipantsWindow y AgendaWindow.

    Args:
        QMainWindow QMainWindow: Clase base para crear una ventana principal.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Registro')

        self.participants_window = ParticipantsWindow()
        self.setCentralWidget(self.participants_window)

        self.agenda_window = AgendaWindow()

        self.create_menu()

    def create_menu(self):
        """Funcion que crea el menú
        """
        menu_bar = self.menuBar()
        archivo_menu = menu_bar.addMenu('Archivo')

        participants_action = archivo_menu.addAction('Registro de Participantes')
        participants_action.triggered.connect(self.show_participants_window)

        agenda_action = archivo_menu.addAction('Registro de Agenda')
        agenda_action.triggered.connect(self.show_agenda_window)

    def show_participants_window(self):
        """Funcion que muestra la ventana del registro de participantes
        """
        self.setCentralWidget(self.participants_window)

    def show_agenda_window(self):
        """Funcion que muestra la venta de la agenda
        """
        self.setCentralWidget(self.agenda_window)


class AudioWindow(QWidget):
    """Ventana de División y Reconocimiento de Audio.

    Esta clase extiende de QWidget y se utiliza para la funcionalidad relacionada con la división y reconocimiento de audio.
    Proporciona una interfaz para seleccionar archivos de audio, carpetas para segmentos de grabación, reconocer el texto en los segmentos de audio,
    guardar el texto reconocido en archivos de texto y subir archivos de texto.

    Args:
        QWidget: Clase base para crear una ventana.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('División y Reconocimiento de Audio')
        self.layout = QVBoxLayout()

        self.audio_file_button = QPushButton('Abrir archivo de audio')
        self.layout.addWidget(self.audio_file_button)

        self.audio_file_text = QTextEdit('Sin archivo seleccionado...')
        self.audio_file_text.setDisabled(True)
        self.layout.addWidget(self.audio_file_text)

        self.segments_folder_button = QPushButton('Abrir carpeta para segmentos de grabación')
        self.layout.addWidget(self.segments_folder_button)

        self.segments_folder_text = QTextEdit('Sin carpeta seleccionada...')
        self.segments_folder_text.setDisabled(True)
        self.layout.addWidget(self.segments_folder_text)

        self.recognize_button = QPushButton('Reconocer texto')
        self.layout.addWidget(self.recognize_button)

        self.recognize_result = QTextEdit('Aún sin reconocer texto')
        self.recognize_result.setDisabled(True)
        self.layout.addWidget(self.recognize_result)

        self.save_button = QPushButton('Guardar texto')
        self.layout.addWidget(self.save_button)

        self.upload = QPushButton('Subir Texto')
        self.layout.addWidget(self.upload)

        self.upload_text = QTextEdit('Sin archivo seleccionado...')
        self.upload_text.setDisabled(True)
        self.layout.addWidget(self.upload_text)
        
        

        self.setLayout(self.layout)

        self.audio_file_button.clicked.connect(self.select_audio_file)
        self.segments_folder_button.clicked.connect(self.select_segments_folder)
        self.recognize_button.clicked.connect(self.recognize_text)
        self.save_button.clicked.connect(self.show_save_dialog)
        self.upload.clicked.connect(self.upload_aaaaaaaa)

        self.agenda_data = {}

    def select_audio_file(self):
        """bre un diálogo para seleccionar un archivo de audio.

    Actualiza el cuadro de texto del archivo de audio con la ruta del archivo seleccionado.
        """
        file, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo de audio')
        if file:
            self.audio_file_text.setText(file)

    def select_segments_folder(self):
        """Abre un diálogo para seleccionar una carpeta para segmentos de grabación.

    Actualiza el cuadro de texto de la carpeta de segmentos de grabación con la ruta de la carpeta seleccionada.
        """
        folder = QFileDialog.getExistingDirectory(self, 'Seleccionar carpeta para segmentos de grabación')
        if folder:
            self.segments_folder_text.setText(folder)

    def recognize_text(self):
        """Reconoce el texto en los segmentos de audio.

    Lee el archivo de audio seleccionado y realiza el reconocimiento de voz en cada segmento de audio.
    Actualiza el cuadro de texto de texto reconocido con los resultados del reconocimiento.
        """
        audio_file = self.audio_file_text.toPlainText()
        segments_folder = self.segments_folder_text.toPlainText()

        if audio_file and segments_folder:
            try:
                audio = AudioSegment.from_file(audio_file)
                segments = split_on_silence(audio, min_silence_len=3000, silence_thresh=-50)

                for i, segment in enumerate(segments):
                    segment.export(f'{segments_folder}/segment_{i}.wav', format='wav')

                r = sr.Recognizer()
                text = ''

                for i, segment in enumerate(segments):
                    with sr.AudioFile(f'{segments_folder}/segment_{i}.wav') as source:
                        audio_data = r.record(source)
                    segment_text = r.recognize_google(audio_data, language='es-ES')
                    text += f'Segmento {i}: {segment_text}\n'

                self.recognize_result.setText(text)
            except Exception as e:
                QMessageBox.warning(self, "Error al reconocer el audio", str(e))
        else:
            QMessageBox.warning(self, "Error", "Debes seleccionar un archivo de audio y una carpeta de segmentos de grabación.")

    def get_participant_and_point(self):
        """ Obtiene el participante y el punto seleccionados de la agenda.

    Obtiene el participante y el punto seleccionados por medio de los métodos choose_participant_from_agenda y choose_point_from_agenda.

    """
        participant = self.choose_participant_from_agenda(self.agenda_data)
        if participant:
            point = self.choose_point_from_agenda(self.agenda_data, participant)
            if point:
                return participant, point
        return None, None

    def choose_participant_from_agenda(self, agenda_data):
        """Muestra un diálogo para seleccionar un participante de la agenda.

    Muestra un diálogo con los participantes disponibles en la agenda y permite seleccionar uno.

        """
        apartados = list(agenda_data.keys())
        apartado, ok = QInputDialog.getItem(self, "Seleccionar Participante", "Participantes:", apartados, editable=False)
    
    def choose_point_from_agenda(self, agenda_data, participant):
        """ Muestra un diálogo para seleccionar un punto de la agenda.

    Muestra un diálogo con los puntos disponibles para el participante seleccionado y permite seleccionar uno.
"""
        puntos = agenda_data.get(participant, [])
        punto, ok = QInputDialog.getItem(self, "Seleccionar")


    def populate_participants_list(self):
        """Rellena la lista de participantes.

    Obtiene la lista de participantes de la ventana de ParticipantsWindow y la agrega a la lista de participantes en esta ventana
        """
        participants = self.participants_window.participants  # Acceder a la lista de participantes de ParticipantsWindow
        self.participants_list.addItems(participants)

    def show_save_dialog(self):
        """ Muestra un diálogo para guardar el texto reconocido en un archivo de texto.

    Verifica si hay un participante y punto seleccionados.
    Si hay texto reconocido, muestra un diálogo para guardar el texto en un archivo de texto.
    Si no hay texto reconocido, muestra un mensaje de advertencia.
        """
        participant, point = self.get_participant_and_point()

        if participant and point:
            text = self.recognize_result.toPlainText()

            if text:
                if participant in self.agenda_data and point in self.agenda_data[participant]:
                    dialog = QFileDialog(self)
                    dialog.setAcceptMode(QFileDialog.AcceptSave)
                    dialog.setNameFilter('Archivos de texto (*.txt)')

                    if dialog.exec_() == QFileDialog.Accepted:
                        file_path = dialog.selectedFiles()[0]

                        try:
                            with open(file_path, 'w') as file:
                                file.write(f"Participante: {participant}\n")
                                file.write(f"Punto: {point}\n\n")
                                file.write(text)

                            QMessageBox.information(self, "Texto guardado", "El texto reconocido se ha guardado correctamente.")
                        except Exception as e:
                            QMessageBox.warning(self, "Error al guardar", f"No se pudo guardar el archivo:\n{str(e)}")
                else:
                   pass
            else:
                QMessageBox.warning(self, "Sin texto reconocido", "No hay texto reconocido para guardar. Por favor, subir un audio.")
        else:
            pass

    def upload_text_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo de texto')
        if file:
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    self.upload_text.setPlainText(content)  # Modificación: Utilizar setPlainText en lugar de setText
            except Exception as e:
                QMessageBox.warning(self, "Error al abrir archivo de texto", str(e))
                
    def add_audio(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo de audio')
        if file:
            self.audio_segments.append(file)
            QMessageBox.information(self, "Audio agregado", "El archivo de audio se ha agregado correctamente.")

    def get_participant_and_point(self):
        participant = self.choose_participant_from_agenda(self.agenda_data)
        if participant:
            point = self.choose_point_from_agenda(self.agenda_data, participant)
            if point:
                return participant, point
        return None, None

    def choose_participant_from_agenda(self, agenda_data):
        apartados = list(agenda_data.keys())
        apartado, ok = QInputDialog.getItem(self, "Seleccionar Participante", "Participantes:", apartados, editable=False)
        return apartado if ok else None

    def choose_point_from_agenda(self, agenda_data, participant):
        puntos = agenda_data.get(participant, [])
        punto, ok = QInputDialog.getItem(self, "Seleccionar Punto", "Punto:", puntos, editable=False)
        return punto if ok else None

    def upload_aaaaaaaa(self):
            file_dialog = QFileDialog()
            file_dialog.setNameFilter('Archivos de texto (*.txt)')
            file_dialog.setWindowTitle('Seleccionar archivo')
            file_dialog.setFileMode(QFileDialog.ExistingFile)

            if file_dialog.exec_() == QFileDialog.Accepted:
                file_path = file_dialog.selectedFiles()[0]
                self.audio_file_path = file_path
                self.audio_file_text.setText(file_path)


app = QApplication([])
main_window = MainWindow()
audio_window = AudioWindow()
main_window.show()

audio_action = main_window.menuBar().addAction('División y Reconocimiento de Audio')
audio_action.triggered.connect(audio_window.show)

app.exec_()
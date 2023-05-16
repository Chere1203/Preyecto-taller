from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTextEdit, QMessageBox, QVBoxLayout, QWidget, QInputDialog, QListWidget, QLineEdit, QDialogButtonBox, QLabel, QDialog
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr

class ParticipantsWindow(QWidget):
    def __init__(self):
        """
        This is a constructor function that sets up a graphical user interface for a participant
        registration program.
        """
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

    def add_participant(self):
        """
        This function adds a participant to a list and clears the input line.
        """
        participant = self.input_line.text()
        if participant:
            self.participants_list.addItem(participant)
            self.input_line.clear()

    def remove_participant(self):
        """
        This function removes a selected participant from a list of participants.
        """
        selected_item = self.participants_list.currentItem()
        if selected_item:
            self.participants_list.takeItem(self.participants_list.row(selected_item))




class AgendaWindow(QWidget):
    def __init__(self):
        """
        This is the initialization function for a GUI application that allows users to add, edit, and
        remove items from an agenda.
        """

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
        """
        This function adds a new section to an agenda and clears the input field.
        """
        apartado = self.apartado_input.text()
        if apartado:
            self.agenda_data[apartado] = []
            self.update_agenda_text()
            self.apartado_input.clear()

    def add_punto(self):
        """
        This function adds a new item to a selected section in a dictionary and updates the agenda text.
        """
        apartado, ok = QInputDialog.getItem(self, "Seleccionar Apartado", "Apartado:", self.agenda_data.keys(), editable=False)
        if ok and apartado:
            punto = self.punto_input.text()
            if punto:
                self.agenda_data[apartado].append(punto)
                self.update_agenda_text()
                self.punto_input.clear()

    def edit_punto(self):
        """
        This function allows the user to edit a selected point in a given section of an agenda.
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
        """
        This function removes a selected point from a dictionary and updates the agenda text.
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
        """
        This function updates the agenda text by clearing it and appending the agenda data items and
        their points.
        """
        self.agenda_text.clear()
        for apartado, puntos in self.agenda_data.items():
            self.agenda_text.append(f"{apartado}:")
            for punto in puntos:
                self.agenda_text.append(f"  - {punto}")

class MainWindow(QMainWindow):
    def __init__(self):
        """
        This function initializes a main window for a registration system with a central widget and a
        menu.
        """
        super().__init__()
        self.setWindowTitle('Sistema de Registro')

        self.participants_window = ParticipantsWindow()
        self.setCentralWidget(self.participants_window)

        self.agenda_window = AgendaWindow()

        self.create_menu()

    def create_menu(self):
        """
        This function creates a menu bar with two options that trigger the display of different windows
        when clicked.
        """
        menu_bar = self.menuBar()
        archivo_menu = menu_bar.addMenu('Archivo')

        participants_action = archivo_menu.addAction('Registro de Participantes')
        participants_action.triggered.connect(self.show_participants_window)

        agenda_action = archivo_menu.addAction('Registro de Agenda')
        agenda_action.triggered.connect(self.show_agenda_window)

    def show_participants_window(self):
        self.setCentralWidget(self.participants_window)

    def show_agenda_window(self):
        self.setCentralWidget(self.agenda_window)


class AudioWindow(QWidget):
    def __init__(self):
        """
        This is a constructor function that initializes a GUI with buttons for selecting an audio file,
        a folder for audio segments, recognizing text, saving text, and displaying the results.
        """
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

        self.setLayout(self.layout)

        self.audio_file_button.clicked.connect(self.select_audio_file)
        self.segments_folder_button.clicked.connect(self.select_segments_folder)
        self.recognize_button.clicked.connect(self.recognize_text)
        self.save_button.clicked.connect(self.show_save_dialog)

        self.agenda_data = {}

    def select_audio_file(self):
        """
        This function opens a file dialog to select an audio file and sets the selected file path as the
        text of a QLabel widget.
        """
        file, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo de audio')
        if file:
            self.audio_file_text.setText(file)

    def select_segments_folder(self):
        """
        This function opens a file dialog to select a folder and sets the selected folder path as text
        in a QLineEdit widget.
        """
        folder = QFileDialog.getExistingDirectory(self, 'Seleccionar carpeta para segmentos de grabación')
        if folder:
            self.segments_folder_text.setText(folder)

    def recognize_text(self):
        """
        This function takes an audio file and a folder path as inputs, splits the audio file into segments
        based on silence, converts each segment to text using Google's speech recognition API, and
        displays the resulting text in a GUI.
        """
        audio_file = self.audio_file_text.toPlainText()
        segments_folder = self.segments_folder_text.toPlainText()

        if audio_file and segments_folder:
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

    def get_participant_and_point(self):
        """
        This function gets a participant and a point from an agenda data.
        :return: The function `get_participant_and_point` returns a tuple containing the chosen participant
        and point from the agenda data. If a participant or point cannot be chosen, it returns a tuple of
        `None` values.
        """
        participant = self.choose_participant_from_agenda(self.agenda_data)
        if participant:
            point = self.choose_point_from_agenda(self.agenda_data, participant)
            if point:
                return participant, point
        return None, None

    def choose_participant_from_agenda(self, agenda_data):
        """
        This function displays a dialog box to select a participant from a given agenda.
        
        :param agenda_data: It is a dictionary containing the agenda data. The keys of the dictionary
        are the different sections or topics in the agenda, and the values are lists of participants or
        speakers for each section
        """
        apartados = list(agenda_data.keys())
        apartado, ok = QInputDialog.getItem(self, "Seleccionar Participante", "Apartado:", apartados, editable=False)
    def choose_point_from_agenda(self, agenda_data, participant):
        """
        This function allows a participant to choose a point from an agenda.
        
        :param agenda_data: A dictionary containing the agenda items for each participant. The keys are
        participant names and the values are lists of agenda items
        :param participant: The name or identifier of the participant for whom the point is being chosen
        from the agenda
        :return: either the selected point from the agenda data for the given participant, or None if no
        point is selected or the selection is cancelled.
        """
        puntos = agenda_data.get(participant, [])
        punto, ok = QInputDialog.getItem(self, "Seleccionar Punto", "Punto:", puntos, editable=False)
        if ok and punto:
            return punto
        return None

    def show_save_dialog(self):
        """
        This function shows a save dialog and saves recognized text to a selected file path.
        """
        participant, point = self.get_participant_and_point()

        if participant and point:
            text = self.recognize_result.toPlainText()

            if text:
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
                QMessageBox.warning(self, "Sin texto reconocido", "No hay texto reconocido para guardar.")
        else:
            QMessageBox.warning(self, "Selección inválida", "No se ha seleccionado un participante y/o punto válido.")

app = QApplication([])
main_window = MainWindow()
audio_window = AudioWindow()
main_window.show()

audio_action = main_window.menuBar().addAction('División y Reconocimiento de Audio')
audio_action.triggered.connect(audio_window.show)

app.exec_()
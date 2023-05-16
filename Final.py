from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTextEdit, QMessageBox, QVBoxLayout, QWidget, QInputDialog, QListWidget, QLineEdit
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr

class ParticipantsWindow(QWidget):
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

    def add_participant(self):
        participant = self.input_line.text()
        if participant:
            self.participants_list.addItem(participant)
            self.input_line.clear()

    def remove_participant(self):
        selected_item = self.participants_list.currentItem()
        if selected_item:
            self.participants_list.takeItem(self.participants_list.row(selected_item))

class AgendaWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Registro de Agenda')
        self.layout = QVBoxLayout()

        self.apartados_list = QListWidget()
        self.layout.addWidget(self.apartados_list)

        self.apartado_input = QLineEdit()
        self.layout.addWidget(self.apartado_input)

        self.add_apartado_button = QPushButton('Agregar Apartado')
        self.add_apartado_button.clicked.connect(self.add_apartado)
        self.layout.addWidget(self.add_apartado_button)

        self.puntos_list = QListWidget()
        self.layout.addWidget(self.puntos_list)

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

    def add_apartado(self):
        apartado = self.apartado_input.text()
        if apartado:
            self.apartados_list.addItem(apartado)
            self.apartado_input.clear()

    def add_punto(self):
        apartado, ok = QInputDialog.getItem(self, "Seleccionar Apartado", "Apartado:", [self.apartados_list.item(i).text() for i in range(self.apartados_list.count())], editable=False)
        if ok and apartado:
            punto = self.punto_input.text()
            if punto:
                self.puntos_list.addItem(punto)
                self.punto_input.clear()

    def edit_punto(self):
        selected_item = self.puntos_list.currentItem()
        if selected_item:
            nuevo_punto, ok = QInputDialog.getText(self, "Editar Punto", "Nuevo nombre del punto:", text=selected_item.text())
            if ok and nuevo_punto:
                selected_item.setText(nuevo_punto)

    def remove_punto(self):
        selected_item = self.puntos_list.currentItem()
        if selected_item:
            self.puntos_list.takeItem(self.puntos_list.row(selected_item))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Registro')

        self.participants_window = ParticipantsWindow()
        self.setCentralWidget(self.participants_window)

        self.agenda_window = AgendaWindow()

        self.create_menu()

    def create_menu(self):
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

        self.setLayout(self.layout)

        self.audio_file_button.clicked.connect(self.select_audio_file)
        self.segments_folder_button.clicked.connect(self.select_segments_folder)
        self.recognize_button.clicked.connect(self.recognize_text)

    def select_audio_file(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Seleccionar archivo de audio')
        if file:
            self.audio_file_text.setText(file)

    def select_segments_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Seleccionar carpeta para segmentos de grabación')
        if folder:
            self.segments_folder_text.setText(folder)

    def recognize_text(self):
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


app = QApplication([])
main_window = MainWindow()
audio_window = AudioWindow()
main_window.show()

audio_action = main_window.menuBar().addAction('División y Reconocimiento de Audio')
audio_action.triggered.connect(audio_window.show)

app.exec_()
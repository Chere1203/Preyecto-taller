"""
Librerías requeridas:

pip3 install pydub
"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QTextEdit, QMessageBox, QTableView, QWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from pydub import AudioSegment
from pydub.silence import split_on_silence
#Objetos visuales QT declarado globalmente
ruta_grabacion_a_dividir:QTextEdit=None
ruta_carpeta:QTextEdit=None
ruta_grabacion_a_reconocer:QTextEdit=None
resultado:QTextEdit=None

#Evento para el boton de iniciar la división del archivo
def dividir():
    # Duración mínima de la pausa en milisegundos
    min_silence_len = 3000
    archivo_de_audio=ruta_grabacion_a_dividir.toPlainText()
    carpeta_de_segmentos=ruta_carpeta.toPlainText()
    audio_file = AudioSegment.from_wav(archivo_de_audio)

    audio_chunks = split_on_silence(
        audio_file, 
        min_silence_len=min_silence_len, 
        silence_thresh=-50
    )

    for i, chunk in enumerate(audio_chunks):
        print (f'Recorte numero {i} procesado')
        chunk.export(f'{carpeta_de_segmentos}/grabacion_{i}.wav', format='wav')
    
    #Lanza un message box al finalizar las divisiones del audio
    msgBox=QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(f"Se han terminado de procesar el archivo de audio, puede visualizar el resultado en la carpeta: {carpeta_de_segmentos}")
    msgBox.setWindowTitle("Fin del proceso de división")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setDefaultButton(QMessageBox.Ok)
    response = msgBox.exec_()
#Evento para el boton que selecciona el archivo a dividir
def dialogo_grabacion():
    # Creamos el diálogo de selección de archivo
    filename, _ = QFileDialog.getOpenFileName(window,'Seleccionar archivo')
    # Si el usuario selecciona un archivo, mostramos la ruta en un label
    if filename:
        ruta_grabacion_a_dividir.setText(filename)

#Evento para el boton que selecciona la carpeta a almacenar los segmentos de grabaciones
def dialogo_carpeta():
    # Creamos el diálogo de selección de archivo
    directory= QFileDialog.getExistingDirectory(window,'Seleccionar La carpeta')
    # Si el usuario selecciona un archivo, mostramos la ruta en un label
    if directory:
        ruta_carpeta.setText(directory)

#Evento para el boton que selecciona la carpeta a almacenar los segmentos de grabaciones
def dialogo_grabacion_reconocer():
    # Creamos el diálogo de selección de archivo
    filename, _ = QFileDialog.getOpenFileName(window,'Seleccionar archivo')
    # Si el usuario selecciona un archivo, mostramos la ruta en un label
    if filename:
        ruta_grabacion_a_reconocer.setText(filename)

def reconocer_texto():
    #global resultado
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.AudioFile(ruta_grabacion_a_reconocer.toPlainText()) as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data, language='es-ES')
    resultado.setText(text)

class AgendaWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Registro de Agenda")
        self.setFixedSize(400, 200)

        # Crear los widgets de la ventana
        self.name_label = QLabel("Nombre:")
        self.name_input = QLineEdit()
        self.phone_label = QLabel("Teléfono:")
        self.phone_input = QLineEdit()
        self.save_button = QPushButton("Guardar")

        # Configuración del layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.phone_label)
        main_layout.addWidget(self.phone_input)
        main_layout.addWidget(self.save_button)

        # Configuración del widget principal
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Configuración de la acción del botón "Guardar"
        self.save_button.clicked.connect(self.save_contact)

    def save_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()

        if name and phone:
            with open("agenda.txt", "a") as file:
                file.write(f"{name}: {phone}\n")
            self.name_input.setText("")
            self.phone_input.setText("")
            self.name_input.setFocus()


def initUI():
    global ruta_grabacion_a_dividir,ruta_carpeta,ruta_grabacion_a_reconocer,resultado
    # Agregamos un botón para abrir el selector de archivo para la grabación a subdividir
    button = QPushButton('Abrir archivo de audio', window)
    button.setGeometry(0, 0,500,30)
    button.clicked.connect(dialogo_grabacion)
    # Agregamos una caja de texto para determinar la ruta del archivo de la grabación a subdividir
    ruta_grabacion_a_dividir=QTextEdit("Sin seleccionar Archivo...",parent=window)
    ruta_grabacion_a_dividir.setDisabled=True
    ruta_grabacion_a_dividir.setGeometry(0,30,500,90)
    # Agregamos un botón para abrir el selector de la carpeta
    button = QPushButton('Abrir carpeta contenedora de segmentos de grabación', window)
    button.setGeometry(0, 120,500,30)
    button.clicked.connect(dialogo_carpeta)
    # Agregamos una caja de texto para determinar la ruta del archivo de la grabación a subdividir
    ruta_carpeta=QTextEdit("Sin seleccionar carpeta...",parent=window)
    ruta_carpeta.setDisabled=True
    ruta_carpeta.setGeometry(0,150,500,90)
    # Agregamos un botón para abrir el selector del archivo ya cortado a ser reconocido por SpeechRecognition
    button = QPushButton('Abrir el archivo a reconocer:', window)
    button.setGeometry(0, 210,500,30)
    button.clicked.connect(dialogo_grabacion_reconocer)
    # Agregamos una caja de texto para determinar la ruta del archivo de la grabación a subdividir
    ruta_grabacion_a_reconocer=QTextEdit("Sin seleccionar carpeta...",parent=window)
    ruta_grabacion_a_reconocer.setDisabled=True
    ruta_grabacion_a_reconocer.setGeometry(0,240,500,90)
    # Agregamos un botón para abrir iniciar el textRecongnition con el archivo seleciconado
    button = QPushButton('Abrir el archivo a reconocer', window)
    button.setGeometry(0, 210,500,30)
    button.clicked.connect(dialogo_grabacion_reconocer)
    # Agregamos una caja de texto para determinar la ruta del archivo de la grabación a subdividir
    ruta_grabacion_a_reconocer=QTextEdit("Sin seleccionar carpeta...",parent=window)
    ruta_grabacion_a_reconocer.setDisabled=True
    ruta_grabacion_a_reconocer.setGeometry(0,240,500,90)
    # Agregamos un botón para iniciar la división del audio
    button = QPushButton('Iniciar división del archivo', window)
    button.setGeometry(0, 310,500,30)
    button.clicked.connect(dividir)
    # Agregamos un botón para iniciar el SpeechRecognition
    button = QPushButton('Iniciar el reconocimiento del texto', window)
    button.setGeometry(0, 340,500,30)
    button.clicked.connect(reconocer_texto)
    # Agregamos un botón para iniciar el SpeechRecognition
    resultado=QTextEdit("Aún sin reconocer texto",parent=window)
    resultado.setDisabled=True
    resultado.setGeometry(0,370,500,120)
    #Agregamos un boton para la creacion de la agenda
    button = QPushButton('Abrir registro de la agenda', window)
    button.setGeometry(0, 210,500,30)
    button.clicked.connect(AgendaWindow)
    button.clicked.show(AgendaWindow)

    window.setGeometry(0, 0, 500, 500)
    window.setWindowTitle('Selector de archivo')

    window.show()


app = QApplication([])
window = QMainWindow()
initUI()
app.exec_()



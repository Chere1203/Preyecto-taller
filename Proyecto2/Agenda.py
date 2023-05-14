from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QComboBox

class Agenda(QWidget):
    def __init__(self):
        super().__init__()
        
        self.apartados = {'Comprobación de la agenda': [], 
                          'Trámites varios': [], 
                          'Informes de coordinación': [], 
                          'Puntos de foro': [], 
                          'Puntos varios': []}
        
        self.initUI()
        
        
    def initUI(self):
        # Crear widgets
        self.lbl_apartado = QLabel('Apartado:')
        self.cmb_apartado = QComboBox()
        self.cmb_apartado.addItems(list(self.apartados.keys()))
        
        self.lbl_punto = QLabel('Punto:')
        self.txt_punto = QLineEdit()
        
        self.btn_agregar = QPushButton('Agregar')
        self.btn_eliminar = QPushButton('Eliminar')
        
        self.lst_puntos = QListWidget()
        self.lst_puntos.itemDoubleClicked.connect(self.editar_punto)
        
        self.btn_agregar_apartado = QPushButton('Agregar apartado')
        self.btn_eliminar_apartado = QPushButton('Eliminar apartado')
        
        self.cmb_apartado.currentIndexChanged.connect(self.mostrar_puntos)
        self.btn_agregar.clicked.connect(self.agregar_punto)
        self.btn_eliminar.clicked.connect(self.eliminar_punto)
        self.btn_agregar_apartado.clicked.connect(self.agregar_apartado)
        self.btn_eliminar_apartado.clicked.connect(self.eliminar_apartado)
        
        # Crear diseño de la ventana
        hbox_apartado = QHBoxLayout()
        hbox_apartado.addWidget(self.lbl_apartado)
        hbox_apartado.addWidget(self.cmb_apartado)
        
        hbox_punto = QHBoxLayout()
        hbox_punto.addWidget(self.lbl_punto)
        hbox_punto.addWidget(self.txt_punto)
        hbox_punto.addWidget(self.btn_agregar)
        hbox_punto.addWidget(self.btn_eliminar)
        
        hbox_apartados = QHBoxLayout()
        hbox_apartados.addWidget(self.btn_agregar_apartado)
        hbox_apartados.addWidget(self.btn_eliminar_apartado)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_apartado)
        vbox.addWidget(self.lst_puntos)
        vbox.addLayout(hbox_punto)
        vbox.addLayout(hbox_apartados)
        
        self.setLayout(vbox)
        
        self.setWindowTitle('Agenda')
        self.setGeometry(100, 100, 400, 300)
        self.show()
        
    def mostrar_puntos(self, index):
        self.lst_puntos.clear()
        apartado = self.cmb_apartado.currentText()
        puntos = self.apartados[apartado]
        for punto in puntos:
            item = QListWidgetItem(punto)
            self.lst_puntos.addItem(item)
            
            
    def agregar_punto(self):
        apartado = self.cmb_apartado.currentText()
        punto = self.txt_punto.text()
        if punto:
            self.apartados[apartado].append(punto)
            self.mostrar_puntos(self.cmb_apartado.currentIndex())
            self.txt_punto.setText('')
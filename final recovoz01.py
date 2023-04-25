#Registro de voz con agenda y participantes, autores: Erick y Marco
def registra_agenda (): #Función para definir agenda
    """Esta función usa una lista vacía inicia con un ciclo de while mientras la variable continua
    es True, dentro del ciclo, se solicita a usuario un punto de la variable, se condiciona
    cuando es si que agregue e titulo, luego se solicita al usuario que clasifique si es un punto principal
    o secundario, y todo se agrega a la lista agendar, si la respuesta al primer condicionante es
    no, o en las siguientes iteraciones terminara el ciclo y retornara el contenido de la lista agendar"""
    agendar = []
    continua = True
    while continua:
        agregar_punto = input("¿Desea agregar un punto a la agenda? (digite: si/no) ")
        if agregar_punto.lower() == "si":
            titulo_punto= input("Ingrese el titulo de la agenda: ")
            tipo_punto = input("Presione (p) si es un punto principal o (s) si es secundario: ")
            if tipo_punto.lower() == "p":
                agendar.append((titulo_punto, True))
            else:
                agendar.append((titulo_punto, False))
        elif agregar_punto.lower() == 'no':
            continua= False
        else:
            print('Por favor elija si desea ingresar o no algún punto de agenda: ')
            continue
    return  agendar

def menu_agenda (agenda:list):  #Imprime MENÚ de agenda
    """La función utiliza la lista de la agenda, la indexa e utilizando el titulo y su ubicación 
    luego utiliza la selección para saber si era principal o secundario y lo imprime 
    para mostrar el menú para seleccionar cada punto al hablar"""
    for idx, punto in enumerate(agenda):
        tipo_punto = " (Punto Principal) " if punto[1] else " (Subpunto) "
        print (f"{idx+1}.{punto[0]}{tipo_punto}")

def registra_participantes(): 
    """La función utiliza una lista vacia, mientras la variable continua_participante sea True
    el usuario debe ingresar si continua o no, si continua se le solicita un nombre que 
    se agrega a la lista participante, si el usuario ingresa algo diferente a si o no se
    returna al ciclo hasta que elija continuar o no, cuando elige no se cierra el ciclo igualando 
    la variable continua_participante"""
    participante = []
    continua_participante = True
    while continua_participante:
        agregar_participante = input("Desea agregar un nuevo participante (digite: si/no) ")
        
        if agregar_participante.lower() == "si":
            inscribe_participante = input("Ingrese el nombre de la persona: ")
            participante.append((inscribe_participante))
        elif agregar_participante == 'no':
                continua_participante= False
        else: 
            print ('Porfavor selecciones: si / no: ')
            continue
    return participante

def menu_participantes (participantes:list):  #Imprime MENÚ participantes 
    """La función utiliza la lista de participantes, la indexa e imprime para mostrar el menú para 
    seleccionar cada punto al hablar"""
    for idx, person in enumerate(participantes):
        print (f"{idx+1}.{person}")

def reconocimiento ():
    """La función pretende seleccionar una opción del usuario para iniciar el reconocimiento
    tiene una lista vacia que retorna lo que se asigne segun reconocimiento de voz."""
    inicia=True
    nr=[] 
    import speech_recognition as sr
    r = sr.Recognizer()  
    
    while inicia: 
        inicia_reconocimiento=input("¿Desea continuar con el reconocimiento de voz elegido? (si/no)  ")  
        if inicia_reconocimiento.lower()=='si':     
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print('Puede iniciar : ')
                audio = r.listen(source, timeout=6)
                try:
                    text = r.recognize_google(audio)
                    nr.append(text)
                except sr.WaitTimeoutError:
                    print('''pasaron 6 segundos sin participación''')
                
                except:
                    print('Disculpe, no se escucha claramente  ')
        elif inicia_reconocimiento.lower()=='no':
            inicia=False
    return(nr)

def selecciona_punto_agenda(p:list):
    """La funcion solicita escoger un numero de la lista indexada de agenda
    en un ciclo de while que retorne el participante sino que detenga el ciclo"""
    print(menu_agenda (participantes))     
    for i in range(len(p)):
        print(f"{i+1}. {p[i]}")
    elegido=input('Por favor seleccione un punto de la lista: ')
    if not elegido.isnumeric() or int(elegido) not in range(1, len(p) + 1):
        print("Por Favor escoja algun punto de la agenda: ")
        return selecciona_punto_agenda(p)
    return p[int(elegido)-1]

def selecciona_participante(l:list):
    """La funcion solicita escoger un numero de la lista indexada de participantes 
    en un ciclo de while que retorne el participante sino que detenga el ciclo"""
    print(menu_participantes (participantes))     
    for i in range(len(l)):
        print(f"{i+1}. {l[i]}")
    elegido=input('Por favor seleccione un participante de la lista: ')
    if not elegido.isnumeric() or int(elegido) not in range(1, len(l) + 1):
        print("Por Favor escoja algun participante: ")
        return selecciona_participante(l)
    return l[int(elegido)-1]

def agregar_reconocimiento (func1, func2):#esta función toca corregir
    """La función utiliza dos funciones, la primera es para agregar la función de escoger participante
    y la segunda para seleccionar un punto de agenda y realizar un reconocimiento de voz"""
    while func1 != '':
        while func2 != '':
            print(reconocimiento())
        else: 
            return(agregar_reconocimiento)
    else:
        print('Desea terminar el punto de agenda')

agenda=registra_agenda()
print(menu_agenda(agenda))

participantes=registra_participantes()
print(menu_participantes(participantes))

print('A continuación iniciaremos el programa de reconocimiento de voz')
print('favor elegir del menu correspondiente según se solicita los participantes')
print('o puntos de la agenda y procede a inciar el reconocimiento de voz respectivo')

start=True
while start:
    guarda_reconocimiento=[]
    desea_iniciar=input('¿Desea iniciar el sistema? (si/no) ')
    if desea_iniciar.lower()=='si':
        punto_hablar=selecciona_punto_agenda(agenda)
        elegido=selecciona_participante(participantes)
        guarda_reconocimiento.append(print(f"{punto_hablar}{elegido}",reconocimiento()))
    elif desea_iniciar.lower()=='no':
        start==False
    
    



#print(menu_participantes(participantes))
#print(agregar_reconocimiento(selecciona_participante(participantes), selecciona_punto_agenda(agenda)))

#print(selecciona_participante(participantes))

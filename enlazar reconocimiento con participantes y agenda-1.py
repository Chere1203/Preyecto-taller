agenda = ['Examenes', 'Parciales', 'Reposición', 'Trámites', 'Permisos']
participantes = ['Marco Antonio Quir Cab ', 'Dayana Lizt Cam Mar ', 'Anton Jos Quir Cab ', 'Lizet Quir Cab ']

#Imprime menú de agenda
def menu_agenda (agenda:list):  
    '''La función utiliza la lista de la agenda, la indexa e imprime para mostrar el menú para 
    seleccionar cada punto al hablar'''
    for idx, punto in enumerate(agenda):
        print (f"{idx+1}.{punto}")

#Imprime menú de participantes
def menu_participantes (participantes:list):  
    '''La función utiliza la lista de participantes, la indexa e imprime para mostrar el menú para 
    seleccionar cada punto al hablar'''
    for idx, person in enumerate(participantes):
        print (f"{idx+1}.{person}")

print(menu_agenda(agenda))

def reconocimiento ():
    '''la función pretende seleccionar una opción del usuario para iniciar el reconocimiento'''    
    inicia=True
    nr=[] 
    import speech_recognition as sr
    r = sr.Recognizer()  
    
    while inicia: 
        inicia_reconocimiento=input("¿Desea comenzar el reconocimiento de voz elegido? (si/no)  ")  
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

#print(reconocimiento())

#print(menu_agenda(agenda))
def selecciona_punto_agenda(p:list):
    '''la funcion solicita escoger un numero de la lista indexada de agenda
    en un ciclo de while que retorne el participante sino que detenga el ciclo'''
    print(menu_agenda (participantes))     
    for i in range(len(p)):
        print(f"{i+1}. {p[i]}")
    elegido=input('Por favor seleccione un punto de la lista: ')
    if not elegido.isnumeric() or int(elegido) not in range(1, len(p) + 1):
        print("Por Favor escoja algun punto de la agenda: ")
        return selecciona_punto_agenda(p)
    return p[int(elegido)-1]
        
#print(selecciona_punto_agenda(agenda))

def selecciona_participante(l:list):
    '''la funcion solicita escoger un numero de la lista indexada de participantes 
    en un ciclo de while que retorne el participante sino que detenga el ciclo'''
    print(menu_participantes (participantes))     
    for i in range(len(l)):
        print(f"{i+1}. {l[i]}")
    elegido=input('Por favor seleccione un participante de la lista: ')
    if not elegido.isnumeric() or int(elegido) not in range(1, len(l) + 1):
        print("Por Favor escoja algun participante: ")
        return selecciona_participante(l)
    return l[int(elegido)-1]


def agregar_reconocimiento (func1, func2):
    while func1 != '':
        while func2 != '':
            print(reconocimiento())
        else: 
            return(agregar_reconocimiento)
    else:
        print('Desea terminar el punto de agenda')

print(agregar_reconocimiento(selecciona_participante(participantes), selecciona_punto_agenda(agenda)))

#print(selecciona_participante(participantes))


'''
seleccion_agenda=input('Por favor seleccione un punto de la lista de agenda por favor:  ')
while seleccion_agenda in agenda:
    print(menu_participantes (participantes))
    selección_participante=input('Por favor seleccione un participante de la lista')'''
    
    

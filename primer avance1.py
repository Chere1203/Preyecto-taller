#registro de agenda:

'''Para cada sesión del consejo de unidad, se debe preparar una agenda previa con los
puntos a tratar. Por lo tanto, el sistema propuesto en este proyecto deberá, en primer lugar,
solicitar los puntos de la agenda, los cuales podrán estar agrupados en varios apartados.
Por ejemplo, algunos de los apartados generales pueden incluir: comprobación de la
agenda, trámites varios, informes de coordinación, puntos de foro y puntos varios. Tanto los
apartados como los puntos pueden ser varios, por lo que el sistema debe solicitar primero
el apartado y, posteriormente, uno o varios puntos dentro de él. Este proceso se repetirá
sucesivamente hasta completar la agenda.'''


agenda = []
continua = True

while continua:
    agregar_punto = input("¿Desea agregar un punto a la agenda? (digite: si/no) ")
    if agregar_punto.lower() == "si":
        titulo_punto= input("Ingrese el titulo de la agenda: ")
        tipo_punto = input("Presione (p) si es un punto principal o (s) si es secundario: ")
        if tipo_punto.lower() == "p":
            agenda.append((titulo_punto, True))
        else:
            agenda.append((titulo_punto, False))
    elif agregar_punto.lower() == 'no':
        continua= False
    else:
        print('Por favor elija si desea ingresar o no algún punto de agenda: ')
        continue
    
 

print("\nReport:")
for idx, item in enumerate(agenda):
    item_type = "Punto Principal" if item[1] else "Subpunto"
    print(f"{idx+1}. {item[0]} ({item_type})")





#registro de participantes:
'''
El siguiente paso del sistema es solicitar la lista de personas que participarán en la sesión.
Estas personas deben ser registradas una por una, hasta que se complete la lista con los
nombres completos de todos los participantes.'''



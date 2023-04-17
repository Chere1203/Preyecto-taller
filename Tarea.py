def interseccion(L1,L2):
    resultado = []
    for sublista in L2:
         interseccion_sublista = list(set(sublista) & set(L1))
    if interseccion_sublista:
            resultado.append(interseccion_sublista)
    return resultado

L1 = [1, 7, 3, 8, 5, 6, 21]
L2 = [[1, 7, 15], [11, 14], [21, 19, 14, 7, 3]]
resultado = interseccion(L1, L2)
print(resultado)

def diferencia(l1, l2):
    resultado = []
    for elemento in l1:
        if elemento not in l2:
            resultado.append(elemento)
    return resultado

L1 = [1, 3, 7, 5]
L2 = [4, 7, 3]
resultado = diferencia(L1, L2)
print(resultado)

def aplanar(lista):
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(aplanar(elemento))
        else:
            resultado.append(elemento)
    return resultado

L1 = [1, [4, 3, 7], 3, [11, 2, 13], 5]
resultado = aplanar(L1)
print(resultado)

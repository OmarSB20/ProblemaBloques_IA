import numpy as np

g = 0 
movimientos = 0
vEM = 1

#Estado meta
eM = np.array ([
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
])

mComparacion = np.array ([
    [1, 2, 3],
    [8, 150, 4],
    [7, 6, 5]
])

#Matriz inicial
matriz = np.array ([
    [1, 2, 3],
    [7, 8, 4],
    [6, 5, 0]
])

matriz_copia = np.array ([
    [],
    [],
    []
])

estado_previo = np.array([
    [],
    [],
    []
])

estados_previos = np.empty((0, 3, 3))

nuevo_estado = np.array ([
    [],
    [],
    []
])

comodin = [0, 0]

"""
Aqui se compara 
"""
def compararMatriz(nuevo_estado):
    
    for estados in estados_previos:
        son_iguales = np.array_equal(nuevo_estado, estados)

        if son_iguales:
            return 150
        

    else:
        matriz_boleana = (nuevo_estado == mComparacion)
        cantidad_de_false = np.count_nonzero(matriz_boleana == False)
        
        return cantidad_de_false + g -1

#Estas funciones son lo que va a ahcer con el numero que se va a mover
def subir(x, y):
    z = x+1
    a = matriz[z][y]

    return obtenerNuevaMatriz(x, y, z, y, a)

def bajar(x, y):
    z = x-1
    a = matriz[z][y]

    return obtenerNuevaMatriz(x, y, z, y, a)

def izq(x, y):
    z = y+1
    a = matriz[x][z]

    return obtenerNuevaMatriz(x, y, x, z, a)

def derecha(x, y):
    z = y-1
    a = matriz[x][z]

    return obtenerNuevaMatriz(x, y, x, z, a)

#Se obtiene las nuevas matrices posibles para ser analizadas y obtener f´
def obtenerNuevaMatriz(x, y, nueva_x, nueva_y, a):

    nuevo_estado = np.copy(matriz)
    nuevo_estado[x, y] = a
    nuevo_estado[nueva_x, nueva_y] = 0

    return compararMatriz(nuevo_estado)

#Busca el numero menor dentro del arreglo de f´ para ver cual es el mejor movimiento
def buscarMenor(array_movimientos):
    numero_menor = np.min(array_movimientos)

    return numero_menor

def realizarMovimiento(comodin, matriz, estado_previo, array_movimientos):

    numero_menor = buscarMenor(array_movimientos)
    
    cantidad_de_repetidos = np.count_nonzero(array_movimientos == numero_menor)
    
    "if encuentra mas de 1 con el mismo valor se va a otro metodo"
    if cantidad_de_repetidos > 1:
        matriz_copia = np.copy(matriz)
        posicion = buscarMejorRuta(numero_menor, matriz_copia, array_movimientos, comodin)
        estado_previo = np.copy(matriz)

    else:
        posicion = np.where(array_movimientos == numero_menor)
        posicion = posicion[0]
        estado_previo = np.copy(matriz)
    
    matriz, comodin = realizarCambios(posicion, comodin, matriz)
    
    return matriz, estado_previo, comodin

def realizarCambios(posicion, comodin, matriz):

    "hay que separar esto en su propia funcion"
    if posicion == 0 or posicion == 1:
        z = comodin[0]+1
        a = matriz[z][comodin[1]]

        matriz[comodin[0], comodin[1]] = a
        matriz[z, comodin[1]] = 0

        comodin=[z, comodin[1]]
    
    elif posicion == 2 or posicion == 3:
        z = comodin[0]-1
        a = matriz[z][comodin[1]]

        matriz[comodin[0], comodin[1]] = a
        matriz[z, comodin[1]] = 0

        comodin=[z, comodin[1]]

    elif posicion == 4 or posicion == 5:
        z = comodin[1]+1
        a = matriz[comodin[0]][z]

        matriz[comodin[0], comodin[1]] = a
        matriz[comodin[0], z] = 0

        comodin=[comodin[0], z]

    elif posicion == 6 or posicion == 7:
        z = comodin[1]-1
        a = matriz[comodin[0]][z]

        matriz[comodin[0], comodin[1]] = a
        matriz[comodin[0], z] = 0

        comodin=[comodin[0], z]
    
    return matriz, comodin

#En caso de que se encuentren se encuentren varias opciones
def buscarMejorRuta(numero_menor, matriz_copia, array_movimientos, comodin):

    g = 0
    posiciones = np.where(array_movimientos == numero_menor)

    posiciones = posiciones[0]
    b = 100
    
    for posicion in posiciones:

        g = g+1
        
        matriz_copia, comodin = realizarCambios(posicion, comodin, matriz_copia)
        array_movimientos = np.array ([])
        comodin, matriz_copia, array_movimientos = llenarArregloMovimientos(comodin, matriz_copia, array_movimientos)
        
        numero_menor = buscarMenor(array_movimientos)
        a = numero_menor
        x = posicion

        if a < b:
            b = a            
            y = x

    "aqui se regresa el menor"
    return y

def compararEM():

    son_iguales = np.array_equal(matriz,eM)
    
    if son_iguales:
        return 0
    
    else:
        return 1
    
def llenarArregloMovimientos(comodin, matriz, array_movimientos):

    if comodin[0] == 0:
        "subir el numero hacia el comodin"
        array_movimientos = np.append(array_movimientos, subir(0, comodin[1]))
    else:
        array_movimientos = np.append(array_movimientos, 150)
        
    if comodin[0] == 1:
        "subir y bajar"
        array_movimientos = np.append(array_movimientos, subir(1, comodin[1]))
        array_movimientos = np.append(array_movimientos, bajar(1, comodin[1]))
    else:
        array_movimientos = np.append(array_movimientos, 150)
        array_movimientos = np.append(array_movimientos, 150)

    if comodin[0] == 2:
        "bajar el numero hacia el comodin"
        array_movimientos = np.append(array_movimientos, bajar(2, comodin[1]))
    else:
        array_movimientos = np.append(array_movimientos, 150)

    if comodin[1] == 0:
        "mover hacia la izq el numero hacia el comodin"
        array_movimientos = np.append(array_movimientos, izq(comodin[0], 0))
    else:
        array_movimientos = np.append(array_movimientos, 150)

    if comodin[1] == 1:
        "izq y derecha"
        array_movimientos = np.append(array_movimientos, izq(comodin[0], 1))
        array_movimientos = np.append(array_movimientos, derecha(comodin[0], 1))
    else:
        array_movimientos = np.append(array_movimientos, 150)
        array_movimientos = np.append(array_movimientos, 150)

    if comodin[1] == 2:
        "derecha"
        array_movimientos = np.append(array_movimientos, derecha(comodin[0], 2))
    else:
        array_movimientos = np.append(array_movimientos, 150)

    return comodin, matriz, array_movimientos

print("Inicio \n",matriz,"\n\n")
estado_previo = np.copy(matriz)

posiciones = np.where(matriz == 0)
comodin[0]=int(posiciones[0])
comodin[1]=int(posiciones[1])

while vEM != 0:
    array_movimientos = np.array ([])
    g = g + 1

    estados_previos = np.concatenate((estados_previos, [estado_previo]), axis=0)
    comodin, matriz, array_movimientos = llenarArregloMovimientos(comodin, matriz, array_movimientos)

    #Aqui detectar si todo el array esta lleno de 150 por lo que ya no hay mas movimientos disponibles
    if np.all(array_movimientos == 150):
        print("No se pudo llegar a una solucion, ya no quedan movimientos disponibles")
        break

    matriz, estado_previo, comodin = realizarMovimiento(comodin, matriz, estado_previo, array_movimientos)
    
    vEM = compararEM()
    movimientos = movimientos + 1
    
    print("Movimiento: ",movimientos,"\n",matriz,"\n\n")
    
#Impresion de movimientos totales
print("Movimientos totales: ",movimientos)
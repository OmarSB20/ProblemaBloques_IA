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

matrz_Comparacion = np.array ([
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


#Se compara el nuevo estado deseado con todos los estados previos ademas de obtner la factibilidad de este movimiento

def compararMatriz(nuevo_estado):
    
    for estados in estados_previos:
        son_iguales = np.array_equal(nuevo_estado, estados)

        if son_iguales:
            return 150
        

    else:
        matriz_boleana = (nuevo_estado == matrz_Comparacion)
        cantidad_de_false = np.count_nonzero(matriz_boleana == False)
        
        return cantidad_de_false + g -1

#Estas funciones van a generar los nuevos estados posibles de la matriz
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
    
    #Si se encuentran 2 o mas veces el mismo numero menor se busca la mejor ruta
    if cantidad_de_repetidos > 1:
        matriz_copia = np.copy(matriz)
        posicion = buscarMejorRuta(numero_menor, matriz_copia, array_movimientos, comodin)
        estado_previo = np.copy(matriz)

    #De lo contrario se continua normal
    else:
        posicion = np.where(array_movimientos == numero_menor)
        posicion = posicion[0]
        estado_previo = np.copy(matriz)
    
    matriz, comodin = realizarCambios(posicion, comodin, matriz)
    
    return matriz, estado_previo, comodin

#Segun la posicion en donde se encuentre el numero menor es el cambio que se le realizara a la matriz
def realizarCambios(posicion, comodin, matriz):

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

#Funcion que busca la mejor ruta si se encuentran 2 o mas veces el mismo numero menor
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

    return y

#Funcion para saber si ya se llego al Estado Meta
def compararEM():

    son_iguales = np.array_equal(matriz,eM)
    
    if son_iguales:
        return 0
    
    else:
        return 1

#Llena el arreglo de movimientos segun la factibilidad de cada movimiento, si no se puede realizar el movimiento
#o el movimiento genera una matriz ya generada anterirmente se agrega un numero 150
def llenarArregloMovimientos(comodin, matriz, array_movimientos):

    #Este movimiento busca subir un numero hacia nuestro espacio en blanco (0)
    if comodin[0] == 0:
        array_movimientos = np.append(array_movimientos, subir(0, comodin[1]))
    else:
        array_movimientos = np.append(array_movimientos, 150)
    
    #Este movimiento busca subir o bajar un numero hacia nuestro espacio en blanco (0)
    if comodin[0] == 1:
        array_movimientos = np.append(array_movimientos, subir(1, comodin[1]))
        array_movimientos = np.append(array_movimientos, bajar(1, comodin[1]))
    else:
        array_movimientos = np.append(array_movimientos, 150)
        array_movimientos = np.append(array_movimientos, 150)

    #Este movimiento busca bajar un numero hacia nuestro espacio en blanco (0)
    if comodin[0] == 2:
        array_movimientos = np.append(array_movimientos, bajar(2, comodin[1]))
    else:
        array_movimientos = np.append(array_movimientos, 150)

    #Este movimiento busca mover a la izq un numero hacia nuestro espacio en blanco (0)
    if comodin[1] == 0:
        array_movimientos = np.append(array_movimientos, izq(comodin[0], 0))
    else:
        array_movimientos = np.append(array_movimientos, 150)

    #Este movimiento busca mover a la izq o a la derecha un numero hacia nuestro espacio en blanco (0)
    if comodin[1] == 1:
        array_movimientos = np.append(array_movimientos, izq(comodin[0], 1))
        array_movimientos = np.append(array_movimientos, derecha(comodin[0], 1))
    else:
        array_movimientos = np.append(array_movimientos, 150)
        array_movimientos = np.append(array_movimientos, 150)

    #Este movimiento busca mover a la derecha un numero hacia nuestro espacio en blanco (0)
    if comodin[1] == 2:
        array_movimientos = np.append(array_movimientos, derecha(comodin[0], 2))
    else:
        array_movimientos = np.append(array_movimientos, 150)

    return comodin, matriz, array_movimientos

#Se imprime la matriz inicial
print("Inicio \n",matriz,"\n\n")
estado_previo = np.copy(matriz)

#Se buscan las posiciones x,y de nuestro espacio en blanco (0) con respecto a la matriz inicial
posiciones = np.where(matriz == 0)
comodin[0]=int(posiciones[0])
comodin[1]=int(posiciones[1])

#Ciclo que termina con el EM encontrado o cuando ya no hay movimientos posibles
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
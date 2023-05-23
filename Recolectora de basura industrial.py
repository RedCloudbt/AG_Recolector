import numpy as np
import random

#Distancias momentarias
distancias = [
    [0, 1100, 1200, 1300, 1600, 950, 1400, 2700, 1700, 1200, 1600],   #punto de partida
    [1100, 0, 700, 1000, 1400, 1400, 900, 1600, 1300, 1500, 1200], # American Coach de México
    [1200, 700, 0, 400, 700, 550, 250, 850, 600, 850, 500],  # Metal Mecánica Integral
    [1300, 1000, 400, 0, 400, 550, 550, 1400, 950, 550, 800], #GreenBrier   
    [1300, 1400, 850, 400, 0, 950, 1100, 1500, 1300, 120, 1200], #Greenbrier Sahagún
    [950, 1200, 650, 550, 950, 0, 900, 1400, 1100, 1100, 1000], #DSF INDUSTRIAS
    [1400, 900, 210, 600, 950, 750, 0, 600, 350, 1100, 240], #Giant Motors Latinoamérica
    [1200, 1600, 850, 1400, 1600, 1400, 650, 0, 250, 1700, 550], #METMET
    [1800, 1300, 600, 1000, 1300, 1100, 350, 250, 0, 1400, 300], #Dina Camiones, S.A. De C.V.
    [1300, 1700, 1000, 550, 0, 1000, 1200, 1700, 1400, 0, 1300], # Gunderson Concarril
    [1800, 1300, 600, 1200, 1600, 1200, 400, 400, 550, 1700, 0] #CIIMMATH
]
 # Crear una matriz vacía para guardar las sumas de las distancias de cada vector
fitness = [] 
# rutas
p=10
#probabilidad de mutación
pm=0.1
#probrabilidad de cruce
pc=0.75


# Pedir al usuario el tamaño del vector 
n = int(input("Fabricas: "))

# Generar matriz de vectores aleatorios
matriz = np.array([np.concatenate(([1], np.random.permutation(np.arange(2, n+1)), [1])) for _ in range(p)])
for i in range(matriz.shape[0]):
    while 1 in matriz[i, 1:-1]:
        idx = np.where(matriz[i, 1:-1] == 1)[0][0] + 1
        new_val = np.random.choice(np.arange(2, n+1))
        matriz[i, idx] = new_val

# Calcular la suma de las distancias de cada vector en la matriz
for vector in matriz:
    suma_distancias = 0
    for i in range(len(vector)-1):
        suma_distancias += distancias[vector[i]-1][vector[i+1]-1]
    fitness.append(suma_distancias)

 #Imprimir matriz de vectores generados
for i in range(p):
    print("Ruta ", i+1 ,": ",matriz[i]," Fitness: ", fitness[i])
    
for j in range(10000):
    # vector para ganadores
    ganadores = []
    # vector para almacenar hijos
    hijos = []
    #Selección por torneo
    for i in range(2): # Repetir el proceso 2 veces
        pos1 = random.randint(0, len(fitness)-1) # Seleccionar una posición aleatoria del vector fitness
        #print("posición 1 de la ronda: ",i+1, ": ", pos1)
        pos2 = random.randint(0, len(fitness)-1) # Seleccionar otra posición aleatoria del vector fitness
      #  print("posición 2 de la ronda: ",i+1, ": ", pos2)
        while pos2 == pos1: # Si las dos posiciones son iguales, seleccionar otra posición aleatoria para pos2
            pos2 = random.randint(0, len(fitness)-1)
        if fitness[pos1] < fitness[pos2]: # Comparar los valores almacenados en las posiciones seleccionadas
            ganadores.append(pos1) # Almacenar la posición con el valor más bajo en el vector ganadores
        else:
            ganadores.append(pos2) # Almacenar la posición con el valor más bajo en el vector ganadores
      
        # Cruce
    rpc = random.random()
    # Cruce
    rpc = random.random()
    if rpc <= pc:
        for i in range(0, len(ganadores), 2):
            padre1 = matriz[ganadores[i]].copy()
            padre2 = matriz[ganadores[i+1]].copy()
            punto_cruce = random.randint(1, n-1)
            # Primer segmento del hijo1 es el número 1
            hijo1 = np.array([1])
            # Completar primera mitad de hijo1 con números del padre1 sin repeticiones excepto el 1
            for j in padre1[:n//2]:
                if j != 1 and j not in hijo1:
                    hijo1 = np.append(hijo1, j)
            # Completar segunda mitad de hijo1 con números del padre2 sin repeticiones excepto el 1
            for j in padre2:
                if j != 1 and j not in hijo1:
                    hijo1 = np.append(hijo1, j)
            # Añadir el número 1 al final de hijo1
            hijo1 = np.append(hijo1, 1)
            
            # Primer segmento del hijo2 es el número 1
            hijo2 = np.array([1])
            # Completar primera mitad de hijo2 con números del padre2 sin repeticiones excepto el 1
            for j in padre2[:n//2]:
                if j != 1 and j not in hijo2:
                    hijo2 = np.append(hijo2, j)
            # Completar segunda mitad de hijo2 con números del padre1 sin repeticiones excepto el 1
            for j in padre1:
                if j != 1 and j not in hijo2:
                    hijo2 = np.append(hijo2, j)
            # Añadir el número 1 al final de hijo2
            hijo2 = np.append(hijo2, 1)
            
            hijos.append(hijo1)
            hijos.append(hijo2)
          #  print("si hubo cruce")

    else:
       # print("no")
        for i in range(0, len(ganadores), 2):
            hijo1 = matriz[ganadores[i]].copy()
            hijo2 = matriz[ganadores[i+1]].copy()
          #  hijo1 = np.unique(hijo1, return_index=False)
           # hijo2 = np.unique(hijo2, return_index=False)
            hijos.append(hijo1)
            hijos.append(hijo2)

    #print(hijos)

    #Mutación
    rpm = random.random()
    for i in range(len(hijos)):
        if rpm <= pm:
        #    print("Se realizó la mutación")
            puntos_mutacion = random.sample(range(1, n-1), 2)  # Seleccionar dos puntos de mutación diferentes, excluyendo la posición 0 y la última posición
            hijo_mutado = hijos[i].copy()  # Copiar el hijo original para no modificarlo directamente
            hijo_mutado[puntos_mutacion[0]], hijo_mutado[puntos_mutacion[1]] = hijo_mutado[puntos_mutacion[1]], hijo_mutado[puntos_mutacion[0]]  # Intercambiar los valores en los puntos de mutación
            hijos[i] = hijo_mutado  # Reemplazar el hijo original con el hijo mutado
      #      print("Se produjo mutación en el hijo ", i+1)
       # else:
       #     print("No se realizó la mutación")
            
    #print(hijos)
    # Calcula el fitness de los hijos
    fitness_hijos = []
    for vector in hijos:
        suma_distancias = 0
        for i in range(len(vector)-1):
            suma_distancias += distancias[vector[i]-1][vector[i+1]-1]
        fitness_hijos.append(suma_distancias)        
        
   # print("______________________________________________________________")
    #for i in range(2):
    #   print("ganadore ", i+1 ,matriz[ganadores[i]], fitness[ganadores[i]])
     #  print("hijos ", i+2 ,hijos[i], fitness_hijos[i])
   
   # Cambiando posiciones y fitness por los más bajos
    if fitness_hijos[0]<=fitness[ganadores[0]]:
        fitness[ganadores[0]]=fitness_hijos[0]
        matriz[ganadores[0]]=hijos[0]
    else:
        if fitness_hijos[1]<=fitness[ganadores[1]]:
            fitness[ganadores[1]]=fitness_hijos[1]
            matriz[ganadores[1]]=hijos[1]
        else:
            if fitness_hijos[0]<=fitness[ganadores[1]]:
                fitness[ganadores[1]]=fitness_hijos[0]
                matriz[ganadores[1]]=hijos[0]
            else:
                if fitness_hijos[1]<=fitness[ganadores[1]]:
                        fitness[ganadores[0]]=fitness_hijos[1]
                        matriz[ganadores[0]]=hijos[1]
            
    #Limpiar vectores
    for x in range(len(ganadores)-1,-1,-1):
        ganadores.pop
       # print("eliminado de ganadores: ",ganadores.pop)
        
    for x in range(len(hijos)-1,-1,-1):
        hijos.pop
       # print(hijos.pop)

for i in range(p):
    print("Ruta ", i+1 ,": ",matriz[i]," Fitness: ", fitness[i])


        
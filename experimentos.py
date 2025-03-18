import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from debug import *

def guardar_funciones(ruta, funciones):
    '''
    El formato del JSON es el siguiente:
    Lista de puntuaciones (de 0 a M_CLIQUE)
        Para cada lista se añaden todas las funciones computadas con dicha puntuación
            Para cada función se guarda una pareja (FND, p),
            donde FND es su forma normal disyuntiva y p es el número de puertas que ha hecho falta para computarla
    '''
    if funciones == None:
        return
    
    # Convertimos la lista en una cadena de texto con el formato deseado
    json_text = "{\n"
    for punt, lista in enumerate(funciones):
        if punt != 0:
            json_text += ",\n"
        json_text += (f'\t\"{punt}\": [\n')
        first = True
        for funcion in lista:
            if not first:
                json_text += ",\n"
            first = False
            json_text += (f"\t\t[{funcion[0]}, {punt}]")
        json_text += ("\n\t]")
    json_text += ("}")

    # Guardamos el JSON como un archivo de texto con extensión .json
    with open(ruta, "w") as f:
        f.write(json_text)

    # with open(ruta, "w") as f:
    #     f.write("{")
    #     for punt, lista in enumerate(funciones):
    #         f.write(f'\"{punt}\": [')
    #         for funcion in lista:
    #             f.write(f"{funcion[0]},")
    #         f.write("]")
    #     f.write("}")
    # dict_funciones = {str(i) : lista for i, lista in enumerate(funciones)}
    # # Guardar FNDs en JSON
    # with open(ruta, "w") as f:
    #     json.dump(dict_funciones, f, indent=4, separators=(",",": "))

def guardar_coordenadas(ruta, xAND, yAND, xOR, yOR):
    # Guardar coordenadas en CSV
    if xAND != None and yAND != None:
        with open(os.path.join(ruta, "coordenadasAND.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["old $\mu_x(f)$", "new $\mu_x(f)$"])
            writer.writerows([xAND, yAND])

    if xOR != None and yOR != None:
        with open(os.path.join(ruta, "coordenadasOR.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["old $\mu_x(f)$", "new $\mu_x(f)$"])
            writer.writerows([xOR, yOR])    

def guardar_graficas(ruta, iter, xAND=None, yAND=None, xOR=None, yOR=None):
    if xAND != None and yAND != None:
        fig = plt.figure(figsize = (8,5))
        plt.plot(xAND, yAND, 'ro', alpha = 0.5, label = "Incremento con AND")
        # plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
        title = "Simulación tras " + str(iter) + " iteraciones"
        plt.title(title)
        plt.legend()
        plt.xlabel("$\mu_x(f)$")
        plt.ylabel("$\mu_x(f)$")
        plt.savefig(os.path.join(ruta, "graficaAND.png"))
        plt.close()

    if xOR != None and yOR != None:
        fig = plt.figure(figsize = (8,5))
        # plt.plot(xAND, yAND, 'ro', alpha = 0.5, label = "Incremento con AND")
        plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
        title = "Simulación tras " + str(iter) + " iteraciones"
        plt.title(title)
        plt.legend()
        plt.xlabel("$\mu_x(f)$")
        plt.ylabel("$\mu_x(f)$")
        plt.savefig(os.path.join(ruta, "graficaOR.png"))
        plt.close()
    
    if xAND != None and yAND != None and xOR != None and yOR != None:
        fig = plt.figure(figsize = (8,5))
        plt.plot(xAND, yAND, 'ro', alpha = 0.5, label = "Incremento con AND")
        plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
        title = "Simulación tras " + str(iter) + " iteraciones"
        plt.title(title)
        plt.legend()
        plt.xlabel("$\mu_x(f)$")
        plt.ylabel("$\mu_x(f)$")
        plt.savefig(os.path.join(ruta, "graficaMixta.png"))
        plt.close()

def generar_nombre_experimento():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def guardar_simulacion(nombre, punt_funciones, iter, xAND, yAND, xOR, yOR):
    if nombre == None:
        nombre = generar_nombre_experimento()
    
    ruta = os.path.join("experimentos", nombre)
    
    # Crear la carpeta del experimento antes de guardar los archivos
    os.makedirs(ruta, exist_ok=True)

    guardar_funciones(os.path.join(ruta, "funciones_fnd.json"), punt_funciones)
    guardar_coordenadas(ruta, xAND, yAND, xOR, yOR)
    guardar_graficas(ruta, iter, xAND, yAND, xOR, yOR)

def guarda_genetico(nombre, poblaciones, puertas):
    '''Función para guardar los mejores pares de funciones por cada puerta utilizada'''
    if nombre == None:
        nombre = generar_nombre_experimento()
    for p in puertas:
        ruta = os.path.join("experimentos", nombre)
        with open(os.path.join(ruta, f"mejores_{p}.json")) as f:
            f.write(poblaciones[p])
    
def grafica_genetico(poblaciones, puertas):
    colores = {"AND": 'ro', "OR": 'bo'}
    fig = plt.figure(figsize = (8,5))
    for p in puertas:
        xs, ys = [], []
        for f in poblaciones[p]:
            xs.append(f[0][1]); xs.append(f[1][1])
            ys.append(f[2]); ys.append(f[2])
        #plt.xlim([0,420])
        plt.plot(xs, ys, colores[p], alpha = 0.5, label = f"Incremento con {p}")
        title = f"Máximo incremento con puerta {p}"
        plt.title(title)
        plt.legend()
        plt.xlabel("$\mu_x(f)$")
        plt.ylabel("Incremento")
    
    plt.show()

def leer_json_funciones(ruta):
    '''
    Lee un JSON donde tenemos listas de funciones (parejas FND-puertas) agrupadas por puntuaciones
    (las funciones le la lista n tienen puntuación n)
    Si el archivo está vacío o no tiene datos válidos, devuelve una lista vacía
    '''
    if not os.path.exists(ruta) or os.stat(ruta).st_size == 0:
        return []
    
    try:
        with open(ruta, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []   # En caso de que el JSON esté vacío o mal formado

    # El índice en la lista es la puntuación de las funciones
    ret = []
    for puntuacion, funciones in data.items():
        ret.append(funciones)

    # Nos quedamos solo con funciones hasta la puntuación máxima, no queremos listas vacías a partir de ahí
    while len(ret) > 0 and len(ret[-1]) == 0:
        ret.pop()

    return ret

def leer_fnds_por_puntuacion(ruta):
    funciones = leer_json_funciones(ruta)
    ret = []
    for lista in funciones:
        fnds = []
        for f in lista:
            fnds.append(f[0])   # La primera componente de cada item es la FND, la segunda es el número de puertas
        ret.append(fnds)
    
    return ret

def almacena_fnds(ruta_nuevas, ruta_almacen):
    '''
    Función para almacenar en ruta_almacen todas las FNDs provenientes de ruta_nuevas.
    Para cada FND (acompañada del número de puertas usado para computarla),
    se comprobará si ya estaba en ruta_almacen. En tal caso, se actualizará el número de puertas
    si resulta ser menor al que ya se tenía
    '''
    almacen = leer_json_funciones(ruta_almacen)
    nuevas = leer_json_funciones(ruta_nuevas)
    
    # Buscamos cada una de las nuevas FNDs
    max_punt = len(nuevas) - 1
    while len(almacen) <= max_punt:
        almacen.append([])
    for punt in range(max_punt):
        for f in nuevas[punt]:
            if len(f) == 0:
                continue
            fnd = f[0]
            encontrada = False
            for g in almacen[punt]:
                if fnd == g[0]:
                    g[1] = min(g[1], f[1])
                    encontrada = True
                    break
            if not encontrada:
                almacen[punt].append(f)

    # Nos quedamos solo con funciones hasta la puntuación máxima, no queremos listas vacías a partir de ahí
    while len(almacen) > 0 and len(almacen[-1]) == 0:
        almacen.pop()

    # Guardamos el almacen actualizado
    guardar_funciones(ruta_almacen, almacen)

def grafica_puntuaciones_por_puertas(funciones):
    '''
    Función para graficar la puntuación máxima obtenida por número de puertas
    El argumento es una lista de listas donde el índice indica la puntuación.
    Dentro, cada sublista contiene listas de dos elementos
        El primer elemento es una FND, y el segundo es el número de puertas necesitado para computarla
    '''
    # TODO No se deberían ver los puntos que realmente no existen

    por_puertas = []
    for punt, lista in enumerate(funciones):
        for funcion in lista:
            puertas = funcion[1]
            if punt > 30 and puertas == 0:
                debug(funcion)
            while len(por_puertas) <= puertas:
                por_puertas.append(0)
            por_puertas[puertas] = max(por_puertas[puertas], punt)
    
    fig = plt.figure(figsize = (8,5))
    plt.plot(range(len(por_puertas)), por_puertas, 'ro', alpha = 0.5)
    # plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
    title = "Relación entre número de puertas y puntuación máxima"
    plt.title(title)
    # plt.legend()
    plt.xlabel("Número de puertas")
    plt.ylabel("Puntuación máxima")
    # plt.savefig(os.path.join(ruta, "graficaAND.png"))
    plt.show()
    # plt.close()
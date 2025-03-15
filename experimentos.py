import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def guardar_funciones(ruta, punt_funciones):
    '''
    El formato del JSON es el siguiente:
    Lista de puntuaciones (de 0 a M_CLIQUE)
        Para cada lista se añaden todas las funciones computadas con dicha puntuación
            Para cada función se guarda una pareja (FND, p),
            donde FND es su forma normal disyuntiva y p es el número de puertas que ha hecho falta para computarla
    '''
    if punt_funciones == None:
        return
    dict_funciones = {str(i) : lista for i, lista in enumerate(punt_funciones)}
    # Guardar FNDs en JSON
    with open(os.path.join(ruta, "funciones_fnd.json"), "w") as f:
        json.dump(dict_funciones, f, indent=4)

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

def guardar_experimento(nombre=None, punt_funciones=None, iter=None, xAND=None, yAND=None, xOR=None, yOR=None):
    if nombre == None:
        nombre = generar_nombre_experimento()
    
    ruta = os.path.join("experimentos", nombre)

    # Crear la carpeta del experimento antes de guardar los archivos
    os.makedirs(ruta, exist_ok=True)

    guardar_funciones(ruta, punt_funciones)
    guardar_coordenadas(ruta, xAND, yAND, xOR, yOR)
    guardar_graficas(ruta, iter, xAND, yAND, xOR, yOR)
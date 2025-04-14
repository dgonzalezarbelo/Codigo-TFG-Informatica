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
            json_text += (f"\t\t[{funcion[0]}, {funcion[1]}]")
        json_text += ("\n\t]")
    json_text += ("}")

    # Guardamos el JSON como un archivo de texto con extensión .json
    with open(ruta, "w") as f:
        f.write(json_text)

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
        ruta = os.path.join("experimentos/experimentos_n8", f"{nombre}_{p}.json")
        json_text = "[\n"
        for i in range(len(poblaciones[p])):
            if i > 0:
                json_text += ",\n"
            json_text += "\t[\n"
            [f1, f2, incr] = poblaciones[p][i]
            json_text += f"\t\t[{f1[0]}, {f1[1]}],\n"
            json_text += f"\t\t[{f2[0]}, {f2[1]}],\n"
            json_text += f"\t\t{incr}\n"
            json_text += "\t]"
        json_text += "\n]"
        with open(ruta, "w") as f:
            f.write(json_text)

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

def leer_json_parejas(ruta):
    # '''
    # Lee un JSON donde tenemos listas de funciones (parejas FND-puertas) agrupadas por puntuaciones
    # (las funciones le la lista n tienen puntuación n)
    # Si el archivo está vacío o no tiene datos válidos, devuelve una lista vacía
    # '''
    if not os.path.exists(ruta) or os.stat(ruta).st_size == 0:
        return []
    
    try:
        with open(ruta, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []   # En caso de que el JSON esté vacío o mal formado
    
    return data

def leer_top_parejas(ruta, n_parejas):
    '''Función para leer las mejores n_parejas parejas obtenidas con algoritmo genético de parejas'''
    parejas = leer_json_parejas(ruta)
    ret = []
    for i in range(min(n_parejas, len(parejas))):
        ret.append([parejas[i][0][0], parejas[i][1][0]])
    return ret

def leer_top_funciones(ruta, n_funciones):
    '''Función para leer las mejores n_funciones funciones obtenidas con algoritmo genético de parejas'''
    datos = leer_json_parejas(ruta)
    funciones = []
    for i in range(0, min(n_funciones, len(datos)) // 2):
        par = datos[i]
        funciones.append(par[0][0])
        funciones.append(par[1][0])
    return funciones

def funciones_de_almacen_en_rango(ini, fin, ruta_almacen = "experimentos/experimentos_n8/almacen_fnds.json"):
    almacen = leer_json_funciones(ruta_almacen)
    funciones = []
    for punt in range(ini, fin):
        funciones += almacen[punt]
    return funciones

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

def filtrar_almacen_por_longitud(ruta_almacen="experimentos/experimentos_n8/almacen_fnds.json"):
    almacen = leer_json_funciones(ruta_almacen)
    LONG_MAXIMA = 150
    nuevo_almacen = [[] for _ in range(len(almacen))]
    for punt in range(len(almacen)):
        for [fnd, puertas] in almacen[punt]:
            if len(fnd) > LONG_MAXIMA:  # Descartamos la función si es demasiado larga
                continue
            nuevo_almacen[punt].append([fnd, puertas])
    # Borramos el contenido del archivo por ahora
    with open(ruta_almacen, "w") as f:
        pass
    guardar_funciones(ruta_almacen, nuevo_almacen)

def reducir_almacen(reduce, m, ruta_almacen="experimentos/experimentos_n8/almacen_fnds.json"):
    almacen = leer_json_funciones(ruta_almacen)
    nuevo_almacen = [[] for _ in range(len(almacen))]
    count = 0
    for punt in range(len(almacen)):
        for [fnd, puertas] in almacen[punt]:
            l = len(fnd)
            fnd = reduce(fnd)
            new_punt = m(fnd)
            if len(fnd) < l or new_punt != punt:
                count += 1
            nuevo_almacen[new_punt].append([fnd, puertas])
    # Borramos el contenido del archivo por ahora
    with open(ruta_almacen, "w") as f:
        pass
    guardar_funciones(ruta_almacen, nuevo_almacen)
    print(f"Había {count} funciones sin reducir")

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

def grafica_comparaciones(conjuntos_de_funciones, metrica, medida, nombre):
    '''
    Esta función sirve para hacer gráficas en las que se comparen los valores
    de cierta medida para varios grupos de funciones.
    Principalmente se usará para comparar funciones simuladas, aleatorias y pseudoaleatorias.
    Argumentos:
        conjuntos_de_funciones: Diccionario donde la clave es el tipo de función (simulada, aleatoria, ...)
                                y la clave es una lista de listas (índice = puntuación de las funciones)
    '''
    # fig = plt.figure(figsize = (8,5))
    fig, ax = plt.subplots(figsize=(8, 6))
    i_color = 0
    colores = ['ro', 'bo', 'go', 'yo']
    title = f"Comparación de puntuación y {nombre}"
    maximos, minimos = {}, {}

    # Recogemos los datos
    texto_info = ""
    for tipo, funciones in conjuntos_de_funciones.items():
        maximos[tipo], minimos[tipo] = float('-inf'), float('inf')
        xs, ys = [], []
        for f in funciones:
            xs.append(metrica(f))
            y = medida(f)
            ys.append(y)
            maximos[tipo] = max(maximos[tipo], y)
            minimos[tipo] = min(minimos[tipo], y)
            if len(xs) % 100 == 0:
                print(f"{len(xs)} puntos de funciones {tipo} calculados")
        # plt.plot(xs, ys, colores[i_color], alpha = 0.5, label = f"Funciones {tipo}")
        ax.plot(xs, ys, colores[i_color], alpha=0.5, label=f"Funciones {tipo}")
        i_color += 1

    # Mostramos mínimos y máximos debajo de la gráfica
    for tipo in conjuntos_de_funciones.keys():
        texto_info += f"{len(conjuntos_de_funciones[tipo])} funciones {tipo}: Máx = {maximos[tipo]:.4f}, Mín = {minimos[tipo]:.4f}\n"
    
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel(nombre)
    
    # Ajustamos márgenes para dejar espacio para el texto
    plt.subplots_adjust(bottom=0.25)

    # Ajustamos la posición del texto justo debajo de la gráfica
    ax.text(0.5, -0.35, texto_info, ha="center", fontsize=10, transform=ax.transAxes)

    plt.show()

def grafica_histograma(conjuntos_de_funciones, medida, nombre):
    '''
    Genera un histograma para comparar la distribución de una medida en distintos conjuntos de funciones.
    
    Argumentos:
        conjuntos_de_funciones: Diccionario donde la clave es el tipo de función (simulada, aleatoria, ...)
                                y el valor es una lista de listas de funciones.
        medida: Función que calcula la medida de interés para cada función.
        nombre: Nombre de la medida que se mostrará en los ejes y título.
    '''
    fig, ax = plt.subplots(figsize=(8, 6))
    colores = ['r', 'b', 'g', 'y', 'm', 'c']  # Colores para distinguir cada conjunto
    i_color = 0
    
    # Determinar el rango de valores de la medida
    min_valor, max_valor = 0, 4500 # El maximo para n = 8 es 4480
    bins = np.arange(min_valor // 100 * 100, (max_valor // 100 + 2) * 100, 100)
    
    # Recolectamos los valores de la medida para cada conjunto de funciones
    for tipo, funciones in conjuntos_de_funciones.items():
        valores_medida = [medida(f) for f in funciones]
        ax.hist(valores_medida, bins=bins, alpha=0.5, color=colores[i_color % len(colores)], 
                label=f"Funciones {tipo}", edgecolor='black', align='mid')
        i_color += 1
    
    plt.title(f"Distribución de {nombre}")
    plt.xlabel(nombre)
    plt.ylabel("Número de funciones")
    plt.legend()
    plt.show()

def grafica_variacion_medida(parejas, metrica, medida, combAND, combOR, nombre):
    '''
    Esta función sirve para hacer gráficas en las que se comparen los valores
    de cierta medida para parejas de funciones antes y después de pasar por una puerta AND o OR.
    '''
    # fig = plt.figure(figsize = (8,5))
    fig, ax = plt.subplots(figsize=(8, 6))
    colores = ['ro', 'bo', 'go', 'yo']
    title = f"Comparación de puntuación y variación de {nombre}"

    min_AND, max_AND, min_OR, max_OR = float('inf'), float('-inf'), float('inf'), float('-inf')

    # Recogemos los datos
    texto_info = ""
    xAND, yAND = [], []
    xOR, yOR = [], []
    for [f, g] in parejas:
        # maximos[tipo], minimos[tipo] = float('-inf'), float('inf')
        m_f, m_g = metrica(f), metrica(g)
        med_f, med_g = medida(f), medida(g)
        xAND.append(m_f); xAND.append(m_g)
        xOR.append(m_f); xOR.append(m_g)
        
        conj = combAND(f, g)
        disy = combOR(f, g)
        med_conj, med_disy = medida(conj), medida(disy)
        yAND.append(med_conj - med_f); yAND.append(med_conj - med_g)
        yOR.append(med_disy - med_f); yOR.append(med_disy - med_g)

        min_AND = min(min_AND, med_conj - med_f, med_conj - med_g)
        max_AND = max(max_AND, med_conj - med_f, med_conj - med_g)
        min_OR = min(min_OR, med_disy - med_f, med_disy - med_g)
        max_OR = max(max_OR, med_disy - med_f, med_disy - med_g)

        if (len(xAND) // 2) % 100 == 0:
            print(f"{len(xAND) // 2} puntos con cada puerta calculados")
    
    # plt.plot(xs, ys, colores[i_color], alpha = 0.5, label = f"Funciones {tipo}")
    ax.plot(xAND, yAND, colores[0], alpha=0.5, label=f"Variación con AND")
    ax.plot(xOR, yOR, colores[1], alpha=0.5, label=f"Variación con OR")

    # Mostramos mínimos y máximos debajo de la gráfica
    texto_info += f"{len(parejas)} parejas\n"
    texto_info += f"Variación AND: Máx = {max_AND:.4f}, Mín = {min_AND:.4f}\n"
    texto_info += f"Variación OR: Máx = {max_OR:.4f}, Mín = {min_OR:.4f}\n"
    
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x$")
    plt.ylabel(f"Variacón de {nombre}")
    
    # Ajustamos márgenes para dejar espacio para el texto
    plt.subplots_adjust(bottom=0.25)

    # Ajustamos la posición del texto justo debajo de la gráfica
    ax.text(0.5, -0.35, texto_info, ha="center", fontsize=10, transform=ax.transAxes)
    plt.savefig(f"metricas/graficas/variacion_{nombre}")
    # plt.show()
    plt.close()
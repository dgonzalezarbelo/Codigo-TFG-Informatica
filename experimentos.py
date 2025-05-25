# Este archivo se usa para todo tipo de experimentos a lo largo del estudio, para el manejo de datos y generación de gráficas, entre otras cosas

import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import random
from collections import defaultdict

def guardar_funciones(ruta, funciones):
    '''
    Guarda funciones resultantes del algoritmo genético.
    El formato del JSON es el siguiente:
    Lista de puntuaciones (de 0 a M_CLIQUE)
        Para cada lista se añaden todas las funciones computadas con dicha puntuación
            Para cada función se guarda una pareja (FND, p),
            donde FND es su forma normal disyuntiva y p es el número de puertas que ha hecho falta para computarla
            (Las puertas realmente no se usan, pero la implementación de muchas funciones mantiene ese formato)
    La función es básicamente un json.dump() pero hecho a mano para que las funciones se vean en una lista y que el archivo sea más fácilmente legible.
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
    '''
    Guarda las coordenadas resultantes del algoritmo genético.
    Las coordenadas son los valores de la métrica sintáctica antes y después de las puertas lógicas.
    '''
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
    '''
    Guarda las gráficas del algoritmo genético.
    Hace una por cada puerta individual y, si se usan ambas, una conjunta.
    '''
    if xAND != None and yAND != None:
        fig = plt.figure(figsize = (8,5))
        plt.plot(xAND, yAND, 'ro', alpha = 0.5, label = "Incremento con AND")
        title = "Simulación tras " + str(iter) + " iteraciones"
        plt.title(title)
        plt.legend()
        plt.xlabel("$\mu_x(f)$")
        plt.ylabel("$\mu_x(f)$")
        plt.savefig(os.path.join(ruta, "graficaAND.png"))
        plt.close()

    if xOR != None and yOR != None:
        fig = plt.figure(figsize = (8,5))
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
    '''Genera un nombre por defecto para experimentos cualesquiera (fecha_hora)'''
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def guardar_simulacion(nombre, punt_funciones, iter, xAND, yAND, xOR, yOR):
    '''
    Guarda toda la información relativa a una ejecución de algoritmo genético de simulación.
    Se guardan as funciones generadas, valores de las gráficas y las gráficas en sí en una carpeta nueva.
    Si no se le da un nombre a la ejecución se genera uno por defecto.
    '''
    if nombre == None:
        nombre = generar_nombre_experimento()
    
    ruta = os.path.join("experimentos", nombre)
    
    # Crear la carpeta del experimento antes de guardar los archivos
    os.makedirs(ruta, exist_ok=True)

    guardar_funciones(os.path.join(ruta, "funciones_fnd.json"), punt_funciones)
    guardar_coordenadas(ruta, xAND, yAND, xOR, yOR)
    guardar_graficas(ruta, iter, xAND, yAND, xOR, yOR)

def guarda_genetico(nombre, poblaciones, puertas):
    '''
    Guarda toda la información relativa a una ejecución de algoritmo genético de parejas.
    Se guardan las mejores parejas con el siguiente formato: ((f1, p1), (f2, p2), incremento), donde f1 y f2 son las puertas que se juntan,
    p1 y p2 son las puntuaciones de f1 y f2 e incremento es el valor que se gana de puntuación al juntar f1 y f2.
    Si no se le da un nombre a la ejecución se genera uno por defecto.
    '''
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
    '''Genera una gráfica con el resultado del algoritmo genético de parejas'''
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
    (las funciones de la n-ésima lista tienen puntuación n).
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
    '''Lee las funciones almacenadas en la ruta, sin el argumento adicional de las puertas'''
    funciones = leer_json_funciones(ruta)
    ret = []
    for lista in funciones:
        fnds = []
        for f in lista:
            fnds.append(f[0])   # La primera componente de cada item es la FND, la segunda es el número de puertas
        ret.append(fnds)
    return ret

def leer_json_parejas(ruta):
    '''Lee el contenido de un archivo de parejas de funciones (formato ((f1, p1), (f2, p2), incremento))'''
    if not os.path.exists(ruta) or os.stat(ruta).st_size == 0:
        return []
    
    try:
        with open(ruta, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []   # En caso de que el JSON esté vacío o mal formado
    return data

def leer_top_parejas(ruta, n_parejas):
    '''Lee las mejores n_parejas parejas obtenidas con algoritmo genético de parejas'''
    parejas = leer_json_parejas(ruta)
    ret = []
    for i in range(min(n_parejas, len(parejas))):
        ret.append([parejas[i][0][0], parejas[i][1][0]])
    return ret

def leer_top_funciones(ruta, n_funciones):
    '''Lee las mejores n_funciones funciones obtenidas con algoritmo genético de parejas'''
    datos = leer_json_parejas(ruta)
    funciones = []
    for i in range(0, min(n_funciones, len(datos)) // 2):
        par = datos[i]
        funciones.append(par[0][0])
        funciones.append(par[1][0])
    return funciones

def funciones_de_almacen_en_rango(ini, fin, ruta_almacen = "experimentos/experimentos_n8/almacen_fnds.json"):
    '''
    Devuelve todas las funciones con puntuaciones en rango [ini, fin] en el archivo indicado.
    Se devuelve una lista donde el índice es la puntuación de todas las funciones en la lista en dicha posición
    '''
    almacen = leer_fnds_por_puntuacion(ruta_almacen)
    funciones = []
    for punt in range(ini, min(fin, len(almacen) - 1) + 1):
        funciones += almacen[punt]
    return funciones

def poblacion_en_rango(ini, fin, n_funciones, ruta_almacen = "experimentos/experimentos_n8/almacen_fnds.json"):
    '''Devuelve una población inicial de n_funciones funciones de la ruta indicada cuyas puntuaciones están en el rango [ini, fin]'''
    todas = funciones_de_almacen_en_rango(ini, fin, ruta_almacen)
    ret = []
    for _ in range(n_funciones):
        ret.append(random.choice(todas))
    return ret

def funciones_almacen_por_puntuacion(puntuaciones, ruta_almacen = "experimentos/experimentos_n8/almacen_fnds.json"):
    '''
    Devuelve una lista de funciones de la ruta indicada donde la puntuación de cada una viene indicada en el argumento puntuaciones.
    puntuaciones es una lista de enteros, donde cada uno refleja el valor de la métrica de la función que se espera
    '''
    almacen = leer_fnds_por_puntuacion(ruta_almacen)
    ret = []
    for p in puntuaciones:
        while p >= len(almacen) or len(almacen[p]) == 0:    # Por si no hay ninguna función con esa puntuación
            p -= 1
        ret.append(random.choice(almacen[p]))
    return ret

def almacena_fnds(ruta_nuevas, ruta_almacen):
    '''
    Almacena en ruta_almacen todas las FNDs provenientes de ruta_nuevas.
    Para cada FND (acompañada del número de puertas usado para computarla),
    se comprobará si ya estaba en ruta_almacen. En tal caso, se actualizará el número de puertas si resulta ser menor al que ya se tenía
    '''
    almacen = leer_json_funciones(ruta_almacen)
    nuevas = leer_json_funciones(ruta_nuevas)
    
    total = new = 0
    for i in range(len(almacen)):
        total += len(almacen[i])

    # Buscamos cada una de las nuevas FNDs
    max_punt = len(nuevas) - 1
    while len(almacen) <= max_punt:
        almacen.append([])
    for punt in range(max_punt + 1):
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
                total += 1
                new += 1

    # Nos quedamos solo con funciones hasta la puntuación máxima, no queremos listas vacías a partir de ahí
    while len(almacen) > 0 and len(almacen[-1]) == 0:
        almacen.pop()

    # Guardamos el almacen actualizado
    guardar_funciones(ruta_almacen, almacen)

    print("Funciones guardadas en el almacén")
    print(f"Total de funciones almacenadas: {total}")
    print(f"Nuevas funciones almacenadas: {new}")

def filtrar_almacen_por_longitud(ruta_almacen="experimentos/experimentos_n8/almacen_fnds.json"):
    '''Escanea un archivo de funciones, eliminando todas aquellas cuya longitud (número de cláusulas) sea mayor al indicado en LONG_MAXIMA'''
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

def grafica_comparaciones(conjuntos_de_funciones, metrica, medida, nombre):
    '''
    Genera una gráfica que compara valores de una medida para varios grupos de funciones.
    Además guarda la gráfica como imagen y las coordenadas como archivo CSV.

    Parámetros:
        conjuntos_de_funciones: dict
            Diccionario con claves como 'simuladas', 'aleatorias', etc. y valores como listas de funciones.
        metrica: function
            Función para obtener el valor del eje x.
        medida: function
            Función para obtener el valor del eje y.
        nombre: str
            Nombre para identificar la medida y nombrar los archivos.
        carpeta_salida: str
            Carpeta donde se guardarán los resultados (imagen y CSV).
    '''

    carpeta_salida=f"metricas/graficas/comparaciones_{nombre}"

    # Crear carpeta si no existe
    os.makedirs(carpeta_salida, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    i_color = 0
    colores = ['ro', 'bo', 'go', 'yo']
    title = f"Comparación de puntuación y {nombre}"
    maximos, minimos = {}, {}

    texto_info = ""
    all_data = []  # Lista para guardar todos los puntos

    for tipo, funciones in conjuntos_de_funciones.items():
        maximos[tipo], minimos[tipo] = float('-inf'), float('inf')
        xs, ys = [], []
        for f in funciones:
            x = metrica(f)
            y = medida(f)
            xs.append(x)
            ys.append(y)
            all_data.append([tipo, x, y])
            maximos[tipo] = max(maximos[tipo], y)
            minimos[tipo] = min(minimos[tipo], y)
            if len(xs) % 100 == 0:
                print(f"{len(xs)} puntos de funciones {tipo} calculados")

        ax.plot(xs, ys, colores[i_color], alpha=0.5, label=f"Funciones {tipo}")
        i_color += 1

    for tipo in conjuntos_de_funciones.keys():
        texto_info += f"{len(conjuntos_de_funciones[tipo])} funciones {tipo}: Máx = {maximos[tipo]:.4f}, Mín = {minimos[tipo]:.4f}\n"

    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel(nombre)
    plt.subplots_adjust(bottom=0.25)
    ax.text(0.5, -0.35, texto_info, ha="center", fontsize=10, transform=ax.transAxes)

    # Guardar la figura
    ruta_imagen = os.path.join(carpeta_salida, f"grafica_{nombre}.png")
    plt.savefig(ruta_imagen)
    print(f"Gráfica guardada en: {ruta_imagen}")

    # Guardar datos en CSV
    ruta_csv = os.path.join(carpeta_salida, f"datos_{nombre}.csv")
    with open(ruta_csv, mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(['tipo', 'x', 'y'])  # Cabecera
        writer.writerows(all_data)
    print(f"Datos guardados en: {ruta_csv}")

    # plt.show()

def grafica_histograma(conjuntos_de_funciones, medida, nombre, valor_maximo):
    '''
    Genera un histograma para comparar la distribución de una medida en distintos conjuntos de funciones.
    Guarda la imagen y los datos en archivos.

    Argumentos:
        conjuntos_de_funciones: dict
            Clave: tipo de función (simulada, aleatoria, etc.)
            Valor: lista de funciones
        medida: function
            Función que calcula la medida de interés.
        nombre: str
            Nombre que se usará para el título, ejes, y nombres de archivos.
        carpeta_salida: str
            Carpeta donde se guardarán los resultados.
    '''
    carpeta_salida=f"metricas/graficas/histograma_{nombre}"

    os.makedirs(carpeta_salida, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    colores = ['r', 'b', 'g', 'y', 'm', 'c']  # Ampliable si hay más grupos
    i_color = 0

    # Rango predefinido del histograma (ajustable)
    min_valor, max_valor = 0, valor_maximo
    paso = (max_valor - min_valor) / 100
    bins = np.arange(min_valor, max_valor + paso, paso)

    # Lista para guardar todos los valores individuales para el CSV
    all_data = []

    for tipo, funciones in conjuntos_de_funciones.items():
        valores_medida = [medida(f) for f in funciones]
        all_data.extend([[tipo, v] for v in valores_medida])  # Guardamos tipo y valor
        ax.hist(valores_medida, bins=bins, alpha=0.5, 
                color=colores[i_color % len(colores)], 
                label=f"Funciones {tipo}", edgecolor='black', align='mid')
        i_color += 1

    plt.title(f"Distribución de {nombre}")
    plt.xlabel(nombre)
    plt.ylabel("Número de funciones")
    plt.legend()

    # Guardar la figura
    ruta_imagen = os.path.join(carpeta_salida, f"histograma_{nombre}.png")
    plt.savefig(ruta_imagen)
    print(f"Histograma guardado en: {ruta_imagen}")

    # Guardar datos en CSV
    ruta_csv = os.path.join(carpeta_salida, f"valores_histograma_{nombre}.csv")
    with open(ruta_csv, mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(['tipo', 'valor_medida'])  # Cabecera
        writer.writerows(all_data)
    print(f"Datos del histograma guardados en: {ruta_csv}")

    plt.show()

def grafica_variacion_medida(medida, combAND_with_not, combOR, nombre, simbolo):
    '''
    H gráficas en las que se comparen los valores de cierta medida para parejas de funciones antes y después de pasar por una puerta AND o OR.
    También guarda los datos en un archivo CSV.
    '''
    carpeta_salida = f"metricas/graficas/variacion_{nombre}"
    os.makedirs(carpeta_salida, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    colores = ['ro', 'bo', 'go', 'yo']
    title = f"Variación de {simbolo}"

    min_AND, max_AND, min_OR, max_OR = float('inf'), float('-inf'), float('inf'), float('-inf')
    xAND, yAND = [], []
    xOR, yOR = [], []

    datos_csv = []  # Aquí almacenamos los datos para el CSV

    almacen = leer_json_funciones("experimentos/experimentos_n8/almacen_fnds.json")

    min_punt = 25

    n_parejas = 500
    for _ in range(n_parejas):
        ok = False
        while not ok:
            ok = True
            m_f = random.randint(min_punt, len(almacen) - 1)
            m_g = random.randint(min_punt, len(almacen) - 1)
            f = random.choice(almacen[m_f])[0]
            g = random.choice(almacen[m_g])[0]
            med_f = medida(f)
            med_g = medida(g)
            fAND = combAND_with_not(f, g)
            if len(fAND) > 150:
                ok = False
                continue
            fOR = combOR(f, g)
            medAND = medida(fAND)
            if medAND == 0:
                ok = False
            medOR = medida(fOR)
        # Añadir a listas para graficar
        xAND.extend([med_f, med_g])
        yAND.extend([medAND, medAND])
        xOR.extend([med_f, med_g])
        yOR.extend([medOR, medOR])

        # Añadir a datos para CSV
        datos_csv.extend([
            ['AND', med_f, medAND],
            ['AND', med_g, medAND],
            ['OR', med_g, medOR],
            ['OR', med_g, medOR],
        ])

        min_AND = min(min_AND, medAND - med_f, medAND - med_g)
        max_AND = max(max_AND, medAND - med_f, medAND - med_g)
        min_OR = min(min_OR, medOR - med_f, medOR - med_g)
        max_OR = max(max_OR, medOR - med_f, medOR - med_g)

        print(f"{len(xAND) // 2} puntos con cada puerta calculados")

    ax.plot(xAND, yAND, colores[0], alpha=0.5, label="Variación con AND")
    ax.plot(xOR, yOR, colores[1], alpha=0.5, label="Variación con OR")

    texto_info = (
        f"{n_parejas} parejas\n"
        f"Variación con puerta AND: Máx = {max_AND:.4f}, Mín = {min_AND:.4f}\n"
        f"Variación con puerta OR:  Máx = {max_OR:.4f}, Mín = {min_OR:.4f}\n"
    )

    plt.title(title)
    plt.legend()
    plt.xlabel(f"{simbolo} antes de puertas")
    plt.ylabel(f"{simbolo} después de puertas")
    plt.subplots_adjust(bottom=0.25)
    ax.text(0.5, -0.35, texto_info, ha="center", fontsize=10, transform=ax.transAxes)

    # Guardar la imagen
    ruta_imagen = os.path.join(carpeta_salida, f"variacion_{nombre}.png")
    plt.savefig(ruta_imagen)
    print(f"Gráfica guardada en: {ruta_imagen}")

    # Guardar datos en CSV
    ruta_csv = os.path.join(carpeta_salida, f"valores_variacion_{nombre}.csv")
    with open(ruta_csv, mode='w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(['puerta', 'medida_antes', 'medida_despues'])  # Cabecera
        writer.writerows(datos_csv)
    print(f"Datos de la variación guardados en: {ruta_csv}")

    # plt.show()

def leer_csv_a_diccionario_generalizado(nombre_archivo):
    """
    Lee un archivo CSV con formato tipo,x,y,z,... y lo convierte en un diccionario.
    
    Argumentos:
    nombre_archivo: str
        El nombre del archivo CSV a leer.
    
    Devuelve dict
        Un diccionario donde las claves son los tipos (e.g. "simuladas", "aleatorias", "pseudoaleatorias")
        y los valores son listas de tuplas con las coordenadas (x, y, z, ...).
    """
    diccionario = {}
    
    with open(nombre_archivo, mode='r') as archivo_csv:
        lector = csv.reader(archivo_csv)
        next(lector)  # Saltamos la cabecera si existe
        
        for fila in lector:
            tipo = fila[0]  # Primer valor es el tipo
            coordenadas = tuple(map(float, fila[1:]))  # Convertimos todas las coordenadas a float
            
            # Si el tipo no está en el diccionario, lo inicializamos
            if tipo not in diccionario:
                diccionario[tipo] = []
            
            # Añadimos la tupla de coordenadas al tipo correspondiente
            diccionario[tipo].append(coordenadas)
    
    return diccionario

def generar_grafica_desde_diccionario(diccionario, ejeX, ejeY, titulo):
    """
    Genera una gráfica de los puntos en el diccionario, con colores distintos para cada tipo de datos,
    y traza una sucesión de segmentos que pasa por los puntos mínimos de las "simuladas" y los máximos
    de las "pseudoaleatorias".
    
    Argumentos:
    diccionario: dict
        Diccionario donde las claves son los tipos ("simuladas", "aleatorias", "pseudoaleatorias")
        y los valores son listas de tuplas con las coordenadas (x, y, z, ...).
    """
    # Definir los colores según el tipo
    colores = {
        "simuladas": "red",      # Rojo para "simuladas"
        "aleatorias": "green",   # Verde para "aleatorias"
        "pseudoaleatorias": "blue"  # Azul para "pseudoaleatorias"
    }

    # Crear la figura y el eje para el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    tipos_a_graficar = ["simuladas", "pseudoaleatorias", "aleatorias"]
    # tipos_a_graficar = ["simuladas", "pseudoaleatorias"]

    # Diccionarios para almacenar los valores mínimos y máximos por x
    simuladas_min = defaultdict(list)  # Para los valores mínimos de simuladas
    pseudoaleatorias_max = defaultdict(list)  # Para los valores máximos de pseudoaleatorias

    maximos, minimos = {}, {}

    # Recorrer el diccionario y dibujar los puntos
    for tipo, puntos in diccionario.items():
        maximos[tipo], minimos[tipo] = float('-inf'), float('inf')
        if tipo not in tipos_a_graficar:
            continue

        puntos = list(filter(lambda x : x[0] > 25, puntos))
        x_vals = [punto[0] for punto in puntos]  # Extraemos los valores de X
        y_vals = [punto[1] for punto in puntos]  # Extraemos los valores de Y
        maximos[tipo] = max(y_vals)
        minimos[tipo] = min(y_vals)

        # Dibujar los puntos con el color correspondiente
        ax.scatter(x_vals, y_vals, color=colores.get(tipo, "black"), label=tipo, alpha=0.6)

        # Agrupar puntos por x y almacenar los mínimos y máximos
        for x, y in zip(x_vals, y_vals):
            if tipo == "simuladas":
                simuladas_min[x].append(y)  # Guardamos los valores de Y para simuladas
            elif tipo == "pseudoaleatorias":
                pseudoaleatorias_max[x].append(y)  # Guardamos los valores de Y para pseudoaleatorias

    # Añadir título y etiquetas a los ejes
    ax.set_title(titulo)
    ax.set_xlabel(ejeX)
    ax.set_ylabel(ejeY)
    
    # Añadir la leyenda
    ax.legend()

    texto_info = ""
    for tipo in tipos_a_graficar:
        texto_info += f"{len(diccionario[tipo])} funciones {tipo}: Máx = {maximos[tipo]:.4f}, Mín = {minimos[tipo]:.4f}\n"

    plt.subplots_adjust(bottom=0.25)
    ax.text(0.5, -0.35, texto_info, ha="center", fontsize=10, transform=ax.transAxes)
    # Mostrar la gráfica
    plt.show()

def generar_histograma_desde_diccionario(diccionario, ejeX, titulo, valor_maximo):
    '''
    Genera un histograma para comparar la distribución de las coordenadas en distintos tipos de puntos.
    
    Argumentos:
        diccionario: dict
            Clave: tipo de punto (simuladas, aleatorias, pseudoaleatorias)
            Valor: lista de tuplas con las coordenadas (x, y, z, ...).
        nombre: str
            Nombre que se usará para el título, ejes, y nombres de archivos.
        valor_maximo: float
            Valor máximo en el eje para la visualización del histograma.
    '''

    fig, ax = plt.subplots(figsize=(8, 6))
    colores = ['r', 'b', 'g', 'y', 'm', 'c']  # Ampliable si hay más grupos
    i_color = 0

    # Rango predefinido del histograma (ajustable)
    min_valor, max_valor = 0, valor_maximo
    paso = (max_valor - min_valor) / 100
    bins = np.arange(min_valor, max_valor + paso, paso)

    tipos_a_graficar = ["simuladas", "pseudoaleatorias"]

    x_min = 25
    maximos, minimos = {}, {}

    # Recorremos el diccionario con los puntos
    for tipo, puntos in diccionario.items():
        maximos[tipo], minimos[tipo] = float('-inf'), float('inf')
        if tipo not in tipos_a_graficar:
            continue

        # Extraemos las coordenadas x y de los puntos
        puntos = list(filter(lambda x : x[0] > x_min, puntos))
        x_vals = [punto[0] for punto in puntos]
        y_vals = [punto[1] for punto in puntos]
        maximos[tipo] = max(y_vals)
        minimos[tipo] = min(y_vals)

        # Dibujamos el histograma de las coordenadas x y en el gráfico
        ax.hist(y_vals, bins=bins, alpha=0.5, 
                color=colores[i_color % len(colores)], 
                label=f"{tipo}", edgecolor='black', align='mid')
        i_color += 1

    texto_info = ""
    for tipo in tipos_a_graficar:
        texto_info += f"{len(diccionario[tipo])} funciones {tipo}: Máx = {maximos[tipo]:.4f}, Mín = {minimos[tipo]:.4f}\n"

    plt.subplots_adjust(bottom=0.25)
    ax.text(0.5, -0.35, texto_info, ha="center", fontsize=10, transform=ax.transAxes)    

    # Configuración de la gráfica
    plt.title(titulo)
    plt.xlabel(ejeX)
    plt.ylabel("Número de funciones")
    plt.legend()
    plt.show()

def generar_variacion_desde_diccionario(diccionario, ejeX, ejeY, titulo):
    '''Genera una gráfica a partir de los valores de los argumentos'''
    
    # Definir los colores según el tipo
    colores = {
        "AND": "red",      # Rojo para "simuladas"
        "OR": "blue"  # Azul para "pseudoaleatorias"
    }

    # Crear la figura y el eje para el gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    puertas_a_graficar = ["AND", "OR"]

    # Diccionarios para almacenar los valores mínimos y máximos por x

    var_max, var_min = {}, {}

    # Recorrer el diccionario y dibujar los puntos
    for puerta, puntos in diccionario.items():
        var_max[puerta], var_min[puerta] = float('-inf'), float('inf')
        if puerta not in puertas_a_graficar:
            continue

        x_vals = [punto[0] for punto in puntos]  # Extraemos los valores de X
        y_vals = [punto[1] for punto in puntos]  # Extraemos los valores de Y
        var_max[puerta] = max([y_vals[i] - x_vals[i] for i in range(len(puntos))])
        var_min[puerta] = min([y_vals[i] - x_vals[i] for i in range(len(puntos))])

        # Dibujar los puntos con el color correspondiente
        ax.scatter(x_vals, y_vals, color=colores.get(puerta, "black"), label=puerta, alpha=0.6)

    # Añadir título y etiquetas a los ejes
    ax.set_title(titulo)
    ax.set_xlabel(ejeX)
    ax.set_ylabel(ejeY)
    
    # Añadir la leyenda
    ax.legend()

    texto_info = (
        f"{len(diccionario["AND"])} parejas\n"
        f"Variación con puerta AND: Máx = {var_max['AND']:.4f}, Mín = {var_min['AND']:.4f}\n"
        f"Variación con puerta OR:  Máx = {var_max['OR']:.4f}, Mín = {var_min['OR']:.4f}\n"
    )

    plt.subplots_adjust(bottom=0.25)
    ax.text(0.5, -0.35, texto_info, ha="center", fontsize=10, transform=ax.transAxes)
    # Mostrar la gráfica
    plt.show()
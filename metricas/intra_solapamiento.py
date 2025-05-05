from syntactic import *
from debug import debug
from genetic import *
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from experimentos import *

def solapamiento(f):
    '''Calcula la intersección promedio entre cláusulas de f'''
    sum = 0
    n = len(f)
    if n <= 1: #FIXME Igual sería mejor lanzar una excepción en este caso, la precondición debería ser n >= 2
        return 0
    for i in range(n):
        for j in range(i + 1, n):
            sum += common_literals(f[i], f[j]) / max(len(f[i]), len(f[j]))
    return sum / (n * (n - 1))

def formula_solapamiento_clique():
    sumatorio = sum([math.comb(x, 2) * math.comb(K, x) * math.comb(N - K, K - x) for x in range(2, K + 1)])
    return (sumatorio - math.comb(K, 2)) / (2 * (math.comb(N, K) - 1) * math.comb(K, 2))

def grafica_sopalamiento_simuladas_vs_aleatorias():
    max_funciones = 10000
    almacen = leer_fnds_por_puntuacion("experimentos/experimentos_n8/almacen_fnds.json")
    ini, fin = 10, 221
    xSim, ySim = [], []
    xAl, yAl = [], []
    for i in range(max_funciones):
        punt = random.randint(ini, fin)
        while len(almacen[punt]) == 0:
            punt = random.randint(ini, fin)
        fSim = random.choice(almacen[punt])
        while len(fSim) == 1:
            fSim = random.choice(almacen[punt])
        xSim.append(punt)
        ySim.append(solapamiento(fSim))
        
        fAl = genera_pseudoaleatoria_puntuacion(punt)
        while len(fAl) == 1:
            fAl = genera_pseudoaleatoria_puntuacion(punt)

        xAl.append(punt)
        yAl.append(solapamiento(fAl))
        debug(f"{i + 1} solapamientos simulados y pseudo-aleatorios calculados")

    # Graficamos los resultados
    fig = plt.figure(figsize = (8,5))
    plt.plot(xSim, ySim, 'ro', alpha = 0.5, label = "Solapamiento de funciones simuladas")
    plt.plot(xAl, yAl, 'bo', alpha = 0.5, label = "Solapamiento de funciones aleatorias")
    title = "Comparación de puntuación y solapamiento para funciones simuladas y aleatorias"
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel("Solapamiento promedio")
    plt.show()

def grafica_intrasolapamiento_mejores(n_funciones):
    simuladas = leer_top_funciones("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    pseudoaleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json", n_funciones)
    aleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_aleatorias_100-150_AND.json", n_funciones)
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, solapamiento, "Solapamiento")

def grafica_variacion_intrasolapamiento(n_funciones):
    parejas = leer_top_parejas("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    grafica_variacion_medida(parejas, m, solapamiento, combAND_with_not, combOR, "Solapamiento")

def compara_solapamiento():
    n_funciones = 1000
    ini, fin = 1, 250
    puntuaciones = [random.randint(ini, fin) for _ in range(n_funciones)]
    simuladas = funciones_almacen_por_puntuacion(puntuaciones)
    # simuladas = poblacion_en_rango(ini, fin, n_funciones)
    aleatorias = funciones_almacen_por_puntuacion(puntuaciones, "experimentos/experimentos_n8/almacen_aleatorias.json")
    pseudoaleatorias = [genera_pseudoaleatoria_puntuacion(p) for p in puntuaciones]
    # aleatorias = poblacion_en_rango(ini, fin, n_funciones, "experimentos/experimentos_n8/almacen_aleatorias.json")
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, solapamiento, "Solapamiento")

def matriz_confusion_umbral_solapamiento(diccionario, umbral=0.1):
    """
    Predice el tipo de cada punto en función de su coordenada Y y muestra la matriz de confusión.

    Argumentos:
        diccionario: dict
            Diccionario con claves "simuladas", "pseudoaleatorias", etc.
            Los valores son listas de tuplas con coordenadas (x, y, ...).
        umbral: float
            Umbral de la coordenada Y para decidir la predicción.
            Por defecto es 0.1.
    """

    # Nos centramos solo en simuladas y pseudoaleatorias
    tipos_validos = ["simuladas", "pseudoaleatorias"]
    y_true = []
    y_pred = []

    for tipo in tipos_validos:
        puntos = diccionario.get(tipo, [])
        for punto in puntos:
            y = punto[1]  # Suponemos que la coordenada Y es la de solapamiento
            y_true.append(tipo)
            if y < umbral:
                y_pred.append("pseudoaleatorias")
            else:
                y_pred.append("simuladas")

    # Generamos la matriz de confusión
    etiquetas = ["simuladas", "pseudoaleatorias"]
    matriz = confusion_matrix(y_true, y_pred, labels=etiquetas)
    disp = ConfusionMatrixDisplay(confusion_matrix=matriz, display_labels=etiquetas)

    # Mostramos la matriz
    disp.plot(cmap=plt.cm.Blues)
    plt.title(f"Matriz de confusión (umbral = {umbral})")
    plt.show()

def variacion_solapamiento():
    grafica_variacion_medida(solapamiento, combAND_with_not, combOR, "Solapamiento")
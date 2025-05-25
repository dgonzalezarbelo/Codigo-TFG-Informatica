from syntactic import *
from genetic import *
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
from experimentos import *

def solapamiento(f):
    '''Función para calcular la medida de solapamiento de f'''
    sum = 0
    n = len(f)
    if n <= 1:
        return 0
    for i in range(n):
        for j in range(i + 1, n):
            sum += common_literals(f[i], f[j]) / max(len(f[i]), len(f[j]))
    return 2 * sum / (n * (n - 1))

def formula_solapamiento_clique():
    '''Calcula el solapamiento de la función que computa Clique en función de n y k'''
    sumatorio = sum([math.comb(x, 2) * math.comb(K, x) * math.comb(N - K, K - x) for x in range(2, K + 1)])
    return (sumatorio - math.comb(K, 2)) / (2 * (math.comb(N, K) - 1) * math.comb(K, 2))

def grafica_solapamiento_mejores(n_funciones):
    '''Genera una gráfica comparando el solapamiento de funciones las mejores funciones
    simuladas, pseudoaleatorias y aleatorias resultantes del algoritmo genético de parejas'''
    simuladas = leer_top_funciones("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    pseudoaleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json", n_funciones)
    aleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_aleatorias_100-150_AND.json", n_funciones)
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, solapamiento, "Solapamiento")

def compara_solapamiento(simuladas, pseudoaleatorias, aleatorias):
    '''Genera una gráfica que compara el solapamiento de funciones simuladas, pseudoaleatorias y aleatorias'''
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, solapamiento, "Solapamiento")

def matriz_confusion_umbral_solapamiento(diccionario, umbral=0.2):
    '''Genera la matriz de confusión de la predicción del tipo de función en base a su valor de solapamiento
        con respecto al de la función que computa Clique'''

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
    '''Genera una gráfica de la variación del solapamiento de funciones simuladas tras la aplicación de puertas AND y OR'''
    grafica_variacion_medida(solapamiento, combAND_with_not, combOR, "Solapamiento", "$\\eta_s$")
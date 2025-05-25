from syntactic import *
from genetic import *
from experimentos import *

def homogeneidad(f):
    '''Función para calcular la medida de homogeneidad de f'''
    veces = [0 for _ in range(A)]
    for c in f:
        for literal in c:
            veces[abs(literal) - 1] += 1
    media = sum(veces) / A
    varianza = sum((s - media) ** 2 for s in veces) / A
    return varianza

def grafica_homogeneidad_mejores(n_funciones):
    '''Genera una gráfica comparando la homogeneidad de funciones las mejores funciones
    simuladas, pseudoaleatorias y aleatorias resultantes del algoritmo genético de parejas'''
    simuladas = leer_top_funciones("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    pseudoaleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json", n_funciones)
    aleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_aleatorias_100-150_AND.json", n_funciones)
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, homogeneidad, "Equidad")

def compara_homogeneidad(simuladas, pseudoaleatorias, aleatorias):
    '''Genera una gráfica que compara la homogeneidad de funciones simuladas, pseudoaleatorias y aleatorias'''
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, homogeneidad, "Homogeneidad")

def variacion_homogeneidad():
    '''Genera una gráfica de la variación de la homogeneidad de funciones simuladas tras la aplicación de puertas AND y OR'''
    grafica_variacion_medida(homogeneidad, combAND_with_not, combOR, "Homogeneidad", "$\\eta_h$")
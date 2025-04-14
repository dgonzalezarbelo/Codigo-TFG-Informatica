from syntactic import *
from debug import debug
from genetic import *

def intra_solapamiento(f):
    '''Calcula la intersección promedio entre cláusulas de f'''
    sum = 0
    n = len(f)
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
        ySim.append(intra_solapamiento(fSim))
        
        fAl = genera_pseudoaleatoria_puntuacion(punt)
        while len(fAl) == 1:
            fAl = genera_pseudoaleatoria_puntuacion(punt)

        xAl.append(punt)
        yAl.append(intra_solapamiento(fAl))
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
    grafica_comparaciones(dic, m, intra_solapamiento, "Intra-solapamiento")

def grafica_variacion_intrasolapamiento(n_funciones):
    parejas = leer_top_parejas("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    grafica_variacion_medida(parejas, m, intra_solapamiento, combAND_with_not, combOR, "Intra-solapamiento")
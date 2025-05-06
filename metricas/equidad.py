from syntactic import *
from debug import debug
from genetic import *
from experimentos import *

def homogeneidad(fnd):
    veces = [0 for _ in range(A)]
    for c in fnd:
        for literal in c:
            veces[abs(literal) - 1] += 1
    media = sum(veces) / A
    varianza = sum((s - media) ** 2 for s in veces) / A

    return varianza

def grafica_equidad_simuladas_vs_aleatorias():
    max_funciones = 1000
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
        ySim.append(homogeneidad(fSim))
        
        fAl = genera_pseudoaleatoria_puntuacion(punt)
        while len(fAl) == 1:
            fAl = genera_pseudoaleatoria_puntuacion(punt)

        xAl.append(punt)
        yAl.append(homogeneidad(fAl))
        debug(f"{i + 1} equidades simuladas y pseudoaleatorias calculadas")

    # Graficamos los resultados
    fig = plt.figure(figsize = (8,5))
    plt.plot(xSim, ySim, 'ro', alpha = 0.5, label = "Equidad de funciones simuladas")
    plt.plot(xAl, yAl, 'bo', alpha = 0.5, label = "Equidad de funciones aleatorias")
    title = "Comparación de puntuación y equidad para funciones simuladas y aleatorias (muestreo de 100000 grafos)"
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel("Equidad")
    plt.show()

def grafica_equidad_mejores(n_funciones):
    simuladas = leer_top_funciones("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    pseudoaleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json", n_funciones)
    aleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_aleatorias_100-150_AND.json", n_funciones)
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, homogeneidad, "Equidad")

def grafica_variacion_equidad(n_funciones):
    parejas = leer_top_parejas("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    grafica_variacion_medida(parejas, m, homogeneidad, combAND_with_not, combOR, "Equidad")

def compara_homogeneidad(simuladas, pseudoaleatorias, aleatorias):
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, homogeneidad, "Homogeneidad")

def variacion_homogeneidad():
    grafica_variacion_medida(homogeneidad, combAND_with_not, combOR, "Homogeneidad", "$\\eta_s$")
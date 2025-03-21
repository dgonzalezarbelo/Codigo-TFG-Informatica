from syntactic import *
from debug import debug
from genetic import *

def perdidas(f):
    m_f, asignaciones = m(f, devuelve_asignacion=True)
    asig = [0 for i in range(max(len(f), len(clique)) + 1)]
    for (a, b) in asignaciones:
        asig[a] = b
    malas_asignaciones, punt_ideal = 0, 0
    for i in range(len(f)):
        mejor_asig = 0
        for j in range(len(clique)):
            cur_asig = common_literals(f[i], clique[j])
            mejor_asig = max(mejor_asig, cur_asig)
        punt_ideal += mejor_asig
        if asig[i + 1] == 0 or asig[i + 1] - 1 >= len(clique) or mejor_asig > common_literals(f[i], clique[asig[i + 1] - 1]):
            malas_asignaciones += 1
    return [malas_asignaciones, punt_ideal - m_f]

def grafica_perdidas_simuladas_vs_aleatorias():
    max_funciones = 1000
    almacen = leer_fnds_por_puntuacion("experimentos/experimentos_n8/almacen_fnds.json")
    ini, fin = 10, 221
    xSim, ySimMalasAsig, ySimPerdidas = [], [], []
    xAl, yAlMalasAsig, yAlPerdidas = [], [], []
    for i in range(max_funciones):
        punt = random.randint(ini, fin)
        while len(almacen[punt]) == 0:
            punt = random.randint(ini, fin)
        fSim = random.choice(almacen[punt])
        while len(fSim) == 1:
            fSim = random.choice(almacen[punt])
        xSim.append(punt)
        [malasAsig, perd] = perdidas(fSim)
        ySimMalasAsig.append(malasAsig)
        ySimPerdidas.append(perd)
        
        fAl = genera_pseudoaleatoria_puntuacion(punt)
        while len(fAl) == 1:
            fAl = genera_pseudoaleatoria_puntuacion(punt)

        xAl.append(punt)
        [malasAsig, perd] = perdidas(fAl)
        yAlMalasAsig.append(malasAsig)
        yAlPerdidas.append(perd)
        debug(f"{i + 1} pérdidas simuladas y pseudoaleatorias calculadas")

    # Graficamos los resultados
    fig = plt.figure(figsize = (8,5))
    plt.plot(xSim, ySimMalasAsig, 'ro', alpha = 0.5, label = "Malas asignaciones de funciones simuladas")
    plt.plot(xAl, yAlMalasAsig, 'bo', alpha = 0.5, label = "Malas asignaciones de funciones aleatorias")
    title = "Comparación de puntuación y malas asignaciones para funciones simuladas y aleatorias"
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel("Malas asignaciones")
    plt.show()

    fig = plt.figure(figsize = (8,5))
    plt.plot(xSim, ySimPerdidas, 'ro', alpha = 0.5, label = "Pérdidas de funciones simuladas")
    plt.plot(xAl, yAlPerdidas, 'bo', alpha = 0.5, label = "Pérdidas de funciones aleatorias")
    title = "Comparación de puntuación y pérdidas para funciones simuladas y aleatorias"
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel("Pérdidas")
    plt.show()
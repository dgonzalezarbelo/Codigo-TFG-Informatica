from syntactic import *
from debug import debug
from genetic import *

def evalua_fnd(fnd, valores):
    for clausula in fnd:
        acepta = True
        for literal in clausula:
            if (literal > 0 and valores[literal] == 1) or (literal < 0 and valores[abs(literal)] == -1):
                continue
            else:
                acepta = False
        if acepta:
            return True
    return False

def metrica_sensibilidad(fnd):
    '''
    Función que, dada una función booleana representada como FND,
    calcula su sensibilidad a cliqué, probando con todos los grafos de N vértices
    TODO Escribir bien por algún lado la definición de la métrica
    '''
    sensibilidades = [0 for _ in range(len(clique))]
    tam_muestreo = 1000
    for _ in range(tam_muestreo):
        G = random.randint(0, (1 << A) - 1)
        valores = [0] + [0 for _ in range(A)]
        for i in range(1, A + 1):
            valores[i] = (G >> i) & 1   # Tomamos de la representación de G los valores de cada input
        
        # Tenemos que probar para cada cliqué C si f(G) != f(G union C)
        for C in range(len(clique)):
            new_valores = valores.copy()
            for literal in clique[C]:
                new_valores[literal] = 1
            out1 = evalua_fnd(fnd, valores)
            out2 = evalua_fnd(fnd, new_valores)
            if out1 != out2:
                sensibilidades[C] += 1

    media = sum(sensibilidades) / len(clique)
    varianza = sum((s - media) ** 2 for s in sensibilidades) / len(clique)

    return varianza

def grafica_sopalamiento_simuladas_vs_aleatorias():
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
        ySim.append(metrica_sensibilidad(fSim))
        
        fAl = genera_pseudoaleatoria_puntuacion(punt)
        while len(fAl) == 1:
            fAl = genera_pseudoaleatoria_puntuacion(punt)

        xAl.append(punt)
        yAl.append(metrica_sensibilidad(fAl))
        debug(f"{i + 1} sensibilidades simulados y pseudo-aleatorios calculados")

    # Graficamos los resultados
    fig = plt.figure(figsize = (8,5))
    plt.plot(xSim, ySim, 'ro', alpha = 0.5, label = "Sensibilidad de funciones simuladas")
    plt.plot(xAl, yAl, 'bo', alpha = 0.5, label = "Sensibilidad de funciones aleatorias")
    title = "Comparación de puntuación y sensibilidad para funciones simuladas y aleatorias (muestreo de 100000 grafos)"
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel("Sensibilidad")
    plt.show()
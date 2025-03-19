from syntactic import *
from genetic import *
from experimentos import *
from metrics import *

def prueba_genetico():
    funciones = leer_fnds_por_puntuacion('experimentos/experimentos_n8/Simulacion_300_iteraciones/funciones_fnd.json')
    ini, fin = 150, 200
    validas = []
    for punt in range(ini, min(fin, len(funciones))):
        for f in funciones[punt]:
            validas += [[f, punt]]
    random.shuffle(validas)
    pob_inicial = []
    for i in range(0, len(validas) - 1, 2):
        [f1, punt1] = validas[i]
        [f2, punt2] = validas[i + 1]
        incremento = m(combAND_with_not(f1, f2)) - max(punt1, punt2)
        pob_inicial.append([[f1, punt1], [f2, punt2], incremento])
    genetico(ini, fin, pob_inicial)

def prueba_perdidas():
    # funciones = leer_fnds_por_puntuacion("experimentos/experimentos_n8/almacen_fnds.json")
    funciones = [[] for _ in range(151)]
    for _ in range(1, 3000):
        m_f = random.randint(1, 150)
        m_g = random.randint(1, 150)
        f = get_random_fnd_puntuacion(m_f)
        g = get_random_fnd_puntuacion(m_g)
        h = combAND_with_not(f, g)
        m_h = m(h)
        while len(funciones) <= m_h:
            funciones.append([])
        funciones[m_h].append(h)
    grafica_perdidas(funciones)

def prueba_grafica_sesgo():
    # funciones = leer_fnds_por_puntuacion("experimentos/experimentos_n8/almacen_fnds.json")
    funciones = [[] for _ in range(151)]
    for _ in range(1, 3000):
        m_f = random.randint(1, 150)
        m_g = random.randint(1, 150)
        f = get_random_fnd_puntuacion(m_f)
        g = get_random_fnd_puntuacion(m_g)
        h = combAND_with_not(f, g)
        m_h = m(h)
        while len(funciones) <= m_h:
            funciones.append([])
        funciones[m_h].append(h)
    grafica_sesgo(funciones)

def prueba_diferencia_sesgo_simuladas_aleatorias():
    parejas = leer_json_parejas("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json")
    simuladas = []
    for [[f, m_f], [g, m_g], punt] in parejas:
        simuladas.append([f, m_f])
        simuladas.append([g, m_g])
    compara_sesgo_aleatorias_con_simuladas(100, 150, simuladas)

def prueba_sensibilidad():
    fnd = [[1, 2, 3], [4, 5]]
    print(metrica_sensibilidad(fnd))
from syntactic import *
from itertools import product
from debug import debug
from genetic import *

def generar_listas_binarias(n):
    return [list(p) for p in product([0, 1], repeat=n)]


def restringe_fnd(fnd, asignaciones):
    '''
    Función que, dada una FND y un conjunto de valores para algunos de los inputs,
    calcula la FND resultante de fijar dichos valores
    Argumentos:
        fnd: FND de la función (lista de listas)
        asignaciones: diccionario que a cada literal a fijar en la FND le asigna 0 o 1
    '''
    new_fnd = []
    for clausula in fnd:
        new_clausula = []
        for literal in clausula:
            signo = 1 if literal > 0 else -1
            if abs(literal) in asignaciones:    # Hay que fijar el valor del literal
                if (signo == 1 and asignaciones[abs(literal)] == 1) or (signo == -1 and asignaciones[abs(literal)] == 0):
                    # En este caso simplemente se quita el literal de la cláusula
                    continue
                else:
                    # En este caso la cláusula entera da False
                    new_clausula = [False]
                    break
            else:   # No hay que fijar el valor del literal
                new_clausula.append(literal)
        
        # Si la cláusula es [False] no la añadimos
        if new_clausula == [False]:
            continue

        # Si la cláusula es vacía es que se ha reducido a True, por lo que la FND entera también
        if len(new_clausula) == 0:
            return [True]
        
        # Si no estamos en ninguno de los dos casos, simplemente añadimos la nueva cláusula
        new_fnd.append(new_clausula)

    # En este punto, si la fnd está vacía es que no se ha añadido ninguna cláusula
    # Esto implica que todas eran falsas, así que la FND también
    if len(new_fnd) == 0:
        return [[False]]
    
    # En caso contrario, devolvemos la forma reducida de la nueva FND
    return reduce(new_fnd)

def lista_a_tupla(lista):
    return tuple(lista_a_tupla(e) if isinstance(e, list) else e for e in lista)

def sesgo_de_cliques(fnd):
    '''
    Dada una función, calcula el mínimo enredo que tiene bajo el conocimiento de los estados de los cliqués
    TODO Explicar mejor
    '''
    min_restricciones = 2**A_CLIQUE
    for s in subsets:
        aristas = []
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                v1, v2 = s[i], s[j]
                aristas.append(idx[v1][v2])
        
        # Probamos todos los estados posibles de las A_CLIQUE aristas
        valores = list(product([0, 1], repeat=A_CLIQUE))
        restricciones = set()
        for v in valores:
            asignaciones = {}
            for i in range(A_CLIQUE):
                asignaciones[aristas[i]] = v[i]
            restricciones.add(lista_a_tupla(restringe_fnd(fnd, asignaciones)))
        # debug(f"s -> {s}")
        # debug(f"nº restricciones -> {len(restricciones)}")
        min_restricciones = min(min_restricciones, len(restricciones))
    return min_restricciones

def pruebas_metricas():
    # fnd = [[idx[1][2], -idx[1][3], idx[1][4]], [idx[1][2], -idx[1][5]]]
    # asignaciones = {idx[1][2]: 1, idx[1][3]: 0, idx[1][4]: 1}
    # print(restringe_fnd(fnd, asignaciones))
    # print(sesgo_de_cliques(clique))
    fnd = [[idx[1][2], idx[1][3], idx[1][4], idx[2][3], idx[2][4], idx[3][4]]]
    print(sesgo_de_cliques(fnd))

def grafica_sesgo(funciones):
    '''
    Funciones es una lista donde el índice es la puntuación
    y cada elemento es una lista de funciones con dicha puntuación
    '''
    por_punt = [[] for _ in range(len(funciones))]
    xs, ys = [], []
    for punt, lista in enumerate(funciones):
        debug(punt)
        for f in lista:
            xs.append(punt)
            ys.append(sesgo_de_cliques(f))
    
    fig = plt.figure(figsize = (8,5))
    plt.plot(xs, ys, 'ro', alpha = 0.5)
    # plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
    title = "Relación entre puntuación y sesgo"
    plt.title(title)
    # plt.legend()
    plt.xlabel("Puntuación")
    plt.ylabel("Sesgo")
    # plt.savefig(os.path.join(ruta, "graficaAND.png"))
    plt.show()

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
    for G in range(1 << A):
        if (G + 1) % 100000 == 0:
            debug(G + 1)
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
        

def compara_aleatorias_con_simuladas(ini, fin):
    N_FUNCIONES = 300
    todas_simuladas = leer_fnds_por_puntuacion("experimentos/experimentos_n8/almacen_fnds.json")
    simuladas, aleatorias = [], []
    xSim, ySim, xAl, yAl = [], [], [], []
    for _ in range(N_FUNCIONES):
        # Tomamos una función simulada
        punt = random.randint(ini, fin)
        while len(todas_simuladas[punt]) == 0:
            punt = random.randint(ini, fin)
        simuladas.append(random.choice(todas_simuladas[punt]))
        xSim.append(punt)

        # Generamos una función aleatoria con la misma puntuación que la simulada
        aleatorias.append(get_random_fnd_puntuacion(punt))
        xAl.append(punt)
    for f in simuladas:
        ySim.append(sesgo_de_cliques(f))
    for f in aleatorias:
        yAl.append(sesgo_de_cliques(f))

    # Graficamos los resultados
    fig = plt.figure(figsize = (8,5))
    plt.plot(xSim, ySim, 'ro', alpha = 0.5, label = "Sesgo de funciones simuladas")
    plt.plot(xAl, yAl, 'bo', alpha = 0.5, label = "Sesgo de funciones aleatorias")
    title = "Comparación de puntuación y sesgo para funciones simuladas y aleatorias"
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel("Sesgo")
    plt.show()
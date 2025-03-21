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
    1ª Versión
        Dada una función, calcula el mínimo enredo que tiene bajo el conocimiento de los estados de los cliqués
    2ª Versión
        Dada una función, calcula la varianza de enredo que tiene bajo el conocimiento de los estados de los cliqués
    3ª Versión
        Calcula la diferencia entre el sesgo mínimo y máximo
    4ª Versión
        La media
    TODO Explicar mejor
    '''
    sesgos = []
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
        sesgos.append(len(restricciones))
    media = sum(sesgos) / len(sesgos)
    varianza = sum((s - media) ** 2 for s in sesgos) / len(sesgos)
    return [max(sesgos) - min(sesgos), min(sesgos), media, varianza]

def grafica_sesgo(funciones):
    '''
    Funciones es una lista donde el índice es la puntuación
    y cada elemento es una lista de funciones con dicha puntuación
    '''
    por_punt = [[] for _ in range(len(funciones))]
    xs, max_mins, mins, medias, varianzas = [], [], [], [], []
    for punt, lista in enumerate(funciones):
        debug(punt)
        for f in lista:
            xs.append(punt)
            [max_min, min, media, varianza] = sesgo_de_cliques(f)
            max_mins.append(max_min)
            mins.append(min)
            medias.append(media)
            varianzas.append(varianza)
    

    fig = plt.figure(figsize = (8,5))
    plt.plot(xs, max_mins, 'ro', alpha = 0.5)
    # plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
    title = "Relación entre puntuación y sesgo máximo - sesgo mínimo"
    plt.title(title)
    # plt.legend()
    plt.xlabel("Puntuación")
    plt.ylabel("Sesgo máximo - sesgo mínimo")
    # plt.savefig(os.path.join(ruta, "graficaAND.png"))
    plt.show()

    fig = plt.figure(figsize = (8,5))
    plt.plot(xs, mins, 'ro', alpha = 0.5)
    # plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
    title = "Relación entre puntuación y sesgo mínimo"
    plt.title(title)
    # plt.legend()
    plt.xlabel("Puntuación")
    plt.ylabel("Sesgo mínimo")
    # plt.savefig(os.path.join(ruta, "graficaAND.png"))
    plt.show()
    
    fig = plt.figure(figsize = (8,5))
    plt.plot(xs, medias, 'ro', alpha = 0.5)
    # plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
    title = "Relación entre puntuación y sesgo medio"
    plt.title(title)
    # plt.legend()
    plt.xlabel("Puntuación")
    plt.ylabel("Sesgo medio")
    # plt.savefig(os.path.join(ruta, "graficaAND.png"))
    plt.show()
    
    fig = plt.figure(figsize = (8,5))
    plt.plot(xs, varianzas, 'ro', alpha = 0.5)
    # plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
    title = "Relación entre puntuación y varianza de sesgo"
    plt.title(title)
    # plt.legend()
    plt.xlabel("Puntuación")
    plt.ylabel("Varianza de sesgo")
    # plt.savefig(os.path.join(ruta, "graficaAND.png"))
    plt.show()

def compara_sesgo_aleatorias_con_simuladas(ini, fin, simuladas):
    N_FUNCIONES = 300
    simuladas = simuladas[:N_FUNCIONES]
    aleatorias = []
    xSim, ySim, xAl, yAl = [], [], [], []
    for i in range(N_FUNCIONES):
        # Añadimos la puntuación de cada simulada
        xSim.append(simuladas[i][1])

        # Generamos una función aleatoria con la misma puntuación que la simulada
        punt = random.randint(ini, fin)
        aleatorias.append(genera_pseudoaleatoria_puntuacion(punt))
        xAl.append(punt)
    for i, [f, punt] in enumerate(simuladas):
        ySim.append(sesgo_de_cliques(f))
        debug(f"{i + 1} sesgos de funciones simuladas calculados")
    for i, f in enumerate(aleatorias):
        yAl.append(sesgo_de_cliques(f))
        debug(f"{i + 1} sesgos de funciones aleatorias calculados")

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
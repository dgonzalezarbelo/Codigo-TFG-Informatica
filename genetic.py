from syntactic import *
import time
import math
import random
from debug import debug
from debug import tam_total

def particion_con_limite(suma, n, limite):
    '''Genera una lista de n números positivos menores o iguales a limite que suman exactamente suma'''
    if n <= 0 or suma <= 0 or limite <= 0:
        raise ValueError("suma, n y limite deben ser positivos")
    if n * limite < suma:
        raise ValueError("No es posible generar la lista: limite es demasiado pequeño")
    
    parts = []
    remaining_sum = suma
    remaining_parts = n

    # Si quiero que los n números sean positivos y sumen suma, cada uno debe ser >= ceil(suma // n)
    # Al mismo tiempo, no pueden ser mayores que limite ni mayores que suma - n (pues cada número debe ser al menos 1)
    while remaining_parts > 0:
        min_val = (remaining_sum + remaining_parts - 1) // remaining_parts
        max_val = min(limite, remaining_sum - (remaining_parts - 1))  # Máximo valor posible sin impedir completar M
        num = random.randint(min_val, max_val)  # Generamos un número aleatorio válido
        parts.append(num)
        remaining_sum -= num 
        remaining_parts -= 1

    return parts

def get_random_fnd_puntuacion(puntuacion):
    '''
    Para generar una FND con la puntuación deseada, vamos a hacer lo siguiente:
    De cada cláusula de la FND de cliqué vamos a tomar un subconjunto de literales.
    Si ningún literal estuviera negado, se tendriá que cumplir que los tamaños de los subconjuntos sumen la puntuación.
    Para permitir que haya negaciones, podemos tomar algunos literales de más y negarlos (no suman puntuación).
    '''
    if puntuacion > CLAUSULAS * A_CLIQUE:
        raise ValueError(f"La puntuación no puede ser mayor que la de cliqué ({CLAUSULAS * A_CLIQUE})")

    PROB_NEG = 0.1

    # Por este método, por las reducciones, es posible perder puntuación
    # No obstante, es improbable, así que se puede repetir el proceso hasta que funcione
    # TODO De momento lo dejo así, y si se me ocurre algo mejor en el futuro lo cambio
    fallo = True

    # Primero elegimos la cantidad de cláusulas que queremos que tenga la función
    # No queremos que tenga ni más que la FND de cliqué ni más que la puntuación
    # (pues habría cláusulas inútiles)
    max_clausulas = min(CLAUSULAS, puntuacion)    

    # Teniendo en cuenta que la puntuación máxima de una cláusula es A_CLIQUE,
    # necesitamos, al menos, ceil(puntuacion // A_CLIQUE) cláusulas
    min_clausulas = (puntuacion + A_CLIQUE - 1) // A_CLIQUE
    # debug(f"min -> {min_clausulas}")
    # debug(f"max -> {max_clausulas}")
    while fallo:
        fallo = False
        num_clausulas = random.randint(min_clausulas, max_clausulas)
        # Ahora queremos determinar la puntuación que va a aportar cada cláusula
        puntuaciones = particion_con_limite(puntuacion, num_clausulas, A_CLIQUE)
        
        # Como el orden de las cláusulas no importa, las añadimos por tamaño,
        # de forma que una nueva cláusula no pueda absorber a una anterior
        puntuaciones.sort()

        # Ahora, vamos a tomar num_clausulas aleatorias de la FND de cliqué, y de cada una vamos a tomar,
        # al menos, tantos literales como puntuación le corresponde a la cláusula.
        # Con cierta probabilidad tomaremos algún literal más y lo negaremos
        ind_clausulas = random.sample(range(0, CLAUSULAS), num_clausulas)

        fnd = []

        for i in range(num_clausulas):
            while len(fnd) < i + 1:
                literales = clique[ind_clausulas[i]].copy()
                cur = random.sample(literales, puntuaciones[i])
                for x in cur:
                    literales.remove(x)
                
                while random.uniform(0, 1) < PROB_NEG and len(cur) < K:
                    literal_negar = random.choice(literales)
                    literales.remove(literal_negar)
                    cur.append(-literal_negar)

                cur.sort(key=abs)
                fnd.append(cur)

        fnd = reduce(fnd)
        if m(fnd) != puntuacion:
            fallo = True
    
    fnd.sort(key=lambda x: (len(x), sorted(x, key=abs)))  # TODO Lo de sorted no hace falta, es para depurar más fácilmente
    assert(m(fnd) == puntuacion)
    return fnd

def poblacion_inicial(ini, fin, n, puerta):
    '''
    Función que devuelve una población inicial de tamaño n mezclando FNDs con puntuaciones
    en el rango [ini, fin] combinadas con la puerta recibida como argumento
    '''
    ret = []
    for _ in range(2 * n):
        punt1 = random.randint(ini, fin)
        punt2 = random.randint(ini, fin)
        f1 = get_random_fnd_puntuacion(punt1)
        f2 = get_random_fnd_puntuacion(punt2)
        if puerta == 'OR':
            incremento = m(combOR(f1, f2)) - max(punt1, punt2)
        elif puerta == 'AND':
            incremento = m(combAND_with_not(f1, f2)) - max(punt1, punt2)
        else:
            raise ValueError("La puerta debe ser OR o AND")
        ret.append([[f1, punt1], [f2, punt2], incremento])
    return ret

def genetico(ini, fin):
    '''
    Algoritmo genético para buscar pares de funciones con puntuaciones en un rango dado
    que generen el máximo incremento de la métrica
    
    Parámetros: TODO Dejar esto más limpio, por ahora solo lo pongo para ubicarme yo con el tema
        Rango: par de enteros indicando el rango de puntuaciones de las funciones
        Fitness: función que evalúa "cómo de buena" es una pareja de funciones (a priori la métrica sintáctica)
        Población inicial
        Método de selección:
            Selección por torneo:
                Tamaño del torneo
                Probabilidad de tomar al mejor
        Método de cruce:
            Número de cruces AND
            Número de cruces OR
            Elección de si es destructivo o no
        Método de mutación:
            Probabilidad de mutación
            Mutación de puertas NOT:
                Número de literales a negar
            Mutación de intercambio de cláusulas:
                Elección de qué cláusulas intercambiar
 
    Genotipo: Listas de varios elementos
        -> [FND1, puntuación(FND1)]
        -> [FND2, puntuación(FND2)]
        -> Incremento de puntuación
            -> El incremento de puntuación se calcula respecto a la puntuación máxima de FND1 y FND2
    '''

    PUERTAS = ['OR', 'AND']
    PUERTAS_HABILITADAS = ['OR', 'AND'] # Por si no queremos usar todas en la simulación
    COMBINACIONES = {'OR': combOR, 'AND': combAND_with_not}
    ITERACIONES = {'OR': 50, 'AND': 50} # Iteraciones de cada puerta
    POPULATION_SIZE = 300
    NUM_GENERATIONS = 300
    T = 4   # Tamaño de los torneos para la selección
    CLAVE = lambda gen: -gen[2]  # Tomamos máximos según el incremento de la métrica (negativo para tomar el máximo)

    xs, ys = {}, {}   # Para graficar los resultados
    for p in PUERTAS_HABILITADAS:
        xs[p], ys[p] = [], []

    # Lo primero que tenemos que conseguir es una población inicial para arrancar el algoritmo
    poblaciones = {}
    for p in PUERTAS_HABILITADAS:
        poblaciones[p] = poblacion_inicial(ini, fin, POPULATION_SIZE, p)
    tiempo = 0
    print("Poblaciones iniciales generadas")
    print("Iniciando algoritmo genético")
    for generation in range(1, NUM_GENERATIONS + 1):
        start_time = time.perf_counter()
        for p in PUERTAS_HABILITADAS:
            for it in range(ITERACIONES[p]):
                # Selección por torneo de T individuos
                torneo1 = random.sample(poblaciones[p], T)
                torneo2 = random.sample(poblaciones[p], T)
                gen1 = max(torneo1, key=CLAVE)
                gen2 = max(torneo2, key=CLAVE)
                for i in range(2):
                    for j in range(2):
                        f, g = gen1[i][0], gen2[j][0]
                        m_f, m_g = gen1[i][1], gen2[j][1]
                        comb = COMBINACIONES[p](f, g)   # Juntamos las dos funciones a través de la puerta
                        incremento = m(comb) - max(m_f, m_g)
                        gen = [[f, m_f], [g, m_g], incremento]
                        xs[p].append(m_f); xs[p].append(m_g)
                        ys[p].append(incremento); ys[p].append(incremento)
                        # TODO Como estoy viendo parejas, igual tiene más sentido una representación 3D
                        # TODO Debería limitar la longitud de las FNDs
                        # Mutación TODO


                        poblaciones[p].append(gen)
            poblaciones[p].sort(key=CLAVE)
            poblaciones[p] = poblaciones[p][:POPULATION_SIZE]   # Nos quedamos con los mejores

        # Imprimir estadísticas
        end_time = time.perf_counter()
        tiempo += end_time - start_time
        print(f"Generación {generation}: Tiempo = {end_time - start_time:.2f} s")
        for p in PUERTAS_HABILITADAS:
            print(f"    Mejor incremento con puerta {p}: {-CLAVE(max(poblaciones[p], key=CLAVE))}")
        if generation == 10:
            estimacion = (NUM_GENERATIONS - 10) * tiempo / 10
            horas, minutos = estimacion / 3600, estimacion / 60
            if horas >= 1:
                print(f"Tiempo restante estimado: {horas:.3f} horas")
            else:
                print(f"Tiempo restante estimado: {minutos:.3f} minutos")
        print()
        # TODO Falta guardar datos externamente

genetico(1, 10)
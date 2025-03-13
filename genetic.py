from syntactic import *
import time
import math
import random
from debug import debug

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
    debug(f"min -> {min_clausulas}")
    debug(f"max -> {max_clausulas}")
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

def genetico():
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
    '''
    
    OR_ITER = 15
    AND_ITER = 15
    POPULATION_SIZE = 300

    # Lo primero que tenemos que conseguir es una población inicial para arrancar el algoritmo
    population = [generate_individual() for _ in range(POPULATION_SIZE)]
    
    for generation in range(NUM_GENERATIONS):
        start_time = time.perf_counter()

        # Evaluación
        population.sort(key=fitness, reverse=True)
        best_fitness = fitness(population[0])

        # Selección
        new_population = population[:POPULATION_SIZE // 2]  # Elitismo (mejores sobreviven)
        while len(new_population) < POPULATION_SIZE:
            # Cruce
            p1, p2 = select_parents(population)
            child1, child2 = crossover(p1, p2)

            # Mutación
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])

        population = new_population[:POPULATION_SIZE]

        # Imprimir estadísticas
        end_time = time.perf_counter()
        print(f"Generación {generation+1}: Mejor aptitud = {best_fitness}, Tiempo = {end_time - start_time:.6f} s")

        # Criterio de parada opcional
        if best_fitness == GENOME_LENGTH:
            print("Óptimo encontrado. Deteniendo...")
            break

    return population[0]
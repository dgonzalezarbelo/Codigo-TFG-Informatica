from syntactic import *
from itertools import product
from genetic import *
from experimentos import *

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

def grados_libertad(f):
    '''Función para calcular la métrica de grados de libertad de f'''
    grados = []
    for s in subsets: # Bucle que itera sobre todos los cliques
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
            restricciones.add(lista_a_tupla(restringe_fnd(f, asignaciones)))
        grados.append(len(restricciones))
    media = sum(grados) / len(grados)
    return media

def grafica_grados_libertad_mejores(n_funciones):
    '''Genera una gráfica comparando los grados de libertad de funciones las mejores funciones
    simuladas, pseudoaleatorias y aleatorias resultantes del algoritmo genético de parejas'''
    simuladas = leer_top_funciones("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    pseudoaleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json", n_funciones)
    aleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_aleatorias_100-150_AND.json", n_funciones)
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_histograma(dic, grados_libertad, "Grados de libertad")

def compara_grados_libertad(simuladas, pseudoaleatorias, aleatorias):
    '''Genera una gráfica que compara los grados de libertad de funciones simuladas, pseudoaleatorias y aleatorias'''
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, grados_libertad, "Grados de libertad")

def histograma_grados_libertad():
    '''Genera un histograma con los grados de libertad de funciones simuladas, pseudoaleatorias y aleatorias'''
    n_funciones = 20
    ini, fin = 1, 250
    simuladas = poblacion_en_rango(ini, fin, n_funciones)
    pseudoaleatorias = [genera_pseudoaleatoria_puntuacion(random.randint(ini, fin)) for _ in range(n_funciones)]
    aleatorias = poblacion_en_rango(ini, fin, n_funciones, "experimentos/experimentos_n8/almacen_aleatorias.json")
    conjuntos_de_funciones = {}
    conjuntos_de_funciones["simuladas"] = simuladas
    conjuntos_de_funciones["pseudoaleatorias"] = pseudoaleatorias
    conjuntos_de_funciones["aleatorias"] = aleatorias
    grafica_histograma(conjuntos_de_funciones, grados_libertad, "Grados de libertad", 64)

def variacion_grados_libertad():
    '''Genera una gráfica de la variación de los grados de libertad de funciones simuladas tras la aplicación de puertas AND y OR'''
    grafica_variacion_medida(grados_libertad, combAND_with_not, combOR, "Grados de libertad", "$\\mu_{\\delta}$")
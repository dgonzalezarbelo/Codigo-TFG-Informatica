from syntactic import *
from itertools import product
from debug import debug
from genetic import *

def clausulas_perfectas(fnd):
    perfectas = 0
    for clausula in fnd:
        vertices = set()
        for literal in clausula:
            if literal < 0:
                continue
            (a, b) = inv_idx[literal]
            vertices.add(a)
            vertices.add(b)
        if len(vertices) <= K:
            perfectas += 1
    return perfectas / len(fnd)

def grafica_clausulas_perfectas_mejores(n_funciones):
    simuladas = leer_top_funciones("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    pseudoaleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json", n_funciones)
    aleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_aleatorias_100-150_AND.json", n_funciones)
    dic = {}
    dic["simuladas"] = simuladas
    dic["pseudoaleatorias"] = pseudoaleatorias
    dic["aleatorias"] = aleatorias
    grafica_comparaciones(dic, m, clausulas_perfectas, "Cláusulas perfectas")
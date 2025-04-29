# Código basado en el trabajo de Jaime Romo González (GitHub: JaimeRG01)
# Repositorio original: https://github.com/JaimeRG01/TFG

from hungarian import matching
import random 
import math
from random import sample
import matplotlib.pyplot as plt
from collections import deque
from collections import defaultdict
import time
from pyeda.inter import *
from experimentos import guardar_simulacion

N = 8 # Vértices
K = N // 2 # Tamaño del clique
A = N * (N-1) // 2 # Aristas en el grafo
A_CLIQUE = K * (K-1) // 2 # Aristas en un cliqué de tamaño K
CLAUSULAS = math.comb(N, K)
M_CLIQUE = CLAUSULAS * A_CLIQUE # Puntuación de la función Cliqué
subsets = []
idx = [[0 for i in range(N+1)] for j in range(N+1)]
inv_idx = [(0, 0) for _ in range(A+1)]

# Genera los subconjuntnso de tamaño sz a partir de la variable ini
def generate_subset(n, ini, sz, acc) : 
    if sz == 0: 
        subsets.append(acc.copy())
    elif ini <= n: 
        # Generar los subconjuntos que incluyen a ini
        acc.append(ini)
        generate_subset(n, ini+1, sz-1, acc)

        # Generar los subconjuntos que no incluyen a ini
        acc.pop()
        generate_subset(n, ini+1, sz, acc)

# Genera la función booleana que computa el clique
def generate_fun_clique(subsets) :
    res = []
    cnt = 1
    for i in range(1,N+1) :
        for j in range(i+1, N+1) :
            idx[i][j] = cnt
            inv_idx[cnt] = (i, j)
            cnt += 1
    for s in subsets : 
        f = []
        for i in range(K) :
            for j in range(i+1, K) :
                f.append(idx[s[i]][s[j]])
        res.append(f)
    return res


generate_subset(N, 1, K, [])
# print(subsets)
clique = generate_fun_clique(subsets)
# print(clique)


# Calcula cuántos literales de f están en g
# TODO No sé si es relevante pero igual esto se puede hcaer más rápido si los inputs vienen ordenados
def common_literals(f, g) :
    res = 0
    for i in f :
        if i in g: res += 1
    return res

# Calcula la métrica. Usa el algoritmo húngaro para asignar el máximo posible
def m(f, g=clique, devuelve_asignacion=False) :
    n = len(f)
    m = len(g)
    # Costes negativos para maximizar
    # min (f(x)) = -max(-f(x))
    if n <= m : 
        mat = [[-common_literals(f[i], g[j]) for j in range(m)] for i in range(n)]
    else : 
        mat = [[-common_literals(f[i], g[j]) for i in range(n)] for j in range(m)]
    #for i in mat : print(i)
    #print(n, m)
    if not devuelve_asignacion:
        res = -matching(mat, devuelve_asignacion)
        return res
    else:
        res, asignacion = matching(mat, devuelve_asignacion)
        return [-res, asignacion]

# Comprueba si f es prefijo de g
def is_prefix(f, g) :
    if len(f) > len(g) : return False
    else : return f == g[:len(f)]

# Comprueba si los literales de f son un subconjunto de los de g (f absorbe a g)
def absorbs(f, g):
    # Precondición: los literales de f y g vienen ordenados
    if len(f) > len(g):
        return False
    i = j = 0
    while i < len(f) and j < len(g):
        if f[i] == g[j]:
            i += 1
        elif f[i] > g[j]:
            j += 1
        else:
            return False
    return i == len(f)

# Reduce f. CUIDADO CON LOS NOT
def reduce(f, k = (K * (K-1) // 2), use_not = True) :
    l = len(f)
    for i in range(l) :
        f[i] = list(set(f[i]))
        f[i].sort()
    
    # Ordenamos las cláusulas para luego hacer fácilmente la absorción de cláusulas inútiles
    f.sort(key=len)

    # Quitar elementos que no aportan informacion
    res = []
    # Vamos a marcar las cláusulas inútiles (por absorción o por ser demasiado largas en caso de no usar puertas NOT)
    mark = [False] * l

    '''ESTE FOR SOLO CUANDO NO HAY NOTS'''
    if not use_not:
        for i in range(l) :
            if len(f[i]) > k : mark[i] = True

    for i in range(l) :
        if mark[i] : continue
        # Si la cláusula i es prefijo de la j, al combinarlas con OR se absorbe la j, así que no nos sirve
        for j in range(i+1, l) :
            # if is_prefix(f[i], f[j]) : mark[j] = True
            if absorbs(f[i], f[j]) : mark[j] = True
        res.append(f[i])
    return res  

def fnd_to_pyeda(fnd):
    # Obtener el conjunto de variables necesarias (sin signo)
    vars_needed = {abs(lit) for clause in fnd for lit in clause}
    
    # Crear las variables con exprvar
    variables = {i: exprvar(f"x{i}") for i in vars_needed}

    # Convertimos cada cláusula
    pyeda_clauses = []
    for clause in fnd:
        literals = []
        for lit in clause:
            var = variables[abs(lit)]
            literals.append(~var if lit < 0 else var)
        pyeda_clauses.append(And(*literals))  # Conjunción dentro de la cláusula

    # Disyunción total de cláusulas
    return Or(*pyeda_clauses)

def pyeda_to_fnd(expr):
    dnf_expr = expr.to_dnf()
    clauses = []

    for cube in dnf_expr.cover:
        clause = []
        for lit in cube:
            var_name = str(lit).lstrip('~')  # 'x3' o '~x3' → 'x3'
            var_index = int(var_name[1:])    # 'x3' → 3
            if str(lit).startswith('~'):
                clause.append(-var_index)
            else:
                clause.append(var_index)
        clause.sort()
        clauses.append(clause)

    return clauses

def reduce_pyeda(f):
    fp = fnd_to_pyeda(f)
    try:
        fpr = espresso_exprs(fp.to_dnf())[0]
    except ValueError:  # Sale error cuando la función es idénticamente cierta o nula FIXME (creo)
        return []
    try:
        ret = pyeda_to_fnd(fpr)
        return ret
    except ValueError:
        return []

# Calcula f and g
# Junta todos los pares de f y g 
def combAND(f, g, k = (K * (K-1) // 2)) :
    aux = []
    n1 = len(f); n2 = len(g)
    for i in range(n1) :
        for j in range(n2) :
            aux.append(f[i] + g[j])

    return reduce(aux)

# Función aleatoria
def get_rand_fun() :
    l = random.randint(1, len(clique))
    aux = sample(clique, l)
    res = []
    for i in aux : 
        l = random.randint(1, len(i))
        res.append(sample(i, l))
    return res

# Función aleatoria de baja puntuación
def get_rand_low_fun(punt) : 
    aux = sample(clique, punt)
    res = []
    for i in aux : 
        r = min(len(i), punt)
        res.append(sample(i, r))
        punt -= r
        if punt == 0: break
    return res

# Función aleatoria con NOT
def get_rand_fun_with_not() :
    l = random.randint(1, len(clique))
    aux = sample(clique, l)
    res = []
    for i in aux : 
        l = random.randint(1, len(i))
        res.append(sample(i, l))

    for i in range(len(res)) :
        l = random.randint(0, len(res[i]))
        neg = sample(range(0, len(res[i])), l)
        for j in neg : res[i][j] *= -1
    return res

# Genera una función realmente aleatoria
def genera_funcion_aleatoria():
    '''Genera una función totalmente aleatoria'''
    n_clausulas = random.randint(30, CLAUSULAS)
    fnd = []
    inputs = [i for i in range(1, A + 1)]
    for i in range(n_clausulas):
        l_clausula = random.randint(1, A)
        literales = random.sample(inputs, l_clausula)
        negaciones = random.randint(0, l_clausula)
        literales_negar = random.sample(range(l_clausula), negaciones)
        for i in literales_negar:
            literales[i] *= -1
        fnd.append(literales)
    return reduce_pyeda(fnd)

# AND con NOT
def combAND_with_not(f, g) :
    aux = []
    n1 = len(f); n2 = len(g)
    for i in range(n1) :
        for j in range(n2) :
            aux.append(f[i] + g[j])

    # Eliminar aquellas que se cancelan por los not
    ret = []
    for i in aux :
        ok = True
        for j in i :
            if (-j) in i : 
                ok = False
                break
        if ok : ret.append(i)
    # return reduce(ret)
    return reduce_pyeda(ret)

# Compara funciones aleatorias
def compare_rand_fun() :
    iter = 100
    fig = plt.figure(figsize = (8,5))
    x = []
    y = []
    for _ in range(iter) :
        print("Iteración número:", _+1)
        f = reduce(get_rand_fun())
        g = reduce(get_rand_fun())
        h = combAND(f, g)
        m1 = m(f)
        m2 = m(g)
        m3 = m(h)
        #print(m1, m2, " -> ", m3)
        x.append(m1); y.append(m3)
        x.append(m2); y.append(m3)
   
    plt.plot(x, y, 'ro', label = '$\mu_x(f \wedge g)$')
    plt.xlabel('$\mu_x$ antes de AND')
    plt.ylabel('$\mu_x$ despues de AND')
    title = "Comparación de " + str(iter) + " pares de funciones aleatorias"
    plt.title(title)
    plt.legend()
    plt.show()

# Compara funciones aleatorias con NOT
def compare_rand_fun_with_not() :
    iter = 1000
    fig = plt.figure(figsize = (8,5))
    x = []
    y = []
    maxi_rand = -1
    maxi_and = -1
    for _ in range(iter) :
        print("Iteración número:", _+1)
        f = reduce(genera_funcion_aleatoria())
        g = reduce(genera_funcion_aleatoria())
        h = combAND_with_not(f, g)
        m1 = m(f)
        m2 = m(g)
        m3 = m(h)
        maxi_rand = max(m1, m2, maxi_rand)
        maxi_and = max(maxi_and, m3)
        #print(m1, m2, " -> ", m3)
        x.append(m1); y.append(m3)
        x.append(m2); y.append(m3)
    
    plt.plot(x, y, 'ro', label = '$\mu_x(f \wedge g)$')
    plt.xlabel('$\mu_x$ antes de AND')
    plt.ylabel('$\mu_x$ despues de AND')
    title = "Comparación de " + str(iter) + " pares de funciones aleatorias con NOT"
    plt.title(title)
    plt.legend()
    plt.show()

# Genera una función con m cláusulas donde cada cláusula tiene 
# n variables y en total usa el mínimo número de variables posibles
def endogamic_fun(n, m, reverse = False) :
    S = [i for i in range(1, A+1)]
    if reverse : S.reverse()
    #random.shuffle(S)
    res = []
    q = deque()
    ini = [S[i] for i in range(n)]
    ini.sort()
    vis = set()
    vis.add(tuple(ini))
    res.append(ini)
    q.append((ini, n))
    cnt = 1
    while cnt < m and len(q) > 0 : 
        (cur, id) = q.popleft()
        i = 0
        if id >= len(S) : break
        while i < len(cur) and cnt < m :
            new = cur.copy()
            new[i] = S[id]
            new.sort()
            if not tuple(new) in vis :
                vis.add(tuple(new))
                res.append(new.copy())
                q.append((new.copy(), id+1))
                cnt += 1
            i += 1
    res.sort()
    return res

# OR de dos funciones
def combOR(f, g) :
    res = f + g
    # return reduce(res)
    return reduce_pyeda(res)

# Simula el circuito
def simulate_circuit() :
    # Variables
    S = [([[i]],1) for i in range(1, A+1)]
    
    or_iter = 10
    and_iter = 10
    max_size = len(clique)
    limit = 300
    iter = 100
    xOR = []; xAND = []
    yOR = []; yAND = []
    for _ in range(iter) :
        for i in range(or_iter) :
            (f, aux) = random.choice(S)
            (g, aux) = random.choice(S)
            h = combOR(f, g)
            if len(h) <= max_size and h != []: 
                m1 = m(f); m2 = m(g); m3 = m(h)
                if m3 == 0 : print(f, g)
                xOR.append(m1); xOR.append(m2)
                yOR.append(m3); yOR.append(m3)
                S.append((h, m3))
        for i in range(and_iter) :
            (f, aux) = random.choice(S)
            (g, aux) = random.choice(S)
            h = combAND(f, g)
            if len(h) <= max_size and h != []: 
                m1 = m(f); m2 = m(g); m3 = m(h)
                xAND.append(m1); xAND.append(m2)
                yAND.append(m3); yAND.append(m3)
                S.append((h, m3))
        
        print("Iteración: ", _+1)
        S.sort(key = lambda elem : elem[1], reverse = True)
        while len(S) > limit : S.pop()
    
    
    fig = plt.figure(figsize = (8,5))
    #plt.xlim([0,420])
    plt.plot(xAND, yAND, 'ro')
    plt.plot(xOR, yOR, 'bo')
    plt.show()

# Simula el circuito con NOT
def simulate_circuit_with_not() :
    # Variables (FND, métrica, puertas)
    S1 = [([[i]], 1, 0) for i in range(1, A + 1)]
    S2 = [([[-i]], 0, 0) for i in range(1, A + 1)]
    S = S1 + S2
    T = 20
    CLAVE = lambda f: f[1]  # Métrica en negativo para tomar el máximo
    CLAVE_NEG = lambda f: -CLAVE(f)
    or_iter = 15
    and_iter = 15
    max_size = 150
    limit = 300
    # iter = 1000
    # iter = 300
    # iter = 50
    iter = 10
    xOR = []; xAND = []
    yOR = []; yAND = []

    # fnds es una lista en la que, para cada valor de la métrica,
    # vamos a guardar las FNDs calculadas y las puertas que han hecho falta para ello
    # El número de puertas puede no ser óptimo, pero nos lo guardamos para analizar datos en otro momento
    fnds = [[] for _ in range(M_CLIQUE + 1)]
    for i in range(1, A + 1):
        fnds[1].append(([[i]], 0))
        fnds[0].append(([[-i]], 0))

    tiempo = 0
    for _ in range(iter) :
        start_time = time.perf_counter()
        for i in range(or_iter) :
            # Selección aleatoria
            (f, m1, p1) = random.choice(S)
            (g, m2, p2) = random.choice(S)

            # # Selección por torneo de T individuos
            # torneo1 = random.sample(S, T)
            # torneo2 = random.sample(S, T)
            # (f, m1, p1) = max(torneo1, key=CLAVE)
            # (g, m2, p2) = max(torneo2, key=CLAVE)

            h = combOR(f, g)
            if len(h) <= max_size and h != []: 
                # m1 = m(f); m2 = m(g)
                m3 = m(h)
                p3 = p1 + p2 + 1    # Puertas empleadas para computar h
                # if m3 == 0 : print(f, g)
                xOR.append(m1); xOR.append(m2)
                yOR.append(m3); yOR.append(m3)
                S.append((h, m3, p3))
                fnds[m3].append((h, p3))
        for i in range(and_iter) :
            (f, m1, p1) = random.choice(S)
            (g, m2, p2) = random.choice(S)

            # # Selección por torneo de T individuos
            # torneo1 = random.sample(S, T)
            # torneo2 = random.sample(S, T)
            # (f, m1, p1) = max(torneo1, key=CLAVE)
            # (g, m2, p2) = max(torneo2, key=CLAVE)
            h = combAND_with_not(f, g)
            if len(h) <= max_size and h != []: 
                # m1 = m(f); m2 = m(g)
                m3 = m(h)
                xAND.append(m1); xAND.append(m2)
                yAND.append(m3); yAND.append(m3)
                S.append((h, m3, p3))
                fnds[m3].append((h, p3))
        
        end_time = time.perf_counter()
        iteration_time = end_time - start_time
        tiempo += iteration_time
        print(f"Iteración: {_+1} (Tiempo de ejecución: {iteration_time:.2f} segundos)")
        
        S.sort(key = CLAVE_NEG)
        while len(S) > limit : S.pop()
        print(f"Máxima puntuación: {CLAVE(max(S, key=CLAVE))}")
    
    guardar_simulacion(None, fnds, iter, xAND, yAND, xOR, yOR)
    
    mostrar_grafica = False
    if mostrar_grafica:
        print("Incremento máximo:", CLAVE(max(S, key=CLAVE)))
        print(f"Tiempo de ejecución: {tiempo}")
        fig = plt.figure(figsize = (8,5))
        #plt.xlim([0,420])
        plt.plot(xAND, yAND, 'ro', alpha = 0.5, label = "Incremento con AND")
        plt.plot(xOR, yOR, 'bo', alpha = 0.5, label = "Incremento con OR")
        title = "Simulación tras " + str(iter) + " iteraciones"
        plt.title(title)
        plt.legend()
        plt.xlabel("$\mu_x(f)$")
        plt.ylabel("$\mu_x(f)$")
        plt.show()
    
# Compara funciones endogámicas de poca puntuación
def compare_low_end_fun() :

    M = len(clique)
    tam = 100
    tope = int(math.sqrt(M))
    end_funs1 = [endogamic_fun(random.randint(1, K//2), random.randint(1, tope)) for _ in range(tam)]
    end_funs2 = [endogamic_fun(random.randint(1, K//2), random.randint(1, tope), True) for _ in range(tam)]
    #for f in end_funs1 : print(f)
    #for f in end_funs2 : print(f)


    x = []
    y = []

    mf1 = [m(f) for f in end_funs1]
    mf2 = [m(f) for f in end_funs2]
    maxpunt = {}
    for i in range(len(end_funs1)):
        maxpunt[mf1[i]] = 0 
        maxpunt[mf2[i]] = 0

    maxi = -1
    for i in range(tam) :
        print("Iteración:", i)
        for j in range(tam) :
            h = combAND(end_funs1[i], end_funs2[j])
            m3 = m(h)
            x.append(mf1[i]); y.append(m3)
            x.append(mf2[j]); y.append(m3)
            maxi = max(maxi, mf1[i], mf2[j])
            maxpunt[mf1[i]] = max(maxpunt[mf1[i]], m3)
            maxpunt[mf2[j]] = max(maxpunt[mf2[j]], m3)

    plt.plot(x, y, 'ro', label = "$\mu_x(f_{s,t})$")
    vals = [(a,b) for a,b in maxpunt.items()]
    vals.sort(key = lambda x : x[0])
    v1 = [i[0] for i in vals]
    v2 = [i[1] for i in vals]
    plt.plot(v1, v2, '-', color = 'orange', label = "Incremento máximo")

    x = []
    y = []
    rand_low_funs = []
    m_rand_low_funs = []
    iter = 50
    print("Maximo:", maxi)
    for j in range(1, maxi+1) :
        for i in range(iter) :    
            f = reduce(get_rand_low_fun(j))
            mf = m(f)
            rand_low_funs.append(f)
            m_rand_low_funs.append(mf)

    for i in range(len(rand_low_funs)) :
        print(i)
        for j in range(i+1, len(rand_low_funs)) :

            h = combAND(rand_low_funs[i], rand_low_funs[j])
            m3 = m(h)
            m1 = m_rand_low_funs[i]
            m2 = m_rand_low_funs[j]
            x.append(m1); y.append(m3)
            x.append(m2); y.append(m3)

    plt.plot(x, y, 'bo', label = "$\mu_x(f)$")
    plt.legend()
    plt.xlabel("$\mu_x$ antes de AND")
    plt.ylabel("$\mu_x$ después de AND")
    plt.title("$f_{s,t}$ vs $f$")
    plt.show()

# Compara funciones endogámicas de más puntuación
def compare_big_end_fun() : 
    
    M = len(clique)
    tam = 10
    tope = M // 2
    end_funs1 = [endogamic_fun(random.randint(1, K//2), random.randint(1, tope)) for _ in range(tam)]
    end_funs2 = [endogamic_fun(random.randint(1, K//2), random.randint(1, tope), True) for _ in range(tam)]
    #for f in end_funs1 : print(f)
    #for f in end_funs2 : print(f)


    x = []
    y = []

    mf1 = [m(f) for f in end_funs1]
    mf2 = [m(f) for f in end_funs2]
    maxpunt = {}
    for i in range(len(end_funs1)):
        maxpunt[mf1[i]] = 0 
        maxpunt[mf2[i]] = 0

    maxi = -1
    for i in range(tam) :
        print("Iteración:", i)
        for j in range(tam) :
            h = combAND(end_funs1[i], end_funs2[j])
            m3 = m(h)
            x.append(mf1[i]); y.append(m3)
            x.append(mf2[j]); y.append(m3)
            maxi = max(maxi, mf1[i], mf2[j])
            maxpunt[mf1[i]] = max(maxpunt[mf1[i]], m3)
            maxpunt[mf2[j]] = max(maxpunt[mf2[j]], m3)

    plt.plot(x, y, 'ro', label = "$\mu_x(f_{s,t})$", zorder = 4)
    vals = [(a,b) for a,b in maxpunt.items()]
    vals.sort(key = lambda x : x[0])
    v1 = [i[0] for i in vals]
    v2 = [i[1] for i in vals]
    plt.plot(v1, v2, '-', color = 'orange', label = "Incremento máximo", zorder = 6)

    x = []
    y = []
    rand_low_funs = []
    m_rand_low_funs = []
    iter = 50
    print("Maximo:", maxi)
    for i in range(iter) :    
        f = reduce(get_rand_low_fun(random.randint(1,maxi)))
        mf = m(f)
        rand_low_funs.append(f)
        m_rand_low_funs.append(mf)

    for i in range(len(rand_low_funs)) :
        print(i)
        for j in range(i+1, len(rand_low_funs)) :

            h = combAND(rand_low_funs[i], rand_low_funs[j])
            m3 = m(h)
            m1 = m_rand_low_funs[i]
            m2 = m_rand_low_funs[j]
            x.append(m1); y.append(m3)
            x.append(m2); y.append(m3)

    plt.plot(x, y, 'bo', label = "$\mu_x(f)$", zorder = 8)
    plt.legend()
    plt.xlabel("$\mu_x$ antes de AND")
    plt.ylabel("$\mu_x$ después de AND")
    plt.title("$f_{s,t}$ vs $f$")
    plt.show()


'''LLAMAR A LO QUE SE NECESITE'''

# simulate_circuit_with_not()
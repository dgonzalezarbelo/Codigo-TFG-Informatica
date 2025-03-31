from syntactic import *
from debug import debug
from genetic import *

def inter_solapamiento(f, g):
    '''Calcula la intersección promedio entre cláusulas de f y g'''
    sum = 0
    n, m = len(f), len(g)
    for i in range(n):
        for j in range(m):
            sum += common_literals(f[i], g[j]) / max(len(f[i]), len(g[j]))
    return sum / (n * m)

def grafica_relacion_puntuacion_inter_solapamiento(ruta):
    '''
    Función que genera una gráfica que relaciona la métrica obtenida por una pareja
    con la inter-solapamiento de la misma
    '''
    data = leer_json_parejas(ruta)
    xs, ys = [], []
    for i, info in enumerate(data):
        if i % 100 == 0:
            debug(i)
        [[f, m_f], [g, m_g], punt] = info
        xs.append(punt)
        ys.append(inter_solapamiento(f, g))

    # Graficamos los resultados
    fig = plt.figure(figsize = (8,5))
    plt.plot(xs, ys, 'ro', alpha = 0.5)
    title = "Comparación de puntuación e inter-solapamiento de parejas de funciones"
    plt.title(title)
    plt.legend()
    plt.xlabel("$\mu_x(f)$")
    plt.ylabel("Inter-solapamiento")
    plt.show()
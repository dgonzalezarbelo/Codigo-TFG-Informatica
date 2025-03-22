from syntactic import *
from genetic import *
from experimentos import *
from pruebas import *
from metricas.inter_solapamiento import *
from metricas.intra_solapamiento import *
from metricas.sensibilidad import *
from metricas.sesgo import *
from metricas.equidad import *
from metricas.perdidas import *

# Función a la que llamar para hacer lo que quiera
def main():
    # obtener_mejores_aleatorias(150, 200)
    
    # obtener_mejores_aleatorias(200, 250)
    
    # obtener_mejores_simuladas(150, 200)
    
    # prueba_diferencia_sesgo_simuladas_aleatorias()
    # filtrar_almacen_por_longitud()
    # fnd = [[idx[1][2], idx[1][3], idx[1][4], idx[2][3], idx[2][4], idx[3][4]]]
    # print(sesgo_de_cliques(fnd))
    # prueba_diferencia_sesgo_simuladas_aleatorias()
    # print(intra_solapamiento(clique))
    # grafica_sopalamiento_simuladas_vs_aleatorias()
    # simulate_circuit_with_not()
    # compare_rand_fun_with_not()

    # f = genera_pseudoaleatoria_puntuacion(300)
    # g = genera_pseudoaleatoria_puntuacion(300)
    # print(m(combAND_with_not(f, g)))

    # grafica_sesgo(leer_fnds_por_puntuacion("experimentos/experimentos_n8/almacen_fnds.json"))

    # aleatorias = [[] for _ in range(420)]
    # for _ in range(1000):
    #     punt = random.randint(1, 250)
    #     aleatorias[punt].append(genera_pseudoaleatoria_puntuacion(punt))
    # grafica_sesgo(aleatorias)
    
    # grafica_sopalamiento_simuladas_vs_aleatorias()

    # grafica_relacion_puntuacion_inter_solapamiento("experimentos/experimentos_n8/mejores_aleatorias_1-50_AND.json")
    # grafica_relacion_puntuacion_inter_solapamiento("experimentos/experimentos_n8/mejores_simuladas_1-50_AND.json")

    # grafica_sopalamiento_simuladas_vs_aleatorias()

    # print(sesgo_de_cliques(clique))

    # grafica_equidad_simuladas_vs_aleatorias()

    # print(intra_solapamiento(clique))
    
    # genera_aleatorias()
    # obtener_mejores_aleatorias(100, 150)

    # prueba_metricas_funciones_aleatorias()

    # f = [[3, 5], [1, 2, 3, 8, 9, 14]]
    # print(perdidas(f))
    # grafica_perdidas_simuladas_vs_aleatorias()

    # grafica_equidad_mejores(2500)
    # grafica_intrasolapamiento_mejores(2500)
    # grafica_perdidas_asignaciones_mejores(2500)
    # grafica_perdidas_puntuacion_mejores(2500)
    # grafica_sesgo_min_mejores(100)
    # grafica_sesgo_medio_mejores(100)

    grafica_variacion_equidad(100)
    grafica_variacion_intrasolapamiento(100)
    grafica_variacion_perdidas_asignaciones(100)
    grafica_variacion_perdidas_puntuacion(100)
    grafica_variacion_sesgo_min(100)
    grafica_variacion_sesgo_medio(100)

main()
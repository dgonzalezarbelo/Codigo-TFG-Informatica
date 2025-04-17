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
from metricas.clausulas_perfectas import *
from kNN.knn import *
import time

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

    # grafica_relacion_puntuacion_inter_solapamiento("experimentos/experimentos_n8/mejores_aleatorias_100-150_AND.json")
    # grafica_relacion_puntuacion_inter_solapamiento("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json")
    # grafica_relacion_puntuacion_inter_solapamiento("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json")

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
    # grafica_clausulas_perfectas_mejores(2500)

    # grafica_variacion_equidad(100)
    # grafica_variacion_intrasolapamiento(100)
    # grafica_variacion_perdidas_asignaciones(100)
    # grafica_variacion_perdidas_puntuacion(100)
    # grafica_variacion_sesgo_min(100)
    # grafica_variacion_sesgo_medio(100)
    
    # grafica_grados_libertad_mejores(1000)

    # print(intra_solapamiento(clique))
    # print(formula_solapamiento_clique())

    # print(sesgo_medio(clique))
    # print(grados_libertad(clique))
    # print(sesgo_medio([[3]]))
    # print(grados_libertad([[3]]))
    # print(1 + (K*(K-1))/(N*(N-1)))
    # print(f"2^({K} sobre 2) = {2**math.comb(K, 2)}")
    # lista = [((-1)**(i % 2)) * (math.comb(K, i) * 2**(math.comb(K,2) - math.comb(i, 2))) for i in range(2*K - N,K+1)]
    # print(f"Lista: {lista}")
    # print(f"Sumatorio = {sum(lista)}")

    # simulate_circuit_with_not()

    # f = [[1,3],[3,4,5],[1,2,3]]
    # print(f)
    # print(reduce(f))

    # reducir_almacen(reduce, m)
    # reducir_almacen(reduce, ruta_almacen="experimentos/experimentos_n8/almacen_fnds copy.json")
    # reducir_almacen(reduce, m, ruta_almacen="experimentos/experimentos_n8/almacen_aleatorias copy.json")

    # pruebas_reduccion()

    # obtener_mejores_pseudoaleatorias(300, 350)
    # almacena_fnds("experimentos/experimentos_n8/Simulacion_300_iteraciones_reducidas/funciones_fnd.json", "experimentos/experimentos_n8/almacen_fnds.json")
    # almacena_fnds("experimentos/2025-04-15_18-11-26/funciones_fnd.json", "experimentos/experimentos_n8/almacen_fnds.json")

    # genera_aleatorias()
    # compara_solapamiento()
    # compara_homogeneidad()
    # compara_grados_libertad()

    # histograma_grados_libertad()

    # genera_dataset_knn()
    # knn()

    # dic = leer_csv_a_diccionario_generalizado("metricas/graficas/comparaciones_Solapamiento/datos_Solapamiento.csv")
    # generar_grafica_desde_diccionario(dic)
    # generar_histograma_desde_diccionario(dic, "Grados de libertad", 64)
    # matriz_confusion_umbral_solapamiento(dic)

    # variacion_solapamiento()
    # variacion_homogeneidad()
    variacion_grados_libertad()

main()
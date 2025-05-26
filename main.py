from syntactic import *
from genetic import *
from experimentos import *
from medidas.solapamiento import *
from medidas.grados_libertad import *
from medidas.homogeneidad import *
from kNN.knn import *
import time
import csv

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

    # for _ in range(20):
    #     f = genera_pseudoaleatoria_puntuacion(100)
    #     g = genera_pseudoaleatoria_puntuacion(100)
    #     fandg = combAND_with_not(f, g)
    #     print(m(fandg), len(fandg))

    # for _ in range(20):
    #     [f] = poblacion_en_rango(50, 100, 1, "experimentos/experimentos_n8/almacen_fnds.json")
    #     [g] = poblacion_en_rango(50, 100, 1, "experimentos/experimentos_n8/almacen_fnds.json")
    #     fandg = combAND_with_not(f, g)
    #     print(m(fandg), len(fandg))
    
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
    # reducir_almacen(reduce_pyeda, m, ruta_almacen="experimentos/experimentos_n8/almacen_aleatorias.json")

    # pruebas_reduccion()

    # obtener_mejores_pseudoaleatorias(300, 350)
    # almacena_fnds("experimentos/experimentos_n8/Simulacion_300_iteraciones_reducidas/funciones_fnd.json", "experimentos/experimentos_n8/almacen_fnds.json")
    # almacena_fnds("experimentos/2025-04-15_18-11-26/funciones_fnd.json", "experimentos/experimentos_n8/almacen_fnds.json")

    # genera_aleatorias()
    # n_funciones = 1000
    # ini, fin = 1, 250
    # puntuaciones = [random.randint(ini, fin) for _ in range(n_funciones)]
    # pseudoaleatorias = []
    # for i, p in enumerate(puntuaciones):
    #     pseudoaleatorias.append(genera_pseudoaleatoria_puntuacion(p))
    #     print(f"{i} funciones pseudoaleatorias generadas")
    # simuladas = funciones_almacen_por_puntuacion(puntuaciones)
    # aleatorias = funciones_almacen_por_puntuacion(puntuaciones, "experimentos/experimentos_n8/almacen_aleatorias.json")
    # compara_solapamiento(simuladas, pseudoaleatorias, aleatorias)
    # compara_homogeneidad(simuladas, pseudoaleatorias, aleatorias)
    # compara_grados_libertad(simuladas, pseudoaleatorias, aleatorias)

    # histograma_grados_libertad()

    # genera_dataset_knn()
    # knn()

    # # Leer y modificar el CSV
    # with open("medidas/graficas/comparaciones_Solapamiento/datos_Solapamiento.csv", 'r', newline='') as infile:
    #     reader = csv.reader(infile)
    #     header = next(reader)  # Guardar cabecera
    #     rows = []
    #     for row in reader:
    #         row[2] = str(float(row[2]) / 2)  # Multiplica valor2 por 2
    #         rows.append(row)

    # # Escribir el archivo modificado
    # with open("medidas/graficas/comparaciones_Solapamiento/datos_Solapamiento.csv", 'w', newline='') as outfile:
    #     writer = csv.writer(outfile)
    #     writer.writerow(header)
    #     writer.writerows(rows)


    # dic = leer_csv_a_diccionario_generalizado("medidas/graficas/comparaciones_Solapamiento/datos_Solapamiento.csv")
    # generar_grafica_desde_diccionario(dic, "$\\mu_x(f)$", "$\\eta_s(f)$", "Relación de la métrica sintáctica y el solapamiento")
    # generar_histograma_desde_diccionario(dic, "$\\eta_s(f)$", "Valores de $\\eta_s$ para funciones pseudoaleatorias y simuladas", 1.0)
    # matriz_confusion_umbral_solapamiento(dic)

    # dic = leer_csv_a_diccionario_generalizado("medidas/graficas/comparaciones_Homogeneidad/datos_Homogeneidad.csv")
    # generar_grafica_desde_diccionario(dic, "$\\mu_x(f)$", "$\\eta_h(f)$", "Relación de la métrica sintáctica y la homogeneidad")
    # generar_histograma_desde_diccionario(dic, "$\\eta_s(f)$", "Valores de $\\eta_h$ para funciones pseudoaleatorias y simuladas", 1000000)
    # matriz_confusion_umbral_solapamiento(dic)

    # dic = leer_csv_a_diccionario_generalizado("medidas/graficas/comparaciones_Grados de libertad/datos_Grados de libertad.csv")
    # generar_grafica_desde_diccionario(dic, "$\\mu_x(f)$", "$\\mu_{\\delta}(f)$", "Relación de la métrica sintáctica y los grados de libertad")

    # variacion_solapamiento()
    # variacion_homogeneidad()
    # variacion_grados_libertad()

    # dic = leer_csv_a_diccionario_generalizado("medidas/graficas/Variacion_Solapamiento/valores_variacion_Solapamiento.csv")
    # generar_variacion_desde_diccionario(dic, "$\\eta_s$ antes de puertas", "$\\eta_s$ después de puertas", "Variación de $\\eta_s$")

    # dic = leer_csv_a_diccionario_generalizado("medidas/graficas/Variacion_Homogeneidad/valores_variacion_Homogeneidad.csv")
    # generar_variacion_desde_diccionario(dic, "$\\eta_h$ antes de puertas", "$\\eta_h$ después de puertas", "Variación de $\\eta_h$")
    
    # dic = leer_csv_a_diccionario_generalizado("medidas/graficas/Variacion_Grados de libertad/valores_variacion_Grados de libertad.csv")
    # generar_variacion_desde_diccionario(dic, "$\\mu_{\\delta}$ antes de puertas", "$\\mu_{\\delta}$ después de puertas", "Variación de $\\mu_{\\delta}$")
    
    # compare_rand_fun()
    # compara_productividad_simuladas_pseudoaleatorias()
    ...

main()
from syntactic import *
from genetic import *
from experimentos import *
from pruebas import *

# Función a la que llamar para hacer lo que quiera
def main():
    # obtener_mejores_aleatorias(100, 150)
    # f = [[12, 13, 23], [13, 14, 34], [23, 24, 34]]
    # g = [[12, 13], [13, 23]]
    # print(inter_heterogeneidad(f, g))
    # grafica_relacion_puntuacion_heterogeneidad("experimentos/experimentos_n8/mejores_aleatorias_1-50_AND.json")
    obtener_mejores_simuladas(100, 150)
    # prueba_diferencia_sesgo_simuladas_aleatorias()
    # filtrar_almacen_por_longitud()

main()
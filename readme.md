# Trabajo de fin de grado: Estudio de complejidad de circuitos para el problema CLIQUE

Este repositorio contiene el código desarrollado para mi TFG de informática presentado en la Universidad Complutense de Madrid (curso 2024-2025).

## Resumen del TFG
Este trabajo explora la complejidad computacional del problema CLIQUE desde la perspectiva de circuitos booleanos. Incluye una parte teórica basada en resultados clásicos sobre circuitos de profundidad constante y una parte experimental centrada en la métrica sintáctica. Se estudian distintas medidas para caracterizar funciones booleanas y se entrena un modelo de aprendizaje supervisado para clasificar funciones según su origen. El repositorio contiene el código para el análisis de medidas, la generación de datos y los experimentos de clasificación.

## Estructura del repositorio
├── experimentos/           # Datos usados y generados (FNDs, simulaciones, etc.)

├── kNN/                    # Código para el modelo de predicción con k-NN

├── medidas/                # Código referente al manejo de las medidas de solapamiento, homogeneidad y grados de libertad

│   ├── grados_libertad.py  # Código para el estudio de la medida de grados de libertad

│   ├── homogeneidad.py     # Código para el estudio de la medida de homogeneidad

│   ├── solapamiento.py     # Código para el estudio de la medida de solapamiento

│   └── graficas/           # Gráficas con las medidas anteriores

├── experimentos.py         # Funciones generales para el manejo de datos y generación de gráficas

├── genetic.py              # Algoritmo genético de parejas y otras funciones relevantes para su uso

├── hungarian.py            # Script con el algoritmo húngaro para el cálculo de la métrica sintáctica

└── syntactic.py            # Archivo con funciones relacionadas con el cálculo de la métrica sintáctica

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo [LICENSE](./LICENSE).

# Bachelor's thesis: Study of circuit complexity for the problem CLIQUE

This repository contains the code for my Computer Science Bachelor's Thesis at Universidad Complutense de Madrid (academic year 2024–2025).

## Thesis summary

This project investigates the computational complexity of the CLIQUE problem from the perspective of boolean circuits. It includes a theoretical review of classic results on constant-depth circuits and an experimental analysis based on the syntactic metric. Several measures are studied to characterize boolean functions, and a supervised learning model is trained to classify functions by their origin. The repository contains code for measure analysis, data generation, and classification experiments.

## Repository structure
├── experimentos/           # Data used and generated (DNFs, simulations, etc.)

├── kNN/                    # Code for the k-NN prediction model

├── medidas/                # Code for the overlap, homogeneity, and degrees of freedom measures

│   ├── grados_libertad.py  # Code for the degrees of freedom measure

│   ├── homogeneidad.py     # Code for the homogeneity measure

│   ├── solapamiento.py     # Code for the overlap measure

│   └── graficas/           # Graphs for the above measures

├── experimentos.py         # General functions for data handling and plotting

├── genetic.py              # Pair-genetic algorithm and supporting functions

├── hungarian.py            # Hungarian algorithm for computing the syntactic metric

└── syntactic.py            # Functions related to the syntactic metric

## License

This project is licensed under the MIT License. For more details, please see the [LICENSE](./LICENSE) file.
# Imports

# Imports generales
from syntactic import *
from genetic import *
from metricas.intra_solapamiento import *
from metricas.equidad import *
from metricas.sesgo import *
from experimentos import *

import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib


# Función para generar el CSV
def genera_dataset_knn():
    n_funciones = 20
    simuladas = leer_top_funciones("experimentos/experimentos_n8/mejores_simuladas_100-150_AND.json", n_funciones)
    pseudoaleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json", n_funciones)
    # aleatorias = leer_top_funciones("experimentos/experimentos_n8/mejores_pseudoaleatorias_100-150_AND.json", n_funciones)
    aleatorias = None
    datos = []
    for f in simuladas:
        metrica = m(f)
        solapamiento = intra_solapamiento(f)
        homogeneidad = equidad(f)
        grados_libertad = sesgo_medio(f)
        datos.append((metrica, solapamiento, homogeneidad, grados_libertad, 'simulada'))
        
    for f in pseudoaleatorias:
        metrica = m(f)
        solapamiento = intra_solapamiento(f)
        homogeneidad = equidad(f)
        grados_libertad = sesgo_medio(f)
        datos.append((metrica, solapamiento, homogeneidad, grados_libertad, 'pseudoaleatoria'))

    if aleatorias is not None:
        for f in aleatorias:
            metrica = m(f)
            solapamiento = intra_solapamiento(f)
            homogeneidad = equidad(f)
            grados_libertad = sesgo_medio(f)
            datos.append((metrica, solapamiento, homogeneidad, grados_libertad, 'aleatoria'))

    with open('k-NN/dataset_knn.csv', mode='w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['metrica', 'solapamiento', 'homogeneidad', 'grados_de_libertad', 'etiqueta'])
        escritor.writerows(datos)

    print("CSV generado correctamente.")


# Función para entrenar y evaluar el k-NN
def knn():
    # Cargar el dataset
    df = pd.read_csv('dataset_knn.csv')

    # Características y etiquetas
    X = df[['metrica', 'solapamiento', 'homogeneidad', 'grados_de_libertad']]
    y = df['etiqueta']

    # Escalar características
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Codificar etiquetas
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Dividir en entrenamiento y test
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Modelo k-NN
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X_train, y_train)

    # Predicción
    y_pred = modelo.predict(X_test)

    # Guardar el modelo, el escalador y el codificador de etiquetas
    joblib.dump(modelo, 'modelo_knn.pkl')
    joblib.dump(scaler, 'escalador.pkl')
    joblib.dump(le, 'label_encoder.pkl')

    # Evaluación
    print("Precisión:", accuracy_score(y_test, y_pred))
    print("\nReporte de clasificación:\n", classification_report(y_test, y_pred, target_names=le.classes_))
    # y_test: etiquetas reales
    # y_pred: etiquetas predichas
    cm = confusion_matrix(y_test, y_pred)
    print("Matriz de confusión:")
    print(cm)

# Uso del modelo ya entrenado
def usar_modelo():
    modelo = joblib.load('modelo_knn.pkl')
    scaler = joblib.load('escalador.pkl')
    le = joblib.load('label_encoder.pkl')

    nuevos_datos = [[0.78, 0.21, 0.45, 0.12]]  # ejemplo

    nuevos_datos_escalados = scaler.transform(nuevos_datos)

    pred = modelo.predict(nuevos_datos_escalados)

    etiqueta = le.inverse_transform(pred)
    print("Predicción:", etiqueta[0])

# Generación del dataset
# genera_dataset_knn()

# Entrenamiento y evaluación
# knn()
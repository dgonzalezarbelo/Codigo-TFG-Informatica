from syntactic import *
from genetic import *
from medidas.solapamiento import *
from medidas.homogeneidad import *
from medidas.grados_libertad import *
from experimentos import *

import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

def genera_dataset_knn():
    '''
    Genera un dataset para el k-NN que predice, en base a los valores de las medidas, si una función es simulada o no.
    Por defecto se hace un 80% de entrenamiento y un 20% de test, y se usan 6000 funciones simuladas, 3000 pseudoaleatorias y 3000 aleatorias.
    El dataset se guarda en un CSV. Se guardan también el label_encoder, el escalador y el modelo_knn.
    '''
    n_funciones = 6000   # Funciones de cada tipo
    ini, fin = 25, 250
    simuladas = poblacion_en_rango(ini, fin, n_funciones)
    pseudoaleatorias = [genera_pseudoaleatoria_puntuacion(random.randint(ini, fin)) for _ in range(n_funciones // 2)]
    # aleatorias = []
    aleatorias = poblacion_en_rango(ini, fin, n_funciones // 2, "experimentos/experimentos_n8/almacen_aleatorias.json")
    no_simuladas = pseudoaleatorias + aleatorias
    datos = []
    for i, f in enumerate(simuladas):
        metrica = m(f)
        solapamiento = solapamiento(f)
        homogeneidad = homogeneidad(f)
        grados_libertad = grados_libertad(f)
        datos.append((metrica, solapamiento, homogeneidad, grados_libertad, 'simulada'))
        if (i + 1) % 10 == 0:
            print(f"{i+1} funciones simuladas añadidas al dataset")
        
    for i, f in enumerate(no_simuladas):
        metrica = m(f)
        solapamiento = solapamiento(f)
        homogeneidad = homogeneidad(f)
        grados_libertad = grados_libertad(f)
        datos.append((metrica, solapamiento, homogeneidad, grados_libertad, 'no_simulada'))
        if (i + 1) % 10 == 0:
            print(f"{i+1} funciones no-simuladas añadidas al dataset")

    with open('kNN/dataset_knn.csv', mode='w', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['metrica', 'solapamiento', 'homogeneidad', 'grados_de_libertad', 'etiqueta'])
        escritor.writerows(datos)

    print("CSV generado correctamente.")


def knn():
    '''Entrena y evalua el k-NN a partir de los valores del dataset previamente generado'''
    # Cargar el dataset
    df = pd.read_csv('kNN/dataset_knn.csv')

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
    joblib.dump(modelo, 'kNN/modelo_knn.pkl')
    joblib.dump(scaler, 'kNN/escalador.pkl')
    joblib.dump(le, 'kNN/label_encoder.pkl')

    # Evaluación
    print("Precisión:", accuracy_score(y_test, y_pred))
    print("\nReporte de clasificación:\n", classification_report(y_test, y_pred, target_names=le.classes_))
    # y_test: etiquetas reales
    # y_pred: etiquetas predichas
    cm = confusion_matrix(y_test, y_pred)
    print("Matriz de confusión:")
    print(cm)
    etiquetas = ["simuladas", "no simuladas"]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=etiquetas)

    # Mostramos la matriz
    disp.plot(cmap=plt.cm.Blues)
    plt.title(f"Matriz de confusión")
    plt.show()

def usar_modelo():
    '''Usa el modelo de k-NN previamente entrenado'''
    modelo = joblib.load('kNN/modelo_knn.pkl')
    scaler = joblib.load('kNN/escalador.pkl')
    le = joblib.load('kNN/label_encoder.pkl')

    nuevos_datos = [[0.78, 0.21, 0.45, 0.12]]  # ejemplo

    nuevos_datos_escalados = scaler.transform(nuevos_datos)

    pred = modelo.predict(nuevos_datos_escalados)

    etiqueta = le.inverse_transform(pred)
    print("Predicción:", etiqueta[0])
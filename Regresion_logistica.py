import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# Cargar el conjunto de datos
url = ""# aca va el ds
names = ['X', 'Y', 'month', 'day', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area']
data = pd.read_csv(url, names=names)

# Eliminar características innecesarias y normalizar
data = data.drop(['X', 'Y', 'area'], axis=1)
data = (data - data.min()) / (data.max() - data.min())

# Crear un indicador binario para la presencia de incendios (area quemada > 0)
data['area_burned'] = data['area'].apply(lambda x: 1 if x > 0 else 0)

# Separar los datos en variables predictoras y variable objetivo
X = data.drop('area_burned', axis=1)
y = data['area_burned']

# Dividir los datos en un conjunto de entrenamiento y un conjunto de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear un modelo de regresión logística
model = LogisticRegression()

# Entrenar el modelo con los datos de entrenamiento
model.fit(X_train, y_train)

# Realizar predicciones sobre el conjunto de prueba
predictions = model.predict(X_test)

# Calcular métricas de rendimiento del modelo
print("Accuracy:", accuracy_score(y_test, predictions))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))
print("\nClassification Report:")
print(classification_report(y_test, predictions))

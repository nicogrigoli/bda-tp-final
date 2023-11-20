import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Cargar el dataset .csv
data = pd.read_csv('datasets/ETL/random-forest/etl_datos_finales_random_forest.csv')

# Preparar los datos para el entrenamiento del modelo
# (Este paso depende del dataset específico que estés utilizando)
X = data.drop('indice_incendio', axis=1)
X = X.drop('fecha', axis=1)
y = data['indice_incendio']

# Dividir el dataset en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Crear y entrenar el modelo RandomForestRegressor
regression_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
regression_model.fit(X_train, y_train)

# Realizar predicciones en el conjunto de entrenamiento
y_train_pred = regression_model.predict(X_train)

print('predicciones en el conjunto de entrenamiento')
print(y_train_pred)

# Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R^2) en el conjunto de entrenamiento
mse_train = mean_squared_error(y_train, y_train_pred)
r2_train = r2_score(y_train, y_train_pred)

# Realizar predicciones en el conjunto de prueba
y_test_pred = regression_model.predict(X_test)

print('predicciones en el conjunto de entrenamiento')
print(y_test_pred)

# Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R^2) en el conjunto de prueba
mse_test = mean_squared_error(y_test, y_test_pred)
r2_test = r2_score(y_test, y_test_pred)

print('Error cuadrático medio en el conjunto de entrenamiento:', mse_train)
print('Error cuadrático medio en el conjunto de prueba:', mse_test)
print('Coeficiente de determinación en el conjunto de entrenamiento:', r2_train)
print('Coeficiente de determinación en el conjunto de prueba:', r2_test)

# Graficar los resultados
plt.figure(figsize=(12, 6))
plt.scatter(y_test, y_test_pred, color='blue', label='Prueba')
plt.scatter(y_train, y_train_pred, color='red', label='Entrenamiento')
plt.legend()
plt.xlabel('Valores reales')
plt.ylabel('Valores predichos')
plt.title('Gráfico de valores reales vs valores predichos')
plt.show()

#https://www.youtube.com/watch?v=OJ6hF5ZUSuo&t=768s
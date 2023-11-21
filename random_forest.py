import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset .csv
data = pd.read_csv('datasets/ETL/random-forest/etl_datos_finales_random_forest.csv')

# Preparar los datos para el entrenamiento del modelo
# (Este paso depende del dataset específico que estés utilizando)



# Separar el string 'date_time' en una lista de strings
data[['mes','anio']] = data['fecha'].str.split('-', expand=True)

# Convertir la columna 'date' en valores enteros
data['mes'] = data['mes'].astype(int)

# Convertir la columna 'time' en valores enteros
data['anio'] = data['anio'].astype(int)

X = data.drop('indice_incendio', axis=1)
X = X.drop('fecha', axis=1)
y = data['indice_incendio']

# Dividir el dataset en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=None)

# Crear y entrenar el modelo RandomForestRegressor
regression_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=None)
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

print('predicciones en el conjunto de prueba')
print(y_test_pred)

# Calcular el error cuadrático medio (MSE) y el coeficiente de determinación (R^2) en el conjunto de prueba
mse_test = mean_squared_error(y_test, y_test_pred)
r2_test = r2_score(y_test, y_test_pred)

print('Error cuadrático medio en el conjunto de entrenamiento:', mse_train)
print('Error cuadrático medio en el conjunto de prueba:', mse_test)
print('Coeficiente de determinación en el conjunto de entrenamiento:', r2_train)
print('Coeficiente de determinación en el conjunto de prueba:', r2_test)



df = pd.DataFrame(X_test)
df['date_year'] = df['mes'].astype(str) + '-' + df['anio'].astype(str)

# Convertir la columna 'date_year' a datetime
df['date_year'] = pd.to_datetime(df['date_year'], format='%m-%Y')

# Cambiar el formato de la columna 'date' a 'YYYY-MM'
df['date_year'] = df['date_year'].dt.strftime('%Y-%m')

# Ordenar la columna 'date_year'
df = df.sort_values('date_year')

df['date_year'] = df['date_year'].astype(str)

# Crear el gráfico de líneas múltiples
plt.figure(figsize=(10, 6))

plt.plot(df['date_year'], df['factor_temperatura'], label='Temperatura', marker='o')
plt.plot(df['date_year'], df['factor_humedad'], label='Baja humedad', marker='o')
plt.plot(df['date_year'], df['factor_precipitaciones'], label='Baja precipitación', marker='o')
plt.plot(df['date_year'], y_test, label='Incendios', marker='o')

# Configurar el eje x para que muestre las fechas de manera legible
plt.xticks(rotation=45)
plt.xlabel('Fechas x mes')

# Configurar etiquetas y leyenda
plt.ylabel('Variables')
plt.title('Indice de incendios en funcion del tiempo')
plt.legend()

# Mostrar el gráfico
plt.tight_layout()
plt.show()

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
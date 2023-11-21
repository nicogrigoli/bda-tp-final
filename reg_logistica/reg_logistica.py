import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error
import csv

import pandas as pd
import matplotlib.pyplot as plt


# Valores de entrada: avg_temp, avg_humidity, avg_rain, avg_wind_speed
x = []

# Valores de salida: riesgo_incendio_num
y = []

# Leo el dataset procesado
with open('etl_datos_finales_reg_logistica.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue  # Salteo el header
        else:
            x.append([
                float(row[2]),
                float(row[3]),
                float(row[4]),
                float(row[5]),
                float(row[6]),
                float(row[7]),
            ])

            y.append(float(row[9]))

            line_count += 1


# Entreno el modelo 1000 veces y calculo el error cuadratico medio en cada iteracion
# tambien registro las observaciones
mean_squared_errors = []
observations = []
for i in range(1000):
    if i % 10 == 0:
        print(int(i / 10), '%')

    # Particiono el dataset, 70% para entrenamiento y 30% para test
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.30, random_state=None)

    # Entreno el modelo con el dataset de entrenamiento
    model = LogisticRegression(
        multi_class='multinomial', solver='lbfgs', max_iter=10000)
    model.fit(x_train, y_train)

    # Hago las predicciones con el dataset de test
    y_pred = model.predict(x_test)

    # Calculo el error cuadratico medio para ver que tan bien predice el modelo
    mse = mean_squared_error(y_test, y_pred)
    mean_squared_errors.append(mse)

    # Guardo las observaciones obtenidas
    for i in range(len(y_test)):
        observations.append({
            'real_value': y_test[i],
            'predicted_value': y_pred[i]
        })


print('\n')
# Calculo el promedio de los errores cuadraticos medios
print('Mean Squared Error promedio: ', np.mean(mean_squared_errors))

predicciones_acertadas = len(
    list(filter(lambda x: x['real_value'] == x['predicted_value'], observations)))
print('Total observaciones: ', len(observations))
print('Predicciones acertadas: ', predicciones_acertadas)
print('Porcentaje acierto: ', predicciones_acertadas * 100 / len(observations))





data = []
for i in range(3):
    data.append({
        'real_value': i + 1,
        'Bajo': len(list(filter(lambda x: x['real_value'] == i + 1 and x['predicted_value'] == 1, observations))),
        'Medio': len(list(filter(lambda x: x['real_value'] == i + 1 and x['predicted_value'] == 2, observations))),
        'Alto': len(list(filter(lambda x: x['real_value'] == i + 1 and x['predicted_value'] == 3, observations))),
    })


df = pd.DataFrame(data)
ax = df.plot.bar(x='real_value', stacked=True, title='Observaciones por riesgo de incendio y predicciones', color=['green', 'orange', 'red'])
ax.set_xticklabels(['Bajo','Medio','Alto'], rotation=0)
ax.set_xlabel('Valores reales')
plt.legend( title="Predicciones")

plt.savefig('graficos/6.predicciones.png',bbox_inches='tight')
plt.cla()


print('Porcentaje de acierto por riesgo de incendio')
print('Bajo: ', data[0]['Bajo'] * 100 / (data[0]['Bajo'] + data[0]['Medio'] + data[0]['Alto']))
print('Medio: ', data[1]['Medio'] * 100 / (data[1]['Bajo'] + data[1]['Medio'] + data[1]['Alto']))
print('Alto: ', data[2]['Alto'] * 100 / (data[2]['Bajo'] + data[2]['Medio'] + data[2]['Alto']))

import openpyxl
import csv
from datetime import datetime
import numpy
import numbers


# Primero vamos a extraer del dataset sup_bosques_nativos_afectadas_por_mes_acumulado_98_19 el acumulado de hectareas quemadas por mes
# Con estos datos vamos a calcular el porcentaje de hectareas quemadas por mes en relacion al total de hectareas quemadas en el año, 
# para saber en que meses hay mayor probabilidad de que ocurran incendios
total_hectareas_afectadas = 0
datos_superficie_mes = []
with open('reg_log_datasets/sup_bosques_nativos_afectadas_por_mes_acumulado_98_19.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue # Para el header no hago nada

        total_hectareas_afectadas += int(row[2])
        datos_superficie_mes.append({
            'mes': line_count, # Los meses estan ordenados en el dataset
            'total_hectareas_afectadas': int(row[2]),
        })
        line_count += 1

# Calculo el porcentaje de hectareas quemadas por mes en relacion al total de hectareas quemadas en el año
for mes in datos_superficie_mes:
    mes['porcentaje'] = mes['total_hectareas_afectadas'] / total_hectareas_afectadas * 100

print('Probabilidad de incendio por mes: ');
for mes in datos_superficie_mes:
    print('Mes: ', mes['mes'], ' - Porcentaje: ', "{:.2f}".format(mes['porcentaje']))
print('\n')



# Filtro los datos del excel de incendios por provincia == Córdoba
dataframe_incendios = openpyxl.load_workbook("reg_log_datasets/superficie-incendiada-provincias-tipo-de-vegetacion_2022.xlsx")

datos_incendios = []
for row_num, row in enumerate(dataframe_incendios.active.iter_rows(values_only=True), start=1):
    if row_num == 1:
        continue  # Salteo el header
    if row[1] == "Córdoba":
        datos_incendios.append({
            'anio': row[0],
            'provincia': row[1],
            'total_hectareas_afectadas': row[2] if isinstance(row[2], numbers.Number) else 0,
            'hectareas_bosques_nativos': row[3] if isinstance(row[3], numbers.Number) else 0,
            'hectareas_bosques_cultivados': row[4] if isinstance(row[4], numbers.Number) else 0,
            'hectareas_pastizal': row[6] if isinstance(row[6], numbers.Number) else 0,
        })


# Utilizando los porcentajes de hectareas quemadas por mes, divido los datos de incendio anuales
# en datos de incendio mensuales. Utilizo solo los datos de BOSQUES NATIVOS
datos_incendios_mes = []
for dato_incendio in datos_incendios:
    for mes in datos_superficie_mes:
        datos_incendios_mes.append({
            'anio_mes': str(dato_incendio['anio']) + '-' + str(mes['mes']),
            'hectareas_bosques_nativos': dato_incendio['hectareas_bosques_nativos'] * (mes['porcentaje'] / 100),
        })



# Agrupo los datos meteorologicos por año y mes
datos_meteorologicos = []
with open('reg_log_datasets/Cordoba 1990-01-01 to 2023-11-07.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue # Salteo el header
        else:
            fecha = datetime.fromisoformat(row[1])
            data_anio_mes = next(filter(lambda x: x['anio_mes'] == str(fecha.year) + '-' + str(fecha.month), datos_meteorologicos), None)

            if data_anio_mes is None:
                data_anio_mes = {
                    'anio_mes': str(fecha.year) + '-' + str(fecha.month),
                    'registros': [],
                }
                datos_meteorologicos.append(data_anio_mes)

            data_anio_mes['registros'].append(row)
            line_count += 1



# Por cada mes calculo el promedio diario de temperatura, humedad, lluvia y velocidad del viento
for data_anio_mes in datos_meteorologicos:
    # Hay muy pocos registros que no tienen informacion, los filtro
    data_anio_mes['registros'] = list(filter(lambda x: x[4] != '', data_anio_mes['registros']))

    data_anio_mes['registros_count'] = len(data_anio_mes['registros'])
    data_anio_mes['avg_temp'] = numpy.mean([float(registro[4]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_min_temp'] = numpy.mean([float(registro[3]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_max_temp'] = numpy.mean([float(registro[2]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_humidity'] = numpy.mean([float(registro[9]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_rain'] = numpy.mean([float(registro[10]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_wind_speed'] = numpy.mean([float(registro[17]) for registro in data_anio_mes['registros']])




# Combino los datos de incendios mensuales con los datos del clima
datos_finales = []
for dato_incendio_mes in datos_incendios_mes:
    dato_meteorologico = next(filter(lambda x: x['anio_mes'] == dato_incendio_mes['anio_mes'], datos_meteorologicos), None)

    datos_finales.append({
        'anio_mes': dato_incendio_mes['anio_mes'],
        'hectareas_bosques_nativos': dato_incendio_mes['hectareas_bosques_nativos'],
        'avg_temp': dato_meteorologico['avg_temp'],
        'avg_min_temp': dato_meteorologico['avg_min_temp'],
        'avg_max_temp': dato_meteorologico['avg_max_temp'],        
        'avg_humidity': dato_meteorologico['avg_humidity'],
        'avg_rain': dato_meteorologico['avg_rain'],
        'avg_wind_speed': dato_meteorologico['avg_wind_speed'],
    })


# Clasifico cada anio_mes en riesgo de incendio bajo, medio o alto
hectareas_quemadas = [dato['hectareas_bosques_nativos'] for dato in datos_finales]
hectareas_quemadas.sort()

# Calculo el percentil 33 y 66 para saber el rango de hectareas quemadas que se considera bajo, medio y alto
percentil_33 = numpy.percentile(hectareas_quemadas, 33)
percentil_66 = numpy.percentile(hectareas_quemadas, 66)

for dato in datos_finales:
    if dato['hectareas_bosques_nativos'] <= percentil_33:
        dato['riesgo_incendio'] = 'bajo'
        dato['riesgo_incendio_num'] = 1
    elif dato['hectareas_bosques_nativos'] > percentil_33 and dato['hectareas_bosques_nativos'] <= percentil_66:
        dato['riesgo_incendio'] = 'medio'
        dato['riesgo_incendio_num'] = 2
    else:
        dato['riesgo_incendio'] = 'alto'
        dato['riesgo_incendio_num'] = 3


print('Cantidad de bajos: ', len(list(filter(lambda x: x['riesgo_incendio'] == 'bajo', datos_finales))))
print('Cantidad de medios: ', len(list(filter(lambda x: x['riesgo_incendio'] == 'medio', datos_finales))))
print('Cantidad de altos: ', len(list(filter(lambda x: x['riesgo_incendio'] == 'alto', datos_finales))))


# Guardo los datos finales en un csv
with open('etl_datos_finales_reg_logistica.csv', 'w', newline="") as f:  # open('test.csv', 'w', newline="") for python 3
    c = csv.writer(f)
    c.writerow(['anio_mes', 'hectareas_bosques_nativos', 'avg_temp', 'avg_min_temp', 'avg_max_temp', 'avg_humidity', 'avg_rain', 'avg_wind_speed', 'riesgo_incendio', 'riesgo_incendio_num'])
    for dato in datos_finales:
        c.writerow([dato['anio_mes'], dato['hectareas_bosques_nativos'], dato['avg_temp'], dato['avg_min_temp'], dato['avg_max_temp'], dato['avg_humidity'], dato['avg_rain'], dato['avg_wind_speed'], dato['riesgo_incendio'], dato['riesgo_incendio_num']])


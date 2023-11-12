
import openpyxl
import csv
from datetime import datetime
import numpy


#  Filtro los datos del excel de incendios por provincia
dataframe_incendios = openpyxl.load_workbook("superficie-incendiada-provincias-tipo-de-vegetacion_2022.xlsx")

datos_incendios = []
# Iterate the loop to read the cell values
for row_num, row in enumerate(dataframe_incendios.active.iter_rows(values_only=True), start=1):
    if row_num == 1:
        continue  # Skip the first row
    if row[1] == "Córdoba":
        datos_incendios.append({
            'anio': row[0],
            'provincia': row[1],
            'total_hectareas_afectadas': row[2],
            'hectareas_bosques_nativos': row[3],
            'hectareas_bosques_cultivados': row[4],
            'hectareas_pastizal': row[6],
        })



# Filtro los datos del csv de clima por año
weather_data = []
with open('Cordoba 2000-01-02 to 2023-11-07.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        else:
            fecha = datetime.fromisoformat(row[1])
            data_anio = next(filter(lambda x: x['anio'] == fecha.year, weather_data), None)

            if data_anio is None:
                data_anio = {
                    'anio': fecha.year,
                    'registros': [],
                }
                weather_data.append(data_anio)

            data_anio['registros'].append(row)

            line_count += 1

# Por cada registro de clima anual, calculo los promedios de temperatura, sensacion termica, humedad, lluvia y velocidad del viento
for data_anio in weather_data:
    data_anio['registros'] = list(filter(lambda x: x[4] != '', data_anio['registros']))

    data_anio['registros_count'] = len(data_anio['registros'])
    data_anio['avg_temp'] = numpy.mean([float(registro[4]) for registro in data_anio['registros']])
    data_anio['avg_feel_temp'] = numpy.mean([float(registro[7]) for registro in data_anio['registros']])
    data_anio['avg_humidity'] = numpy.mean([float(registro[9]) for registro in data_anio['registros']])
    data_anio['avg_rain'] = numpy.mean([float(registro[10]) for registro in data_anio['registros']])
    data_anio['avg_wind_speed'] = numpy.mean([float(registro[17]) for registro in data_anio['registros']])



# Combino los datos de incendios con los datos del clima
datos_finales = []

for dato_incendio in datos_incendios:
    dato_clima = next(filter(lambda x: x['anio'] == dato_incendio['anio'], weather_data), None)

    datos_finales.append({
        'anio': dato_incendio['anio'],
        'provincia': dato_incendio['provincia'],
        'total_hectareas_afectadas': dato_incendio['total_hectareas_afectadas'],
        'hectareas_bosques_nativos': dato_incendio['hectareas_bosques_nativos'],
        'hectareas_bosques_cultivados': dato_incendio['hectareas_bosques_cultivados'],
        'hectareas_pastizal': dato_incendio['hectareas_pastizal'],
        #'registros_count': dato_clima['registros_count'],
        'avg_temp': dato_clima['avg_temp'] if dato_clima is not None else "-",
        'avg_feel_temp': dato_clima['avg_feel_temp'] if dato_clima is not None else "-",
        'avg_humidity': dato_clima['avg_humidity'] if dato_clima is not None else "-",
        'avg_rain': dato_clima['avg_rain'] if dato_clima is not None else "-",
        'avg_wind_speed': dato_clima['avg_wind_speed'] if dato_clima is not None else "-",
    })

# Exporto los datos finales a un csv
with open('datos_finales.csv', 'w', newline="") as f:  # open('test.csv', 'w', newline="") for python 3
    c = csv.writer(f)
    c.writerow(['anio', 'provincia', 'total_hectareas_afectadas', 'hectareas_bosques_nativos', 'hectareas_bosques_cultivados', 'hectareas_pastizal', 'avg_temp', 'avg_feel_temp', 'avg_humidity', 'avg_rain', 'avg_wind_speed'])
    for row in datos_finales:
        c.writerow([row['anio'], row['provincia'], row['total_hectareas_afectadas'], row['hectareas_bosques_nativos'], row['hectareas_bosques_cultivados'], row['hectareas_pastizal'], row['avg_temp'], row['avg_feel_temp'], row['avg_humidity'], row['avg_rain'], row['avg_wind_speed']])
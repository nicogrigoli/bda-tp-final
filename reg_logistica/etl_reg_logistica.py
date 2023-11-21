
import openpyxl
import csv
from datetime import datetime
import numpy
import numbers
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


def create_grafico_hectareas_mes(datos_superficie_mes):
    df = pd.DataFrame(datos_superficie_mes)

    # Set the 'mes_nombre' column as the index
    df.set_index('mes_nombre', inplace=True)
    df.plot(kind='bar', y='total_hectareas_afectadas')

    # Para sacar la notacion cientifica
    def no_scientific_notation(x, pos):
        return '%.0f' % x
    formatter = FuncFormatter(no_scientific_notation)
    plt.gca().yaxis.set_major_formatter(formatter)

    # Add a title to the plot
    plt.title('Total de hectáreas de bosques nativos afectadas por mes a nivel país')
    # Display the plot
    plt.xticks(rotation=25)
    plt.legend().set_visible(False)

    plt.savefig('graficos/1.total_hectareas_afectadas_por_mes.png')
    plt.cla()

def create_grafico_porcentaje_hectareas_mes(datos_superficie_mes):
    colors = ['yellowgreen','red','gold','lightskyblue','white','lightcoral','blue','pink', 'darkgreen','yellow','grey','violet','magenta','cyan']

    patches, texts = plt.pie([i['porcentaje'] for i in datos_superficie_mes] , colors=colors, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i['mes_nombre'], i['porcentaje']) for i in datos_superficie_mes]

    plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.5, 0.5), fontsize=8)
    plt.title('Porcentaje de hectáreas de bosques nativos afectadas por mes a nivel país',)

    plt.savefig('graficos/2.porcentaje_hectareas_afectadas_por_mes.png',bbox_inches='tight')
    plt.cla()


def create_grafico_hectareas_cordoba_anio(datos_incendios):
    df = pd.DataFrame(datos_incendios)

    # Set the 'anio' column as the index
    df.set_index('anio', inplace=True)
    df.plot(kind='bar', y='hectareas_bosques_nativos')

    # Para sacar la notacion cientifica
    def no_scientific_notation(x, pos):
        return '%.0f' % x
    formatter = FuncFormatter(no_scientific_notation)
    plt.gca().yaxis.set_major_formatter(formatter)

    # Add a title to the plot
    plt.title('Total de hectáreas afectadas por año para la provincia de Córdoba')
    # Display the plot
    plt.xticks(rotation=90)
    plt.legend().set_visible(False)

    plt.savefig('graficos/3.total_hectareas_afectadas_por_anio.png')
    plt.cla()

# Line plot
def create_grafico_hectareas_cordoba_mes(datos_incendios_mes):
    df = pd.DataFrame(datos_incendios_mes)

    # Set the 'anio_mes' column as the index
    df.set_index('anio_mes', inplace=True)
    df.plot(kind='line', y='hectareas_bosques_nativos',)

    # Para sacar la notacion cientifica
    def no_scientific_notation(x, pos):
        return '%.0f' % x
    formatter = FuncFormatter(no_scientific_notation)
    plt.gca().yaxis.set_major_formatter(formatter)

    # Add a title to the plot
    plt.title('Total de hectáreas afectadas por mes para la provincia de Córdoba')
    # Display the plot
    plt.xticks(rotation=30)
    plt.legend().set_visible(False)
    plt.margins(x=0, y=0)

    plt.savefig('graficos/4.total_hectareas_afectadas_por_mes.png')
    plt.cla()


def create_grafico_riesgo_incendio(datos_finales, q1, q3, p1, p99):
    df = pd.DataFrame(datos_finales)

    # order by 'surface_burnt'
    df = df.sort_values('hectareas_bosques_nativos')

    # create a list of labels for the 3 parts of the dataset
    categories = [
        {
            'label': 'Riesgo Bajo: ',
            'color': 'green'
        },
        {
            'label': 'Riesgo Medio: ',
            'color': 'orange'
        },
        {
            'label': 'Riesgo Alto: ',
            'color': 'red'
        }]

    # plot the data
    fig, ax = plt.subplots()
    for i, category in enumerate(categories):
        if i == 0:
            subset = df[df['hectareas_bosques_nativos'] <= q1]
        elif i == len(categories) - 1:
            subset = df[df['hectareas_bosques_nativos'] >= q3]
        else:
            subset = df[(df['hectareas_bosques_nativos'] > q1) & (df['hectareas_bosques_nativos'] < q3)]
        ax.plot(subset['anio_mes'], subset['hectareas_bosques_nativos'],'o', label=category['label'] + str(len(subset)) + ' registros', color=category['color'], markersize=3)

    plt.hlines(y=q1, xmin=0, xmax=len(datos_finales), colors='blue', linestyles='dashed', lw=0.5, label='P50 = ' + str("{:.0f}".format(q1)) + ' hectareas afectadas')
    plt.hlines(y=q3, xmin=0, xmax=len(datos_finales), colors='blue', linestyles='solid', lw=0.5, label='P85 = ' + str("{:.0f}".format(q3)) + ' hectareas afectadas')
    plt.hlines(y=p1, xmin=0, xmax=len(datos_finales), colors='red', linestyles='solid', lw=0.5, label='P1 = ' + str("{:.0f}".format(p1)) + ' hectareas afectadas')
    plt.hlines(y=p99, xmin=0, xmax=len(datos_finales), colors='red', linestyles='solid', lw=0.5, label='P99 = ' + str("{:.0f}".format(p99)) + ' hectareas afectadas')


    ax.set_xlabel('Observaciones mensuales ordenadas por hectáreas afectadas')
    ax.set_ylabel('Cantidad hectáreas afectadas')
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    

    plt.margins(x=0)
    plt.legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)

    plt.savefig('graficos/5.riesgo_incendio.png',bbox_inches='tight')
    plt.cla()









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
            continue  # Para el header no hago nada

        total_hectareas_afectadas += int(row[2])
        datos_superficie_mes.append({
            'mes': line_count,  # Los meses estan ordenados en el dataset
            'total_hectareas_afectadas': int(row[2]),
            'mes_nombre': row[1],
        })
        line_count += 1

create_grafico_hectareas_mes(datos_superficie_mes)

# Calculo el porcentaje de hectareas quemadas por mes en relacion al total de hectareas quemadas en el año
for mes in datos_superficie_mes:
    mes['porcentaje'] = mes['total_hectareas_afectadas'] / \
        total_hectareas_afectadas * 100
    
create_grafico_porcentaje_hectareas_mes(datos_superficie_mes)


print('Probabilidad de incendio por mes: ')
for mes in datos_superficie_mes:
    print('Mes: ', mes['mes'], ' - Porcentaje: ',
          "{:.2f}".format(mes['porcentaje']))
print('\n')


# Filtro los datos del excel de incendios por provincia == Córdoba
dataframe_incendios = openpyxl.load_workbook(
    "reg_log_datasets/superficie-incendiada-provincias-tipo-de-vegetacion_2022.xlsx")

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

create_grafico_hectareas_cordoba_anio(datos_incendios)

# Utilizando los porcentajes de hectareas quemadas por mes, divido los datos de incendio anuales
# en datos de incendio mensuales. Utilizo solo los datos de BOSQUES NATIVOS
datos_incendios_mes = []
for dato_incendio in datos_incendios:
    for mes in datos_superficie_mes:
        datos_incendios_mes.append({
            'anio_mes': str(dato_incendio['anio']) + '-' + str(mes['mes']),
            'hectareas_bosques_nativos': dato_incendio['hectareas_bosques_nativos'] * (mes['porcentaje'] / 100),
        })

create_grafico_hectareas_cordoba_mes(datos_incendios_mes)


# Agrupo los datos meteorologicos por año y mes
datos_meteorologicos = []
with open('reg_log_datasets/Cordoba 1990-01-01 to 2023-11-07.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue  # Salteo el header
        else:
            fecha = datetime.fromisoformat(row[1])
            data_anio_mes = next(filter(lambda x: x['anio_mes'] == str(
                fecha.year) + '-' + str(fecha.month), datos_meteorologicos), None)

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
    data_anio_mes['registros'] = list(
        filter(lambda x: x[4] != '', data_anio_mes['registros']))

    data_anio_mes['registros_count'] = len(data_anio_mes['registros'])
    data_anio_mes['avg_temp'] = numpy.mean(
        [float(registro[4]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_min_temp'] = numpy.mean(
        [float(registro[3]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_max_temp'] = numpy.mean(
        [float(registro[2]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_humidity'] = numpy.mean(
        [float(registro[9]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_rain'] = numpy.mean(
        [float(registro[10]) for registro in data_anio_mes['registros']])
    data_anio_mes['avg_wind_speed'] = numpy.mean(
        [float(registro[17]) for registro in data_anio_mes['registros']])


# Combino los datos de incendios mensuales con los datos del clima
datos_finales = []
for dato_incendio_mes in datos_incendios_mes:
    dato_meteorologico = next(filter(
        lambda x: x['anio_mes'] == dato_incendio_mes['anio_mes'], datos_meteorologicos), None)

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
hectareas_quemadas = [dato['hectareas_bosques_nativos']
                      for dato in datos_finales]
hectareas_quemadas.sort()

# Calculo el percentil 33 y 66 para saber el rango de hectareas quemadas que se considera bajo, medio y alto
q1 = numpy.percentile(hectareas_quemadas, 50)
q3 = numpy.percentile(hectareas_quemadas, 85)

for dato in datos_finales:
    if dato['hectareas_bosques_nativos'] <= q1:
        dato['riesgo_incendio'] = 'bajo'
        dato['riesgo_incendio_num'] = 1
    elif dato['hectareas_bosques_nativos'] > q1 and dato['hectareas_bosques_nativos'] <= q3:
        dato['riesgo_incendio'] = 'medio'
        dato['riesgo_incendio_num'] = 2
    else:
        dato['riesgo_incendio'] = 'alto'
        dato['riesgo_incendio_num'] = 3

p1 = numpy.percentile(hectareas_quemadas, 1)
p99 = numpy.percentile(hectareas_quemadas, 99)

create_grafico_riesgo_incendio(datos_finales, q1, q3, p1, p99)

print('Cantidad de registros: ', len(datos_finales))

datos_finales = list(filter(lambda x: x['hectareas_bosques_nativos'] > p1 and x['hectareas_bosques_nativos'] < p99, datos_finales))
print('Cantidad de registros filtrados: ', len(datos_finales))

print('Cantidad de bajos: ', len(
    list(filter(lambda x: x['riesgo_incendio'] == 'bajo', datos_finales))))
print('Cantidad de medios: ', len(
    list(filter(lambda x: x['riesgo_incendio'] == 'medio', datos_finales))))
print('Cantidad de altos: ', len(
    list(filter(lambda x: x['riesgo_incendio'] == 'alto', datos_finales))))


# Guardo los datos finales en un csv
# open('test.csv', 'w', newline="") for python 3
with open('etl_datos_finales_reg_logistica.csv', 'w', newline="") as f:
    c = csv.writer(f)
    c.writerow(['anio_mes', 'hectareas_bosques_nativos', 'avg_temp', 'avg_min_temp', 'avg_max_temp',
               'avg_humidity', 'avg_rain', 'avg_wind_speed', 'riesgo_incendio', 'riesgo_incendio_num'])
    for dato in datos_finales:
        c.writerow([dato['anio_mes'], dato['hectareas_bosques_nativos'], dato['avg_temp'], dato['avg_min_temp'], dato['avg_max_temp'],
                   dato['avg_humidity'], dato['avg_rain'], dato['avg_wind_speed'], dato['riesgo_incendio'], dato['riesgo_incendio_num']])




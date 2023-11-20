
import openpyxl
import csv
from datetime import datetime
import numpy
import numbers
from decimal import Decimal, getcontext

#Aca se configuran los limites de los parametros de temperatura, humedad, precipitaciones y velocidad del viento
TEMPERATURA_MAXIMA = 30 #En grados celsius
HUMEDAD = 40 #En porcentaje
PRECIPITACIONES = 2 #Milimetros
VELOCIDAD_VIENTO = 35 #Km/hs

#PONDERACIONES
PONDERACION_VIENTO = Decimal(0.10)
PONDERACION_PRECIPITACION = Decimal(0.35)  
PONDERACION_HUMEDAD = Decimal(0.20)
PONDERACION_TEMPERATURA = Decimal(0.35)

contadores_meteorologicos = []
# Comienzo a leer el dataset para contabilizar los dias con humedad, temperatura, viento y precipitaciones segun los limites definidos en las constantes.
with open('datasets/sources/random-forest/Cordoba 1990-01-01 to 2023-11-07.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    #Inicializo contadores
    line_count = 0
    temp_max_count = 0
    humedad_count = 0
    precipitaciones_count = 0
    velocidad_viento_count = 0
    cantidad_dias = 1

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        
        else: 
            fecha = datetime.fromisoformat(row[1])

            if line_count == 1:
                month = fecha.month
                year = fecha.year

            else:
                cantidad_dias += 1 

            line_count += 1

            #Aplico condiciones para comenzar a contabilizar
            temp_max_value = float(row[2]) if row[2] != "" else 0
            if temp_max_value > TEMPERATURA_MAXIMA and temp_max_value != 0:
                temp_max_count+=1

            humedad = float(row[9]) if row[9] != "" else 0
            if humedad <= HUMEDAD and humedad != 0:
                humedad_count+=1

            precipitaciones = float(row[10]) if row[10] != "" else 0
            if precipitaciones > PRECIPITACIONES and precipitaciones != 0:
                precipitaciones_count+=1

            velocidad_viento = float(row[17]) if row[17] != "" else 0
            if velocidad_viento > VELOCIDAD_VIENTO and velocidad_viento != 0:
                velocidad_viento_count+=1
            
            #Si el mes cambia guardo la informacion en un objeto de contadores y la fecha (contadores_x_mes)
            if fecha.month != month:
                
                fechaFormateada = str(month) +"-"+ str(year)
                month = fecha.month
                year = fecha.year
                
                contadores_x_mes = {
                    'temperatura_max_count': temp_max_count,
                    'humedad_count': humedad_count,
                    'precipitaciones_count': precipitaciones_count,
                    'velocidad_viento_count': velocidad_viento_count,
                    'cantidad_dias_count': cantidad_dias,
                    'fecha': fechaFormateada,
                }
                #Reinicio contadores para calcular el nuevo mes
                temp_max_count = 0
                humedad_count = 0
                precipitaciones_count = 0
                velocidad_viento_count = 0
                cantidad_dias = 0
                contadores_meteorologicos.append(contadores_x_mes)

datos_finales = []
#Recorro el array armado enteriormente con todos los contadores por mes y voy haciendo los calculos de los factores y el indice de probabilidad segun los mismos
for contadores_x_mes in contadores_meteorologicos:
    factor_temperatura = round(contadores_x_mes['temperatura_max_count'] / contadores_x_mes['cantidad_dias_count'],2)
    factor_humedad = round(contadores_x_mes['humedad_count'] / contadores_x_mes['cantidad_dias_count'],2)
    factor_precipitaciones  = round(contadores_x_mes['precipitaciones_count'] / contadores_x_mes['cantidad_dias_count'],2)
    factor_viento = round(contadores_x_mes['velocidad_viento_count'] / contadores_x_mes['cantidad_dias_count'],2)


    #Si alguno de los factores es 0 no se puede calcular indice
    if factor_temperatura == 0 or factor_humedad == 0 or factor_precipitaciones == 0 or factor_viento == 0:
        continue

    #Algunos valores decimales son muy chicos con lo cual es necesario utilizar la libreria decimal.
    #Seteo la precision que van a tener los decimales
    getcontext().prec = 20
    #Los transformo a decimal y los multiplico para sacar el indice de probabilidad     
    indice_probabilidad = (PONDERACION_TEMPERATURA * Decimal(factor_temperatura)) + (PONDERACION_HUMEDAD * Decimal(factor_humedad)) + (PONDERACION_PRECIPITACION * Decimal(factor_precipitaciones)) + (PONDERACION_VIENTO * Decimal(factor_viento))



    #Se redondea el indice de probabilidad con una precision de 4 decimales.
    indice_incedio = round(indice_probabilidad,4)

    #Se guarda la informacion final en el objeto datos
    datos = {
        'fecha' : contadores_x_mes['fecha'],
        'factor_temperatura' : factor_temperatura,
        'factor_humedad' : factor_humedad,
        'factor_precipitaciones' : factor_precipitaciones,
        'factor_viento' : factor_viento,
        'indice_incendio' : indice_incedio
   }

    #Se guarda el objeto datos en datos_finales
    datos_finales.append(datos)

#Aca se escriben los datos en un nuevo archivo .csv
with open('datasets/ETL/random-forest/etl_datos_finales_random_forest.csv', 'w', newline="") as f:  # open('test.csv', 'w', newline="") for python 3
    c = csv.writer(f)
    c.writerow(['fecha', 'factor_temperatura', 'factor_humedad', 'factor_precipitaciones', 'factor_viento', 'indice_incendio'])
    for dato in datos_finales:
        c.writerow([dato['fecha'], dato['factor_temperatura'], dato['factor_humedad'], dato['factor_precipitaciones'], dato['factor_viento'], dato['indice_incendio']])



            



        



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargamos los conjuntos de datos en bruto
df_clima = pd.read_csv('imp_salidas/72505394728.csv', low_memory=False)
df_accidentes = pd.read_csv('imp_salidas/Motor_Vehicle_Collisions_-_Crashes_20260906.csv', low_memory=False)

# ==========================================
# ANALIZAMOS LA FUENTE DE DATOS: CLIMA
# ==========================================

# Filtramos el DataFrame para quedarnos solo con las columnas esenciales
df_clima = df_clima[['DATE', 'LATITUDE', 'LONGITUDE', 'WND', 'VIS', 'TMP', 'AA1']]

# Rellenamos valores nulos de la columna AA1 con 0
df_clima['AA1'] = df_clima['AA1'].fillna(0)


# ==========================================
# ANALIZAMOS LA FUENTE DE DATOS: ACCIDENTES
# ==========================================

# Filtramos el DataFrame para quedarnos solo con las columnas esenciales
df_accidentes = df_accidentes[[
    'CRASH DATE', 'CRASH TIME', 'BOROUGH', 'ZIP CODE', 'ON STREET NAME', 'CROSS STREET NAME', 'LATITUDE', 'LONGITUDE',
    'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED', 'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF CYCLIST INJURED',
    'CONTRIBUTING FACTOR VEHICLE 1', 'VEHICLE TYPE CODE 1'
]]

# Limpieza de las columnas de datos
# Rellenamos los nulos de las columnas de texto con 'UNSPECIFIED'
columnas_texto = ['BOROUGH', 'CONTRIBUTING FACTOR VEHICLE 1', 'VEHICLE TYPE CODE 1', 'ZIP CODE', 'ON STREET NAME', 'CROSS STREET NAME']
df_accidentes[columnas_texto] = df_accidentes[columnas_texto].fillna('UNSPECIFIED')

# Eliminamos las filas que no tienen coordenadas (borra la fila completa si falta latitud o longitud)
df_accidentes = df_accidentes.dropna(subset=['LATITUDE', 'LONGITUDE'])

# Preparamos el clima
# Convertimos el texto a un objeto de tiempo y "cortamos" los minutos usando .dt.floor('h')
df_clima['DATETIME'] = pd.to_datetime(df_clima['DATE']).dt.floor('h')

# Preparamos los datos de accidente
# Primero sumamos los dos textos con un espacio en medio, lo convertimos a tiempo y cortamos los minutos
df_accidentes['DATETIME'] = pd.to_datetime(df_accidentes['CRASH DATE'] + ' ' + df_accidentes['CRASH TIME']).dt.floor('h')


# ==========================================
# UNION DE TABLAS df_final
# ==========================================

# Unimos la tabla de accidentes con la del clima usando nuestra llave maestra DATETIME
df_final = pd.merge(df_accidentes, df_clima, on='DATETIME', how='inner')

# Eliminamos las columnas de coordenadas del clima que duplicaban información (_y)
df_final = df_final.drop(columns=['LATITUDE_y', 'LONGITUDE_y'])

# Renombramos las coordenadas reales de los accidentes (_x) para quitarles el sufijo
df_final = df_final.rename(columns={
    'LATITUDE_x': 'LATITUDE',
    'LONGITUDE_x': 'LONGITUDE'
})


# ==========================================
# TRANSFORMACIÓN DE VARIABLES DEL CLIMA
# ==========================================

# Lluvia (AA1): Extraemos la posición 1 y dividimos entre 10 para milímetros
df_final['CANTIDAD_LLUVIA'] = df_final['AA1'].str.split(',').str[1]
df_final['CANTIDAD_LLUVIA'] = pd.to_numeric(df_final['CANTIDAD_LLUVIA'], errors='coerce') / 10

# Temperatura (TMP): Extraemos la posición 0 y dividimos entre 10 para °C
df_final['TEMPERATURA'] = df_final['TMP'].str.split(',').str[0]
df_final['TEMPERATURA'] = pd.to_numeric(df_final['TEMPERATURA'], errors='coerce') / 10

# Visibilidad (VIS): Extraemos la posición 0 (se queda en metros)
df_final['VISIBILIDAD'] = df_final['VIS'].str.split(',').str[0]
df_final['VISIBILIDAD'] = pd.to_numeric(df_final['VISIBILIDAD'], errors='coerce')

# Viento (WND): Extraemos la velocidad en la posición 3 y dividimos entre 10 para m/s
df_final['VELOCIDAD_VIENTO'] = df_final['WND'].str.split(',').str[3]
df_final['VELOCIDAD_VIENTO'] = pd.to_numeric(df_final['VELOCIDAD_VIENTO'], errors='coerce') / 10

# Reemplazando 999.9 por np.nan en nuestra columna TEMPERATURA
df_final['TEMPERATURA'] = df_final['TEMPERATURA'].replace(999.9, np.nan)

# Reemplazando 999.9 por np.nan en nuestra columna VELOCIDAD_VIENTO
df_final['VELOCIDAD_VIENTO'] = df_final['VELOCIDAD_VIENTO'].replace(999.9, np.nan)

# Reemplazando 999999 por np.nan en nuestra columna VISIBILIDAD
df_final['VISIBILIDAD'] = df_final['VISIBILIDAD'].replace(999999, np.nan)

# Rellenamos los vacíos (NaN) con 0.0 milímetros
df_final['CANTIDAD_LLUVIA'] = df_final['CANTIDAD_LLUVIA'].fillna(0.0)


# ==========================================
# ANÁLISIS Y VISUALIZACIÓN
# ==========================================

# ====================
# ACCIDENTES EN DÍAS SECOS VS DÍAS LLUVIOSOS
# ====================
# Filtramos los accidentes con suelo seco (lluvia exactamente igual a cero)
accidentes_seco = df_final[df_final['CANTIDAD_LLUVIA'] == 0.0]

# Filtramos los accidentes con lluvia (lluvia mayor a cero)
accidentes_lluvia = df_final[df_final['CANTIDAD_LLUVIA'] > 0.0]

# Contamos cuántos accidentes hay en cada una usando len()
total_seco = len(accidentes_seco)
total_lluvia = len(accidentes_lluvia)

# Preparamos las listas para el gráfico
categorias = ['Suelo Seco', 'Con Lluvia']
totales = [total_seco, total_lluvia]

# Dibujamos el gráfico de barras
plt.bar(categorias, totales, color=['green', 'blue']) # Colores para diferenciar
plt.title('Accidentes de Tránsito en NY: Suelo Seco vs. Mojado')
plt.ylabel('Cantidad Total de Accidentes')


# ====================
# ACCIDENTES DURANTE TODO EL AÑO MES A MES
# ====================
# Transformamos toda la columna CRASH DATE a formato de fecha
df_final['CRASH DATE'] = pd.to_datetime(df_final['CRASH DATE'])

# Extraemos solo el número del mes y lo guardamos en una nueva columna
df_final['MES'] = df_final['CRASH DATE'].dt.month

# Contamos los accidentes por mes y los ordenamos del 1 al 12
accidentes_por_mes = df_final['MES'].value_counts().sort_index()

# Dibujamos el gráfico de líneas
plt.figure(figsize=(10, 6))

# Usamos marker='o' para poner un puntito en cada mes
plt.plot(accidentes_por_mes.index, accidentes_por_mes.values, marker='o', color='purple', linewidth=2)

plt.title('Accidentes de Tránsito en NY durante el año 2024', fontsize=14)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Cantidad de Accidentes', fontsize=12)

# Esto asegura que veamos los números del 1 al 12 en la barra de abajo y tengamos cuadrícula
plt.xticks(range(1, 13)) 
plt.grid(True)


# ==========================================
# DISTRIBUCIÓN DE ACCIDENTES SEGÚN LA VISIBILIDAD
# ==========================================

# Extraemos la columna de visibilidad (y quitamos posibles valores vacíos por seguridad)
visibilidad_datos = df_final['VISIBILIDAD'].dropna()

# Dibujamos el histograma
plt.figure(figsize=(10, 6))

# Para que tengamos 20 grupos usamos bins=20
plt.hist(visibilidad_datos, bins=20, color='teal', edgecolor='black')

plt.title('Distribución de Accidentes según la Visibilidad en NY', fontsize=14)
plt.xlabel('Visibilidad (metros)', fontsize=12)
plt.ylabel('Cantidad Total de Accidentes', fontsize=12)
plt.grid(axis='y', alpha=0.75)


# ==========================================
# CAUSAS DE ACCIDENTES
# ==========================================

# Contamos todas las causas de la columna
causas = df_final['CONTRIBUTING FACTOR VEHICLE 1'].value_counts()

# Quitamos la categoría 'Unspecified' para ver los motivos reales
causas_reales = causas[causas.index != 'Unspecified']

# Guardamos las causas
top_10_causas = causas_reales.head(10)

# Invertimos la lista para que la causa #1 aparezca hasta arriba
top_10_causas = top_10_causas.iloc[::-1]

# Graficamos horizontalmente barh()
plt.figure(figsize=(12, 6))
plt.barh(top_10_causas.index, top_10_causas.values, color='gray', edgecolor='black')

plt.title('Top 10 Causas Principales de Accidentes en NY (2024)', fontsize=14)
plt.xlabel('Cantidad de Accidentes', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)


# ==========================================
# ANÁLISIS ESTADÍSTICO DE GRAVEDAD
# ==========================================

# Por seguridad, rellenamos los valores vacíos de heridos con 0
df_final['NUMBER OF PERSONS INJURED'] = df_final['NUMBER OF PERSONS INJURED'].fillna(0)

# Filtramos el ruido ('Unspecified') para enfocarnos en causas reales
df_causas = df_final[df_final['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified']

# Agrupamos por causa y calculamos estadísticamentes: cantidad de choques y promedio de heridos
estadisticas = df_causas.groupby('CONTRIBUTING FACTOR VEHICLE 1')['NUMBER OF PERSONS INJURED'].agg(['count', 'mean'])

# Renombramos para mayor claridad
estadisticas.columns = ['Total_Accidentes', 'Promedio_Heridos_por_Choque']

# Filtramos causas con más de 1,000 accidentes para que el dato sea confiable
causas_frecuentes = estadisticas[estadisticas['Total_Accidentes'] > 1000]

# Ordenamos para ver cuál tiene el promedio de heridos MÁS ALTO
top_gravedad = causas_frecuentes.sort_values(by='Promedio_Heridos_por_Choque', ascending=False)

# Guardamos los datos limpios para usarlos en Power BI
df_final.to_csv('accidentes_ny_limpio.csv', index=False)

# Lanzamos las 4 gráficas
plt.show()
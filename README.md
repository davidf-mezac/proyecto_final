# Proyecto Final
# **🚦 Análisis de Siniestralidad y Seguridad Vial en NY: Exploración y Visualización de Datos**

## 📖 Descripción del Proyecto
Este proyecto realiza un análisis exploratorio de datos (EDA) integral para entender la dinámica de los accidentes de tráfico en la ciudad de Nueva York durante el año 2024. El objetivo principal es identificar si las condiciones meteorológicas son el principal causante de accidentes o si prevalece el factor humano, además de detectar los focos geográficos de mayor riesgo.

Para resolver este problema, se cruzaron dos bases de datos masivas: los registros oficiales de colisiones vehiculares de NY y los reportes meteorológicos históricos de la estación NOAA. Mediante el uso de Python para la transformación de datos (manejo de nulos, estandarización de fechas y cálculos estadísticos de gravedad) se construyó un Cuadro de Mando Operativo en Power BI que permite a las autoridades tomar decisiones estratégicas para proteger a la población vulnerable.

## 📂 Estructura del Proyecto
La organización de los archivos en este repositorio es la siguiente para facilitar la navegación y entender el flujo de trabajo:

* 📁 `data/`
  * 📁 `Datos crudos/`
    * 📄 **[72505394728.csv](./data/Datos%20crudos/72505394728.csv)** - Datos meteorológicos crudos (NOAA)
    * 📄 **[Motor_Vehicle_Collisions_-_Crashes_20260906.csv](./data/Datos%20crudos/Motor_Vehicle_Collisions_-_Crashes_20260906.csv)** - Datos de colisiones
  * 📁 `Datos procesados/`
    * 📄 **[accidentes_ny_limpio.csv](./data/Datos%20procesados/accidentes_ny_limpio.csv)** - Dataset final procesado y limpio
* 📁 `notebooks/`
  * 📄 **[exploracion_datos.ipynb](./notebooks/exploracion_datos.ipynb)** - Notebook de Jupyter con el análisis paso a paso
* 📁 `src/`
  * 📄 **[proyecto_final.py](./src/proyecto_final.py)** - Script de limpieza, cruce (merge) y exportación
* 📁 `dashboard/`
  * 📄 **[Accidentalidad y Seguridad Vial en la ciudad de Nueva York.pbix](./dashboard/Accidentalidad%20y%20Seguridad%20Vial%20en%20la%20ciudad%20de%20Nueva%20York.pbix)** - Dashboard interactivo
  * 📄 **[MemoriasPowerBI.pdf](./dashboard/MemoriasPowerBI.pdf)** - Bitácora visual del manejo en Power BI
* 📁 `results/`
  * 🖼️ **[Figura 1.png](./results/Figura%201.png)** - Gráfico "Accidentes de Tránsito en NY: Suelo Seco VS. Mojado"
  * 🖼️ **[Figura 2.png](./results/Figura%202.png)** - Gráfico "Accidentes de Tránsito en NY durante el año 2024"
  * 🖼️ **[Figura 3.png](./results/Figura%203.png)** - Gráfico "Distribución de Accidentes según la Visibilidad en NY"
  * 🖼️ **[Figura 4.png](./results/Figura%204.png)** - Gráfico "Top 10 Causas Principales de Accidentes en NY (2024)"
* 📄 `README.md` - Descripción general del proyecto

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** Python 3.12
* **Manipulación y Limpieza de Datos:** Pandas, NumPy
* **Visualización Exploratoria:** Matplotlib
* **Visualización Dinámica e Inteligencia de Negocios:** Power BI
* **Entorno de Desarrollo:** Visual Studio Code / Jupyter
* **Control de Versiones:** Git & GitHub

## 🛠️ Instalación e Instrucciones de Ejecución
Para ejecutar los scripts de procesamiento y explorar el Notebook, se requieren las siguientes bibliotecas:

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias ejecutando en tu terminal: `pip install pandas numpy matplotlib jupyter`
3. **Para ejecutar el pipeline:** Ejecuta el archivo principal en la terminal con `python src/proyecto_final.py`. El script generará automáticamente el archivo `accidentes_ny_limpio.csv`, listo para ser importado a Power BI.
4. **Para ver el análisis:** Inicia Jupyter Notebook (`jupyter notebook`) y abre el archivo `notebooks/exploracion_datos.ipynb` para visualizar el paso a paso de los gráficos y la lógica detrás del código.

## 📊 Resultados y Conclusiones
* **El factor humano supera al clima:** Contrario a la creencia popular, las lluvias o la niebla no son los principales causantes de siniestros. La "Distracción del Conductor" lidera la estadística con más de 26,000 casos.
* **La gravedad vs. El volumen:** Al calcular el promedio de víctimas por choque, descubrimos que ignorar las señales de tráfico (*Traffic Control Disregarded*) es la infracción más peligrosa, promediando 0.92 heridos por evento, muy por encima de la simple distracción.
* **Focos geográficos:** Brooklyn y Queens concentran de manera conjunta más del 62% del total de los accidentes de la ciudad.
* **Estacionalidad:** Identificamos aumentos atípicos de accidentalidad en los meses de mayo (primavera) y diciembre (festividades), rompiendo el sesgo de que solo el clima invernal eleva el riesgo.
* **Población Vulnerable:** Los peatones son, con gran diferencia, el grupo más afectado en todos los distritos, superando siempre a los ciclistas heridos.

## 🚀 Próximos Pasos
* **Análisis Geoespacial Avanzado:** Aprovechar las columnas limpias de `LATITUDE` y `LONGITUDE` para construir mapas de calor (Heatmaps) que señalen las intersecciones exactas más peligrosas.
* **Modelo Predictivo:** Implementar técnicas de *Machine Learning* para estimar la probabilidad de un accidente grave basándose en la zona, el clima y la hora del día.

## 🤝 Contribuciones
Las contribuciones son bienvenidas. Si deseas mejorar la eficiencia del script `proyecto_final.py` o expandir el dashboard en Power BI, por favor abre un *pull request* o una *issue*.

## ✍️ Autores y Agradecimientos
**Autor**
* David Felipe Meza Castaño - Ingeniero de Sistemas y Telecomunicaciones [@davidf-mezac](https://github.com/davidf-mezac)

**🤝 Agradecimientos**
* A los portales de Open Data de la Ciudad de Nueva York y la NOAA por proveer acceso transparente a las bases de datos públicas utilizadas en este análisis.

# <img src="https://png.pngtree.com/png-clipart/20250513/original/pngtree-cruise-ship-png-vintage-transport-clipart-png-image_20950498.png" width="70"> Dashboard Interactivo de Cruceros

#### *Asignatura:* 
Python para Diploma en Ciencia de Datos e Inteligencia Artificial Aplicada
#### *Institución:* 
  <img src="https://logoteca.uy/wp-content/uploads/sites/3/2024/09/Logo-Universidad-Catolica.svg" width="70"> 
  
#### *Grupo:* 
Grupo C  
#### *Integrantes:* 
Nicolas Perez/Hector Martin/Paulina Carrocio/Marcelo Ocampo

---

##  Descripción del proyecto

Este proyecto consiste en el análisis exploratorio, procesamiento de datos y desarrollo de un **Dashboard Interactivo de Revenue Management** para la industria de cruceros. El conjunto de datos abarca más de **77,000 registros** de reservas, permitiendo analizar ingresos, estacionalidad, comportamiento de compra según el tipo de suite, canales de reserva y país de origen de los huéspedes.

El trabajo se estructuró en dos fases consecutivas:
1. **Fase 1 (ETL y EDA):** Carga, limpieza profunda, tratamiento de datos atípicos y exportación en Jupyter Notebook (`notebooks/practice.ipynb`).
2. **Fase 2 (Aplicación web interactiva):** Creación y despliegue de un dashboard dinámico en **Streamlit** (`app.py`).

---

##  Estructura del repositorio

```text
├── data/
│   ├── raw/
│   │   └── reporte_cruceros_revenue_management.csv   # Dataset original (+77k filas)
│   └── processed/
│       └── cruceros_procesados.csv                    # Dataset limpio y transformado
├── notebooks/
│   └── practice.ipynb                                 # Notebook de EDA y Limpieza (note.ipynb)
├── app.py                                             # Código de la aplicación interactiva
├── requirements.txt                                    # Dependencias del proyecto
└── README.md                                          # Documentación del proyecto
```

---

##  Fase 1: Carga, limpieza y procesamiento de datos (`notebooks/practice.ipynb`) <img src="https://cdn-icons-png.flaticon.com/512/5143/5143301.png" width="30"> 

En esta etapa realizada en el cuaderno de notas se aplicaron las siguientes transformaciones con **Pandas** y **NumPy**:

* **Depuración de duplicados:** Se eliminaron 300 registros idénticos.
* **Tratamiento de nulos:**
  * `Gasto_Promedio_Diario_Huesped_USD` y `Puntuacion_Satisfaccion`: Se imputaron utilizando la **mediana**.
  * `Guest_Country`: Se completaron las celdas vacías con la categoría `'UNKNOWN'`.
* **Estandarización de variables:**
  * Formateo de texto en países (mayúsculas y limpieza de espacios, ej. `'ESPAÑA'` a `'SPAIN'`).
  * Corrección de valores inconsistentes/negativos en `Lead_Time_Dias`.
  * Conversión de `Fecha_Viaje` y `Fecha_Reserva` a formato `datetime`.
* **Tratamiento de outliers extremos:**
  * Se identificaron valores atípicos severos en `Ingreso_Total_Reserva_USD` y se aplicó un tope técnico (*Winsorization*) al **percentil 99** para preservar la estabilidad de los análisis.
* **Exportación de datos:** Se guardó el DataFrame resultante en `data/processed/cruceros_procesados.csv` con **77,040 registros de alta calidad**.

---

## Fase 2: aplicación web interactiva (`app.py`) <img src="https://cdn-icons-png.magnific.com/256/1875/1875702.png?semt=ais_white_label" width="30"> 

La aplicación construida en **Streamlit** permite la exploración interactiva mediante los siguientes componentes:

###  Filtros interactivos 
* **Slider de rango:** Filtrado dinámico por días de anticipación de reserva (`Lead_Time_Dias`).
* **Rango de fechas (`st.date_input`):** Filtro por fechas de salida de los cruceros (`Fecha_Viaje`).
* **Multiselect categórico:** Selección de rutas específicas (`Tipo_Ruta`).

###  Indicadores clave (KPIs) y tablas estadísticas
* Tarjetas métricas en tiempo real: *Total de Reservas*, *Ingreso Promedio*, *Satisfacción Media* y *Pasajeros Totales*.
* **Resumen estadístico descriptivo:** Cuadro interactivo desplegable que calcula la Media, Mediana, Rango (Máx - Min), Desviación Estándar y Cuartiles (Q1, Q3) sobre el subconjunto de datos filtrados.

###  Visualizaciones dinámicas 
1. **Distribución del ingreso total (USD):** Histograma interactivo con diagrama de caja (*Boxplot*) en el margen.
2. **Modelo de regresión ajustado:** Gráfico de dispersión (*Scatter plot*) de Noches de Estancia vs. Ingreso Total, con línea de tendencia OLS por tipo de suite.
3. **Tendencia temporal:** Gráfico de líneas con la evolución mensual de la facturación.
4. **Distribución geográfica:** Mapa de coropletas (*Choropleth Map*) interactivo por país de residencia.

---

##  Instalación y ejecución local <img src="https://png.pngtree.com/png-vector/20220724/ourmid/pngtree-download-icon-data-install-icon-vector-png-image_38121638.png" width="30"> 

Para ejecutar el proyecto en tu máquina local:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/NicolasPerez1495/Diploma-DS_GRUPO_C.git
   cd Diploma-DS_GRUPO_C
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lanzar la aplicación:**
   ```bash
   streamlit run app.py
   ```

---

##  Despliegue en la nube ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) 

La aplicación se encuentra desplegada y disponible para su uso en la plataforma **Streamlit**:

 **[Acceder al dashboard](https://crucerosapp.streamlit.app/)** 

---

##  Tecnologías Utilizadas ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

* **Lenguaje:** Python 3.10+
* **Manipulación de datos:** Pandas, NumPy
* **Visualización:** Plotly Express, Matplotlib, Seaborn
* **Modelado estadístico:** Statsmodels
* **Framework web:** Streamlit


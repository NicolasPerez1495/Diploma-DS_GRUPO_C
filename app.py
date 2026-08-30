import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración inicial de la aplicación
st.set_page_config(page_title="Cruise Revenue Analytics", page_icon="🚢", layout="wide")
st.title(" Dashboard Interactivo: Revenue Management de Cruceros")
st.markdown("""Herramienta interactiva enfocada en entender mejor el negocio de los cruceros a 
través del análisis de datos. Permite explorar cómo varían las reservas y los ingresos según la época del año, 
la anticipación con la que compran los clientes y las rutas elegidas.""")

# Carga de datos procesados
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/cruceros_procesados.csv')
    df['Fecha_Viaje'] = pd.to_datetime(df['Fecha_Viaje'])
    df['Fecha_Reserva'] = pd.to_datetime(df['Fecha_Reserva'])
    return df

df = load_data()

# Sidebar de Control y Filtros
st.sidebar.markdown("## Filtros de Navegación")

# 1. Slider de Rango Numérico
min_lead, max_lead = int(df['Lead_Time_Dias'].min()), int(df['Lead_Time_Dias'].max())
rango_lead_time = st.sidebar.slider(
    "Anticipación de Reserva (Días Lead Time):",
    min_value=min_lead, 
    max_value=max_lead,
    value=(min_lead, max_lead)
)

# 2. Selector de Rango de Fechas
min_date, max_date = df['Fecha_Viaje'].min().date(), df['Fecha_Viaje'].max().date()
fecha_inicio, fecha_fin = st.sidebar.date_input(
    "Rango de Fechas de Viaje:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# 3. Multiselect Categórico
rutas_disponibles = list(df['Tipo_Ruta'].unique())
rutas_seleccionadas = st.sidebar.multiselect(
    "Seleccionar Rutas de Crucero:",
    options=rutas_disponibles,
    default=rutas_disponibles
)

# Filtrado dinámico del DataFrame
df_filt = df[
    (df['Lead_Time_Dias'] >= rango_lead_time[0]) & 
    (df['Lead_Time_Dias'] <= rango_lead_time[1]) &
    (df['Fecha_Viaje'].dt.date >= fecha_inicio) &
    (df['Fecha_Viaje'].dt.date <= fecha_fin) &
    (df['Tipo_Ruta'].isin(rutas_seleccionadas))
]

# Indicadores Clave de Desempeño
st.markdown("---")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Total Reservas", value=f"{len(df_filt):,}")
kpi2.metric(label="Ingreso Promedio", value=f"${df_filt['Ingreso_Total_Reserva_USD'].mean():,.2f}" if len(df_filt) > 0 else "$0")
kpi3.metric(label="Satisfacción Media", value=f" {df_filt['Puntuacion_Satisfaccion'].mean():.2f}/5.0" if len(df_filt) > 0 else "0")
kpi4.metric(label="Pasajeros Totales", value=f"{df_filt['Pasajeros_Reserva'].sum():,}")
st.markdown("---")

# Resumen Estadístico
st.markdown("### Resumen Estadístico Descriptivo")
with st.expander("Desplegar métricas detalladas (Media, Mediana, Rango, Cuartiles)"):
    if len(df_filt) > 0:
        cols_analisis = ['Ingreso_Total_Reserva_USD', 'Lead_Time_Dias', 'Noches_Estancia', 'Gasto_Promedio_Diario_Huesped_USD']
        resumen = []
        for col in cols_analisis:
            v_min, v_max = df_filt[col].min(), df_filt[col].max()
            resumen.append({
                'Variable': col,
                'Media': round(df_filt[col].mean(), 2),
                'Mediana': round(df_filt[col].median(), 2),
                'Rango (Max - Min)': f"{round(v_max, 2)} - {round(v_min, 2)} ({round(v_max - v_min, 2)})",
                'Desv. Estándar': round(df_filt[col].std(), 2),
                'Q1 (25%)': round(df_filt[col].quantile(0.25), 2),
                'Q3 (75%)': round(df_filt[col].quantile(0.75), 2)
            })
        st.dataframe(pd.DataFrame(resumen), use_container_width=True)
    else:
        st.warning("No hay registros que coincidan con los filtros seleccionados.")

# Visualizaciones Interactivas Principal
if len(df_filt) > 0:
    col1, col2 = st.columns(2)

    # 1. Histograma de Distribución
    with col1:
        st.markdown("#### Distribución del Ingreso Total USD")
        fig_hist = px.histogram(
            df_filt, x='Ingreso_Total_Reserva_USD', nbins=35,
            color_discrete_sequence=['#2b5c8f'], marginal="box",
            title="Distribución de Ingresos Filtrados"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # 2. Scatter Plot con Línea de Regresión
    with col2:
        st.markdown("#### Regresión: Noches de Estancia vs Ingreso")
        df_sample = df_filt.sample(n=min(2500, len(df_filt)), random_state=42)
        fig_scatter = px.scatter(
            df_sample, x='Noches_Estancia', y='Ingreso_Total_Reserva_USD',
            color='Suite_Type', trendline='ols', opacity=0.7,
            title="Ingreso Total vs. Noches según Tipo de Suite"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)

    # 3. Tendencia Temporal
    with col3:
        st.markdown("#### Tendencia Temporal de Facturación")
        df_temp = df_filt.groupby(df_filt['Fecha_Viaje'].dt.to_period('M'))['Ingreso_Total_Reserva_USD'].sum().reset_index()
        df_temp['Fecha_Viaje'] = df_temp['Fecha_Viaje'].dt.to_timestamp()
        fig_line = px.line(
            df_temp, x='Fecha_Viaje', y='Ingreso_Total_Reserva_USD', markers=True,
            title="Evolución de Ingresos Mensuales", color_discrete_sequence=['#27ae60']
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # 4. Distribución Geográfica en Mapa
    with col4:
        st.markdown("#### Demanda Global por País de Origen")
        df_geo = df_filt['Guest_Country'].value_counts().reset_index()
        df_geo.columns = ['País', 'Reservas']
        fig_map = px.choropleth(
            df_geo, locations="País", locationmode="country names",
            color="Reservas", color_continuous_scale="Viridis",
            title="Distribución Geográfica de Pasajeros"
        )
        st.plotly_chart(fig_map, use_container_width=True)

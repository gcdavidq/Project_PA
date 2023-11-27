import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Configuración de la página
st.set_page_config(
    page_title="Sismos en el Perú",
    page_icon="volcano",
    initial_sidebar_state="expanded",
)

# Título principal
st.title('Análisis de Sismos en el Perú (1960-2022)')


df = pd.read_excel("prueba_project_5000.xlsx")

# Cambiar los nombres de las columnas

# Extraer Año, Mes y Día de la columna Fecha_UTC
df['Año'] = df['FECHA_UTC'].astype(str).str[:4]
df['Mes'] = df['FECHA_UTC'].astype(str).str[4:6]
df['Día'] = df['FECHA_UTC'].astype(str).str[6:]

st.subheader('PROFUNDIDAD DE LOS SISMOS TOMANDO EN CUENTA LOS AÑOS')  # Subtítulo
# Crear slider para seleccionar un rango de años de 'Fecha_UTC'
min_year = df['Año'].astype(int).min()
max_year = df['Año'].astype(int).max()

st.text("SELECCIONE EL RANGO DE AÑOS EN EL QUE DESEA VER LAS TABLAS Y EL GRAFICO DE PROFUNDIDAD")
selected_years = st.slider('Seleccione:',
                          min_value=min_year,
                          max_value=max_year,
                          value=(min_year, max_year),
                          key="select_slider_years")



# Crear un DataFrame con los valores de Profundidad y su frecuencia
conteo_profundidad = df['PROFUNDIDAD'].value_counts()
df_profundidad = pd.DataFrame({'Profundidad': conteo_profundidad.index, 'Frecuencia': conteo_profundidad.values})

# Rangos para Profundidad
rangos_profundidad = pd.cut(df['PROFUNDIDAD'], bins=5)
df['Rango_Profundidad'] = rangos_profundidad.astype(str)

# Actualizar el DataFrame de frecuencia por rango de Profundidad
conteo_rangos_profundidad = pd.cut(df['PROFUNDIDAD'], bins=5).value_counts().sort_index()
df_conteo_rangos_profundidad = pd.DataFrame({'RANGO_PROFUNDIDAD': [str(rango) for rango in conteo_rangos_profundidad.index],
                                            'FRECUENCIA_PROFUNDIDAD': conteo_rangos_profundidad.values})

# Filtrar el DataFrame por el rango seleccionado de años
df_filtrado = df[(df['Año'].astype(int) >= selected_years[0]) & (df['Año'].astype(int) <= selected_years[1])]

# Actualizar el DataFrame de Profundidad y Frecuencia de acuerdo al año seleccionado
conteo_profundidad_filtrado = df_filtrado['PROFUNDIDAD'].value_counts()
df_profundidad_filtrado = pd.DataFrame({'PROFUNDIDAD': conteo_profundidad_filtrado.index, 'Frecuencia': conteo_profundidad_filtrado.values})

# Actualizar el DataFrame de frecuencia por rango de Profundidad de acuerdo al año seleccionado
conteo_rangos_profundidad_filtrado = pd.cut(df_filtrado['PROFUNDIDAD'], bins=5).value_counts().sort_index()
df_conteo_rangos_profundidad_filtrado = pd.DataFrame({'RANGO_PROFUNDIDAD': [str(rango) for rango in conteo_rangos_profundidad_filtrado.index],
                                                      'FRECUENCIA_PROFUNDIDAD': conteo_rangos_profundidad_filtrado.values})

# Mostrar los DataFrames en Streamlit
st.text("TABLA DE FRECUENCIA PARA UN RANGO DE PROFUNDIDAD")
st.dataframe(df_conteo_rangos_profundidad_filtrado) #MOSTRAR EL DATAFRAME DE RANGOS DE PROFUNIDAD RESPECTO A LOS AÑOS SELECCIONADOS
st.text("TABLA DE FRECUENCIA PARA PROFUNIDADES PUNTUALES")
st.dataframe(df_profundidad_filtrado) #MOSTRAR EL DATAFRAME DEL CONTEO DE PROFUNIDAD RESPECTO A LOS AÑOS SELECCIONADOS

# Crear gráfico Plotly Express con el Dataframe de Rangos actualizado
fig = px.bar(df_conteo_rangos_profundidad_filtrado, x='RANGO_PROFUNDIDAD', y='FRECUENCIA_PROFUNDIDAD', color='RANGO_PROFUNDIDAD', labels={'FRECUENCIA_PROFUNDIDAD': 'Frecuencia'})
fig.update_layout(title=f'Frecuencia de Sismos en Rangos de Profundidad ({selected_years[0]} - {selected_years[1]})', xaxis_title='Rango de Profundidad', yaxis_title='Frecuencia')


# Mostrar el gráfico en Streamlit
st.text("GRAFICO DE BARRAS DE LOS RANGOS DE PROFUNIDAD PRESENTES EN LOS SISMOS RESPECTO A LOS AÑOS SELECCIONADOS")
st.plotly_chart(fig)


#----------------------------------------------------------------------------
st.subheader(' MAGNITUD DE LOS SISMOS TOMANDO EN CUENTA LOS AÑOS')
st.text("SELECCIONE EL RANGO DE AÑOS EN EL QUE DESEA VER LAS TABLAS Y EL GRAFICO DE MAGNITUD")
selected_year = st.slider('Seleccione:',
                          min_value=min_year,
                          max_value=max_year,
                          value=(min_year, max_year),
                          key="select_slider_year")



# Crear un DataFrame con los valores de Magnitud y su frecuencia
conteo_magnitud = df['MAGNITUD'].value_counts()
df_magnitud = pd.DataFrame({'MAGNITUD': conteo_magnitud.index, 'Frecuencia': conteo_magnitud.values})

# Rangos para Magnitud
rangos_magnitud= pd.cut(df['MAGNITUD'], bins=5)
df['Rango_Magnitud'] = rangos_magnitud.astype(str)

# Actualizar el DataFrame de frecuencia por rango de Profundidad
conteo_rangos_magnitud = pd.cut(df['MAGNITUD'], bins=5).value_counts().sort_index()
df_conteo_rangos_magnitud = pd.DataFrame({'RANGO_MAGNITUD': [str(rango) for rango in conteo_rangos_magnitud.index],
                                            'FRECUENCIA_MAGNITUD': conteo_rangos_magnitud.values})

# Filtrar el DataFrame por el rango seleccionado de años
df_filtrado_ = df[(df['Año'].astype(int) >= selected_year[0]) & (df['Año'].astype(int) <= selected_year[1])]

# Actualizar el DataFrame de Profundidad y Frecuencia de acuerdo al año seleccionado
conteo_magnitud_filtrado = df_filtrado_['MAGNITUD'].value_counts()
df_magnitud_filtrado = pd.DataFrame({'MAGNITUD': conteo_magnitud_filtrado.index, 'Frecuencia': conteo_magnitud_filtrado.values})

# Actualizar el DataFrame de frecuencia por rango de Profundidad de acuerdo al año seleccionado
conteo_rangos_magnitud_filtrado = pd.cut(df_filtrado_['MAGNITUD'], bins=5).value_counts().sort_index()
df_conteo_rangos_magnitud_filtrado = pd.DataFrame({'RANGO_MAGNITUD': [str(rango) for rango in conteo_rangos_magnitud_filtrado.index],
                                                      'FRECUENCIA_MAGNITUD': conteo_rangos_magnitud_filtrado.values})

# Mostrar los DataFrames en Streamlit
st.text("TABLA DE FRECUENCIA PARA UN RANGO DE MAGNITUD")
st.dataframe(df_conteo_rangos_magnitud_filtrado) #MOSTRAR EL DATAFRAME DE RANGOS DE PROFUNIDAD RESPECTO A LOS AÑOS SELECCIONADOS
st.text("TABLA DE FRECUENCIA PARA PROFUNIDADES MAGNITUD")
st.dataframe(df_magnitud_filtrado) #MOSTRAR EL DATAFRAME DEL CONTEO DE PROFUNIDAD RESPECTO A LOS AÑOS SELECCIONADOS

# Crear gráfico Plotly Express con el Dataframe de Rangos actualizado
fig_ = px.bar(df_conteo_rangos_magnitud_filtrado, x='RANGO_MAGNITUD', y='FRECUENCIA_MAGNITUD', color='RANGO_MAGNITUD', labels={'FRECUENCIA_MAGNITUD': 'Frecuencia'})
fig_.update_layout(title=f'Frecuencia de Sismos en Rangos de Magnitud ({selected_year[0]} - {selected_year[1]})', xaxis_title='Rango de Magnitud', yaxis_title='Frecuencia')


# Mostrar el gráfico en Streamlit
st.text("GRAFICO DE BARRAS DE LOS RANGOS DE MAGNITUD PRESENTES EN LOS SISMOS RESPECTO A LOS AÑOS SELECCIONADOS")
st.plotly_chart(fig_)

#_________________________________________________________________________________________________

# USAR LAS CORDENADAS
st.subheader('MAPA ESTATICO')

# Configurar el mapa centrado en la primera ubicación
mapa = folium.Map(location=[df['LATITUD'].iloc[0], df['LONGITUD'].iloc[0]], zoom_start=10)

# Añadir marcadores al mapa para cada ubicación en el DataFrame
for i, row in df.iterrows():
    folium.Marker([row['LATITUD'], row['LONGITUD']], popup=f"Magnitud: {row['MAGNITUD']}").add_to(mapa)

# Mostrar el mapa en Streamlit
folium_static(mapa)
#------------------------------------------

# Crear el mapa con el sismo de mayor magnitud por año
st.subheader('MAPA CON LA MAYOR MAGNITUD DE CADA AÑO')

# Mapa con el sismo de mayor magnitud por año
df_max_magnitudes = df.loc[df.groupby('Año')['MAGNITUD'].idxmax()]

# Configurar el mapa centrado en la primera ubicación
mapa_max_magnitudes = folium.Map(location=[df_max_magnitudes['LATITUD'].iloc[0], df_max_magnitudes['LONGITUD'].iloc[0]], zoom_start=6)

# Añadir marcadores al mapa para cada sismo con mayor magnitud por año
for i, row in df_max_magnitudes.iterrows():
    folium.Marker([row['LATITUD'], row['LONGITUD']],
                  popup=f"Año: {row['Año']}, Magnitud: {row['MAGNITUD']}",
                  tooltip=f"Sismo en {row['Año']}").add_to(mapa_max_magnitudes)

# Mostrar el mapa en Streamlit
folium_static(mapa_max_magnitudes)


#-----------------------------------------------
# Crear el mapa con el sismo de mayor magnitud por año
st.subheader('MAPA CON LA MAYOR PROFUNIDAD DE CADA AÑO')

# Mapa con el sismo de mayor magnitud por año
df_max_profundidades = df.loc[df.groupby('Año')['PROFUNDIDAD'].idxmax()]

# Configurar el mapa centrado en la primera ubicación
mapa_max_profundidades = folium.Map(location=[df_max_profundidades['LATITUD'].iloc[0], df_max_profundidades['LONGITUD'].iloc[0]], zoom_start=6)

# Añadir marcadores al mapa para cada sismo con mayor magnitud por año
for i, row in df_max_profundidades.iterrows():
    folium.Marker([row['LATITUD'], row['LONGITUD']],
                  popup=f"Año: {row['Año']}, Profundidad: {row['PROFUNDIDAD']} Km.",
                  tooltip=f"Sismo en {row['Año']}").add_to(mapa_max_profundidades)

# Mostrar el mapa en Streamlit
folium_static(mapa_max_profundidades)
#--------------------------------------------

# Mapa con opción de selección
st.subheader('MAPA DE MAGNITUD TOMANDO EN CUENTA LA SELECCION DE LOS AÑOS')

# Crear slider para la magnitud de los sismos
min_value_7_5 = df['MAGNITUD'].min()
max_value_7_5 = df['MAGNITUD'].max()

min_selected_value_7_5, max_selected_value_7_5 = st.slider(
    'Selecciona un rango de valores de Magnitud',
    min_value_7_5, max_value_7_5, (min_value_7_5, max_value_7_5),
    key="slider_7_5"
)

# Crear opciones de selección para año y mes mínimo
min_year_option = st.selectbox('Selecciona el año mínimo', options=list(range(min_year, max_year + 1)))

min_month_option = st.selectbox('Selecciona el mes mínimo', options=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

# Crear opciones de selección para año y mes máximo
max_year_option = st.selectbox('Selecciona el año máximo', options=list(range(min_year, max_year + 1)))

max_month_option = st.selectbox('Selecciona el mes máximo', options=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

# Mapear los nombres de los meses a números
meses_a_numeros = {'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04', 'Mayo': '05', 'Junio': '06', 'Julio': '07', 'Agosto': '08', 'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11', 'Diciembre': '12'}

# Obtener los números de los meses
min_month_option_num = meses_a_numeros[min_month_option]
max_month_option_num = meses_a_numeros[max_month_option]

# Filtrar el DataFrame por los rangos seleccionados
df_filtrado_opcion = df[
    (df['Año'].astype(int) >= min_year_option) & (df['Mes'].astype(int) >= int(min_month_option_num)) &
    (df['Año'].astype(int) <= max_year_option) & (df['Mes'].astype(int) <= int(max_month_option_num)) &
    (df['MAGNITUD'] >= min_selected_value_7_5) & (df['MAGNITUD'] <= max_selected_value_7_5)
]

# Actualizar el mapa con los filtros de opción de selección
if not df_filtrado_opcion.empty:
    mapa_filtrado_opcion = folium.Map(location=[df_filtrado_opcion['LATITUD'].iloc[0], df_filtrado_opcion['LONGITUD'].iloc[0]],
                                      zoom_start=10)

    for i, row in df_filtrado_opcion.iterrows():
        folium.Marker([row['LATITUD'], row['LONGITUD']], popup=f"MAGNITUD: {row['MAGNITUD']}").add_to(mapa_filtrado_opcion)

    # Mostrar el mapa filtrado en Streamlit
    folium_static(mapa_filtrado_opcion)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")

st.subheader("TABLA CON TODOS LOS DATOS QUE SE HAN ANALIZADO")
st.dataframe(df)

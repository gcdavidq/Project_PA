import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from shapely.geometry import Point
from streamlit_folium import folium_static
import plotly.express as px
@st.cache_data
def load_department_boundaries():
    peru_departments = gpd.read_file('departamentos_perú.geojson')
    return peru_departments

@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    data['Año'] = data['FECHA_UTC'].astype(str).str[:4]
    data['Mes'] = data['FECHA_UTC'].astype(str).str[4:6]
    data['Día'] = data['FECHA_UTC'].astype(str).str[6:]
    return data

def assign_departments(data, department_boundaries):
    geometry = [Point(xy) for xy in zip(data['LONGITUD'], data['LATITUD'])]
    geo_df = gpd.GeoDataFrame(data, geometry=geometry, crs='EPSG:4326')
    merged = gpd.sjoin(geo_df, department_boundaries, op='within')
    return merged

def create_map(data):
    if not data.empty:
        st.subheader('Mapa de Puntos y Gráfico de Barras')

        # Asignar colores oscuros a cada departamento
        department_colors = px.colors.qualitative.Dark24[:len(data['DEPARTAMENTOS'].unique())]
        department_color_dict = dict(zip(data['DEPARTAMENTOS'].unique(), department_colors))

        # Normalizar la magnitud y la profundidad para el mapa
        data['normalized_magnitude'] = data['MAGNITUD'] / data['MAGNITUD'].max()
        data['normalized_depth'] = data['PROFUNDIDAD'] / data['PROFUNDIDAD'].max()

        # Mapa de puntos
        m = folium.Map(location=[-9.1900, -75.0152], zoom_start=5)
        for index, row in data.iterrows():
            # Calcular el color en función de la magnitud y profundidad
            color = f'rgba(0, 0, 0, {row["normalized_magnitude"] * 0.8})'
            fill_opacity = row['normalized_depth']

            # Asignar color oscuro a cada departamento
            color = department_color_dict[row['DEPARTAMENTOS']]

            # Crear el círculo con información de magnitud y profundidad en el mapa
            folium.CircleMarker(
                location=[row['LATITUD'], row['LONGITUD']],
                radius=10,
                color=color,
                fill=True,
                fill_opacity=fill_opacity,
                tooltip=f'Magnitud: {row["MAGNITUD"]}, Profundidad: {row["PROFUNDIDAD"]}'
            ).add_to(m)

        folium_static(m)

        # Gráfico de barras
        st.subheader('Cantidad de Sismos por DEPARTAMENTOS')
        fig = px.bar(data, x='DEPARTAMENTOS', color='DEPARTAMENTOS', title='Cantidad de Sismos por Departamento',
                     labels={'DEPARTAMENTOS': 'Departamento', 'count': 'Cantidad'},
                     color_discrete_map=department_color_dict)

        dtick_value = max(1, int(len(data) / 10))
        fig.update_layout(xaxis_title='Departamento', yaxis_title='Cantidad de Sismos', yaxis=dict(dtick=dtick_value))
        st.plotly_chart(fig)
def show_departments_count(data):
    st.subheader('Mapa Sísmico del Perú periodo 1960-2022 (IGP) ')

    data = data.rename(columns={'NOMBDEP': 'DEPARTAMENTOS'})
    options = ['DEPARTAMENTOS']

    selected_column = st.selectbox('Selecciona una columna:', options)
    all_values_option = 'Todos'
    unique_values = data[selected_column].unique()

    # Establecer el primer departamento como seleccionado por defecto
    default_values = [unique_values[0]] if len(unique_values) > 0 else [all_values_option]

    selected_values = st.multiselect(f'Selecciona el (los) DEPARTAMENTO(OS):',
                                     options=[all_values_option] + list(unique_values),
                                     default=default_values)

    select_all = all_values_option in selected_values
    if select_all:
        st.write(f'Se muestran todos los sismos de todos los departamentos.')
        print("Data (Todos):", data)
        create_map(data)
    elif not selected_values:
        st.warning("No se han seleccionado departamentos. ")
        ##Creamos un mapa vació con enfoque a Perú.
        peru_center_coords = [-9.1900, -75.0152]
        peru_map = folium.Map(location=peru_center_coords, zoom_start=4.8)
        st.components.v1.html(peru_map._repr_html_(), width=800, height=600, scrolling=True)
    else:
        # Hay departamentos seleccionados
        filtered_data = data[data[selected_column].isin(selected_values)]
        print("Filtered Data:", filtered_data)

        min_year = filtered_data['Año'].astype(int).min()
        max_year = filtered_data['Año'].astype(int).max()

        st.markdown("**SELECCIONE EL RANGO DE AÑOS EN EL QUE DESEA VER LAS TABLAS "
                    "Y EL GRÁFICO DE PROFUNDIDAD**")
        selected_years = st.slider('Seleccione:',
                                   min_value=min_year,
                                   max_value=max_year,
                                   value=(min_year, max_year),
                                   key="select_slider_years")

        # Aplicar el filtro de año
        filtered_data = filtered_data[(filtered_data['Año'].astype(int) >= selected_years[0]) &
                                      (filtered_data['Año'].astype(int) <= selected_years[1])]

        if len(selected_values) > 0:
            department_count = filtered_data.shape[0]
            ## Mostrar mensajes de acuerdo a los departamentos seleccionados
            if len(selected_values) == 1:
                st.write(f'En el departamento de {selected_values[0]} hay {department_count} punto{"s" if department_count > 1 else ""} para los años {selected_years[0]} - {selected_years[1]}.')
            else:
                st.write(f'En los departamentos seleccionados hay {department_count} puntos para los años {selected_years[0]} - {selected_years[1]}.')

            create_map(filtered_data)

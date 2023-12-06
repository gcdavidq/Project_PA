import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import folium_static

def cargar_datos(ruta_archivo):
    df = pd.read_excel(ruta_archivo)
    return df

def extraer_columnas_fecha(df):
    df['Año'] = df['FECHA_UTC'].astype(str).str[:4]
    df['Mes'] = df['FECHA_UTC'].astype(str).str[4:6]
    df['Día'] = df['FECHA_UTC'].astype(str).str[6:]

def crear_slider_ano(df):
    min_year = df['Año'].astype(int).min()
    max_year = df['Año'].astype(int).max()
    selected_year = st.slider('Seleccione:',
                              min_value=min_year,
                              max_value=max_year,
                              value=(min_year, max_year),
                              key="select_slider_year")
    return selected_year

def actualizar_dataframe_rangos_magnitud(df, selected_year):
    rangos_magnitud = pd.cut(df['MAGNITUD'], bins=5)
    df['Rango_Magnitud'] = rangos_magnitud.astype(str)
    df_filtrado = df[(df['Año'].astype(int) >= selected_year[0]) & (df['Año'].astype(int) <= selected_year[1])]
    conteo_rangos_magnitud = pd.cut(df['MAGNITUD'], bins=5).value_counts().sort_index()
    df_conteo_rangos_magnitud = pd.DataFrame({'RANGO_MAGNITUD': [str(rango) for rango in conteo_rangos_magnitud.index],
                                              'FRECUENCIA_MAGNITUD': conteo_rangos_magnitud.values})
    conteo_rangos_magnitud_filtrado = pd.cut(df_filtrado['MAGNITUD'], bins=5).value_counts().sort_index()
    df_conteo_rangos_magnitud_filtrado = pd.DataFrame({'RANGO_MAGNITUD': [str(rango) for rango in conteo_rangos_magnitud_filtrado.index],
                                                        'FRECUENCIA_MAGNITUD': conteo_rangos_magnitud_filtrado.values})
    return df_filtrado, df_conteo_rangos_magnitud_filtrado

def crear_grafico_barras(df_conteo_rangos_magnitud_filtrado, selected_year):
    fig_ = px.bar(df_conteo_rangos_magnitud_filtrado, x='RANGO_MAGNITUD', y='FRECUENCIA_MAGNITUD', color='RANGO_MAGNITUD', labels={'FRECUENCIA_MAGNITUD': 'Frecuencia'})
    fig_.update_layout(title=f'Frecuencia de Sismos en Rangos de Magnitud ({selected_year[0]} - {selected_year[1]})', xaxis_title='Rango de Magnitud', yaxis_title='Frecuencia')
    return fig_

def crear_grafico_lineas(df_frecuencia_rangos_magnitudes_filtrado):
    fig_lineas_rangos_magnitudes = px.line(df_frecuencia_rangos_magnitudes_filtrado, x='Rango_Magnitud', y='FRECUENCIA', color='Año',
                                           title='Frecuencia de Rangos de Magnitudes a lo largo de los Años')
    fig_lineas_rangos_magnitudes.update_layout(xaxis_title='Rango de Magnitud', yaxis_title='Frecuencia', legend_title='Año')
    return fig_lineas_rangos_magnitudes

def seleccionar_tipo_grafico():
    tipo_grafico = st.radio("Seleccione el tipo de gráfico:", ["Gráfico de Barras", "Gráfico de Líneas"])
    return tipo_grafico

def mostrar_grafico(fig, tipo_grafico):
    if tipo_grafico == "Gráfico de Barras":
        st.text("GRAFICO DE BARRAS DE LOS RANGOS DE MAGNITUD PRESENTES EN LOS SISMOS RESPECTO A LOS AÑOS SELECCIONADOS")
        st.plotly_chart(fig)
    elif tipo_grafico == "Gráfico de Líneas":
        st.text("GRÁFICO DE LÍNEAS: Frecuencia de Rangos de Magnitudes a lo largo de los Años")
        st.plotly_chart(fig)

def crear_mapa(df_filtrado_opcion):
    mapa_filtrado_opcion = folium.Map(location=[0, 0], zoom_start=2)  # Definir un mapa vacío con ubicación de respaldo

    if not df_filtrado_opcion.empty:
        mapa_filtrado_opcion = folium.Map(location=[df_filtrado_opcion['LATITUD'].iloc[0], df_filtrado_opcion['LONGITUD'].iloc[0]],
                                          zoom_start=10, control_scale=True, prefer_canvas=True)
        for i, row in df_filtrado_opcion.iterrows():
            folium.Marker([row['LATITUD'], row['LONGITUD']],
                          popup=f"MAGNITUD: {row['MAGNITUD']}",
                          icon=folium.Icon(color='blue', icon='info-sign')).add_to(mapa_filtrado_opcion)
        folium.TileLayer('Stamen Watercolor').add_to(mapa_filtrado_opcion)

    return mapa_filtrado_opcion

def mostrar_mapa(mapa_filtrado_opcion):
    if mapa_filtrado_opcion.location != [0, 0]:  # Verificar si no es el mapa vacío
        folium_static(mapa_filtrado_opcion)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")

def descargar_archivos(df_conteo_rangos_magnitud_filtrado, fig_, fig_lineas_rangos_magnitudes, mapa_filtrado_opcion):
    dataframe_download_button = st.download_button(
        label="Descargar Dataframe Seleccionado",
        data=df_conteo_rangos_magnitud_filtrado.to_html(),
        file_name="data_frame.html",
        key="download_frame_chart"
    )

    bar_chart_download_button = st.download_button(
        label="Descargar Gráfico de Barras",
        data=fig_.to_html(),
        file_name="grafico_barras.html",
        key="download_bar_chart"
    )

    line_chart_download_button = st.download_button(
        label="Descargar Gráfico de Líneas",
        data=fig_lineas_rangos_magnitudes.to_html(),
        file_name="grafico_lineas.html",
        key="download_line_chart"
    )

    map_download_button = st.download_button(
        label="Descargar Mapa",
        data=mapa_filtrado_opcion._repr_html_(),
        file_name="mapa.html",
        key="download_map"
    )

def main():
    ruta_archivo = "prueba_project_5000.xlsx"
    df = cargar_datos(ruta_archivo)
    extraer_columnas_fecha(df)

    st.subheader('MAGNITUD DE LOS SISMOS TOMANDO EN CUENTA LOS AÑOS')
    st.text("SELECCIONE EL RANGO DE AÑOS EN EL QUE DESEA VER LAS TABLAS Y EL GRAFICO DE MAGNITUD")

    selected_year = crear_slider_ano(df)

    df_filtrado, df_conteo_rangos_magnitud_filtrado = actualizar_dataframe_rangos_magnitud(df, selected_year)


    fig_ = crear_grafico_barras(df_conteo_rangos_magnitud_filtrado, selected_year)

    df_frecuencia_rangos_magnitudes_filtrado = df.groupby(['Año', pd.cut(df['MAGNITUD'], bins=10)]).size().reset_index(name='FRECUENCIA')
    df_frecuencia_rangos_magnitudes_filtrado['Rango_Magnitud'] = df_frecuencia_rangos_magnitudes_filtrado['MAGNITUD'].astype(str)
    df_frecuencia_rangos_magnitudes_filtrado['Rango_Magnitud'] = df_frecuencia_rangos_magnitudes_filtrado['Rango_Magnitud'].str.replace('(', '[')
    df_frecuencia_rangos_magnitudes_filtrado = df_frecuencia_rangos_magnitudes_filtrado[
        (df_frecuencia_rangos_magnitudes_filtrado['Año'].astype(int) >= selected_year[0]) &
        (df_frecuencia_rangos_magnitudes_filtrado['Año'].astype(int) <= selected_year[1])
    ]

    fig_lineas_rangos_magnitudes = crear_grafico_lineas(df_frecuencia_rangos_magnitudes_filtrado)

    tipo_grafico = seleccionar_tipo_grafico()

    if tipo_grafico == "Gráfico de Barras":
        fig = crear_grafico_barras(df_conteo_rangos_magnitud_filtrado, selected_year)
    elif tipo_grafico == "Gráfico de Líneas":
        df_frecuencia_rangos_magnitudes_filtrado = df.groupby(['Año', pd.cut(df['MAGNITUD'], bins=10)]).size().reset_index(name='FRECUENCIA')
        df_frecuencia_rangos_magnitudes_filtrado['Rango_Magnitud'] = df_frecuencia_rangos_magnitudes_filtrado['MAGNITUD'].astype(str)
        df_frecuencia_rangos_magnitudes_filtrado['Rango_Magnitud'] = df_frecuencia_rangos_magnitudes_filtrado['Rango_Magnitud'].str.replace('(', '[')
        df_frecuencia_rangos_magnitudes_filtrado = df_frecuencia_rangos_magnitudes_filtrado[
            (df_frecuencia_rangos_magnitudes_filtrado['Año'].astype(int) >= selected_year[0]) &
            (df_frecuencia_rangos_magnitudes_filtrado['Año'].astype(int) <= selected_year[1])
        ]

        fig = crear_grafico_lineas(df_frecuencia_rangos_magnitudes_filtrado)

    mostrar_grafico(fig, tipo_grafico)

    st.subheader('MAPA DE MAGNITUD TOMANDO EN CUENTA LA SELECCION DE LOS AÑOS')

    min_value_7_5 = df['MAGNITUD'].min()
    max_value_7_5 = df['MAGNITUD'].max()

    min_selected_value_7_5, max_selected_value_7_5 = st.slider(
        'Selecciona un rango de valores de Magnitud',
        min_value_7_5, max_value_7_5, (min_value_7_5, max_value_7_5),
        key="slider_7_5"
    )

    min_year_option = st.selectbox('Selecciona el año mínimo', options=list(range(selected_year[0], selected_year[1] + 1)))
    min_month_option = st.selectbox('Selecciona el mes mínimo',
                                    options=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto',
                                             'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

    max_year_option = st.selectbox('Selecciona el año máximo', options=list(range(selected_year[0], selected_year[1] + 1)))
    max_month_option = st.selectbox('Selecciona el mes máximo',
                                    options=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto',
                                             'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

    meses_a_numeros = {'Enero': '01', 'Febrero': '02', 'Marzo': '03', 'Abril': '04', 'Mayo': '05', 'Junio': '06',
                       'Julio': '07', 'Agosto': '08', 'Septiembre': '09', 'Octubre': '10', 'Noviembre': '11',
                       'Diciembre': '12'}

    min_month_option_num = meses_a_numeros[min_month_option]
    max_month_option_num = meses_a_numeros[max_month_option]

    df_filtrado_opcion = df[
        (df['Año'].astype(int) >= min_year_option) & (df['Mes'].astype(int) >= int(min_month_option_num)) &
        (df['Año'].astype(int) <= max_year_option) & (df['Mes'].astype(int) <= int(max_month_option_num)) &
        (df['MAGNITUD'] >= min_selected_value_7_5) & (df['MAGNITUD'] <= max_selected_value_7_5)
    ]

    mapa_filtrado_opcion = folium.Map(location=[0, 0], zoom_start=2)  # Valor predeterminado para el caso sin datos

    if not df_filtrado_opcion.empty:
        mapa_filtrado_opcion = crear_mapa(df_filtrado_opcion)
        mostrar_mapa(mapa_filtrado_opcion)
    else:
        st.warning("No hay datos disponibles para los filtros seleccionados.")

    descargar_archivos(df_conteo_rangos_magnitud_filtrado, fig_, fig_lineas_rangos_magnitudes, mapa_filtrado_opcion)


if __name__ == "__main__":
    main()
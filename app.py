import streamlit as st
from PIL import Image
from analisis_nacional import visualizacion_a_nivel_nacional
from analisis_departamental import load_department_boundaries, load_data, assign_departments, show_departments_count
st.set_page_config(
    page_title="Sismos en el Perú",
    page_icon="volcano",
    initial_sidebar_state="expanded",
)
page_bg_video = """
    <style>
    body {
        margin: 0;
        overflow: hidden;
    }

    iframe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
    </style>

    <iframe src="https://assets.pinterest.com/ext/embed.html?id=710513278733252311" height="354" width="450" frameborder="0" scrolling="no" ></iframe>
"""

st.markdown(page_bg_video, unsafe_allow_html=True)

image1 = Image.open('image.jpg')

# Añadimos un panel de control
tab1, tab2, tab3 = st.tabs([  "Inicio", "Análisis a nivel nacional", "Anális a nivel departamental"])

with tab1:
    st.image(image1)

# Análisis a nivel nacional
with tab2:
    visualizacion_a_nivel_nacional("Catalogo1960_2022.csv")


# Análisis a nivel departamental
with tab3:
    st.header("Análisis Departamental")
    department_boundaries = load_department_boundaries()
    file_path = 'Proyecto_final.csv'
    data = load_data(file_path)
    merged_data = assign_departments(data, department_boundaries)
    show_departments_count(merged_data)

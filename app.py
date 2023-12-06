import streamlit as st
from PIL import Image
from analisis_nacional import visualizacion_a_nivel_nacional
from analisis_departamental import load_department_boundaries, load_data, assign_departments, show_departments_count
st.set_page_config(
    page_title="Sismos en el Perú",
    page_icon="volcano",
    initial_sidebar_state="expanded",
)

page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-image: url("https://raw.githubusercontent.com/gcdavidq/Project_PA/main/10.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: local;
    }
    </style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

image1 = Image.open('Img_3.jpeg')

# Añadimos un panel de control
tab1, tab2, tab3 = st.tabs(["_Streamlit_ is :blue[_Inicio_] :sunglasses:", "Análisis a nivel nacional", "Anális a nivel departamental"])

with tab1:
    color = 'blue'
    st.markdown(f'<h3 style="color:{color};">ANÁLISIS SÍSMICO REGISTRADOS EN EL PERÚ (1960_2022)</h3>', unsafe_allow_html=True)
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

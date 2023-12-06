import streamlit as st
from PIL import Image
from analisis_nacional import visualizacion_a_nivel_nacional
from analisis_departamental import load_department_boundaries, load_data, assign_departments, show_departments_count
st.set_page_config(
    page_title="Sismos en el Perú",
    page_icon="volcano",
    initial_sidebar_state="expanded",
)
page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://raw.githubusercontent.com/gcdavidq/Project_PA/main/Imagen_fondo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: local;
    }}
    </style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

image1 = Image.open('image1.png')

######################
# Establecer el estilo de fuente y colores
estilo_fuente = "Cooper Black"
color_fondo = "#f0f0f0"  # Puedes ajustar este color según tus preferencias
color_texto = "#1f1f1f"  # Puedes ajustar este color según tus preferencias

# Aplicar el estilo a las pestañas directamente
with st.beta_container():
    with st.beta_container():
        st.title("Inicio")
        # Agregar contenido para la pestaña de inicio aquí
        st.image(image1)

with st.beta_container():
    with st.beta_container():
        st.title("Análisis a nivel nacional")
        # Agregar contenido para la pestaña de análisis nacional aquí
        visualizacion_a_nivel_nacional("Catalogo1960_2022.csv")

with st.beta_container():
    with st.beta_container():
        st.title("Análisis a nivel departamental")
        # Agregar contenido para la pestaña de análisis departamental aquí
        st.header("Análisis Departamental")
        department_boundaries = load_department_boundaries()
        file_path = 'Proyecto_final.csv'
        data = load_data(file_path)
        merged_data = assign_departments(data, department_boundaries)
        show_departments_count(merged_data)

# Aplicar el estilo de fuente y colores a todo el contenido
st.markdown(
    f"""
    <style>
        .reportview-container {{
            background-color: {color_fondo};
            color: {color_texto};
            font-family: "{estilo_fuente}", sans-serif;
        }}
        .sidebar .sidebar-content {{
            background-color: {color_fondo};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


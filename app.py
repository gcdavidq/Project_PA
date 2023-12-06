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
        background-image: url("https://raw.githubusercontent.com/gcdavidq/Project_PA/main/8.png");
        background-size: cover;
        background-position: center;
        background-attachment: local;
    }}
    </style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

video_file = st.file_uploader("p1", type=["mp4"])

# Mostrar video si se ha cargado uno
if video_file is not None:
    video_url = f"data:video/{video_file.type};base64,{video_file.read().encode('base64').decode()}"
    st.markdown(f'<video autoplay loop muted playsinline width="100%" height="auto"><source src="{video_url}" type="video/{video_file.type}"></video>', unsafe_allow_html=True)

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

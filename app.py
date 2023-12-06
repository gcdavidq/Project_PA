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

image1 = Image.open('image1.png')

# Añadimos un panel de control
# Crear las pestañas
tab1, tab2, tab3 = st.beta_columns(3)
tabs = [tab1, tab2, tab3]

# Estilos de letra y color personalizados
tab_styles = [
    "font-size: 20px; font-weight: bold; color: #1f78b4;",  # Inicio
    "font-size: 20px; font-weight: bold; color: #33a02c;",  # Análisis a nivel nacional
    "font-size: 20px; font-weight: bold; color: #e31a1c;",  # Análisis a nivel departamental
]

# Aplicar estilos de letra y color a las pestañas
for i, tab in enumerate(tabs):
    tab.markdown(f"<h1 style='{tab_styles[i]}'>{['Inicio', 'Análisis a nivel nacional', 'Análisis a nivel departamental'][i]}</h1>", unsafe_allow_html=True)

#####
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


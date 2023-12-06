import streamlit as st
from PIL import Image
from analisis_nacional import visualizacion_a_nivel_nacional
from analisis_departamental import load_department_boundaries, load_data, assign_departments, show_departments_count
st.set_page_config(
    page_title="Sismos en el Perú",
    page_icon="volcano",
    initial_sidebar_state="expanded",
)
video_file = st.file_uploader("Cargar video", type=["mp4"])

if video_file is not None:
    # Crea un identificador único para el elemento video
    video_id = st.markdown(f'<div id="stVideoPlayer"></div>', unsafe_allow_html=True)

    # Obtén la ruta del video cargado
    video_path = video_file.name

    # Muestra el video
    st.video(video_file)

    # Agrega el estilo CSS necesario para el fondo de video
    st.markdown(
        f"""
        <style>
        body {{
            margin: 0;
            overflow: hidden;
        }}
        
        #stVideoPlayer {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }}
        </style>
        <script>
        const videoPlayer = document.getElementById('stVideoPlayer');
        videoPlayer.innerHTML = '<video autoplay loop muted playsinline><source src="/files/{video_path}" type="video/mp4">Tu navegador no soporta el elemento de video.</video>';
        </script>
        """,
        unsafe_allow_html=True
    )

image1 = Image.open('Img_3.jpeg')

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

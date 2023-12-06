import streamlit as st
import cv2
from PIL import Image
from analisis_nacional import visualizacion_a_nivel_nacional
from analisis_departamental import load_department_boundaries, load_data, assign_departments, show_departments_count
st.set_page_config(
    page_title="Sismos en el Perú",
    page_icon="volcano",
    initial_sidebar_state="expanded",
)

# Cargar el video
cap = cv2.VideoCapture('p1.mp4')

# Configurar el codec de salida a H.264
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480))

while(cap.isOpened()):
   ret, frame = cap.read()
   if ret==True:
       out.write(frame)
   else:
       break

# Liberar el video y el escritor
cap.release()
out.release()

# Cargar el video convertido en Streamlit
video_file = open('output.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)


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

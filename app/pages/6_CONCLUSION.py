import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from fpdf import FPDF
import base64

# Configuración de la página
st.set_page_config(
    page_title="Conclusión del Proyecto",
    page_icon="🏅",
    layout="wide"
)

def set_professional_header(image_path):
    """
    Configura un encabezado profesional con una imagen y estilo para toda la aplicación.
    """
    # Verifica si la imagen existe
    try:
        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
        img_base64 = base64.b64encode(img_bytes).decode()
    except FileNotFoundError:
        st.error("No se encontró la imagen. Asegúrate de que la ruta sea correcta.")
        return

    # Crear encabezado con imagen y título
    st.markdown(
        f"""
        <div style="
            background-color: #F2F3F4;
            padding: 15px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
            <img src="data:image/png;base64,{img_base64}" style="width: 120px; height: auto; margin-right: 20px;">
            <div>
                <h1 style="color: #2C3E50; margin: 0; font-size: 28px;">Análisis Olímpico: Tendencias y Predicciones</h1>
                <p style="color: #566573; margin: 0; font-size: 16px;">Descubriendo el impacto de los factores globales en los Juegos Olímpicos</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Ruta de la imagen de encabezado
header_image_path = "C:/Users/luna/OneDrive/Escritorio/BOOTCAMP_DATA/PROYECTO_FINAL_JJOO/app/pages/jjoo_background.png"

# Configurar el encabezado profesional
set_professional_header(header_image_path)

# Función para cargar datos
@st.cache_data
def load_data():
    # Cargar el dataset principal
    data = pd.read_csv(r"C:\Users\luna\OneDrive\Escritorio\BOOTCAMP_DATA\PROYECTO_FINAL_JJOO\app\pages\final_dataset_cleaned.csv")
    return data

# Función para crear gráficos
def plot_top_countries(data):
    st.subheader("🎖️ Top 10 Países con Más Medallas")
    country_medals = data.groupby('NOC')['Medal'].count().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    country_medals.plot(kind='bar', ax=ax, color='gold')
    ax.set_title("Top 10 Países con Más Medallas")
    ax.set_ylabel("Número de Medallas")
    st.pyplot(fig)

def plot_medals_over_time(data):
    st.subheader("📊 Evolución del Número de Medallas a lo Largo del Tiempo")
    medals_by_year = data.groupby('Year')['Medal'].count()
    fig, ax = plt.subplots()
    medals_by_year.plot(ax=ax, color='skyblue', marker='o')
    ax.set_title("Evolución de las Medallas")
    ax.set_xlabel("Año")
    ax.set_ylabel("Número de Medallas")
    st.pyplot(fig)

# Carga del dataset
data = load_data()

# Título principal
st.title("🏆 Conclusiones y Recomendaciones")

# Resumen de hallazgos clave
st.markdown("""
### Resumen de Hallazgos
- Los países con mayor PIB y población tienden a tener mejores resultados en los JJOO.
- Las anomalías climáticas pueden afectar la participación en deportes al aire libre.
- El análisis histórico muestra fluctuaciones cíclicas en el rendimiento por región y deporte.

### Implicaciones
- Invertir en programas deportivos y sostenibilidad puede maximizar el éxito olímpico.
- Comprender las tendencias históricas permite planificar con anticipación.

### Líneas Futuras
- Ampliar el análisis para incluir deportes específicos y datos de género.
- Incorporar factores culturales y políticas deportivas nacionales.
""")

# Visualizaciones
col1, col2 = st.columns(2)

with col1:
    plot_top_countries(data)

with col2:
    plot_medals_over_time(data)

# Resumen de predicciones
st.markdown("## 🔮 Resumen de Predicciones")
st.markdown("""
- **Modelo ARIMA**: Predicciones cíclicas para el total de medallas en los próximos JJOO.
- **Modelo XGBoost**: Estimaciones precisas de participación utilizando datos macroeconómicos y climáticos.
""")

# Descarga de archivo PDF
st.markdown("### 📥 Descarga del Resumen en PDF")
st.markdown("""
Puedes descargar un resumen profesional en formato PDF con todos los hallazgos y predicciones.
""")

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen del Proyecto JJOO", ln=True, align='C')
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="""
    Resumen de Hallazgos:
    - Los países con mayor PIB y población tienden a tener mejores resultados en los JJOO.
    - Las anomalías climáticas pueden afectar la participación en deportes al aire libre.
    - El análisis histórico muestra fluctuaciones cíclicas en el rendimiento por región y deporte.

    Implicaciones:
    - Invertir en programas deportivos y sostenibilidad puede maximizar el éxito olímpico.
    - Comprender las tendencias históricas permite planificar con anticipación.

    Líneas Futuras:
    - Ampliar el análisis para incluir deportes específicos y datos de género.
    - Incorporar factores culturales y políticas deportivas nacionales.

    Resumen de Predicciones:
    - Modelo ARIMA: Predicciones cíclicas para el total de medallas en los próximos JJOO.
    - Modelo XGBoost: Estimaciones precisas de participación utilizando datos macroeconómicos y climáticos.
    """)
    pdf.output("Resumen_Proyecto_JJOO.pdf")

if st.button("Generar y Descargar PDF"):
    generate_pdf()
    pdf_path = "Resumen_Proyecto_JJOO.pdf"
    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Descargar PDF",
            data=pdf_file,
            file_name=pdf_path,
            mime="application/pdf"
        )

# Nota final
st.info("Gracias por explorar este proyecto. Esperamos que los hallazgos sean útiles para futuros análisis deportivos y estratégicos.")

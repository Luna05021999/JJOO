import streamlit as st
import base64

st.set_page_config(page_title="Análisis Olímpico", page_icon="🏅", layout="wide", initial_sidebar_state="expanded")

# Nueva función para configurar el encabezado profesional
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

# Función para la portada
def portada():
    set_professional_header(header_image_path)
    st.markdown("<h1 style='text-align: center; font-size: 60px; color: #2E4053;'>🔎 <b>Análisis Olímpico Global</b> 🌍</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #566573;'>Analizando tendencias y predicciones de los Juegos Olímpicos</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: #1C2833;'>
    🏅 <b>Por Luna Outerelo, analista deportiva.</b><br>
    📊 <b>Propósito:</b> Entender el impacto de factores económicos, climáticos y sociales en el rendimiento olímpico.<br>
    📈 <b>Resultado esperado:</b> Proporcionar insights y predicciones para la optimización de estrategias futuras.
    </div>
    """, unsafe_allow_html=True)
    # Sección destacada con mejor alineación y estilo
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 20px;">
        <div style="display: flex; justify-content: center; gap: 60px;">
            <div style="text-align: center;">
                <p style="color: #2E4053; font-size: 16px; margin-top: 10px;"><b>Historia Olímpica</b><br>Explora tendencias desde 1896</p>
            </div>
            <div style="text-align: center;">
                <p style="color: #2E4053; font-size: 16px; margin-top: 10px;"><b>Análisis Profundo</b><br>Descubre predicciones y patrones</p>
            </div>
            <div style="text-align: center;">
                <p style="color: #2E4053; font-size: 16px; margin-top: 10px;"><b>Impacto Global</b><br>Analiza datos de todo el mundo</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Línea divisoria decorativa
    st.markdown("<hr style='border: 2px solid #ABB2B9; margin-top: 30px;'>", unsafe_allow_html=True)

    # Texto centrado después de la imagen
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #1C2833;'>¿Listo para comenzar el análisis? 🚀</h3>", unsafe_allow_html=True)

def eda():
    set_professional_header(header_image_path)
    st.title("Exploración de Datos (EDA)")
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)

# Función para la sección CDA
def cda():
    set_professional_header(header_image_path)
    st.title("Análisis Confirmatorio de Datos (CDA)")
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)

# Función para la sección de Análisis Predictivo
def analisis_predictivo():
    set_professional_header(header_image_path)
    st.title("Análisis Predictivo")
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)

# Función para la sección de Series Temporales
def series_temporales():
    set_professional_header(header_image_path)
    st.title("Series Temporales")
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)

# Función para la conclusión
def conclusion():
    set_professional_header(header_image_path)
    st.title("Conclusión")
    st.markdown("### Resumen y hallazgos finales.")
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)

if __name__ == "__main__":
    portada()

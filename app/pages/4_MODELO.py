import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import base64

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

def page_analisis_predictivo():
    # Configurar el encabezado profesional
    set_professional_header(header_image_path)

    # Título de la sección
    st.title("Análisis Predictivo")
    st.markdown("""
    ### Explorando la participación futura en los Juegos Olímpicos
    En esta sección, mostramos cómo nuestro modelo predictivo permite prever la **participación** futura en los Juegos Olímpicos:
    - Proporciona predicciones basadas en factores clave como el **PIB**, la **población** y las **anomalías climáticas**.
    - Optimizado para analizar patrones de participación global en eventos olímpicos.
    """)
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)

    # Esquema del despliegue del modelo (mantenemos el diagrama)
    st.markdown("#### Esquema del Modelo Predictivo")
    st.image(
        "c:/Users/luna/OneDrive/Escritorio/BOOTCAMP_DATA/PROYECTO_FINAL_JJOO/app/pages/Modelo_XGBoost.png",
        caption="Flujo del modelo implementado",
        use_column_width=False,
        width=600
    )

    # Simulación interactiva
    st.subheader("Simulación interactiva: Ajusta los parámetros")
    
    # Ajustar PIB en miles de millones
    pib_input = st.slider("PIB Promedio (en miles de millones USD)", 1, 2000, step=50)  # Más amigable
    pib_scaled = pib_input * 1e9  # Escalar para el modelo

    # Ajustar Población en millones
    poblacion_input = st.slider("Población (en millones)", 1, 1000, step=10)  # Más amigable
    poblacion_scaled = poblacion_input * 1e6  # Escalar para el modelo

    # Ajustar anomalías climáticas
    anomaly_input = st.slider("Anomalías climáticas (°C)", -1.0, 2.0, step=0.1)

    # Botón para realizar la predicción
    if st.button("Realizar Predicción"):
        try:
            # Cargar el modelo y el escalador desde los archivos
            with open(r"C:\Users\luna\OneDrive\Escritorio\BOOTCAMP_DATA\PROYECTO_FINAL_JJOO\app\pages\nuevo_scaler.pkl", "rb") as f:
                scaler = pickle.load(f)
            with open(r"C:\Users\luna\OneDrive\Escritorio\BOOTCAMP_DATA\PROYECTO_FINAL_JJOO\app\pages\xgboost_model.pkl", "rb") as f:
                model = pickle.load(f)

            # Crear un DataFrame con las características necesarias para el escalador
            input_data = pd.DataFrame({
                "GDP": [pib_scaled],
                "Population": [poblacion_scaled],
                "Annual Anomaly": [anomaly_input],
                "Monthly Anomaly": [0.1],  # Valor por defecto
                "Participation_Per_Million": [0.5]  # Valor por defecto
            })

            # Escalar los datos
            scaled_data = scaler.transform(input_data)

            # Realizar la predicción
            prediction = model.predict(scaled_data)[0]

            # Mostrar la predicción
            st.success(f"Basado en los parámetros proporcionados, el modelo predice una participación estimada de {prediction / 1_000_000:,.2f} millones de personas.")

            # Visualización adicional
            st.markdown("#### Predicción visualizada")
            data = {
                "Factor": ["PIB (en miles de millones)", "Población (en millones)", "Anomalías"],
                "Valor": [pib_input, poblacion_input, anomaly_input]
            }
            df = pd.DataFrame(data)
            fig = px.bar(df, x="Factor", y="Valor", title="Factores que influyen en la predicción")
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"No se pudo realizar la predicción: {e}")

    # Explicación técnica del modelo
    st.markdown("""
    #### Descripción técnica del modelo
    - **Modelo seleccionado:** XGBoost, optimizado por su precisión y capacidad para manejar datos tabulares complejos.
    - **Variables clave:** PIB promedio, población y anomalías climáticas.
    - **Implementación:** Local utilizando el modelo previamente entrenado.
    """)

# Para probar la página directamente
if __name__ == "__main__":
    page_analisis_predictivo()

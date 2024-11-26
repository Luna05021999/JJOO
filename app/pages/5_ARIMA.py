import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import base64
import plotly.express as px

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

def page_arima_predictivo():
    # Ruta de la imagen de encabezado
    header_image_path = "C:/Users/luna/OneDrive/Escritorio/BOOTCAMP_DATA/PROYECTO_FINAL_JJOO/app/pages/jjoo_background.png"
    
    # Configurar el encabezado profesional
    set_professional_header(header_image_path)
    
    st.title("Predicción Interactiva con ARIMA")
    st.markdown("""
    ### Modelo ARIMA interactivo
    Explora cómo diferentes filtros afectan la predicción del número de medallas en los próximos Juegos Olímpicos.
    """)
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)

    # Cargar el dataset
    df = pd.read_csv(r'C:\Users\luna\OneDrive\Escritorio\BOOTCAMP_DATA\PROYECTO_FINAL_JJOO\app\pages\final_dataset_cleaned.csv')  # Asegúrate de que este archivo esté en la ruta correcta

    # Filtros interactivos
    st.sidebar.subheader("Filtros")
    years = st.sidebar.slider("Rango de años", int(df['Year'].min()), int(df['Year'].max()), (1980, 2020))
    medal_type = st.sidebar.selectbox("Tipo de medallas", ["Todas", "Gold", "Silver", "Bronze"])
    region = st.sidebar.multiselect("Región", options=df['Region'].dropna().unique(), default=None)

    # Aplicar filtros
    df_filtered = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]
    if medal_type != "Todas":
        df_filtered = df_filtered[df_filtered['Medal'] == medal_type]
    if region:
        df_filtered = df_filtered[df_filtered['Region'].isin(region)]

    # Agrupar datos por año
    df_series_medals = df_filtered.groupby('Year').size().reset_index(name='Total Medals')

    if df_series_medals.empty:
        st.warning("No hay datos disponibles para los filtros seleccionados. Intenta ajustar los filtros.")
        return

    # Mostrar datos filtrados
    st.markdown("### Evolución histórica de medallas con los filtros aplicados")
    fig = px.line(
        df_series_medals,
        x='Year',
        y='Total Medals',
        title="Evolución histórica del número total de medallas",
        labels={'Year': 'Año', 'Total Medals': 'Número total de medallas'},
        markers=True
    )
    st.plotly_chart(fig)

    # Ajustar el modelo ARIMA
    st.markdown("### Predicciones futuras de medallas")
    try:
        model = ARIMA(df_series_medals['Total Medals'], order=(1, 1, 1))
        model_fit = model.fit()
        
        # Realizar predicción
        steps = st.slider("Número de años a predecir", 1, 10, 5)
        forecast = model_fit.forecast(steps=steps)
        
        # Crear DataFrame para las predicciones
        last_year = df_series_medals['Year'].max()
        forecast_years = [last_year + i for i in range(1, steps + 1)]
        forecast_df = pd.DataFrame({
            "Año": forecast_years,
            "Predicción de Medallas": forecast
        })

        # Mostrar tabla de predicciones
        st.table(forecast_df)

        # Mostrar gráfico de predicciones
        st.markdown("### Visualización de las predicciones")
        fig_forecast = px.line(
            forecast_df,
            x='Año',
            y='Predicción de Medallas',
            title="Predicción del número total de medallas",
            labels={'Año': 'Año', 'Predicción de Medallas': 'Número total de medallas'},
            markers=True
        )
        st.plotly_chart(fig_forecast)
    except Exception as e:
        st.error(f"No se pudo ajustar el modelo ARIMA: {e}")

    # Añadir tabla estática de predicciones
    static_forecast_df = pd.DataFrame({
        "Año": [2028, 2032, 2036, 2040, 2044],
        "Predicción de Medallas": [600, 1900, 640, 1861, 679]  # Valores generados previamente
    })
    st.markdown("### Predicciones estáticas de medallas")
    st.table(static_forecast_df)

# Probar la página directamente
if __name__ == "__main__":
    page_arima_predictivo()
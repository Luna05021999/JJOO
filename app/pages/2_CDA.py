import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import base64
import matplotlib.pyplot as plt

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

def page_cda():
    # Ruta de la imagen de encabezado
    header_image_path = "C:/Users/luna/OneDrive/Escritorio/BOOTCAMP_DATA/PROYECTO_FINAL_JJOO/app/pages/jjoo_background.png"

    # Configurar el encabezado profesional
    set_professional_header(header_image_path)

    st.title("Análisis Confirmatorio de Datos (CDA)")
    st.markdown("### Explorando patrones clave en los datos olímpicos.")
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)

    # Ruta del dataset
    dataset_path = "c:/Users/luna/OneDrive/Escritorio/BOOTCAMP_DATA/PROYECTO_FINAL_JJOO/app/pages/final_dataset_cleaned.csv"
    try:
        # Cargar el dataset
        df = pd.read_csv(dataset_path)

        # Crear pestañas
        tabs = st.tabs([
            "Relación PIB-Medallas",
            "Crecimiento deportivo",
            "Países desarrollados vs en desarrollo",
            "Test de Hipótesis"
        ])

        # Pestaña 1: Relación PIB-Medallas
        with tabs[0]:
            st.subheader("Relación entre PIB promedio y medallas ganadas")
            if "GDP" in df.columns and "Medal" in df.columns:
                df_medals = df[df["Medal"] != "No Medal"]
                df_pib_medals = df_medals.groupby("NOC").agg({"GDP": "mean", "Medal": "count"}).reset_index()

                fig = px.scatter(
                    df_pib_medals,
                    x="GDP",
                    y="Medal",
                    labels={"GDP": "PIB Promedio (USD)", "Medal": "Número de Medallas"},
                    title="Relación entre el PIB Promedio y el Número de Medallas",
                    hover_name="NOC",
                    template="plotly_white",
                    size="Medal",
                    color="Medal",
                    color_continuous_scale="Viridis"
                )
                fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color="DarkSlateGrey")))
                fig.update_layout(
                    title_x=0.5,
                    xaxis=dict(title="PIB Promedio (USD)", tickangle=45, gridcolor="LightGrey"),
                    yaxis=dict(title="Número de Medallas", gridcolor="LightGrey")
                )
                st.plotly_chart(fig)
            else:
                st.warning("El dataset no contiene las columnas necesarias ('GDP' y 'Medal').")

        # Pestaña 2: Crecimiento deportivo
        with tabs[1]:
            st.subheader("Crecimiento de participación en deportes en las últimas décadas")
            if "Sport" in df.columns and "Year" in df.columns:
                recent_decades = df[df["Year"] >= 1980]
                top_sports = recent_decades["Sport"].value_counts().nlargest(10).index
                recent_decades_top_sports = recent_decades[recent_decades["Sport"].isin(top_sports)]
                sport_medals = recent_decades_top_sports.groupby(["Year", "Sport"])["Medal"].count().reset_index()
                
                fig = px.line(
                    sport_medals,
                    x="Year",
                    y="Medal",
                    color="Sport",
                    title="Crecimiento de participación en los 10 deportes más practicados desde 1980",
                    labels={"Year": "Año", "Medal": "Número de Medallas", "Sport": "Deporte"},
                    markers=True,
                    template="plotly_white"
                )
                fig.update_traces(line=dict(width=3), marker=dict(size=6, opacity=0.6))
                fig.update_layout(
                    title_x=0.5,
                    xaxis=dict(title="Año", tickangle=45, gridcolor="LightGrey"),
                    yaxis=dict(title="Número de Medallas", gridcolor="LightGrey"),
                    legend_title="Deporte"
                )
                st.plotly_chart(fig)
            else:
                st.warning("El dataset no contiene las columnas necesarias ('Sport' y 'Year').")

        # Pestaña 3: Países desarrollados vs en desarrollo
        with tabs[2]:
            st.subheader("Participación y medallas: Países desarrollados vs en desarrollo")
            if "Income Group" in df.columns and "Year" in df.columns and "Medal" in df.columns:
                income_medals = df[df["Medal"] != "No Medal"].groupby(["Year", "Income Group"])["Medal"].count().reset_index()
                fig = px.line(
                    income_medals,
                    x="Year",
                    y="Medal",
                    color="Income Group",
                    title="Tendencias de Medallas: Países por Grupos de Ingresos",
                    labels={"Year": "Año", "Medal": "Número de Medallas", "Income Group": "Grupo de Ingresos"},
                    markers=True,
                    template="plotly_white"
                )
                fig.update_traces(line=dict(width=3), marker=dict(size=6, opacity=0.6))
                fig.update_layout(
                    title_x=0.5,
                    xaxis=dict(title="Año", tickangle=45, gridcolor="LightGrey"),
                    yaxis=dict(title="Número de Medallas", gridcolor="LightGrey"),
                    legend_title="Grupo de Ingresos"
                )
                st.plotly_chart(fig)
            else:
                st.warning("El dataset no contiene las columnas necesarias ('Income Group', 'Year', y 'Medal').")

        with tabs[3]:
            st.subheader("Test de Hipótesis")
            st.markdown("### 1️⃣ ¿La economía de un país está relacionada con su participación olímpica?")
            
            # Subsection: PIB y participaciones
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("#### Hipótesis:")
                st.markdown("Los países con un PIB promedio más alto tienen una mayor participación en los Juegos Olímpicos.")
                st.markdown("### Resultado: ")
                st.markdown("- **Correlación de Pearson:** 0.79 (p-value: 0.0000)")
                st.markdown("- **Correlación de Spearman:** 0.85 (p-value: 0.0000)")
                st.markdown("### Conclusión:")
                st.write("""
                Con base en los resultados del análisis, **sí existe una relación significativa entre el PIB promedio de un país y su participación en los Juegos Olímpicos**. 
                Los países con un PIB más alto tienden a participar con mayor frecuencia en las competencias.
                """)
            
            with col2:
                # Gráfico interactivo para PIB vs Participaciones
                if "Income Group" in df.columns and "GDP" in df.columns:
                    income_pib_participation = df.groupby("Income Group").agg({
                        "GDP": "mean",
                        "Year": "count"
                    }).reset_index().rename(columns={"Year": "Participaciones", "GDP": "PIB Promedio"})
                    
                    fig1 = px.scatter(
                        income_pib_participation,
                        x="PIB Promedio",
                        y="Participaciones",
                        size="Participaciones",
                        color="Income Group",
                        hover_name="Income Group",
                        title="Relación entre el PIB Promedio y las Participaciones Olímpicas",
                        labels={"PIB Promedio": "PIB Promedio (USD)", "Participaciones": "Número de Participaciones"},
                        template="plotly_white"
                    )
                    fig1.update_layout(title_x=0.5)
                    st.plotly_chart(fig1)
                    

            st.markdown("---")

            st.markdown("### 2️⃣ ¿La población de un país influye en el número de atletas enviados?")
            
            # Subsection: Población y atletas enviados
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("#### Hipótesis:")
                st.markdown("Los países con mayor población envían más atletas a los Juegos Olímpicos.")
                st.markdown("### Resultado:")
                st.markdown("- **Pendiente (slope):** 0.0000")
                st.markdown("- **Intercepto:** 1009.4244")
                st.markdown("- **R-cuadrado:** 0.0526")
                st.markdown("- **p-value:** 0.0118")
                st.markdown("### Conclusión:")
                st.write("""
                        Los resultados sugieren que **la población tiene un impacto moderado en el número de atletas enviados por un país**.
                        Aunque existe una relación positiva, otros factores como la inversión en deportes y la infraestructura también juegan un rol importante.
                        """)
                
            
            with col2:
                # Gráfico interactivo para Población vs Atletas
                if "Population" in df.columns and "NOC" in df.columns:
                    population_athletes = df.groupby("NOC").agg({
                        "Population": "mean",
                        "Year": "count"
                    }).reset_index().rename(columns={"Year": "Atletas Enviados", "Population": "Población Promedio"})

                    fig2 = px.scatter(
                        population_athletes,
                        x="Población Promedio",
                        y="Atletas Enviados",
                        size="Atletas Enviados",
                        color="NOC",
                        hover_name="NOC",
                        title="Relación entre la Población Promedio y los Atletas Enviados",
                        labels={"Población Promedio": "Población Promedio", "Atletas Enviados": "Número de Atletas"},
                        template="plotly_white"
                    )
                    fig2.update_layout(title_x=0.5)
                    
                    
                    st.plotly_chart(fig2)
    except FileNotFoundError:
        st.error(f"No se encontró el archivo {dataset_path}. Asegúrate de que está en el directorio correcto.")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    page_cda()
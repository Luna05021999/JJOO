import streamlit as st
import pandas as pd
import plotly.express as px
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

def page_predictive_analysis():
    set_professional_header(header_image_path)
    
    st.title("Análisis Predictivo")
    st.markdown("### Explorando el rendimiento olímpico a través de un mapa interactivo")
    st.markdown(
        "Este mapa interactivo permite analizar el rendimiento de los países en los Juegos Olímpicos, "
        "con la posibilidad de filtrar por año, temporada y tipo de medalla."
    )
    
    # Cargar dataset
    dataset_path = r"C:\Users\luna\OneDrive\Escritorio\BOOTCAMP_DATA\PROYECTO_FINAL_JJOO\app\pages\final_dataset_cleaned.csv"
    df = pd.read_csv(dataset_path)
    
    # Filtrar dataset
    st.sidebar.header("Filtros para el Mapa")
    years = sorted(df["Year"].unique())
    selected_year = st.sidebar.selectbox("Selecciona un Año", years, index=len(years) - 1)
    
    seasons = df["Season"].unique()
    selected_season = st.sidebar.radio("Selecciona una Temporada", seasons)
    
    medals = ["Gold", "Silver", "Bronze"]
    selected_medal = st.sidebar.multiselect("Selecciona el Tipo de Medalla", medals, default=medals)
    
    # Filtrar dataset según los filtros seleccionados
    filtered_df = df[
        (df["Year"] == selected_year) &
        (df["Season"] == selected_season) &
        (df["Medal"].isin(selected_medal))
    ]
    
    # Crear datos agregados por país
    country_medals = filtered_df.groupby("NOC", as_index=False).agg({"Medal": "count"})
    country_medals.rename(columns={"Medal": "Número de Medallas"}, inplace=True)
    
    # Asegurarnos de tener un archivo con los códigos ISO de cada país
    country_codes = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv")
    country_medals = pd.merge(country_medals, country_codes, left_on="NOC", right_on="CODE", how="inner")
    
    # Crear mapa interactivo
    st.markdown("#### Mapa de Medallas Olímpicas por País")
    fig = px.choropleth(
        country_medals,
        locations="CODE",
        color="Número de Medallas",
        hover_name="COUNTRY",
        hover_data=["Número de Medallas"],
        title=f"Medallas por País en {selected_year} - {selected_season}",
        color_continuous_scale="Viridis",
        projection="natural earth"
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="LightGray",
            projection_type="natural earth"
        ),
        width=1000,  # Ajustar el ancho del mapa
        height=700   # Ajustar la altura del mapa
    )
    
    st.plotly_chart(fig)

    # Información adicional debajo del mapa
    st.markdown(
        f"En el mapa se muestran los países que participaron en los Juegos Olímpicos de {selected_year} ({selected_season}). "
        f"El tamaño y color indican el número de medallas ganadas."
    )

page_predictive_analysis()
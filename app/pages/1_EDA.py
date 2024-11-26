import streamlit as st
from PIL import Image
import pandas as pd
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

def page_eda():
    st.markdown("<h1 style='text-align: center;'>Exploración de Datos (EDA)</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Vista del Dataset Final</h3>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #ABB2B9;'>", unsafe_allow_html=True)
    
    dataset_path = r"C:\Users\luna\OneDrive\Escritorio\BOOTCAMP_DATA\PROYECTO_FINAL_JJOO\app\pages\final_dataset_cleaned.csv"
    
    try:
        # Cargar el dataset
        df = pd.read_csv(dataset_path)

        # Mostrar un resumen inicial del dataset
        st.subheader("Vista previa del dataset:")
        st.dataframe(df.head(7))  # Mostrar las primeras filas
        
        st.markdown("**Dimensiones del Dataset**")
        st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
        
        st.markdown("**Resumen estadístico del dataset**")
        st.write(df.describe())
        
        # Crear pestañas para cada gráfico
        tabs = st.tabs(["Top 10 países con más medallas", "Relación entre PIB promedio y medallas", "Medallas por rango de PIB", "Relación entre deportes y clima"])

        # Gráfico 1: Top 10 países con más medallas
        with tabs[0]:
            if "NOC" in df.columns and "Medal" in df.columns:
                st.subheader("Top 10 países con más medallas")
                medals_by_country = df.groupby("NOC")["Medal"].count().sort_values(ascending=False).head(10)
                medals_data = pd.DataFrame({
                    "País (NOC)": medals_by_country.index,
                    "Número de medallas": medals_by_country.values
                })
                fig1 = px.bar(
                    medals_data,
                    x="País (NOC)",
                    y="Número de medallas",
                    color="Número de medallas",
                    color_continuous_scale="Viridis",
                    title="Top 10 países con más medallas",
                    text="Número de medallas"
                )
                fig1.update_traces(textposition="outside", textfont_size=12)
                fig1.update_layout(
                    xaxis_title="País (NOC)",
                    yaxis_title="Número de medallas",
                    title_x=0.5
                )
                st.plotly_chart(fig1)

        # Gráfico 2: Relación entre PIB promedio y medallas por grupo de ingresos
        with tabs[1]:
            if "Income Group" in df.columns and "GDP" in df.columns:
                st.subheader("Relación entre PIB promedio y medallas por grupo de ingresos")
                income_group_medals = df.groupby("Income Group").agg({
                    "Medal": "count",
                    "GDP": "mean"
                }).reset_index()
                pib_medallas = df.groupby('Income Group', as_index=False).agg({
                    'GDP': 'mean',
                    'Medal': 'count'
                }).rename(columns={'Medal': 'Total de medallas', 'GDP': 'Promedio PIB'})    #PIB y medallas

                fig = px.bar(
                    pib_medallas,
                    x='Income Group',
                    y='Total de medallas',
                    color='Income Group',
                    title='Relación entre el PIB Promedio y las medallas totales por Income Group',
                    text='Total de medallas',
                    barmode='stack',
                    template='plotly_white'
                )

                fig.update_layout(
                    title=dict(font=dict(size=20, color='black'), x=0.5),
                    xaxis=dict(title='Grupo de Ingresos', titlefont=dict(size=14)),
                    yaxis=dict(title='Total de medallas', titlefont=dict(size=14)),
                    legend_title_text='Grupo de Ingresos'
                )

                st.plotly_chart(fig)

        # Gráfico 3: Medallas por rango de PIB
        with tabs[2]:
            if "GDP" in df.columns:
                st.subheader("Número de medallas por rango de PIB")
                df["GDP Range"] = pd.cut(df["GDP"], bins=5, labels=["Bajo", "Medio Bajo", "Medio", "Medio Alto", "Alto"])
                gdp_medals = df.groupby("GDP Range")["Medal"].count().reset_index()
                # Crear categorías para el PIB
                df['PIB_Rango'] = pd.cut(
                    df['GDP'], 
                    bins=[0, 1e10, 5e10, 1e11, 5e11, 1e12, 1.5e12], 
                    labels=['<10B', '10B-50B', '50B-100B', '100B-500B', '500B-1T', '>1T']
                )

                # Filtrar medallas
                filtered_data = df[df['Medal'] != 'No Medal']

                # Contar el número de medallas por rango de PIB
                medals_by_pib_range = filtered_data.groupby('PIB_Rango')['Medal'].count().reset_index()

                # Crear gráfico de barras interactivo
                fig3 = px.bar(
                    medals_by_pib_range,
                    x='PIB_Rango',
                    y='Medal',
                    title='Número de Medallas por Rango de PIB',
                    labels={'PIB_Rango': 'Rango de PIB (USD)', 'Medal': 'Número de Medallas'},
                    text='Medal',
                    color='Medal',
                    color_continuous_scale='viridis'
                )

                fig3.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))

                fig3.update_layout(
                    title=dict(font=dict(size=20, color='black'), x=0.5),
                    xaxis=dict(title='Rango de PIB (USD)', titlefont=dict(size=14)),
                    yaxis=dict(title='Número de Medallas', titlefont=dict(size=14)),
                    template='plotly_white'
                )

                st.plotly_chart(fig3)

        # Gráfico 4: Relación entre deportes y clima (anomalías de temperatura)
        with tabs[3]:
            if "Sport" in df.columns and "Annual Anomaly" in df.columns:
                st.subheader("Relación entre deportes y clima")
                climate_sport = df.groupby("Sport").agg({
                    "Annual Anomaly": "mean",
                    "Medal": "count"
                }).reset_index().sort_values("Annual Anomaly", ascending=False).head(10)
                outdoor_sports = ['Athletics', 'Cycling', 'Rowing', 'Sailing', 'Equestrianism', 'Beach Volleyball', 'Golf', 'Archery']
                indoor_sports = ['Basketball', 'Gymnastics', 'Weightlifting', 'Fencing', 'Table Tennis', 'Ice Hockey', 'Wrestling']

                df['Sport Category'] = df['Sport'].apply(
                    lambda sport: 'Outdoor' if sport in outdoor_sports else ('Indoor' if sport in indoor_sports else 'Other')
                )

                sport_climate = df.groupby(['Sport Category', 'Year'])[['Annual Anomaly']].mean().reset_index()

                fig4 = px.line(
                    sport_climate,
                    x='Year',
                    y='Annual Anomaly',
                    color='Sport Category',
                    markers=True,
                    title='Relación entre Deportes y Clima (Anomalías de Temperatura)',
                    color_discrete_map={'Indoor': 'blue', 'Outdoor': 'green', 'Other': 'red'}
                )

                fig4.update_traces(line=dict(width=3), marker=dict(size=6, opacity=0.6))

                annotations = [
                    dict(x=1996, y=0.4, xref='x', yref='y', text='Incremento notable en anomalías', showarrow=True, arrowhead=2, bgcolor='lightyellow'),
                    dict(x=1980, y=0.2, xref='x', yref='y', text='Incremento en deportes Outdoor', showarrow=True, arrowhead=2, bgcolor='lightyellow')
                ]

                fig4.update_layout(
                    title=dict(font=dict(size=20, color='black'), text='Relación entre Deportes y Clima (Anomalías de Temperatura)', x=0.5),
                    xaxis=dict(title='Año', titlefont=dict(size=14, color='black'), tickangle=45, tickfont=dict(color='black')),
                    yaxis=dict(title='Anomalía de Temperatura (°C)', titlefont=dict(size=14, color='black'), range=[-0.5, 1.5], tickfont=dict(color='black')),
                    template='plotly_white',
                    annotations=annotations,
                    legend=dict(
                        title=dict(font=dict(size=14, color='black'), text='Categoría de Deporte'),
                        orientation='h',
                        y=-0.2,
                        tracegroupgap=0,
                        font=dict(color='black')
                    )
                )

                st.plotly_chart(fig4)

    except FileNotFoundError:
        st.error(f"No se encontró el archivo {dataset_path}. Asegúrate de que está en el directorio correcto.")
    except Exception as e:
        st.error(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    # Ruta de la imagen de encabezado
    header_image_path = "C:/Users/luna/OneDrive/Escritorio/BOOTCAMP_DATA/PROYECTO_FINAL_JJOO/app/pages/jjoo_background.png"

    # Configurar el encabezado profesional
    set_professional_header(header_image_path)
    
    page_eda()
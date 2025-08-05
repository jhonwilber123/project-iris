# app/app.py - VERSIÓN DE DESPLIEGUE FINAL
import streamlit as st
import pandas as pd
import plotly.express as px
import json

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="IRIS Risk Index", layout="wide", page_icon="👁️")

# --- FUNCIONES DE CARGA (YA VALIDADAS) ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/iris_scores_for_dashboard.csv')
    if 'ubigeo_code' in df.columns:
        df.dropna(subset=['ubigeo_code'], inplace=True)
        df['ubigeo_code'] = df['ubigeo_code'].astype(int).astype(str).str.zfill(6)
    return df

@st.cache_data
def load_geojson():
    with open('data/peru_distritos.geojson') as f:
        return json.load(f)

# --- CUERPO PRINCIPAL DE LA APLICACIÓN ---
st.title("👁️ Proyecto IRIS: Índice de Riesgo de Inversión Sub-soberana")
st.write("Mapa interactivo que visualiza el score de riesgo IRIS para distritos en Perú.")

try:
    df_scores = load_data()
    geojson_distritos = load_geojson()
    
    st.header("Mapa de Calor del Riesgo IRIS a Nivel Distrital")

    if 'ubigeo_code' in df_scores.columns and not df_scores.empty:
        
        # --- CÓDIGO DEL MAPA (USANDO LA FUNCIÓN MODERNA Y RECOMENDADA 'choropleth') ---
        fig = px.choropleth(
            df_scores,
            geojson=geojson_distritos,
            locations='ubigeo_code',
            featureidkey="properties.IDDIST",
            color='iris_score',
            color_continuous_scale="Reds",
            scope="south america",
            hover_name='ubigeo',
            hover_data={'iris_score': ':.3f'}
        )
        
        # Centramos el mapa en Perú
        fig.update_geos(
            fitbounds="locations", 
            visible=False
        )
        
        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("No se pudieron generar los datos para el mapa.")

    st.header("Explorador de Datos Completo")
    st.dataframe(df_scores)

except Exception as e:
    st.error(f"Ha ocurrido un error al generar la aplicación: {e}")
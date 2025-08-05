# app/app.py - VERSIÓN CON TOOLTIPS CORREGIDOS
import streamlit as st
import pandas as pd
import json
import pydeck as pdk
import numpy as np
from shapely.geometry import shape

# --- CONFIGURACIÓN DE LA PÁGINA Y FUNCIONES DE CARGA (SIN CAMBIOS) ---
st.set_page_config(page_title="IRIS Risk Index", layout="wide", page_icon="👁️")

@st.cache_data
def load_data():
    df = pd.read_csv('data/iris_scores_for_dashboard.csv')
    if 'ubigeo_code' in df.columns:
        df.dropna(subset=['ubigeo_code'], inplace=True)
        df['ubigeo_code'] = df['ubigeo_code'].astype(int).astype(str).str.zfill(6)
    return df

@st.cache_data
def load_geojson_with_centroids():
    with open('data/peru_distritos.geojson') as f:
        geojson_data = json.load(f)
    geojson_features = []
    for feature in geojson_data['features']:
        properties = feature.get('properties', {})
        ubigeo = properties.get('IDDIST')
        geometry = feature.get('geometry')
        if ubigeo and geometry:
            geom_shape = shape(geometry)
            centroid = geom_shape.centroid
            geojson_features.append({'ubigeo_code': ubigeo, 'lat': centroid.y, 'lon': centroid.x})
    return pd.DataFrame(geojson_features)

# --- CUERPO PRINCIPAL ---
st.title("👁️ Proyecto IRIS: Índice de Riesgo de Inversión Sub-soberana")
st.write("Mapa interactivo que visualiza el score de riesgo IRIS para distritos en Perú.")

try:
    df_scores = load_data()
    df_centroids = load_geojson_with_centroids()
    df_mapa = pd.merge(df_scores, df_centroids, on='ubigeo_code', how='inner')
    
    st.header("Mapa de Riesgo IRIS a Nivel Distrital (usando PyDeck)")
    df_mapa.dropna(subset=['iris_score'], inplace=True)

    max_score = df_mapa['iris_score'].max()
    df_mapa['color'] = df_mapa['iris_score'].apply(
        lambda score: [255, 0, 0, 150 * (score / max_score if max_score > 0 else 0)]
    )

    # --- MEJORA: SLIDER DE FILTRADO INTERACTIVO ---
    score_threshold = st.slider(
        'Mostrar solo distritos con un Score IRIS superior a:',
        min_value=0.0, max_value=max_score, value=0.0, step=0.01
    )
    df_filtrado = df_mapa[df_mapa['iris_score'] >= score_threshold]

    # --- CORRECCIÓN DEL TOOLTIP ---
    # 1. Creamos columnas de texto explícitas para el tooltip
    df_filtrado['tooltip_distrito'] = df_filtrado['ubigeo']
    df_filtrado['tooltip_score'] = df_filtrado['iris_score'].apply(lambda x: f"{x:.4f}")

    # 2. Apuntamos el tooltip a estas nuevas columnas
    tooltip = {
        "html": "<b>Distrito:</b> {tooltip_distrito}<br/><b>Score IRIS:</b> {tooltip_score}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
    
    view_state = pdk.ViewState(latitude=-9.19, longitude=-75.015, zoom=4.5, pitch=50)

    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_filtrado, # Usamos el DataFrame filtrado
        get_position='[lon, lat]',
        get_color='color',
        get_radius=8000,
        pickable=True,
        auto_highlight=True,
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/satellite-streets-v11', # Con mapa satelital
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip # Usamos el tooltip corregido
    ))

    st.header("Explorador de Datos")
    st.dataframe(df_scores)

except Exception as e:
    st.error(f"Ha ocurrido un error al generar la aplicación: {e}")
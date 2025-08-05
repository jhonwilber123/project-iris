# app/app.py - VERSIÓN FINAL CORREGIDA Y PULIDA
import streamlit as st
import pandas as pd
import json
import pydeck as pdk
import numpy as np
from shapely.geometry import shape
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="IRIS Risk Index", 
    layout="wide", 
    page_icon="👁️",
    initial_sidebar_state="expanded"
)

# --- 2. CSS PERSONALIZADO ---
st.markdown("""
<style>
    /* Estilos del cuerpo principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        font-weight: bold;
    }
    /* Tarjetas de métricas */
    .metric-card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid #444;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 600;
    }
    .metric-label {
        font-size: 1rem;
        color: #a1a1a1;
    }
    /* Alertas de riesgo */
    .risk-alert {
        padding: 1rem; border-radius: 8px; margin: 1rem 0;
        border-left: 5px solid; font-size: 1.1rem;
    }
    .risk-high { background-color: #401818; border-left-color: #f44336; }
    .risk-medium { background-color: #4d3c1d; border-left-color: #ff9800; }
    .risk-low { background-color: #1e3b1f; border-left-color: #4caf50; }
</style>
""", unsafe_allow_html=True)

# --- 3. DICCIONARIO DE TEXTOS ---
TEXTS = {
    "es": { "title": "👁️ Proyecto IRIS: Índice de Riesgo para Inversiones en Infraestructura", "subtitle": "Bienvenido al dashboard del Proyecto IRIS...", "map_header": "🗺️ Mapa de Calor del Riesgo IRIS", "slider_label": "Filtrar por Nivel de Riesgo", "slider_help": "...", "analysis_header": "📊 Análisis Detallado por Distrito", "selectbox_label": "Seleccione un Distrito", "profile_for": "Perfil para:", "gauge_title": "Nivel de Riesgo IRIS", "radar_title": "Desglose de Factores para", "bar_title": "Comparación vs. Promedio Nacional", "g_score_label": "G-Score (Gestión)", "s_score_label": "S-Score (Social)", "iris_score_label": "Score IRIS Final", "bar_district": "Distrito Seleccionado", "bar_national": "Promedio Nacional", "data_explorer_header": "🔍 Explorador de Datos", "statistics_header": "📈 Estadísticas Generales", "risk_classification": "Clasificación de Riesgo", "high_risk": "Alto Riesgo", "medium_risk": "Riesgo Medio", "low_risk": "Bajo Riesgo", "total_districts": "Distritos Analizados", "avg_risk": "Riesgo Promedio", "max_risk": "Riesgo Máximo", "min_risk": "Riesgo Mínimo", "top_risk_districts": "🚨 Distritos de Mayor Riesgo", "export_data": "📤 Exportar Datos Filtrados", "download_csv": "Descargar CSV", "download_json": "Descargar JSON", "filters_header": "🔧 Filtros", "department_filter": "Filtrar por Departamento", "province_filter": "Filtrar por Provincia" },
    "en": { "title": "👁️ Project IRIS: Risk Index for Infrastructure Investments", "subtitle": "Welcome to the Project IRIS dashboard...", "map_header": "🗺️ IRIS Risk Heatmap", "slider_label": "Filter by Risk Level", "slider_help": "...", "analysis_header": "📊 Detailed District Analysis", "selectbox_label": "Select a District", "profile_for": "Profile for:", "gauge_title": "IRIS Risk Level", "radar_title": "Factor Breakdown for", "bar_title": "Comparison vs. National Average", "g_score_label": "G-Score (Governance)", "s_score_label": "S-Score (Social)", "iris_score_label": "Final IRIS Score", "bar_district": "Selected District", "bar_national": "National Average", "data_explorer_header": "🔍 Data Explorer", "statistics_header": "📈 General Statistics", "risk_classification": "Risk Classification", "high_risk": "High Risk", "medium_risk": "Medium Risk", "low_risk": "Low Risk", "total_districts": "Analyzed Districts", "avg_risk": "Average Risk", "max_risk": "Maximum Risk", "min_risk": "Minimum Risk", "top_risk_districts": "🚨 Highest Risk Districts", "export_data": "📤 Export Filtered Data", "download_csv": "Download CSV", "download_json": "Download JSON", "filters_header": "🔧 Filters", "department_filter": "Filter by Department", "province_filter": "Filter by Province" }
}

# --- 4. FUNCIONES DE UTILIDAD ---
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
    features = []
    for feature in geojson_data['features']:
        properties = feature.get('properties', {})
        ubigeo = properties.get('IDDIST')
        geometry = feature.get('geometry')
        if ubigeo and geometry:
            geom = shape(geometry)
            centroid = geom.centroid
            features.append({'ubigeo_code': ubigeo, 'lat': centroid.y, 'lon': centroid.x})
    return pd.DataFrame(features)

def classify_risk(score, q1, q3):
    if score > q3: return "high"
    elif score > q1: return "medium"
    else: return "low"

def create_risk_alert(risk_level, score, txt):
    alerts = {
        "high": (f"<strong>⚠️ {txt['high_risk']}</strong><br>Score IRIS: {score:.4f} - Se recomienda precaución especial.", "risk-alert risk-high"),
        "medium": (f"<strong>⚡ {txt['medium_risk']}</strong><br>Score IRIS: {score:.4f} - Monitoreo recomendado.", "risk-alert risk-medium"),
        "low": (f"<strong>✅ {txt['low_risk']}</strong><br>Score IRIS: {score:.4f} - Riesgo bajo detectado.", "risk-alert risk-low")
    }
    message, style = alerts.get(risk_level, ("", ""))
    st.markdown(f'<div class="{style}">{message}</div>', unsafe_allow_html=True)

# --- 5. APLICACIÓN PRINCIPAL ---
def main():
    # --- BARRA LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        language = st.selectbox("🌐 Language / Idioma", ["English", "Español"])
        lang_code = "es" if language == "Español" else "en"
        txt = TEXTS[lang_code]
        st.markdown("---")
        
        st.markdown(f"### {txt['filters_header']}")
        
    # --- CARGA Y PREPARACIÓN DE DATOS ---
    df_scores = load_data()
    df_centroids = load_geojson_with_centroids()
    df_mapa = pd.merge(df_scores, df_centroids, on='ubigeo_code', how='inner')
    df_mapa.dropna(subset=['iris_score'], inplace=True)
    
    # --- FILTROS EN LA BARRA LATERAL ---
    with st.sidebar:
        df_mapa['departamento'] = df_mapa['ubigeo'].str.split('_').str[0]
        all_departments = sorted(df_mapa['departamento'].unique())
        selected_department = st.selectbox(txt['department_filter'], ["Todos"] + all_departments)
        
        min_risk, max_risk = float(df_mapa['iris_score'].min()), float(df_mapa['iris_score'].max())
        risk_range = st.slider("Rango de Riesgo IRIS", min_value=min_risk, max_value=max_risk, value=(min_risk, max_risk), step=0.001)

    # --- APLICACIÓN DE FILTROS ---
    df_display = df_mapa.copy()
    if selected_department != "Todos":
        df_display = df_display[df_display['departamento'] == selected_department]
    df_display = df_display[(df_display['iris_score'] >= risk_range[0]) & (df_display['iris_score'] <= risk_range[1])]

    # --- CUERPO PRINCIPAL ---
    st.markdown(f'# {txt["title"]}')
    st.markdown(f"*{txt['subtitle']}*")
    st.markdown("---")
    
    # --- ESTADÍSTICAS GENERALES ---
    st.markdown(f'## {txt["statistics_header"]}')
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f'<div class="metric-card"><div class="metric-label">{txt["total_districts"]}</div><div class="metric-value">{len(df_display):,}</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-card"><div class="metric-label">{txt["avg_risk"]}</div><div class="metric-value">{df_display["iris_score"].mean():.4f}</div></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-card"><div class="metric-label">{txt["max_risk"]}</div><div class="metric-value">{df_display["iris_score"].max():.4f}</div></div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div class="metric-card"><div class="metric-label">{txt["min_risk"]}</div><div class="metric-value">{df_display["iris_score"].min():.4f}</div></div>', unsafe_allow_html=True)

    # --- MAPA MEJORADO ---
    st.markdown(f'## {txt["map_header"]}')
    max_risk_display = df_display['iris_score'].max()
    df_display['color'] = df_display['iris_score'].apply(lambda s: [255, max(0, 255 * (1 - s / max_risk_display if max_risk_display > 0 else 1)), 0, 180])
    
    # --- CORRECCIÓN DEL TOOLTIP ---
    df_display['tooltip_distrito'] = df_display['ubigeo']
    df_display['tooltip_score'] = df_display['iris_score'].apply(lambda x: f"{x:.4f}")
    df_display['tooltip_g_score'] = df_display['g_score'].apply(lambda x: f"{x:.4f}")
    df_display['tooltip_s_score'] = df_display['s_score'].apply(lambda x: f"{x:.4f}")

    tooltip = {
        "html": f"""<b>Distrito:</b> {{tooltip_distrito}}<br/>
                     <b>{txt['iris_score_label']}:</b> {{tooltip_score}}<br/>
                     <b>{txt['g_score_label']}:</b> {{tooltip_g_score}}<br/>
                     <b>{txt['s_score_label']}:</b> {{tooltip_s_score}}""",
        "style": {"backgroundColor": "rgba(40,40,40,0.8)", "color": "white", "border": "1px solid #555"}
    }
    # --- FIN DE LA CORRECCIÓN ---

    view_state = pdk.ViewState(latitude=-9.19, longitude=-75.015, zoom=4.5, pitch=45)
    layer = pdk.Layer('ScatterplotLayer', data=df_display, get_position='[lon, lat]', get_color='color', get_radius=6000, pickable=True, auto_highlight=True)
    
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', initial_view_state=view_state, layers=[layer], tooltip=tooltip))

    # --- ANÁLISIS DETALLADO ---
    st.markdown(f'## {txt["analysis_header"]}')
    lista_distritos_filtrada = sorted(df_display['ubigeo'].unique())
    
    if lista_distritos_filtrada:
        distrito_seleccionado = st.selectbox(txt["selectbox_label"], lista_distritos_filtrada)
        datos_distrito = df_display[df_display['ubigeo'] == distrito_seleccionado].iloc[0]
        
        q1_risk, q3_risk = df_mapa['iris_score'].quantile(0.33), df_mapa['iris_score'].quantile(0.66)
        risk_level = classify_risk(datos_distrito['iris_score'], q1_risk, q3_risk)
        create_risk_alert(risk_level, datos_distrito['iris_score'], txt)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(txt["g_score_label"], f"{datos_distrito['g_score']:.4f}")
            st.metric(txt["s_score_label"], f"{datos_distrito['s_score']:.4f}")
            
            factor_cols = [col for col in df_scores.columns if '_factor' in col]
            valores_factores = datos_distrito[factor_cols]
            df_bar_comp = pd.DataFrame({'Score': factor_cols, 'Valor': valores_factores}).sort_values('Valor', ascending=False)
            fig_bar = px.bar(df_bar_comp, x='Valor', y='Score', orientation='h', title="Principales Contribuyentes al Riesgo")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=valores_factores, theta=[col.replace('_factor_', '').replace('_', ' ').title() for col in factor_cols], fill='toself', name=distrito_seleccionado))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), title=f"{txt['radar_title']} {distrito_seleccionado}")
            st.plotly_chart(fig_radar, use_container_width=True)
            
    # --- EXPORTACIÓN Y EXPLORADOR DE DATOS ---
    with st.expander(f"📥 {txt['export_data']} & {txt['data_explorer_header']}"):
        st.dataframe(df_display)
        csv_data = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(label=txt["download_csv"], data=csv_data, file_name='iris_filtered_data.csv', mime='text/csv')

if __name__ == "__main__":
    main()
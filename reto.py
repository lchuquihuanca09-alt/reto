import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración inicial de la página web
st.set_page_config(
    page_title="Monitoreo de Salud de Astronautas", page_icon="🚀", layout="wide"
)

st.title(
    "🚀 Sistema de Monitoreo de Salud para Astronautas en Misiones Espaciales"
)
st.write(
    "Herramienta interactiva para recopilar indicadores de salud y evaluar riesgos de radiación, fatiga y aislamiento."
)

# 1. INICIALIZAR LA LISTA DE TRIPULANTES EN LA MEMORIA TEMPORAL (Session State)
if "lista_tripulantes" not in st.session_state:
  st.session_state.lista_tripulantes = [
      "Comandante A. Chuquihuanca",
      "Especialista de Misión B. Smith",
  ]

# Barra lateral para telemetría y controles
st.sidebar.header("📡 Panel de Control de Misión")

# --- NUEVA SECCIÓN: AGREGAR TRIPULANTE DESDE LA INTERFAZ ---
st.sidebar.subheader("👤 Gestión de Tripulación")
nuevo_tripulante = st.sidebar.text_input("Nombre del nuevo tripulante")

if st.sidebar.button("Agregar Tripulante"):
  if (
      nuevo_tripulante
      and nuevo_tripulante not in st.session_state.lista_tripulantes
  ):
    st.session_state.lista_tripulantes.append(nuevo_tripulante)
    st.sidebar.success(f"¡{nuevo_tripulante} registrado con éxito!")
  elif not nuevo_tripulante:
    st.sidebar.warning("Por favor, escribe un nombre válido.")
  else:
    st.sidebar.info("Este tripulante ya se encuentra en la lista.")

# Menú desplegable usando la lista dinámica
astronauta_sel = st.sidebar.selectbox(
    "Seleccionar Tripulante Actual", st.session_state.lista_tripulantes
)

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Simulación de Telemetría")

# Sliders de signos vitales y entorno
ritmo_cardiaco = st.sidebar.slider(
    "Ritmo Cardíaco Actual (BPM)", 40, 180, 69, key="rc"
)
radiacion = st.sidebar.slider(
    "Exposición a Radiación (mSv)", 0.0, 5.0, 1.18, key="rad"
)
horas_sueno = st.sidebar.slider(
    "Horas de Sueño (Último ciclo)", 0.0, 12.0, 5.46, key="sueno"
)

# Sección Principal: Estado de Alertas y Diagnóstico Rápido
st.header("🚨 Estado de Alertas y Diagnóstico Rápido")
st.write(f"Evaluando métricas en tiempo real para: **{astronauta_sel}**")

col1, col2, col3 = st.columns(3)

with col1:
  if ritmo_cardiaco > 100:
    st.error(f"⚠️ Ritmo Cardíaco Elevado: {ritmo_cardiaco} BPM")
  else:
    st.success(f"Ritmo Cardíaco Estable: {ritmo_cardiaco} BPM")

with col2:
  if radiacion > 2.0:
    st.error(
        f"⚠️ Alerta de Radiación: {radiacion} mSv (¡Trasládese al refugio!)"
    )
  else:
    st.success(f"Nivel de Radiación Seguro: {radiacion} mSv")

with col3:
  if horas_sueno < 6.0:
    st.warning(f"⚠️ Fatiga Detectada: {horas_sueno} hrs (Descanso sugerido)")
  else:
    st.success(f"Descanso Adecuado: {horas_sueno} hrs")

# Sección de Tendencias Históricas con Plotly
st.header("📊 Análisis de Tendencias de Salud (Últimos 7 Días)")
tab1, tab2, tab3 = st.tabs(
    ["Ritmo Cardíaco", "Radiación Acumulada", "Calidad de Sueño"]
)

dias = [f"Día {i}" for i in range(1, 8)]

with tab1:
  df_rc = pd.DataFrame(
      {"Día": dias, "BPM": [70, 72, 68, 75, 80, 71, ritmo_cardiaco]}
  )
  fig_rc = px.line(
      df_rc,
      x="Día",
      y="BPM",
      markers=True,
      title=f"Evolución del Pulso - {astronauta_sel}",
  )
  st.plotly_chart(fig_rc, use_container_width=True)

with tab2:
  df_rad = pd.DataFrame(
      {"Día": dias, "mSv": [1.0, 1.2, 1.1, 1.3, 1.4, 1.2, radiacion]}
  )
  fig_rad = px.bar(
      df_rad,
      x="Día",
      y="mSv",
      title=f"Acumulación de Radiación - {astronauta_sel}",
  )
  st.plotly_chart(fig_rad, use_container_width=True)

with tab3:
  df_sueno = pd.DataFrame(
      {"Día": dias, "Horas": [6.5, 7.0, 5.5, 8.0, 6.0, 6.5, horas_sueno]}
  )
  fig_sueno = px.line(
      df_sueno,
      x="Día",
      y="Horas",
      markers=True,
      title=f"Registro de Descanso - {astronauta_sel}",
  )
  st.plotly_chart(fig_sueno, use_container_width=True)
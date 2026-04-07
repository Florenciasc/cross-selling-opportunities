import os
import pandas as pd
import streamlit as st

# -----------------------------------
# Configuración general
# -----------------------------------
st.set_page_config(
    page_title="Webshop Recommender",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------------
# Estilos
# -----------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #16325B;
    }
    .subtitle {
        font-size: 1rem;
        color: #4F709C;
        margin-bottom: 1.2rem;
    }
    .card {
        background-color: #F7FAFC;
        border: 1px solid #D9E2EC;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .card h4 {
        margin: 0 0 8px 0;
        color: #102A43;
    }
    .small-text {
        color: #486581;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Carga de datos (FIX)
# -----------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, "data", "processed", "recomendaciones_modelo.csv")

    if not os.path.exists(path):
        st.error(f"No se encontró el archivo: {path}")
        st.stop()

    return pd.read_csv(path)

recomendaciones = load_data()

# -----------------------------------
# Columnas
# -----------------------------------
col_origen = "grupo_a"
col_reco = "grupo_b"
col_score = "score"
col_freq = "frecuencia"
col_ticket = "ticket_grupo_b"

# -----------------------------------
# LOGO + HEADER
# -----------------------------------
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

col_logo, col_title = st.columns([1, 6])

with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=90)

with col_title:
    st.markdown(
        '<div class="main-title">Sistema de recomendación por macrogrupos</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Demo funcional · Sprint 2 · Recomendaciones basadas en co-ocurrencia y valor económico</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.header("Configuración de la demo")

grupos = sorted(recomendaciones[col_origen].dropna().unique())
grupo_seleccionado = st.sidebar.selectbox("Seleccionar grupo origen", grupos)
top_k = st.sidebar.slider("Cantidad de recomendaciones", 3, 10, 5)

# -----------------------------------
# Filtrado
# -----------------------------------
df_grupo = (
    recomendaciones[recomendaciones[col_origen] == grupo_seleccionado]
    .sort_values(col_score, ascending=False)
    .head(top_k)
    .copy()
)

# -----------------------------------
# Métricas
# -----------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Grupo origen", grupo_seleccionado)

with col2:
    st.metric("Recomendaciones mostradas", len(df_grupo))

with col3:
    if not df_grupo.empty:
        st.metric("Score promedio", f"{df_grupo[col_score].mean():.3f}")
    else:
        st.metric("Score promedio", "0.000")

st.markdown("---")

# -----------------------------------
# Cards
# -----------------------------------
st.subheader("Top recomendaciones")

if df_grupo.empty:
    st.warning("No hay recomendaciones disponibles.")
else:
    cols = st.columns(min(3, len(df_grupo)))

    for i, (_, row) in enumerate(df_grupo.head(3).iterrows()):
        with cols[i]:
            st.markdown(
                f"""
                <div class="card">
                    <h4>{row[col_reco]}</h4>
                    <div class="small-text"><b>Score:</b> {row[col_score]:.3f}</div>
                    <div class="small-text"><b>Frecuencia:</b> {int(row[col_freq])}</div>
                    <div class="small-text"><b>Ticket promedio:</b> ${row[col_ticket]:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------
# Tabla + insights
# -----------------------------------
left, right = st.columns([1.4, 1])

with left:
    st.markdown("### Tabla completa")

    if not df_grupo.empty:
        tabla = df_grupo[[col_reco, col_score, col_freq, col_ticket]].rename(columns={
            col_reco: "Grupo recomendado",
            col_score: "Score",
            col_freq: "Frecuencia",
            col_ticket: "Ticket promedio"
        })

        # ✅ FORMATEO
        tabla["Ticket promedio"] = tabla["Ticket promedio"].apply(lambda x: f"${x:,.2f}")

        # ✅ MOSTRAR
        st.dataframe(tabla, use_container_width=True)

with right:
    st.markdown("### Lectura rápida")
    if not df_grupo.empty:
        mejor = df_grupo.iloc[0][col_reco]
        st.success(f"La mejor recomendación para **{grupo_seleccionado}** es **{mejor}**.")
        st.info(
    "Las recomendaciones se priorizan según frecuencia de co-compra y ticket promedio, permitiendo identificar oportunidades de cross-selling con mayor impacto económico."
)

# -----------------------------------
# Gráfico
# -----------------------------------
if not df_grupo.empty:
    st.markdown("### Ranking visual")
    st.bar_chart(df_grupo.set_index(col_reco)[col_score])

# -----------------------------------
# Explicación
# -----------------------------------
st.markdown("---")
colA, colB = st.columns(2)

with colA:
    st.markdown("### ¿Qué hace el modelo?")
    st.write(
        "Recomienda macrogrupos que suelen comprarse juntos, detectando relaciones en el comportamiento histórico."
    )

with colB:
    st.markdown("### Limitaciones")
    st.write(
        "- No es personalizado por usuario\n"
        "- Algunos grupos tienen poca data\n"
        "- Se puede mejorar con modelos más avanzados"
    )

st.markdown("---")
st.caption("Proyecto Webshop · Sprint 2")
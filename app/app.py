import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# -----------------------------------
# Configuración general
# -----------------------------------
st.set_page_config(
    page_title="Webshop | Cross-Selling Intelligence",
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
        font-size: 2.5rem;
        font-weight: 800;
        color: #16325B;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #4F709C;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }
    .big-card {
        background: linear-gradient(135deg, #EAF2FF, #F8FAFC);
        border: 1px solid #D9E2EC;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
        color: #102A43 !important;
    }
    .big-card p, .big-card div, .big-card span, .big-card b {
        color: #102A43 !important;
    }
    .card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
        min-height: 165px;
        color: #102A43 !important;
    }
    .card h4, .card p, .card div, .card span, .card b {
        color: #102A43 !important;
    }
    .info-box {
        background-color: #EFF6FF;
        border-left: 6px solid #2563EB;
        padding: 16px;
        border-radius: 12px;
        color: #1E3A8A !important;
        font-size: 1rem;
        margin-bottom: 14px;
    }
    .insight-box {
        background-color: #ECFDF5;
        border-left: 6px solid #10B981;
        padding: 16px;
        border-radius: 12px;
        color: #065F46 !important;
        font-size: 1rem;
        margin-bottom: 14px;
    }
    .warn-box {
        background-color: #FEFCE8;
        border-left: 6px solid #CA8A04;
        padding: 16px;
        border-radius: 12px;
        color: #854D0E !important;
        font-size: 1rem;
        margin-bottom: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Carga de datos
# -----------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))

    path_main = os.path.join(base_dir, "data", "processed", "cross_selling_features.csv")
    if not os.path.exists(path_main):
        st.error(f"No se encontró el archivo: {path_main}")
        st.stop()

    return pd.read_csv(path_main)

recomendaciones = load_data()

# -----------------------------------
# Columnas reales
# -----------------------------------
col_origen = "grupo_a"
col_reco = "grupo_b"
col_freq = "frecuencia"
col_ticket_origen = "ticket_grupo_a"
col_ticket_destino = "ticket_grupo_b"
col_score = "score"
col_relevancia = "relevancia"

# -----------------------------------
# Logo
# -----------------------------------
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

# -----------------------------------
# Funciones auxiliares
# -----------------------------------
def clasificar_oportunidad(score: float) -> str:
    if score >= 0.13:
        return "Alta"
    elif score >= 0.08:
        return "Media"
    return "Baja"

def descripcion_macrocategoria(grupo: str) -> str:
    descripciones = {
        "Alimentos": "Macrocategoría de consumo frecuente y alta recurrencia.",
        "Cuidado Personal": "Macrocategoría asociada a higiene, bienestar y consumo diario.",
        "Recreación": "Macrocategoría vinculada a ocio, familia, mascotas y estilo de vida.",
        "Automotor": "Macrocategoría de compras más específicas, con tickets unitarios relevantes.",
        "Hogar": "Macrocategoría de artículos funcionales y de uso cotidiano.",
        "Tecnología": "Macrocategoría con productos de valor percibido mayor y potencial de ticket superior.",
        "Moda": "Macrocategoría asociada a preferencia, estilo y estacionalidad.",
        "Industria y construcción": "Macrocategoría con productos más específicos y uso puntual.",
        "Marketplace": "Macrocategoría amplia y heterogénea dentro del catálogo.",
        "Cultura y entretenimiento": "Macrocategoría asociada a experiencias y ocio.",
        "other": "Macrocategoría residual con menor volumen histórico."
    }
    return descripciones.get(grupo, "Macrocategoría con comportamiento específico dentro del catálogo.")

def insight_negocio(grupo_origen, grupo_recomendado):
    return (
        f"Los clientes que compran en <b>{grupo_origen}</b> también muestran afinidad con <b>{grupo_recomendado}</b>, "
        "lo que sugiere una oportunidad concreta para activar cross-selling y aumentar el ticket promedio."
    )

def acciones_comerciales():
    return [
        ("🛒 Bundle sugerido", "Combinar macrocategorías relacionadas para aumentar valor por compra."),
        ("🎯 Sugerencia en checkout", "Mostrar oportunidades cruzadas durante la compra."),
        ("📢 Campaña segmentada", "Activar promociones dirigidas según afinidad detectada.")
    ]

def fallback_popularidad(df, top_n=5):
    return (
        df.groupby(col_reco)[col_freq]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
        .rename(columns={
            col_reco: "Macrocategoría sugerida",
            col_freq: "Compras conjuntas"
        })
    )

def gauge_mini(valor_pct: float):
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=valor_pct,
        gauge={
            "axis": {"range": [0, 100], "visible": False},
            "bar": {"color": "#2563EB"},
            "bgcolor": "white",
            "steps": [
                {"range": [0, 40], "color": "#FDE68A"},
                {"range": [40, 70], "color": "#93C5FD"},
                {"range": [70, 100], "color": "#86EFAC"}
            ],
        }
    ))

    fig.update_layout(
        height=120,  # 👈 compacto
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return fig

# -----------------------------------
# Header
# -----------------------------------
col_logo, col_title = st.columns([1, 7])

with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=95)

with col_title:
    st.markdown(
        '<div class="main-title">Oportunidades de Cross-Selling</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Identificación de oportunidades comerciales entre macrocategorías para aumentar ticket promedio y potenciar ventas cruzadas.</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.header("Configuración del análisis")

grupos = sorted(recomendaciones[col_origen].dropna().unique())
grupo_seleccionado = st.sidebar.selectbox("Seleccionar macrocategoría analizada", grupos)
top_k = st.sidebar.slider("Cantidad de oportunidades a visualizar", 3, 10, 5)

# -----------------------------------
# Filtrado
# -----------------------------------
df_grupo = (
    recomendaciones[recomendaciones[col_origen] == grupo_seleccionado]
    .sort_values(col_relevancia, ascending=False)
    .head(top_k)
    .copy()
)

# -----------------------------------
# Variables principales
# -----------------------------------
if not df_grupo.empty:
    top = df_grupo.iloc[0]

    mejor = top[col_reco]
    mejor_score = float(top[col_score])
    mejor_freq = int(top[col_freq])
    ticket_origen = float(top[col_ticket_origen])
    ticket_destino = float(top[col_ticket_destino])
    relevancia = float(top[col_relevancia])

    nivel_oportunidad = clasificar_oportunidad(mejor_score)

    impacto_pct = ((ticket_destino - ticket_origen) / ticket_origen) * 100 if ticket_origen > 0 else 0.0
    nivel_oportunidad_pct = min(relevancia, 100)

    score_promedio = float(df_grupo[col_score].mean())
else:
    mejor = "-"
    mejor_score = 0.0
    mejor_freq = 0
    ticket_origen = 0.0
    ticket_destino = 0.0
    relevancia = 0.0
    impacto_pct = 0.0
    nivel_oportunidad_pct = 0.0
    nivel_oportunidad = "-"
    score_promedio = 0.0

# -----------------------------------
# Resumen ejecutivo
# -----------------------------------
st.markdown('<div class="section-title">Resumen ejecutivo</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Macrocategoría analizada", grupo_seleccionado)

with col2:
    st.metric("Principal categoría asociada", mejor)

with col3:
    st.markdown("Nivel de oportunidad")
    st.plotly_chart(gauge_mini(nivel_oportunidad_pct), use_container_width=True)

    # 🎨 Color dinámico según nivel
    if nivel_oportunidad == "Alta":
        color = "#16A34A"   # verde
    elif nivel_oportunidad == "Media":
        color = "#2563EB"   # azul
    else:
        color = "#DC2626"   # rojo

    st.markdown(
        f"<div style='text-align:center; font-weight:600; color:{color}; font-size:1.3rem; letter-spacing:0.5px;'>"
        f"{nivel_oportunidad}</div>",
        unsafe_allow_html=True
    )

# -----------------------------------
# Relación comercial detectada
# -----------------------------------
st.markdown("### Relación comercial detectada")
st.markdown(
    f"""
    <div class="info-box">
    {descripcion_macrocategoria(grupo_seleccionado)}
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Oportunidad principal sugerida
# -----------------------------------
if not df_grupo.empty:
    st.markdown(
        f"""
        <div class="big-card">
            <div class="section-title" style="color:#102A43;">Oportunidad principal sugerida</div>
            <p>Para la macrocategoría <b>{grupo_seleccionado}</b>, la principal categoría asociada es <b>{mejor}</b>.</p>
            <p><b>Nivel de oportunidad:</b> {nivel_oportunidad}</p>
            <p><b>Compras conjuntas observadas:</b> {mejor_freq}</p>
            <p><b>Incremento potencial estimado:</b> {impacto_pct:+.1f}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="warn-box">
        <b>Potencial de activación:</b> {nivel_oportunidad_pct:.1f}%
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("No se encontraron oportunidades para esta macrocategoría.")

# -----------------------------------
# Principales oportunidades sugeridas
# -----------------------------------
st.markdown('<div class="section-title">Principales categorías asociadas</div>', unsafe_allow_html=True)

if df_grupo.empty:
    st.warning("No se encontraron oportunidades para esta macrocategoría.")
else:
    card_cols = st.columns(min(3, len(df_grupo)))

    for idx, (_, row) in enumerate(df_grupo.head(3).iterrows()):
        impacto_card = (
            ((float(row[col_ticket_destino]) - float(row[col_ticket_origen])) / float(row[col_ticket_origen])) * 100
            if float(row[col_ticket_origen]) > 0 else 0.0
        )

        with card_cols[idx]:
            st.markdown(
                f"""
                <div class="card">
                    <h4>{row[col_reco]}</h4>
                    <p><b>Nivel de oportunidad:</b> {clasificar_oportunidad(float(row[col_score]))}</p>
                    <p><b>Compras conjuntas:</b> {int(row[col_freq])}</p>
                    <p><b>Incremento estimado:</b> {impacto_card:+.1f}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------
# Sugerencias de activación + detalle
# -----------------------------------
left, right = st.columns([1.4, 0.8])

with left:
    st.markdown('<div class="section-title">Sugerencias de activación</div>', unsafe_allow_html=True)
    acciones = acciones_comerciales()
    cols_acc = st.columns(3)

    for col, (titulo, desc) in zip(cols_acc, acciones):
        with col:
            st.markdown(
                f"""
                <div class="card">
                    <h4>{titulo}</h4>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

with right:
    st.markdown('<div class="section-title">Detalle de asociaciones</div>', unsafe_allow_html=True)
    st.caption("Vista de respaldo para análisis técnico.")

    if not df_grupo.empty:
        tabla = df_grupo[[col_reco, col_freq, col_ticket_origen, col_ticket_destino, col_score, col_relevancia]].rename(columns={
            col_reco: "Macrocategoría sugerida",
            col_freq: "Compras conjuntas",
            col_ticket_origen: "Ticket origen",
            col_ticket_destino: "Ticket destino",
            col_score: "Score",
            col_relevancia: "Nivel de oportunidad (%)"
        })

        tabla["Ticket origen"] = tabla["Ticket origen"].apply(lambda x: f"${x:,.2f}")
        tabla["Ticket destino"] = tabla["Ticket destino"].apply(lambda x: f"${x:,.2f}")
        tabla["Score"] = tabla["Score"].apply(lambda x: f"{x:.4f}")
        tabla["Nivel de oportunidad (%)"] = tabla["Nivel de oportunidad (%)"].apply(lambda x: f"{x:.1f}%")

        with st.expander("Ver detalle técnico (opcional)", expanded=False):
            st.dataframe(tabla, use_container_width=True, height=220)

# -----------------------------------
# Por qué esta relación importa
# -----------------------------------
st.markdown("### ¿Por qué esta asociación importa?")

if not df_grupo.empty:
    st.markdown(
        f"""
        <div class="insight-box">
        {insight_negocio(grupo_seleccionado, mejor)}
        </div>
        """,
        unsafe_allow_html=True
    )

    if score_promedio >= 0.13:
        st.success("La oportunidad detectada muestra una afinidad comercial alta dentro del catálogo.")
    elif score_promedio >= 0.08:
        st.info("La oportunidad detectada presenta una afinidad comercial moderada y puede activarse tácticamente.")
    else:
        st.warning("La oportunidad detectada es más limitada y conviene validarla antes de una activación amplia.")

    st.markdown("### Nivel de oportunidad")
    st.metric("Potencial estimado", f"{nivel_oportunidad_pct:.1f}%")
    st.progress(nivel_oportunidad_pct / 100)

# -----------------------------------
# Fallback
# -----------------------------------
if df_grupo.empty:
    st.markdown("### Alternativa por volumen histórico")
    fallback = fallback_popularidad(recomendaciones, top_n=5)
    st.dataframe(fallback, use_container_width=True)

# -----------------------------------
# Footer simple
# -----------------------------------
st.markdown("---")
st.caption("Proyecto Webshop · Sprint 2 · CSCM Consulting Group")
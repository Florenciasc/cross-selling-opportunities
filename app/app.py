import os
import pandas as pd
import streamlit as st

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
        font-size: 1.35rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }
    .section-subtitle {
        font-size: 0.95rem;
        color: #CBD5E1;
        margin-top: -0.2rem;
        margin-bottom: 1rem;
    }
    .hero-box {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
    }
    .hero-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 8px;
    }
    .hero-text {
        font-size: 1.03rem;
        color: #E2E8F0;
        line-height: 1.5;
    }
    .kpi-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 18px;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #CBD5E1;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.1;
    }
    .kpi-badge {
        border-radius: 14px;
        padding: 18px;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    .kpi-badge-title {
        font-size: 0.95rem;
        color: #CBD5E1;
        margin-bottom: 8px;
    }
    .kpi-badge-value {
        font-size: 2rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }
    .kpi-badge-desc {
        font-size: 0.92rem;
        line-height: 1.3;
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
    .tag-box {
        background-color: #FEFCE8;
        border-left: 6px solid #CA8A04;
        padding: 14px 16px;
        border-radius: 12px;
        color: #854D0E !important;
        font-size: 1rem;
        margin-bottom: 18px;
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
    .action-card {
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        min-height: 185px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.20);
    }
    .action-card h4 {
        color: #F8FAFC !important;
        margin-bottom: 10px;
    }
    .action-card p {
        color: #CBD5F5 !important;
    }
    .action-card .badge {
        margin-top: 10px;
        font-size: 0.85rem;
        font-weight: 600;
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
    .secondary-box {
        background-color: rgba(255,255,255,0.08);
        border-left: 6px solid #94A3B8;
        padding: 16px;
        border-radius: 12px;
        color: #E2E8F0 !important;
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
    path = os.path.join(base_dir, "data", "processed", "cross_selling_features.csv")

    if not os.path.exists(path):
        st.error(f"No se encontró el archivo: {path}")
        st.stop()

    return pd.read_csv(path)

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
def clasificar_oportunidad_pct(valor_pct: float) -> str:
    if valor_pct >= 70:
        return "Alta"
    elif valor_pct >= 40:
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
        "Viaje y accesorios": "Macrocategoría vinculada a movilidad, equipaje y uso complementario.",
        "other": "Macrocategoría residual con menor volumen histórico."
    }
    return descripciones.get(grupo, "Macrocategoría con comportamiento específico dentro del catálogo.")


def insight_negocio(grupo_origen, grupo_recomendado):
    return (
        f"Los clientes que compran en <b>{grupo_origen}</b> también muestran afinidad con "
        f"<b>{grupo_recomendado}</b>, lo que sugiere una oportunidad concreta para activar "
        "cross-selling y aumentar el ticket promedio."
    )


def acciones_comerciales_contexto(grupo_origen, grupo_destino):
    return [
        (
            f"🛒 Bundle {grupo_origen} + {grupo_destino}",
            f"Crear combos promocionales entre {grupo_origen} y {grupo_destino} para aumentar el ticket promedio.",
            "Alta"
        ),
        (
            "🎯 Cross-sell en checkout",
            f"Recomendar {grupo_destino} cuando el cliente agrega productos de {grupo_origen}.",
            "Media"
        ),
        (
            "📢 Campaña segmentada",
            f"Impactar clientes que compraron {grupo_origen} con ofertas de {grupo_destino}.",
            "Media"
        )
    ]


def render_accion_card(titulo, desc, prioridad):
    if prioridad == "Alta":
        color = "#16A34A"
        bg = "rgba(22,163,74,0.12)"
        badge = "🔥 Alto impacto"
    elif prioridad == "Media":
        color = "#2563EB"
        bg = "rgba(37,99,235,0.12)"
        badge = "⚡ Quick win"
    else:
        color = "#64748B"
        bg = "rgba(100,116,139,0.12)"
        badge = "🧪 Testear"

    return f"""
    <div class="action-card" style="
        border-left: 4px solid {color};
        border: 1px solid {color};
        background:{bg};
    ">
        <h4>{titulo}</h4>
        <p>{desc}</p>
        <div class="badge" style="color:{color};">
            {badge}
        </div>
    </div>
    """


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


def build_priority_badge(nivel_oportunidad: str, nivel_oportunidad_pct: float):
    if nivel_oportunidad == "Alta":
        color = "#16A34A"
        bg = "rgba(22,163,74,0.12)"
        desc = "Relación sólida para activar"
    elif nivel_oportunidad == "Media":
        color = "#2563EB"
        bg = "rgba(37,99,235,0.12)"
        desc = "Relación válida con oportunidad táctica"
    else:
        color = "#DC2626"
        bg = "rgba(220,38,38,0.12)"
        desc = "Relación limitada, requiere validación"

    return f"""
    <div class="kpi-badge" style="background:{bg}; border:1px solid {color};">
        <div class="kpi-badge-title">Prioridad comercial</div>
        <div class="kpi-badge-value" style="color:{color};">{nivel_oportunidad}</div>
        <div class="kpi-badge-desc" style="color:{color};">{nivel_oportunidad_pct:.1f}% · {desc}</div>
    </div>
    """

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

MAX_RELEVANCIA = recomendaciones[col_relevancia].max()

# -----------------------------------
# Variables principales
# -----------------------------------
if not df_grupo.empty:
    top = df_grupo.iloc[0]

    mejor = top[col_reco]
    mejor_freq = int(top[col_freq])
    ticket_origen = float(top[col_ticket_origen])
    ticket_destino = float(top[col_ticket_destino])
    relevancia = float(top[col_relevancia])

    impacto_pct = ((ticket_destino - ticket_origen) / ticket_origen) * 100 if ticket_origen > 0 else 0.0
    nivel_oportunidad_pct = (relevancia / MAX_RELEVANCIA) * 100 if MAX_RELEVANCIA > 0 else 0.0
    nivel_oportunidad = clasificar_oportunidad_pct(nivel_oportunidad_pct)
else:
    mejor = "-"
    mejor_freq = 0
    ticket_origen = 0.0
    ticket_destino = 0.0
    relevancia = 0.0
    impacto_pct = 0.0
    nivel_oportunidad_pct = 0.0
    nivel_oportunidad = "-"

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
# Insight clave
# -----------------------------------
if not df_grupo.empty:
    if nivel_oportunidad == "Alta":
        insight_line = (
            f"Los clientes de <b>{grupo_seleccionado}</b> muestran una asociación sólida con "
            f"<b>{mejor}</b>. Recomendación prioritaria para activar."
        )
    elif nivel_oportunidad == "Media":
        insight_line = (
            f"Detectamos una asociación relevante entre <b>{grupo_seleccionado}</b> y "
            f"<b>{mejor}</b>. Oportunidad táctica para testear activación."
        )
    else:
        insight_line = (
            f"<b>{grupo_seleccionado}</b> se relaciona con <b>{mejor}</b>, pero con baja prioridad "
            f"comercial. Conviene validar antes de escalar."
        )

    st.markdown(
        f"""
        <div class="hero-box">
            <div class="hero-title">💡 Insight clave</div>
            <div class="hero-text">{insight_line}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------
# Lectura rápida
# -----------------------------------
st.markdown('<div class="section-title">Lectura rápida</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Lo más importante para entender esta oportunidad en segundos.</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Macrocategoría analizada</div>
            <div class="kpi-value">{grupo_seleccionado}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Principal categoría asociada</div>
            <div class="kpi-value">{mejor}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(build_priority_badge(nivel_oportunidad, nivel_oportunidad_pct), unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------
# Qué está pasando
# -----------------------------------
st.markdown("### Qué está pasando")
st.markdown(
    f"""
    <div class="info-box">
    {descripcion_macrocategoria(grupo_seleccionado)}
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Qué recomendamos hacer
# -----------------------------------
if not df_grupo.empty:
    st.markdown(
        f"""
        <div class="big-card">
            <div class="section-title" style="color:#102A43;">Qué recomendamos hacer</div>
            <p>Para la macrocategoría <b>{grupo_seleccionado}</b>, la mejor asociación detectada es <b>{mejor}</b>.</p>
            <p><b>Compras conjuntas observadas:</b> {mejor_freq}</p>
            <p><b>Potencial de incremento estimado:</b> {impacto_pct:+.1f}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if impacto_pct >= 50 and nivel_oportunidad == "Baja":
        st.markdown(
            """
            <div class="tag-box">
            <b>Atención:</b> el potencial de incremento es alto, pero la prioridad comercial es baja.
            Se recomienda validar esta activación antes de escalarla.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="tag-box">
            <b>Potencial estimado de activación:</b> {nivel_oportunidad_pct:.1f}%
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.warning("No se encontraron oportunidades para esta macrocategoría.")

# -----------------------------------
# Principales categorías asociadas
# -----------------------------------
st.markdown('<div class="section-title">Principales categorías asociadas</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Relaciones detectadas para esta macrocategoría, ordenadas por prioridad.</div>',
    unsafe_allow_html=True
)

if df_grupo.empty:
    st.warning("No se encontraron oportunidades para esta macrocategoría.")
else:
    card_cols = st.columns(min(3, len(df_grupo.head(3))))

    for col, (i, (_, row)) in zip(card_cols, enumerate(df_grupo.head(3).iterrows(), start=1)):
        impacto_card = (
            ((float(row[col_ticket_destino]) - float(row[col_ticket_origen])) / float(row[col_ticket_origen])) * 100
            if float(row[col_ticket_origen]) > 0 else 0.0
        )
        relevancia_card = float(row[col_relevancia])
        nivel_card_pct = (relevancia_card / MAX_RELEVANCIA) * 100 if MAX_RELEVANCIA > 0 else 0.0
        nivel_card = clasificar_oportunidad_pct(nivel_card_pct)

        with col:
            st.markdown(
                f"""
                <div class="card">
                    <h4>#{i} {row[col_reco]}</h4>
                    <p><b>Prioridad:</b> {nivel_card}</p>
                    <p><b>Compras conjuntas:</b> {int(row[col_freq])}</p>
                    <p><b>Incremento estimado:</b> {impacto_card:+.1f}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------
# Sugerencias de activación + análisis técnico
# -----------------------------------
left, right = st.columns([1.4, 0.8])

with left:
    st.markdown('<div class="section-title">Sugerencias de activación</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Acciones concretas para capturar esta oportunidad.</div>',
        unsafe_allow_html=True
    )

    acciones = acciones_comerciales_contexto(grupo_seleccionado, mejor)
    cols_acc = st.columns(3)

    for col, (titulo, desc, prioridad) in zip(cols_acc, acciones):
        with col:
            st.markdown(
                render_accion_card(titulo, desc, prioridad),
                unsafe_allow_html=True
            )

with right:
    st.markdown('<div class="section-title">Análisis técnico</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Detalle de respaldo para profundizar la relación detectada.</div>',
        unsafe_allow_html=True
    )

    if not df_grupo.empty:
        tabla = df_grupo[[col_reco, col_freq, col_ticket_origen, col_ticket_destino, col_score, col_relevancia]].rename(columns={
            col_reco: "Macrocategoría sugerida",
            col_freq: "Compras conjuntas",
            col_ticket_origen: "Ticket origen",
            col_ticket_destino: "Ticket destino",
            col_score: "Score",
            col_relevancia: "Relevancia"
        })

        tabla["Ticket origen"] = tabla["Ticket origen"].apply(lambda x: f"${x:,.2f}")
        tabla["Ticket destino"] = tabla["Ticket destino"].apply(lambda x: f"${x:,.2f}")
        tabla["Score"] = tabla["Score"].apply(lambda x: f"{x:.4f}")
        tabla["Relevancia"] = tabla["Relevancia"].apply(lambda x: f"{x:.2f}")

        with st.expander("Ver detalle técnico (opcional)", expanded=False):
            st.dataframe(tabla, width="stretch", height=250)

# -----------------------------------
# Por qué importa
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

    if nivel_oportunidad == "Alta":
        st.markdown(
            """
            <div class="secondary-box">
            Esta oportunidad tiene una prioridad alta y puede integrarse directamente en acciones comerciales.
            </div>
            """,
            unsafe_allow_html=True
        )
    elif nivel_oportunidad == "Media":
        st.markdown(
            """
            <div class="secondary-box">
            Esta oportunidad tiene potencial táctico y puede probarse con activaciones puntuales.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="secondary-box">
            Esta oportunidad es más limitada y conviene validarla antes de una activación amplia.
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------------
# Potencial estimado
# -----------------------------------
if nivel_oportunidad_pct >= 70:
    color = "#16A34A"
    desc = "Alta probabilidad de activación comercial"
elif nivel_oportunidad_pct >= 40:
    color = "#2563EB"
    desc = "Oportunidad táctica con potencial de prueba"
else:
    color = "#DC2626"
    desc = "Potencial limitado, conviene validar"

st.markdown(
    f"""
    <div style="
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 10px;
    ">
        <div style="font-size:0.92rem; color:#CBD5E1; margin-bottom:6px;">
            Potencial estimado
        </div>
        <div style="font-size:2.2rem; font-weight:700; color:{color}; line-height:1.1; margin-bottom:8px;">
            {nivel_oportunidad_pct:.1f}%
        </div>
        <div style="font-size:0.95rem; color:#E2E8F0; margin-bottom:12px;">
            {desc}
        </div>
        <div style="
            width:100%;
            height:10px;
            background: rgba(255,255,255,0.12);
            border-radius:999px;
            overflow:hidden;
        ">
            <div style="
                width:{nivel_oportunidad_pct:.1f}%;
                height:100%;
                background:{color};
                border-radius:999px;
            "></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# Fallback
# -----------------------------------
if df_grupo.empty:
    st.markdown("### Alternativa por volumen histórico")
    fallback = fallback_popularidad(recomendaciones, top_n=5)
    st.dataframe(fallback, width="stretch")

# -----------------------------------
# Footer
# -----------------------------------
st.markdown("---")
st.caption("Proyecto Webshop · Sprint 2 · CSCM Consulting Group")
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================================
# CONFIGURACIÓN GENERAL Y PALETA DE COLORES
# ==========================================================

st.set_page_config(
    page_title="URAB IA · Presentación LSL 2026",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

CYAN = "#22d3ee"
VIOLETA = "#8b5cf6"
VERDE = "#10b981"
AMBAR = "#f59e0b"
ROJO = "#f43f5e"
TEXTO = "#e2e8f0"
GRIS = "#94a3b8"

TIPOS = [
    "Asesoría",
    "Queja",
    "Solicitud de Mediación",
    "Solicitud de Conciliación",
]

COLOR_TIPO = {
    "Asesoría": CYAN,
    "Queja": ROJO,
    "Solicitud de Mediación": AMBAR,
    "Solicitud de Conciliación": VIOLETA,
}

TEMAS = [
    "Servicios públicos",
    "Salud",
    "Seguridad social",
    "Vivienda",
    "Educación",
    "Justicia y tutela",
]

CANALES = ["IRIS", "VisionWeb"]

COLOR_CANAL = {
    "IRIS": CYAN,
    "VisionWeb": VIOLETA,
}

RANGOS_COMPONENTES = {
    "M1 Extracción": (0.70, 1.00),
    "M2 Exactitud": (0.65, 1.00),
    "M2 Sensibilidad de urgencias": (0.85, 1.00),
    "M4 Precisión": (0.65, 1.00),
    "M4 Sensibilidad": (0.65, 1.00),
    "M6 Aceptación": (0.45, 1.00),
}

UMBRALES = {
    "M1 Extracción": 0.90,
    "M2 Exactitud": 0.90,
    "M2 Sensibilidad de urgencias": 0.99,
    "M4 Precisión": 0.85,
    "M4 Sensibilidad": 0.90,
    "M6 Aceptación": 0.70,
}

COLORES_METRICAS = {
    "M1 Extracción": CYAN,
    "M2 Exactitud": VIOLETA,
    "M2 Sensibilidad de urgencias": ROJO,
    "M4 Precisión": AMBAR,
    "M4 Sensibilidad": VERDE,
    "M6 Aceptación": "#e879f9",
}


# ==========================================================
# ESTILOS (CSS)
# ==========================================================

CSS_GLOBAL = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(1200px 600px at 15% -10%, rgba(34, 211, 238, 0.12), transparent 60%),
        radial-gradient(1000px 700px at 90% 0%, rgba(139, 92, 246, 0.14), transparent 55%),
        radial-gradient(900px 500px at 50% 110%, rgba(16, 185, 129, 0.08), transparent 60%),
        linear-gradient(160deg, #0b1020 0%, #0f172a 55%, #0b1020 100%);
}

.stApp {
    background: transparent;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.85);
    border-right: 1px solid rgba(148, 163, 184, 0.15);
    backdrop-filter: blur(8px);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* ---------- Hero ---------- */

.hero {
    position: relative;
    text-align: center;
    padding: 2.2rem 1rem 1.4rem;
    overflow: hidden;
}

.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(70px);
    opacity: 0.5;
    animation: flotar 9s ease-in-out infinite;
    pointer-events: none;
}

.orb.o1 { width: 260px; height: 260px; background: rgba(34, 211, 238, 0.30); top: -60px; left: 12%; }
.orb.o2 { width: 300px; height: 300px; background: rgba(139, 92, 246, 0.30); top: -40px; right: 10%; animation-delay: -3s; }
.orb.o3 { width: 180px; height: 180px; background: rgba(16, 185, 129, 0.22); bottom: -70px; left: 45%; animation-delay: -6s; }

@keyframes flotar {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(22px) scale(1.05); }
}

.hero-badge {
    display: inline-block;
    padding: 0.35rem 1.1rem;
    border: 1px solid rgba(34, 211, 238, 0.45);
    border-radius: 999px;
    background: rgba(34, 211, 238, 0.08);
    color: #a5f3fc;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.4px;
    margin-bottom: 1rem;
    animation: aparecer 0.8s ease;
}

.hero-title {
    font-size: 5rem;
    font-weight: 900;
    margin: 0.2rem 0 0.6rem;
    color: #f8fafc;
    letter-spacing: 2px;
    animation: aparecer 0.9s ease;
}

.grad-anim {
    background: linear-gradient(90deg, #22d3ee, #8b5cf6, #f43f5e, #f59e0b, #22d3ee);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: flujo-gradiente 7s linear infinite;
}

@keyframes flujo-gradiente {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

.hero-sub {
    color: #cbd5e1;
    font-size: 1.12rem;
    width: 100%;
    text-align: center;
    margin: 0 auto 1.1rem;
    animation: aparecer 1.1s ease;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.55rem;
    animation: aparecer 1.3s ease;
}

.hero-tag {
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    background: rgba(148, 163, 184, 0.12);
    border: 1px solid rgba(148, 163, 184, 0.25);
    color: #cbd5e1;
}

@keyframes aparecer {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: none; }
}

/* ---------- KPIs ---------- */

.kpi-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.7rem;
    justify-content: center;
    margin: 0.4rem 0 0.9rem;
}

.kpi-chip {
    background: rgba(148, 163, 184, 0.08);
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 14px;
    padding: 0.55rem 1.2rem;
    min-width: 118px;
    text-align: center;
    animation: aparecer 0.5s ease;
}

.kpi-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.45rem;
    font-weight: 700;
    color: #22d3ee;
    line-height: 1.15;
}

.kpi-lbl {
    font-size: 0.72rem;
    color: #94a3b8;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ---------- Tarjetas ---------- */

.card {
    background: rgba(148, 163, 184, 0.06);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 16px;
    padding: 1.1rem 1.2rem;
    height: 100%;
    transition: transform 0.25s ease, border-color 0.25s ease;
}

.card:hover {
    transform: translateY(-4px);
    border-color: rgba(34, 211, 238, 0.55);
}

.card-icono {
    font-size: 1.7rem;
    margin-bottom: 0.45rem;
}

.card-titulo {
    font-weight: 800;
    color: #f1f5f9;
    font-size: 1.02rem;
    margin-bottom: 0.35rem;
}

.card-texto {
    color: #94a3b8;
    font-size: 0.86rem;
    line-height: 1.45;
}

.mod-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin: 0.6rem 0;
}

@media (max-width: 1000px) {
    .mod-grid { grid-template-columns: repeat(2, 1fr); }
}

.mod-card {
    background: rgba(148, 163, 184, 0.06);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 16px;
    padding: 1rem 1.05rem;
    border-top: 3px solid #22d3ee;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.mod-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.35);
}

.mod-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    opacity: 0.85;
}

.mod-titulo {
    font-weight: 800;
    color: #f1f5f9;
    font-size: 0.98rem;
    margin: 0.25rem 0 0.3rem;
}

.mod-desc {
    color: #94a3b8;
    font-size: 0.8rem;
    line-height: 1.42;
}

.mod-meta {
    margin-top: 0.55rem;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.3px;
}

/* ---------- Feed de PQRSD ---------- */

.pqrsd-card {
    background: rgba(148, 163, 184, 0.07);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 12px;
    padding: 0.65rem 0.85rem;
    margin-bottom: 0.45rem;
    animation: slideIn 0.45s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(-14px) scale(0.97); }
    to { opacity: 1; transform: none; }
}

.pqrsd-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
}

.pqrsd-radicado {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    color: #64748b;
}

.pqrsd-tipo {
    font-weight: 800;
    font-size: 0.92rem;
    margin: 0.18rem 0 0.06rem;
}

.pqrsd-tema {
    color: #94a3b8;
    font-size: 0.8rem;
}

.pqrsd-pie {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.3rem;
    font-size: 0.74rem;
    color: #64748b;
}

.chip {
    display: inline-block;
    padding: 0.12rem 0.55rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.4px;
}

.chip-urgente {
    background: rgba(244, 63, 94, 0.16);
    color: #fb7185;
    animation: latido 1.1s ease infinite;
}

@keyframes latido {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.07); }
}

/* ---------- Pista del pipeline ---------- */

.pista-pipeline {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    justify-content: center;
    margin: 0.2rem 0 0.6rem;
}

.pista-paso {
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    border: 1px solid;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    white-space: nowrap;
}

/* ---------- Banners ---------- */

.banner-human {
    background: linear-gradient(120deg, rgba(16, 185, 129, 0.10), rgba(34, 211, 238, 0.08));
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    margin: 0.9rem 0;
}

.banner-human h4 {
    margin: 0 0 0.4rem;
    color: #6ee7b7;
    font-weight: 800;
}

.banner-human p {
    margin: 0;
    color: #cbd5e1;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* ---------- Streamlit: botones, tabs, progreso, métricas ---------- */

.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    border: 1px solid rgba(148, 163, 184, 0.25);
    background: rgba(148, 163, 184, 0.08);
    color: #e2e8f0;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: rgba(34, 211, 238, 0.6);
    color: #ffffff;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #06b6d4, #8b5cf6);
    color: #ffffff;
    border: none;
    box-shadow: 0 8px 26px rgba(34, 211, 238, 0.28);
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 10px 32px rgba(139, 92, 246, 0.45);
    transform: translateY(-1px);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(148, 163, 184, 0.06);
    border-radius: 12px 12px 0 0;
    padding: 0.7rem 1.25rem;
    color: #94a3b8;
    font-weight: 600;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(34, 211, 238, 0.16), rgba(139, 92, 246, 0.16));
    color: #f8fafc;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, #22d3ee, #8b5cf6);
}

[data-testid="stProgress"] > div > div > div > div {
    background: linear-gradient(90deg, #22d3ee, #8b5cf6, #f59e0b);
}

[data-testid="stMetric"] {
    background: rgba(148, 163, 184, 0.07);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 14px;
    padding: 0.7rem 1rem;
}

[data-testid="stMetricValue"] {
    color: #22d3ee;
    font-family: 'JetBrains Mono', monospace;
}

[data-testid="stMetricLabel"] {
    color: #94a3b8;
}

[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #e2e8f0;
}

[data-testid="stCaptionContainer"] {
    color: #64748b;
}

div[data-testid="stMarkdownContainer"] p {
    color: #cbd5e1;
}

div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4 {
    color: #f1f5f9;
}
"""

st.markdown(
    f"<style>{CSS_GLOBAL}</style>",
    unsafe_allow_html=True,
)


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def limitar(valor, minimo=0.0, maximo=1.0):
    return max(minimo, min(maximo, valor))


def limitar_componente(nombre, valor):
    minimo, maximo = RANGOS_COMPONENTES[nombre]
    return limitar(valor, minimo, maximo)


def simular_metricas_iniciales(calidad):
    factor_calidad = limitar((calidad - 0.60) / 0.40, 0.0, 1.0)

    def valor_en_rango(nombre):
        minimo, maximo = RANGOS_COMPONENTES[nombre]
        valor_base = minimo + (maximo - minimo) * factor_calidad
        amplitud = maximo - minimo
        variacion = np.random.uniform(
            -amplitud * 0.08,
            amplitud * 0.08,
        )
        return limitar(valor_base + variacion, minimo, maximo)

    return {
        nombre: valor_en_rango(nombre)
        for nombre in RANGOS_COMPONENTES
    }


def cumple_criterios(metricas):
    return all(
        metricas[k] >= UMBRALES[k]
        for k in UMBRALES
    )


def refinar_modelos(metricas, feedback):
    nuevas = metricas.copy()

    nuevas["M1 Extracción"] = limitar_componente(
        "M1 Extracción",
        nuevas["M1 Extracción"]
        + np.random.uniform(0.008, 0.025)
        + feedback * 0.005,
    )

    nuevas["M2 Exactitud"] = limitar_componente(
        "M2 Exactitud",
        nuevas["M2 Exactitud"]
        + np.random.uniform(0.012, 0.035)
        + feedback * 0.006,
    )

    nuevas["M2 Sensibilidad de urgencias"] = limitar_componente(
        "M2 Sensibilidad de urgencias",
        nuevas["M2 Sensibilidad de urgencias"]
        + np.random.uniform(0.006, 0.022)
        + feedback * 0.004,
    )

    nuevas["M4 Precisión"] = limitar_componente(
        "M4 Precisión",
        nuevas["M4 Precisión"]
        + np.random.uniform(0.010, 0.030),
    )

    nuevas["M4 Sensibilidad"] = limitar_componente(
        "M4 Sensibilidad",
        nuevas["M4 Sensibilidad"]
        + np.random.uniform(0.010, 0.030),
    )

    nuevas["M6 Aceptación"] = limitar_componente(
        "M6 Aceptación",
        nuevas["M6 Aceptación"]
        + np.random.uniform(0.015, 0.045)
        + feedback * 0.008,
    )

    return nuevas


def disparidad_inicial(calidad_datos):
    """Disparidad de equidad inicial: a menor calidad de datos, mayor sesgo."""
    factor_calidad = limitar((calidad_datos - 0.60) / 0.40, 0.0, 1.0)
    return limitar(
        0.12 - 0.06 * factor_calidad + np.random.uniform(-0.015, 0.02),
        0.01,
        0.15,
    )


def refinar_equidad(disparidad):
    """Reduce la disparidad de equidad en cada ciclo de refinamiento."""
    return limitar(disparidad - np.random.uniform(0.006, 0.022), 0.01, 0.15)


def nivel_equidad(disparidad):
    """Devuelve (etiqueta, color) del semáforo de equidad."""
    pct = disparidad * 100
    if pct < 3:
        return "🟢 Verde · monitoreo continuo", VERDE
    if pct < 5:
        return "🟡 Amarillo · revisión técnica", AMBAR
    if pct <= 10:
        return "🟠 Naranja · mitigar en 5 días", "#fb923c"
    return "🔴 Rojo · suspender y notificar", ROJO


def tabla_metricas(metricas):
    filas = []

    for nombre, valor in metricas.items():
        objetivo = UMBRALES[nombre]
        filas.append({
            "Componente": nombre,
            "Resultado": round(valor * 100, 2),
            "Meta": round(objetivo * 100, 2),
            "Estado": "✅ Cumple" if valor >= objetivo else "⚠️ Refinar",
        })

    return pd.DataFrame(filas)


# ==========================================================
# DIAGRAMA DEL PIPELINE (FLUJO ORIGINAL, TEMA OSCURO,
# CON VENTANA DE ZOOM DINÁMICO QUE SIGUE LA ETAPA ACTIVA)
# ==========================================================

NODOS_PIPELINE = {
    "datos": {"label": "PQRSD históricas\\nIRIS + VisionWeb", "shape": "box"},
    "preparacion": {"label": "Preparación y consolidación\\nde datos", "shape": "box"},
    "modelos": {"label": "ADAPTACIÓN DE MODELOS\\n\\nM1 · Ajuste fino\\nM2 · Ajuste fino\\nM4 · Vectores semánticos\\nM6 · RAG", "shape": "box"},
    "evaluacion": {"label": "Evaluación\\nMétricas de desempeño", "shape": "box"},
    "refinamiento": {"label": "REFINAMIENTO\\n\\nM1 + M2 · Ajuste fino\\nM4 · Calibración semántica\\nM6 · RAG + ajuste de instrucciones", "shape": "box"},
    "human": {"label": "Validación humana\\nValidación profesional URAB", "shape": "box"},
    "criterios": {"label": "¿Cumple criterios\\nde aceptación?", "shape": "diamond"},
    "equidad": {"label": "Pruebas de equidad\\nDisparidad ≤ 5%", "shape": "diamond"},
    "deploy": {"label": "Despliegue\\na producción", "shape": "box"},
    "integracion": {"label": "M7 · Interoperabilidad\\nIRIS ↔ IA ↔ VisionWeb", "shape": "box"},
    "operacion": {"label": "Operación integral\\nde PQRSD", "shape": "box"},
    "mlops": {"label": "Operaciones de ML\\nVersionamiento · Monitoreo\\nDrift · Trazabilidad", "shape": "box"},
    "feedback": {"label": "Retroalimentación profesional\\n+ nuevos datos", "shape": "box"},
}

ORDEN_PIPELINE = list(NODOS_PIPELINE.keys())

NOMBRES_ETAPAS = {
    "datos": "Datos históricos",
    "preparacion": "Preparación",
    "modelos": "Adaptación de modelos",
    "evaluacion": "Evaluación",
    "refinamiento": "Refinamiento",
    "human": "Validación humana",
    "criterios": "Criterios",
    "equidad": "Equidad",
    "deploy": "Despliegue",
    "integracion": "Interoperabilidad",
    "operacion": "Operación",
    "mlops": "Operaciones de ML",
    "feedback": "Retroalimentación",
}

VENTANA_ZOOM = 2

INACTIVO = "#1e293b"
ACTIVO = "#f59e0b"
HECHO = "#10b981"
BORDE = "#64748b"
TEXTO_CLARO = "#cbd5e1"
TEXTO_OSCURO = "#0f172a"


def html_pipeline(etapa_activa=None):
    """Pipeline del ciclo de vida en HTML/CSS (compatible con navegador).
    Colores: verde = etapa completada, ámbar = etapa activa (pulso),
    gris = pendiente. Sustituye al diagrama graphviz que requiere un
    binario nativo no disponible en stlite (WebAssembly)."""

    def estado(clave):
        if etapa_activa is None:
            return "pend"
        if clave == etapa_activa:
            return "act"
        if ORDEN_PIPELINE.index(clave) < ORDEN_PIPELINE.index(etapa_activa):
            return "ok"
        return "pend"

    def relleno(tipo):
        return {"pend": INACTIVO, "act": ACTIVO, "ok": HECHO}[tipo]

    def texto(tipo):
        return {"pend": TEXTO_CLARO, "act": TEXTO_OSCURO, "ok": TEXTO_OSCURO}[tipo]

    piezas = []

    for clave in ORDEN_PIPELINE:
        tipo = estado(clave)
        etiqueta = NODOS_PIPELINE[clave]["label"].replace("\\n", "<br>")
        es_diamante = NODOS_PIPELINE[clave]["shape"] == "diamond"
        animacion = "animation:pipeLatido 1.1s ease infinite;" if tipo == "act" else ""
        radio = "50% 14px 14px 14px" if es_diamante else "14px"

        piezas.append(
            '<div style="display:flex;align-items:center;gap:4px;margin:3px 0;">'
            f'<div style="min-width:150px;max-width:170px;text-align:center;'
            f'background:{relleno(tipo)};color:{texto(tipo)};'
            f'border:1px solid {BORDE};border-radius:{radio};'
            f'padding:9px 12px;font-size:11.5px;font-weight:700;line-height:1.35;'
            f'box-shadow:0 4px 14px rgba(0,0,0,0.25);{animacion}">'
            f'<span style="white-space:pre-line;">{etiqueta}</span>'
            "</div>"
            f'<span style="color:{BORDE};font-weight:800;font-size:15px;">→</span>'
            "</div>"
        )

    return (
        '<style>'
        "@keyframes pipeLatido{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}"
        ".pipe-wrap{display:flex;flex-wrap:wrap;gap:4px 6px;align-items:center;"
        "justify-content:center;margin:8px 0;}"
        "</style>"
        f'<div class="pipe-wrap">{"".join(piezas)}</div>'
    )


def html_pista_pipeline(etapa_activa=None):
    """Pista de progreso del flujo que acompaña al zoom del diagrama."""

    if etapa_activa is None:
        return ""

    indice = ORDEN_PIPELINE.index(etapa_activa)
    pildoras = []

    for i, clave in enumerate(ORDEN_PIPELINE):
        if i < indice:
            estilo = "background:rgba(16,185,129,0.18);color:#34d399;border-color:rgba(16,185,129,0.4)"
            marca = "✓"
        elif i == indice:
            estilo = "background:rgba(245,158,11,0.22);color:#fbbf24;border-color:rgba(245,158,11,0.55);animation:latido 1.2s ease infinite"
            marca = "●"
        else:
            estilo = "background:rgba(148,163,184,0.07);color:#64748b;border-color:rgba(148,163,184,0.2)"
            marca = "·"

        pildoras.append(
            f'<span class="pista-paso" style="{estilo}">{marca} {NOMBRES_ETAPAS[clave]}</span>'
        )

    return f'<div class="pista-pipeline">{"".join(pildoras)}</div>'


# ==========================================================
# GRÁFICOS PLOTLY
# ==========================================================

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#e2e8f0", size=12),
    margin=dict(t=44, b=10, l=10, r=10),
)


def fig_metricas(metricas):
    fig = go.Figure()

    nombres = list(UMBRALES.keys())

    for i, nombre in enumerate(nombres):
        valor = metricas[nombre] * 100
        meta = UMBRALES[nombre] * 100
        cumple = valor >= meta
        color = VERDE if cumple else AMBAR

        fig.add_trace(go.Bar(
            y=[nombre],
            x=[valor],
            orientation="h",
            width=0.5,
            marker_color=color,
            text=[f"{valor:.1f}%"],
            textposition="outside",
            cliponaxis=False,
            hovertemplate=f"{nombre}<br>Resultado: %{{x:.1f}}%<br>Meta: {meta:.1f}%<extra></extra>",
            showlegend=False,
        ))

        fig.add_trace(go.Scatter(
            y=[nombre],
            x=[meta],
            mode="markers",
            marker=dict(
                symbol="line-ns",
                size=22,
                color="#f8fafc",
                line=dict(width=3, color="#f8fafc"),
            ),
            name="Meta mínima",
            showlegend=(i == 0),
            hoverinfo="skip",
        ))

    fig.update_layout(
        **LAYOUT_BASE,
        height=390,
        xaxis=dict(range=[0, 113], gridcolor="rgba(148,163,184,0.10)", zeroline=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        legend=dict(orientation="h", yanchor="top", y=-0.34, x=0),
        title=dict(text="Resultado vs. meta por componente", x=0.01, xanchor="left"),
    )

    return fig


def fig_evolucion(df_historial):
    fig = go.Figure()

    for nombre in UMBRALES:
        fig.add_trace(go.Scatter(
            x=df_historial["Ciclo"],
            y=df_historial[nombre],
            mode="lines+markers",
            name=nombre,
            line=dict(color=COLORES_METRICAS[nombre], width=2.6),
            marker=dict(size=7),
        ))

    fig.update_layout(
        **LAYOUT_BASE,
        height=440,
        xaxis=dict(title="Ciclo de refinamiento", dtick=1),
        yaxis=dict(range=[40, 105], title="Desempeño (%)"),
        legend=dict(orientation="h", yanchor="top", y=-0.26, x=0),
        title=dict(text="Evolución del refinamiento", x=0.01, xanchor="left"),
    )

    return fig


def fig_donut_tipos(df):
    conteo = df["Tipo"].value_counts().reindex(TIPOS).fillna(0)

    fig = go.Figure(go.Pie(
        labels=conteo.index,
        values=conteo.values,
        hole=0.72,
        marker=dict(
            colors=[COLOR_TIPO[t] for t in conteo.index],
            line=dict(color="rgba(11,16,32,0.9)", width=2),
        ),
        textinfo="percent",
        textfont=dict(size=13, color="#0b1020"),
        hovertemplate="%{label}<br>%{value} PQRSD (%{percent})<extra></extra>",
    ))

    fig.add_annotation(
        text=f"<b>{int(len(df))}</b><br><span style='font-size:11px'>PQRSD</span>",
        showarrow=False,
        font=dict(size=24, color="#f8fafc"),
    )

    fig.update_layout(
        **LAYOUT_BASE,
        height=330,
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=-0.12, x=0),
        title=dict(text="Distribución por tipo", x=0.01, xanchor="left"),
    )

    return fig


def fig_flujo_recepcion(df):
    ordenado = df.sort_values("Timestamp").reset_index(drop=True)
    ordenado["Acumulado"] = np.arange(1, len(ordenado) + 1)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ordenado["Timestamp"],
        y=ordenado["Acumulado"],
        mode="lines",
        line=dict(color=CYAN, width=2.6),
        fill="tozeroy",
        fillcolor="rgba(34,211,238,0.13)",
        name="Acumulado",
        hovertemplate="%{y} PQRSD recibidas<extra></extra>",
    ))

    for canal in CANALES:
        sub = ordenado[ordenado["Canal"] == canal]
        fig.add_trace(go.Scatter(
            x=sub["Timestamp"],
            y=sub["Acumulado"],
            mode="markers",
            marker=dict(color=COLOR_CANAL[canal], size=7, symbol="circle"),
            name=canal,
            hovertemplate=f"{canal} · %{{y}} acumuladas<extra></extra>",
        ))

    fig.update_layout(
        **LAYOUT_BASE,
        height=350,
        xaxis=dict(title="Tiempo de la jornada", gridcolor="rgba(148,163,184,0.08)"),
        yaxis=dict(title="PQRSD acumuladas", gridcolor="rgba(148,163,184,0.08)"),
        legend=dict(orientation="h", yanchor="top", y=-0.26, x=0),
        title=dict(text="Recepción acumulada en la jornada", x=0.01, xanchor="left"),
    )

    return fig


def fig_produccion(df_prod):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_prod["Periodo"],
        y=df_prod["M2 Exactitud"],
        mode="lines+markers",
        name="M2 Exactitud",
        line=dict(color=VIOLETA, width=2.6),
    ))

    fig.add_trace(go.Scatter(
        x=df_prod["Periodo"],
        y=df_prod["M6 Aceptación"],
        mode="lines+markers",
        name="M6 Aceptación",
        line=dict(color=CYAN, width=2.6),
    ))

    fig.add_trace(go.Bar(
        x=df_prod["Periodo"],
        y=df_prod["Drift"],
        name="Drift",
        marker_color="rgba(245,158,11,0.55)",
        yaxis="y2",
    ))

    fig.update_layout(
        **LAYOUT_BASE,
        height=360,
        xaxis=dict(title="Periodo en producción", dtick=1),
        yaxis=dict(title="Desempeño (%)", range=[0, 105]),
        yaxis2=dict(
            title="Drift (%)",
            overlaying="y",
            side="right",
            range=[0, 35],
            showgrid=False,
        ),
        legend=dict(orientation="h", yanchor="top", y=-0.24, x=0),
        title=dict(text="Monitoreo en producción", x=0.01, xanchor="left"),
    )

    return fig


# ==========================================================
# GRÁFICAS ANIMADAS (HTML + JS NATIVO, SIN DEPENDENCIAS)
# ==========================================================

def html_barras_metricas(metricas, metricas_prev=None, animar=True):
    """Barras de resultado vs. meta. Si `animar` es True, transiciona
    suavemente desde el estado anterior con conteo numérico; si es False,
    se dibuja el estado final sin animación (para re-render sin parpadeo)."""

    nombres = list(UMBRALES.keys())
    uid = f"am-bars-{id(metricas)}"
    filas = []

    for nombre in nombres:
        valor = round(metricas[nombre] * 100, 1)
        previo = round((metricas_prev or {}).get(nombre, 0.0) * 100, 1)
        meta = round(UMBRALES[nombre] * 100, 1)
        cumple = metricas[nombre] >= UMBRALES[nombre]
        color = VERDE if cumple else AMBAR

        filas.append(
            '<div style="display:flex;align-items:center;gap:12px;margin:8px 0;">'
            f'<div style="width:200px;min-width:200px;color:#cbd5e1;'
            f'font-size:12.5px;font-weight:600;text-align:right;">{nombre}</div>'
            '<div style="flex:1;position:relative;height:20px;'
            'background:rgba(148,163,184,0.08);border-radius:10px;overflow:hidden;">'
            '<div class="am-bar" style="position:absolute;left:0;top:0;bottom:0;'
            f'width:{valor}%;border-radius:10px;'
            f'background:linear-gradient(90deg,{color}88,{color});'
            f'box-shadow:0 0 12px {color}55;"></div>'
            f'<div style="position:absolute;left:{min(meta, 100.0)}%;top:-4px;bottom:-4px;'
            'width:2px;background:rgba(248,250,252,0.5);"></div>'
            "</div>"
            '<div class="am-val" style="width:66px;min-width:66px;text-align:right;'
            'font-family:JetBrains Mono,monospace;font-size:13px;font-weight:700;'
            f'color:{color};">{valor:.1f}%</div>'
            "</div>"
        )

    datos_prev = ",".join(
        str(round((metricas_prev or {}).get(n, 0.0) * 100, 1))
        for n in nombres
    )
    datos_curr = ",".join(
        str(round(metricas[n] * 100, 1))
        for n in nombres
    )

    script = f"""
<script>
(function(){{
  var el = document.getElementById("{uid}");
  if (!el) return;
  var prev = el.getAttribute('data-prev').split(',').map(Number);
  var curr = el.getAttribute('data-curr').split(',').map(Number);
  var bars = el.querySelectorAll('.am-bar');
  var vals = el.querySelectorAll('.am-val');
  bars.forEach(function(b, i) {{
    b.style.transition = 'none';
    b.style.width = prev[i] + '%';
  }});
  vals.forEach(function(v, i) {{ v.textContent = prev[i].toFixed(1) + '%'; }});
  requestAnimationFrame(function() {{
    requestAnimationFrame(function() {{
      bars.forEach(function(b, i) {{
        b.style.transition = 'width .9s cubic-bezier(.22,1,.36,1)';
        b.style.width = curr[i] + '%';
      }});
      var t0 = null, dur = 900;
      function paso(ts) {{
        if (t0 === null) t0 = ts;
        var t = Math.min((ts - t0) / dur, 1);
        var e = 1 - Math.pow(1 - t, 3);
        vals.forEach(function(v, i) {{
          v.textContent = (prev[i] + (curr[i] - prev[i]) * e).toFixed(1) + '%';
        }});
        if (t < 1) requestAnimationFrame(paso);
      }}
      requestAnimationFrame(paso);
    }});
  }});
}})();
</script>
""" if animar else ""

    return f"""
<div id="{uid}" style="background:rgba(148,163,184,0.06);border:1px solid rgba(148,163,184,0.18);
border-radius:14px;padding:14px 18px;"
data-prev="{datos_prev}" data-curr="{datos_curr}">
  <div style="display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:6px;margin-bottom:8px;">
    <div style="color:#f1f5f9;font-weight:800;font-size:14.5px;">
      Resultado vs. meta por componente
    </div>
    <div style="display:flex;align-items:center;gap:6px;color:#94a3b8;font-size:11px;">
      <span style="display:inline-block;width:14px;height:2px;
      background:rgba(248,250,252,0.55);"></span> meta mínima
    </div>
  </div>
  {''.join(filas)}
</div>
{script}"""


def html_evolucion_animada(df_historial, animar=True):
    """Líneas de evolución. Si `animar` es True, la línea se dibuja sola y los
    puntos aparecen en cascada; si es False, se muestra el estado final estático."""

    ciclos = df_historial["Ciclo"].astype(int).tolist()
    n = len(ciclos)
    uid = f"am-evo-{id(df_historial)}"

    W, H = 640, 320
    izq, der, sup, inf = 46, 16, 16, 34
    y_min, y_max = 40.0, 105.0

    def px_x(i):
        if n == 1:
            return izq + (W - izq - der) / 2
        return izq + (W - izq - der) * i / (n - 1)

    def px_y(v):
        return sup + (y_max - v) / (y_max - y_min) * (H - sup - inf)

    cuadricula = []

    for v in range(50, 101, 10):
        y = px_y(v)
        cuadricula.append(
            f'<line x1="{izq}" y1="{y:.1f}" x2="{W - der}" y2="{y:.1f}" '
            'stroke="rgba(148,163,184,0.12)" stroke-width="1"/>'
        )
        cuadricula.append(
            f'<text x="{izq - 8}" y="{y + 4:.1f}" text-anchor="end" '
            f'font-size="10.5" fill="#64748b">{v}%</text>'
        )

    etiquetas_x = "".join(
        f'<text x="{px_x(i):.1f}" y="{H - 10}" text-anchor="middle" '
        f'font-size="10.5" fill="#64748b">{c}</text>'
        for i, c in enumerate(ciclos)
    )

    lineas = []
    puntos = []

    for nombre in UMBRALES:
        color = COLORES_METRICAS[nombre]
        valores = df_historial[nombre].astype(float).tolist()
        pts = " ".join(
            f"{px_x(i):.1f},{px_y(v):.1f}"
            for i, v in enumerate(valores)
        )
        lineas.append(
            f'<polyline class="am-line" points="{pts}" fill="none" '
            f'stroke="{color}" stroke-width="2.6" stroke-linecap="round" '
            'stroke-linejoin="round"/>'
        )
        for i, v in enumerate(valores):
            puntos.append(
                f'<circle class="am-pt" cx="{px_x(i):.1f}" cy="{px_y(v):.1f}" '
                f'r="4.5" fill="{color}" stroke="#0b1020" stroke-width="1.6"/>'
            )

    leyenda = "".join(
        '<span style="display:inline-flex;align-items:center;gap:5px;'
        'margin:0 12px 5px 0;color:#94a3b8;font-size:11px;font-weight:600;">'
        f'<span style="width:14px;height:3px;border-radius:2px;'
        f'background:{COLORES_METRICAS[nombre]};display:inline-block;"></span>'
        f"{nombre}</span>"
        for nombre in UMBRALES
    )

    script = f"""
<script>
(function(){{
  var el = document.getElementById("{uid}");
  if (!el) return;
  var st = document.createElement('style');
  st.textContent =
    '@keyframes amPop{{0%{{transform:scale(0);opacity:0}}' +
    '60%{{transform:scale(1.4);opacity:1}}100%{{transform:scale(1);opacity:1}}}}' +
    '.am-pt{{transform-box:fill-box;transform-origin:center;}}';
  document.head.appendChild(st);
  var lines = el.querySelectorAll('.am-line');
  lines.forEach(function(l) {{
    l.style.strokeDasharray = '2000';
    l.style.strokeDashoffset = '2000';
    l.style.transition = 'stroke-dashoffset 1.15s cubic-bezier(.4,0,.2,1) .1s';
  }});
  var pts = el.querySelectorAll('.am-pt');
  pts.forEach(function(c, i) {{
    c.style.animation = 'amPop .5s cubic-bezier(.34,1.56,.64,1) ' +
      (0.5 + i * 0.12) + 's both';
  }});
  requestAnimationFrame(function() {{
    requestAnimationFrame(function() {{
      lines.forEach(function(l) {{ l.style.strokeDashoffset = '0'; }});
    }});
  }});
}})();
</script>
""" if animar else ""

    return f"""
<div id="{uid}" style="background:rgba(148,163,184,0.06);border:1px solid rgba(148,163,184,0.18);
border-radius:14px;padding:14px 18px;">
  <div style="color:#f1f5f9;font-weight:800;font-size:14.5px;margin-bottom:6px;">
    Evolución del refinamiento
  </div>
  <svg viewBox="0 0 {W} {H}" style="width:100%;height:auto;display:block;">
    {''.join(cuadricula)}
    {etiquetas_x}
    {''.join(lineas)}
    {''.join(puntos)}
  </svg>
  <div style="margin-top:6px;">{leyenda}</div>
</div>
{script}"""


def html_equidad(disparidad):
    """Indicador de equidad algorítmica: disparidad entre grupos con su
    semáforo (<3% verde, 3–5% amarillo, 5–10% naranja, >10% rojo)."""

    pct = disparidad * 100
    nivel, color = nivel_equidad(disparidad)

    # barra con las zonas del semáforo; marcador en el valor actual
    ancho = min(max(pct, 0.0), 15.0) / 15.0 * 100

    return f"""
<div style="background:rgba(148,163,184,0.06);border:1px solid rgba(148,163,184,0.18);
border-radius:14px;padding:12px 18px;margin-top:10px;">
  <div style="display:flex;justify-content:space-between;align-items:center;
  flex-wrap:wrap;gap:6px;margin-bottom:8px;">
    <div style="color:#f1f5f9;font-weight:800;font-size:14.5px;">
      ⚖️ Equidad algorítmica
    </div>
    <div style="font-family:JetBrains Mono,monospace;font-size:14px;font-weight:700;color:{color};">
      {pct:.1f}% de disparidad
    </div>
  </div>

  <div style="position:relative;height:16px;border-radius:8px;overflow:hidden;
  background:linear-gradient(90deg,
    rgba(16,185,129,0.5) 0%, rgba(16,185,129,0.5) 20%,
    rgba(245,158,11,0.5) 20%, rgba(245,158,11,0.5) 33.3%,
    rgba(249,115,22,0.55) 33.3%, rgba(249,115,22,0.55) 66.7%,
    rgba(244,63,94,0.6) 66.7%, rgba(244,63,94,0.6) 100%);">
    <div style="position:absolute;left:{min(pct, 15.0) / 15.0 * 100:.1f}%;top:-4px;bottom:-4px;
    width:2px;background:#f8fafc;box-shadow:0 0 8px rgba(248,250,252,0.8);"></div>
  </div>

  <div style="display:flex;justify-content:space-between;margin-top:5px;
  font-size:10.5px;color:#64748b;">
    <span>🟢 &lt;3%</span><span>🟡 3–5%</span><span>🟠 5–10%</span><span>🔴 &gt;10%</span>
  </div>

  <div style="margin-top:8px;font-size:12px;font-weight:600;color:{color};">{nivel}</div>

  <div style="margin-top:4px;color:#64748b;font-size:11px;">
    Equal Opportunity · Demographic Parity · DIR &gt; 0.80 · FNR por grupo
  </div>
</div>
"""


def html_semaforo_equidad():
    """Protocolo de alerta por disparidad: decisión asociada a cada color."""

    niveles = [
        ("🟢", "<3%", "Verde", "Monitoreo continuo.", VERDE),
        ("🟡", "3–5%", "Amarillo", "Revisión técnica; no detiene el despliegue.", AMBAR),
        ("🟠", "5–10%", "Naranja", "Comité de gestión en 5 días · mitigación para el grupo afectado.", "#fb923c"),
        ("🔴", ">10%", "Rojo", "Suspensión del módulo y notificación al Defensor Delegado.", ROJO),
    ]

    filas = "".join(
        '<div style="display:flex;align-items:flex-start;gap:12px;padding:9px 0;'
        'border-bottom:1px solid rgba(148,163,184,0.12);">'
        f'<span style="min-width:80px;color:{color};font-weight:800;font-size:12.5px;">{icono} {umbral}</span>'
        f'<span style="min-width:82px;color:#e2e8f0;font-weight:700;font-size:12.5px;">{nombre}</span>'
        f'<span style="color:#94a3b8;font-size:12px;line-height:1.4;">{accion}</span>'
        '</div>'
        for icono, umbral, nombre, accion, color in niveles
    )

    return f"""
<div style="background:rgba(148,163,184,0.06);border:1px solid rgba(148,163,184,0.18);
border-radius:14px;padding:12px 18px;margin-top:10px;">
  <div style="color:#f1f5f9;font-weight:800;font-size:13.5px;margin-bottom:6px;">
    Protocolo de alerta por disparidad
  </div>
  {filas}
</div>
"""


# ==========================================================
# GENERACIÓN DE PQRSD
# ==========================================================

# Distribución realista de tipos en la Defensoría del Pueblo (URAB):
# las asesorías (orientación jurídica) son la mayoría, seguidas de las
# quejas; la mediación y la conciliación son minoritarias. Se muestrean
# en rangos para que cada ejecución varíe sin salir de lo plausible.
RANGOS_TIPOS = {
    "Asesoría": (0.45, 0.52),
    "Queja": (0.27, 0.32),
    "Solicitud de Mediación": (0.11, 0.15),
    "Solicitud de Conciliación": (0.06, 0.10),
}


def pesos_tipos():
    """Muestrea proporciones por tipo dentro de rangos realistas y
    las normaliza a 1, de modo que cada jornada sea distinta."""
    crudas = {
        tipo: np.random.uniform(*rango)
        for tipo, rango in RANGOS_TIPOS.items()
    }
    total = sum(crudas.values())
    return [crudas[tipo] / total for tipo in TIPOS]


def generar_pqrsd(contador, ts, pesos):
    tipo = np.random.choice(TIPOS, p=pesos)
    tema = np.random.choice(TEMAS)
    canal = np.random.choice(CANALES, p=[0.55, 0.45])
    urgente = np.random.random() < 0.08

    return {
        "Radicado": f"URAB-{ts.strftime('%Y%m%d')}-{contador:06d}",
        "Timestamp": ts,
        "Hora": ts.strftime("%H:%M"),
        "Canal": canal,
        "Tipo": tipo,
        "Tema": tema,
        "Urgente": urgente,
        "Estado": "Radicada",
    }


# ==========================================================
# COMPONENTES HTML
# ==========================================================

def html_kpis(items):
    chips = "".join(
        f'<div class="kpi-chip">'
        f'<div class="kpi-val">{valor}</div>'
        f'<div class="kpi-lbl">{etiqueta}</div>'
        f'</div>'
        for etiqueta, valor in items
    )
    return f'<div class="kpi-row">{chips}</div>'


def html_feed(feed):
    tarjetas = []

    for p in feed:
        color_tipo = COLOR_TIPO[p["Tipo"]]
        chip_canal = (
            f'<span class="chip" style="background:rgba(34,211,238,0.14);'
            f'color:{COLOR_CANAL["IRIS"]}">IRIS</span>'
            if p["Canal"] == "IRIS"
            else
            f'<span class="chip" style="background:rgba(139,92,246,0.16);'
            f'color:{COLOR_CANAL["VisionWeb"]}">VisionWeb</span>'
        )

        chip_urgente = (
            '<span class="chip chip-urgente">🚨 Urgente</span>'
            if p["Urgente"]
            else ""
        )

        tarjetas.append(
            '<div class="pqrsd-card">'
            '<div class="pqrsd-top">'
            f'<span class="pqrsd-radicado">{p["Radicado"]}</span>'
            f"{chip_canal}"
            "</div>"
            f'<div class="pqrsd-tipo" style="color:{color_tipo}">{p["Tipo"]}</div>'
            f'<div class="pqrsd-tema">{p["Tema"]}</div>'
            '<div class="pqrsd-pie">'
            f'<span>🕒 {p["Hora"]}</span>'
            f'<span>· {p["Estado"]}</span>'
            f"{chip_urgente}"
            "</div>"
            "</div>"
        )

    return "".join(tarjetas)


# ==========================================================
# ESTADO DE SESIÓN
# ==========================================================

st.session_state.setdefault("recepcion_df", None)
st.session_state.setdefault("recepcion_estado", None)
st.session_state.setdefault("sim_resultado", None)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.markdown(
        '<h2 style="margin-bottom:0">🤖 <span style="background:linear-gradient(90deg,#22d3ee,#8b5cf6);'
        '-webkit-background-clip:text;background-clip:text;color:transparent">URAB IA</span></h2>',
        unsafe_allow_html=True,
    )
    st.caption("Concurso LSL 2026 · Defensoría del Pueblo")

    st.divider()

    st.markdown("**🏛️ El piloto en cifras**")

    st.markdown(
        "- ≈300 PQRSD recibidas al día\n"
        "- 4 categorías jurídicas · ~12 sub-temas\n"
        "- 8–10 profesionales · 8 semanas de operación controlada\n"
        "- Módulos M1–M8 · validación humana en toda decisión",
    )

    st.divider()

    st.markdown("**🎯 Metas que evalúa la simulación**")

    st.markdown(
        "- M1 extracción: **≥90%**\n"
        "- M2 accuracy: **≥90%** · recall urgencias: **≥99%**\n"
        "- M4 precisión: **≥85%** · recall duplicados: **≥90%**\n"
        "- M6 aceptación profesional: **≥70%**\n"
        "- Equidad: disparidad **≤5%**",
    )

    st.divider()

    st.markdown("**👤 La IA nunca decide**")

    st.markdown(
        "Competencia de la entidad, priorización de riesgo vital, "
        "respuesta de fondo, corrección de duplicados y cierre del caso "
        "son decisiones exclusivamente humanas.",
    )


# ==========================================================
# PORTADA (HERO)
# ==========================================================

st.markdown(
    """
    <div class="hero">
        <div class="orb o1"></div>
        <div class="orb o2"></div>
        <div class="orb o3"></div>
        <div class="hero-badge">🏛️ Defensoría del Pueblo · URAB · Concurso LSL 2026</div>
        <h1 class="hero-title">URAB <span class="grad-anim">IA</span></h1>
        <div class="hero-sub">
            Inteligencia artificial para el macroproceso de atención y trámite de PQRSD:
            desde la recepción multicanal hasta la operación monitoreada, con el
            profesional defensorial siempre al centro de la decisión.
        </div>
        <div class="hero-tags">
            <span class="hero-tag">📥 Recepción multicanal</span>
            <span class="hero-tag">🧠 Módulos M1 – M8</span>
            <span class="hero-tag">👤 Human in the loop</span>
            <span class="hero-tag">🔗 IRIS ↔ VisionWeb</span>
            <span class="hero-tag">📡 MLOps</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# PESTAÑAS
# ==========================================================

tab_simulacion, tab_resultados, tab_recepcion = st.tabs([
    "🎛️ Simulación en vivo",
    "📊 Resultados",
    "📥 Recepción de PQRSD",
])


# ==========================================================
# TAB 1 · RECEPCIÓN DE PQRSD
# ==========================================================

def generar_recepcion(lote_por_paso, total_recibir, velocidad):
    """Generador de frames de la recepción. Cada `yield` entrega el
    estado de la jornada; el driver lo renderiza, duerme y hace rerun.
    Funciona igual en stlite (WebAssembly) que en el servidor."""

    np.random.seed()

    recibidas = []
    feed = []
    contador = 0
    hora_actual = datetime(2026, 1, 5, 8, 0)
    pesos = pesos_tipos()

    while contador < total_recibir:
        lote = min(lote_por_paso, total_recibir - contador)

        for _ in range(lote):
            hora_actual = hora_actual + timedelta(
                minutes=int(np.random.randint(1, 9))
            )
            nueva = generar_pqrsd(contador + 1, hora_actual, pesos)
            recibidas.append(nueva)
            feed.insert(0, nueva)
            contador += 1

        yield {
            "recibidas": list(recibidas),
            "feed": list(feed[:6]),
            "contador": contador,
            "total": total_recibir,
            "hora": hora_actual,
            "duerme": max(0.02, 1.2 - velocidad),
        }

    yield None

with tab_recepcion:

    st.subheader("📥 Recepción inteligente — M1 en acción")

    st.caption(
        "Observa cómo llegan las PQRSD por los canales IRIS y VisionWeb, "
        "son radicadas y clasificadas en tiempo real."
    )

    col_btn, col_vel, col_lote, col_total = st.columns([1.2, 1, 1, 1])

    with col_vel:
        velocidad_recepcion = st.slider(
            "Velocidad",
            min_value=0.1,
            max_value=1.2,
            value=0.55,
            step=0.05,
            key="vel_recepcion",
        )

    with col_lote:
        lote_por_paso = st.slider(
            "PQRSD por pulso",
            min_value=1,
            max_value=15,
            value=5,
            key="lote_recepcion",
        )

    with col_total:
        total_recibir = st.slider(
            "Total a recibir",
            min_value=20,
            max_value=200,
            value=60,
            step=5,
            key="total_recepcion",
        )

    with col_btn:
        st.write("")
        ejecutar_recepcion = st.button(
            "▶ Iniciar recepción",
            type="primary",
            use_container_width=True,
            key="btn_recepcion",
        )

    if st.button("🔄 Reiniciar recepción", key="btn_reset_recepcion"):
        st.session_state.recepcion_df = None
        st.session_state.recepcion_estado = None
        st.rerun()

    if ejecutar_recepcion:
        st.session_state.recepcion_estado = {
            "gen": generar_recepcion(
                lote_por_paso, total_recibir, velocidad_recepcion
            ),
            "activa": True,
            "ultimo": None,
        }
        st.rerun()

    recepcion_estado = st.session_state.get("recepcion_estado")

    if recepcion_estado is not None and recepcion_estado.get("activa"):

        kpi_area = st.empty()
        donut_area = st.empty()
        feed_area = st.empty()
        barra = st.progress(0.0, text="Iniciando recepción...")

        try:
            item = next(recepcion_estado["gen"])
        except StopIteration:
            item = None

        if item is None:
            recepcion_estado["activa"] = False
            st.session_state.recepcion_estado = recepcion_estado

            ultimo = recepcion_estado.get("ultimo")

            if ultimo is not None:
                st.session_state.recepcion_df = pd.DataFrame(ultimo["recibidas"])
                st.success(
                    f"✅ Recepción completada: {ultimo['contador']} PQRSD radicadas "
                    f"por IRIS y VisionWeb durante la jornada."
                )
        else:
            recepcion_estado["ultimo"] = item
            st.session_state.recepcion_estado = recepcion_estado

            df_parcial = pd.DataFrame(item["recibidas"])
            feed = item["feed"]
            contador = item["contador"]
            hora_actual = item["hora"]

            urgentes = int(df_parcial["Urgente"].sum())
            iris = int((df_parcial["Canal"] == "IRIS").sum())
            visionweb = int((df_parcial["Canal"] == "VisionWeb").sum())

            kpi_area.markdown(
                html_kpis([
                    ("Recibidas", f"{contador}"),
                    ("IRIS", f"{iris}"),
                    ("VisionWeb", f"{visionweb}"),
                    ("Urgentes", f"{urgentes}"),
                    ("Hora actual", hora_actual.strftime("%H:%M")),
                ]),
                unsafe_allow_html=True,
            )

            donut_area.plotly_chart(
                fig_donut_tipos(df_parcial),
                config={"displayModeBar": False},
                key=f"donut_recepcion_{contador}",
            )

            feed_area.markdown(
                f'<p style="color:#64748b;font-size:0.8rem;margin:0 0 0.4rem">'
                f"ÚLTIMAS PQRSD RADICADAS</p>{html_feed(feed)}",
                unsafe_allow_html=True,
            )

            barra.progress(
                contador / item["total"],
                text=f"Radicando PQRSD... {contador} de {item['total']}",
            )

            time.sleep(item["duerme"])
            st.rerun()

    df_recepcion = st.session_state.recepcion_df

    if df_recepcion is not None:

        st.divider()

        st.subheader("📊 Resumen de la jornada")

        total = len(df_recepcion)
        urgentes = int(df_recepcion["Urgente"].sum())
        iris = int((df_recepcion["Canal"] == "IRIS").sum())
        visionweb = total - iris

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("PQRSD radicadas", f"{total:,}")
        k2.metric("Vía IRIS", f"{iris:,}")
        k3.metric("Vía VisionWeb", f"{visionweb:,}")
        k4.metric("Prioridad urgencia", f"{urgentes:,}")

        g1, g2 = st.columns(2)

        with g1:
            st.plotly_chart(
                fig_flujo_recepcion(df_recepcion),
                config={"displayModeBar": False},
            )

        with g2:
            st.plotly_chart(
                fig_donut_tipos(df_recepcion),
                config={"displayModeBar": False},
            )

        st.markdown(
            '<div class="banner-human">'
            "<h4>👤 ¿Qué pasa después?</h4>"
            "<p>Cada radicado pasa por <b>M4 anti-duplicación</b> y <b>M2 clasificación y "
            "triaje</b>, y un profesional de la URAB <b>valida</b> la clasificación, el nivel "
            "de urgencia y los sujetos de especial protección antes de asignar el caso. "
            "La IA sugiere; la decisión siempre es humana.</p>"
            "</div>",
            unsafe_allow_html=True,
        )


# ==========================================================
# SIMULACIÓN: GENERADOR DE FRAMES Y RENDER
# ==========================================================

def generar_simulacion(num_pqrsd, calidad_datos, iteraciones_max, nivel_deriva, duracion):
    """Generador de frames de la simulación. Cada `yield` produce un dict con
    el estado a mostrar; el driver lo renderiza y duerme `duerme` segundos."""

    np.random.seed()

    etapas_estimadas = 12 + iteraciones_max * 4
    tiempo_por_evento = duracion / etapas_estimadas

    historial = []
    desplegado = False
    necesita_reentrenamiento = False
    bloqueado_por_equidad = False
    feedback_acumulado = 0
    pqrsd_validas = 0
    disparidad = disparidad_inicial(calidad_datos)

    def frame(tipo, texto, etapa, progreso=None, texto_barra=None,
              metricas=None, metricas_prev=None, historial_frame=None,
              disparidad_frame=None, duerme=0.0, final=False, resultado=None):
        return {
            "tipo": tipo,
            "texto": texto,
            "etapa": etapa,
            "progreso": progreso,
            "texto_barra": texto_barra,
            "metricas": metricas,
            "metricas_prev": metricas_prev,
            "historial": historial_frame,
            "disparidad": disparidad_frame,
            "duerme": duerme,
            "final": final,
            "resultado": resultado,
        }

    # 1. Datos históricos
    yield frame("info", "📥 Recuperando PQRSD históricas desde IRIS y VisionWeb...",
                "datos", 5, "Recuperando datos históricos", duerme=tiempo_por_evento)

    # 2. Preparación
    pqrsd_validas = int(num_pqrsd * calidad_datos)
    yield frame("info", "🧹 Consolidando, depurando y preparando los datos...",
                "preparacion", 12, f"Datos aptos: {pqrsd_validas:,} de {num_pqrsd:,}",
                duerme=tiempo_por_evento)

    # 3. Adaptación de modelos
    metricas = simular_metricas_iniciales(calidad_datos)
    metricas_prev = None
    yield frame("info", "🧠 Adaptando los modelos de IA al contexto de la URAB...",
                "modelos", 20, "Modelos adaptados",
                metricas=metricas, metricas_prev=metricas_prev,
                disparidad_frame=disparidad,
                duerme=tiempo_por_evento)

    # 4. Ciclos de refinamiento
    for ciclo in range(1, iteraciones_max + 1):

        yield frame("warning", f"🔬 Ciclo {ciclo}: evaluando desempeño de los modelos...",
                    "evaluacion", duerme=tiempo_por_evento)

        yield frame("warning", f"⚙️ Ciclo {ciclo}: ejecutando refinamiento...",
                    "refinamiento", duerme=tiempo_por_evento)

        promedio = np.mean(list(metricas.values()))
        errores_estimados = int(pqrsd_validas * (1 - promedio))
        correcciones = int(errores_estimados * np.random.uniform(0.65, 0.90))
        feedback_acumulado += correcciones / max(pqrsd_validas, 1)

        yield frame("warning", f"👤 Ciclo {ciclo}: profesionales URAB validando resultados...",
                    "human", duerme=tiempo_por_evento)

        registro = {"Ciclo": ciclo}
        for k, v in metricas.items():
            registro[k] = round(v * 100, 2)
        registro["Correcciones profesionales"] = correcciones
        historial.append(registro)

        progreso_actual = min(20 + int(ciclo / iteraciones_max * 50), 70)

        yield frame("warning", f"🎯 Ciclo {ciclo}: verificando criterios de aceptación...",
                    "criterios", progreso_actual, f"Ciclo {ciclo} de {iteraciones_max}",
                    metricas=metricas, metricas_prev=metricas_prev,
                    historial_frame=list(historial),
                    duerme=tiempo_por_evento)

        metricas_prev = metricas.copy()

        if cumple_criterios(metricas):

            # Gate de equidad: solo se despliega con disparidad ≤ 5%.
            yield frame("warning", f"⚖️ Ciclo {ciclo}: pruebas de equidad algorítmica...",
                        "equidad", disparidad_frame=disparidad,
                        duerme=tiempo_por_evento)

            if disparidad <= 0.05:
                desplegado = True
                yield frame("success", f"✅ Ciclo {ciclo}: criterios y equidad (≤5%) alcanzados.",
                            "equidad", duerme=tiempo_por_evento)
                break
            else:
                bloqueado_por_equidad = True
                yield frame("warning",
                            f"⚠️ Ciclo {ciclo}: metas cumplidas, pero la disparidad de equidad "
                            f"es de {disparidad * 100:.1f}% (>5%). Se refina para reducir el sesgo.",
                            "equidad", duerme=tiempo_por_evento)

        metricas = refinar_modelos(metricas, feedback_acumulado)
        disparidad = refinar_equidad(disparidad)

    # 5. Despliegue y producción
    produccion = []

    if desplegado:

        yield frame("success", "🚀 Desplegando modelos y agentes en producción...",
                    "deploy", 75, "Despliegue en curso", duerme=tiempo_por_evento)

        yield frame("success", "🔗 Activando interoperabilidad con IRIS y VisionWeb...",
                    "integracion", 80, "Interoperabilidad activa", duerme=tiempo_por_evento)

        yield frame("success", "📨 Solución operando sobre nuevas PQRSD...",
                    "operacion", 85, "Operando PQRSD", duerme=tiempo_por_evento)

        # Operaciones de ML: los 6 periodos de drift se agrupan en un solo frame.
        yield frame("info", "📡 Operaciones de ML monitoreando desempeño y drift...",
                    "mlops", duerme=tiempo_por_evento / 2 * 6)

        metricas_prod = metricas.copy()

        for periodo in range(1, 7):
            deriva_periodo = nivel_deriva * periodo / 6
            ruido = np.random.uniform(0.001, 0.008)

            exactitud_prod = limitar_componente(
                "M2 Exactitud",
                metricas_prod["M2 Exactitud"] - deriva_periodo - ruido,
            )
            aceptacion_prod = limitar_componente(
                "M6 Aceptación",
                metricas_prod["M6 Aceptación"] - deriva_periodo * 0.70,
            )
            produccion.append({
                "Periodo": periodo,
                "M2 Exactitud": round(exactitud_prod * 100, 2),
                "M6 Aceptación": round(aceptacion_prod * 100, 2),
                "Drift": round(deriva_periodo * 100, 2),
            })

        ultimo = produccion[-1]

        if (
            ultimo["M2 Exactitud"] < UMBRALES["M2 Exactitud"] * 100
            or ultimo["M6 Aceptación"] < UMBRALES["M6 Aceptación"] * 100
            or ultimo["Drift"] > 10
        ):
            necesita_reentrenamiento = True

        yield frame("info", "🔄 Incorporando retroalimentación profesional y nuevos datos...",
                    "feedback", 92, "Monitoreo activo", duerme=tiempo_por_evento)

    else:
        if bloqueado_por_equidad:
            yield frame("error", "❌ No se logró reducir la disparidad de equidad al 5%. "
                        "La versión no será promovida a producción.",
                        "equidad", duerme=tiempo_por_evento)
        else:
            yield frame("error", "❌ No se alcanzaron todos los criterios. "
                        "La versión no será promovida a producción.",
                        "criterios", duerme=tiempo_por_evento)

    # 6. Finalización
    if desplegado:
        tipo_final = "success"
        texto_final = "✅ Simulación finalizada: la solución fue desplegada y monitoreada."
        etapa_final = "feedback"
    elif bloqueado_por_equidad:
        tipo_final = "error"
        texto_final = "❌ Simulación finalizada: no se superó el gate de equidad (disparidad >5%)."
        etapa_final = "equidad"
    else:
        tipo_final = "error"
        texto_final = "❌ Simulación finalizada: no se alcanzaron los criterios de aceptación."
        etapa_final = "criterios"

    yield frame(
        tipo_final,
        texto_final,
        etapa_final,
        100, "Simulación finalizada",
        final=True,
        resultado={
            "metricas": metricas,
            "historial": historial,
            "desplegado": desplegado,
            "produccion": produccion,
            "retraining": necesita_reentrenamiento,
            "disparidad": disparidad,
            "bloqueado_por_equidad": bloqueado_por_equidad,
            "validas": pqrsd_validas,
            "rechazadas": num_pqrsd - pqrsd_validas,
            "num_pqrsd": num_pqrsd,
        },
    )


def render_frame(frame, vis, estado_texto, grafico_dinamico, pista_dinamica,
                 barra_progreso, metricas_dinamicas, evolucion_dinamica,
                 equidad_dinamica):
    """Renderiza un frame de la simulación en los contenedores dinámicos."""

    metodos = {
        "info": estado_texto.info,
        "warning": estado_texto.warning,
        "success": estado_texto.success,
        "error": estado_texto.error,
    }
    metodos[frame["tipo"]](frame["texto"])

    grafico_dinamico.markdown(
        html_pipeline(frame["etapa"]),
        unsafe_allow_html=True,
    )
    pista_dinamica.markdown(
        html_pista_pipeline(frame["etapa"]),
        unsafe_allow_html=True,
    )

    if frame["progreso"] is not None:
        barra_progreso.progress(frame["progreso"], text=frame["texto_barra"])

    if frame["metricas"] is not None:
        vis["metricas"] = frame["metricas"]
        vis["metricas_prev"] = frame["metricas_prev"]
        vis["animar_metricas"] = True

    if vis.get("metricas") is not None:
        metricas_dinamicas.html(
            html_barras_metricas(
                vis["metricas"],
                vis.get("metricas_prev"),
                animar=vis.get("animar_metricas", False),
            ),
            unsafe_allow_javascript=True,
        )
        vis["animar_metricas"] = False

    if frame["historial"] is not None:
        vis["historial"] = frame["historial"]
        vis["animar_evolucion"] = True

    if vis.get("historial") is not None:
        evolucion_dinamica.html(
            html_evolucion_animada(
                pd.DataFrame(vis["historial"]),
                animar=vis.get("animar_evolucion", False),
            ),
            unsafe_allow_javascript=True,
        )
        vis["animar_evolucion"] = False

    if frame["disparidad"] is not None:
        vis["disparidad"] = frame["disparidad"]

    if vis.get("disparidad") is not None:
        equidad_dinamica.html(
            html_equidad(vis["disparidad"]),
            unsafe_allow_javascript=True,
        )


# ==========================================================
# TAB 2 · SIMULACIÓN EN VIVO
# ==========================================================

with tab_simulacion:

    st.subheader("🎛️ Simulación del ciclo de vida de la solución")

    st.caption(
        "Ajusta los parámetros y observa cómo la solución entrena, refina, "
        "valida y opera bajo monitoreo continuo."
    )

    s1, s2, s3, s4, s5 = st.columns(5)

    with s1:
        num_pqrsd = st.slider(
            "PQRSD de entrenamiento",
            min_value=100,
            max_value=5000,
            value=1000,
            step=100,
            key="sim_num_pqrsd",
        )

    with s2:
        calidad_datos = st.slider(
            "Calidad inicial de datos",
            min_value=0.60,
            max_value=1.00,
            value=0.82,
            step=0.01,
            key="sim_calidad",
        )

    with s3:
        iteraciones_max = st.slider(
            "Ciclos de refinamiento",
            min_value=1,
            max_value=10,
            value=5,
            key="sim_iteraciones",
        )

    with s4:
        nivel_deriva = st.slider(
            "Drift en producción",
            min_value=0.00,
            max_value=0.30,
            value=0.08,
            step=0.01,
            key="sim_deriva",
        )

    with s5:
        duracion_simulacion = st.slider(
            "Duración (segundos)",
            min_value=5,
            max_value=60,
            value=20,
            step=5,
            key="sim_duracion",
        )

    col_ejecutar, col_reiniciar = st.columns([1.2, 1])

    with col_ejecutar:
        ejecutar = st.button(
            "▶ Ejecutar simulación",
            type="primary",
            use_container_width=True,
            key="btn_sim",
        )

    with col_reiniciar:
        if st.button("🔄 Reiniciar simulación", key="btn_sim_reset"):
            st.session_state.sim_resultado = None
            st.session_state.sim_estado = None
            st.rerun()

    sim = st.session_state.get("sim_estado")

    if sim and sim.get("activa"):
        c_pausa, c_reanudar, c_terminar = st.columns(3)

        with c_pausa:
            if st.button("⏸ Pausar", key="btn_pausa", use_container_width=True):
                sim["pausada"] = True
                st.rerun()

        with c_reanudar:
            if st.button("▶ Reanudar", key="btn_reanudar", use_container_width=True):
                sim["pausada"] = False
                st.rerun()

        with c_terminar:
            if st.button("⏹ Terminar", key="btn_terminar", use_container_width=True):
                st.session_state.sim_estado = None
                st.rerun()

    st.divider()

    estado_texto = st.empty()
    grafico_dinamico = st.empty()
    pista_dinamica = st.empty()
    barra_progreso = st.progress(0, text="Lista para ejecutar")
    metricas_dinamicas = st.empty()
    evolucion_dinamica = st.empty()
    equidad_dinamica = st.empty()

    if ejecutar:
        st.session_state.sim_estado = {
            "gen": generar_simulacion(
                num_pqrsd, calidad_datos, iteraciones_max,
                nivel_deriva, duracion_simulacion,
            ),
            "pausada": False,
            "activa": True,
            "frame": None,
            "vis": {},
        }
        sim = st.session_state.sim_estado

    if sim and sim.get("activa"):
        if sim.get("pausada"):
            if sim.get("frame") is not None:
                f_pausa = dict(sim["frame"])
                f_pausa["metricas"] = None
                f_pausa["historial"] = None
                f_pausa["disparidad"] = None
                render_frame(
                    f_pausa, sim["vis"], estado_texto, grafico_dinamico,
                    pista_dinamica, barra_progreso, metricas_dinamicas,
                    evolucion_dinamica, equidad_dinamica,
                )
            st.caption("⏸ Simulación en pausa — pulsa ▶ Reanudar para continuar.")
        else:
            try:
                frame = next(sim["gen"])
            except StopIteration:
                frame = None

            if frame is not None:
                render_frame(
                    frame, sim["vis"], estado_texto, grafico_dinamico,
                    pista_dinamica, barra_progreso, metricas_dinamicas,
                    evolucion_dinamica, equidad_dinamica,
                )
                sim["frame"] = frame

                if frame["final"]:
                    st.session_state.sim_resultado = frame["resultado"]
                    st.session_state.sim_estado = None
                else:
                    time.sleep(frame["duerme"])
                    st.rerun()


# ==========================================================
# TAB 4 · RESULTADOS
# ==========================================================

with tab_resultados:

    resultado = st.session_state.sim_resultado

    if not resultado:

        st.info(
            "🔍 Aún no hay resultados. Ejecuta la simulación en la pestaña "
            "**🎛️ Simulación en vivo** para ver el desempeño completo aquí."
        )

        c_izq, c_der = st.columns(2)

        with c_izq:
            st.markdown(
                '<div class="card">'
                '<div class="card-icono">🎯</div>'
                '<div class="card-titulo">¿Qué encontrarás aquí?</div>'
                '<div class="card-texto">Métricas finales frente a las metas, evolución por '
                "ciclo de refinamiento, monitoreo de drift en producción y la recomendación "
                "de MLOps al cierre.</div>"
                "</div>",
                unsafe_allow_html=True,
            )

        with c_der:
            st.markdown(
                '<div class="card">'
                '<div class="card-icono">👤</div>'
                '<div class="card-titulo">Human in the loop</div>'
                '<div class="card-texto">Recuerda: la IA nunca decide. Competencia (M3), '
                "priorización de riesgo vital (M2/M6), respuesta de fondo (M6) y cierre (M7) "
                "son decisiones exclusivamente humanas.</div>"
                "</div>",
                unsafe_allow_html=True,
            )

    else:

        st.subheader("📊 Resultados de la simulación")

        k1, k2, k3, k4 = st.columns(4)

        k1.metric(
            "PQRSD analizadas",
            f"{resultado['num_pqrsd']:,}",
        )

        k2.metric(
            "Datos aptos",
            f"{resultado['validas']:,}",
        )

        k3.metric(
            "Ciclos ejecutados",
            len(resultado["historial"]),
        )

        k4.metric(
            "Estado final",
            "Producción" if resultado["desplegado"] else "Refinamiento",
        )

        g1, g2 = st.columns(2)

        with g1:
            st.plotly_chart(
                fig_metricas(resultado["metricas"]),
                config={"displayModeBar": False},
            )

        with g2:
            df_historial = pd.DataFrame(resultado["historial"])

            if not df_historial.empty:
                st.plotly_chart(
                    fig_evolucion(df_historial),
                    config={"displayModeBar": False},
                )

        if not df_historial.empty:

            st.subheader("🔬 Detalle por ciclo")

            st.dataframe(
                df_historial,
                width="stretch",
                hide_index=True,
                column_config={
                    "Ciclo": st.column_config.NumberColumn("Ciclo", format="%d"),
                    "Correcciones profesionales": st.column_config.NumberColumn(
                        "Correcciones profesionales", format="%d"
                    ),
                },
            )

        st.subheader("⚖️ Equidad algorítmica")

        st.markdown(
            html_equidad(resultado["disparidad"]),
            unsafe_allow_html=True,
        )

        st.markdown(
            html_semaforo_equidad(),
            unsafe_allow_html=True,
        )

        if resultado["desplegado"]:

            st.divider()

            st.subheader("📡 Monitoreo en producción")

            df_prod = pd.DataFrame(resultado["produccion"])

            st.plotly_chart(
                fig_produccion(df_prod),
                config={"displayModeBar": False},
            )

            ultimo_prod = df_prod.iloc[-1]
            drift_final = ultimo_prod["Drift"]
            bajo_umbral = (
                ultimo_prod["M2 Exactitud"] < UMBRALES["M2 Exactitud"] * 100
                or ultimo_prod["M6 Aceptación"] < UMBRALES["M6 Aceptación"] * 100
            )

            if drift_final > 10 or bajo_umbral:
                st.error(
                    "🔴 Nivel rojo · Drift >10% o desempeño bajo el umbral: "
                    "suspensión del módulo, notificación al Defensor Delegado y "
                    "nuevo ciclo de refinamiento con validación humana."
                )
            elif drift_final > 5:
                st.warning(
                    "🟠 Nivel naranja · Drift 5–10%: comité de gestión en 5 días "
                    "y mitigación para el grupo afectado."
                )
            elif drift_final >= 3:
                st.warning(
                    "🟡 Nivel amarillo · Drift 3–5%: revisión técnica, "
                    "no detiene el despliegue."
                )
            else:
                st.success(
                    "🟢 Nivel verde · Drift <3%: monitoreo continuo, "
                    "desempeño estable dentro de los criterios."
                )

        st.divider()

        st.markdown(
            '<div class="banner-human">'
            "<h4>🧭 Conclusión</h4>"
            "<p>URAB IA automatiza lo repetitivo —recepción, extracción, clasificación, "
            "borradores— y libera al profesional defensorial para lo que exige criterio "
            "jurídico y empatía. Métricas de desempeño con umbrales exigentes, validación "
            "humana en toda decisión, equidad como requisito de despliegue y MLOps para "
            "evolucionar sin perder control.</p>"
            "</div>",
            unsafe_allow_html=True,
        )


# ==========================================================
# PIE DE PÁGINA
# ==========================================================

st.divider()

st.markdown(
    '<p style="text-align:center;color:#475569;font-size:0.8rem">'
    "LSL 2026 · Concurso de Innovación Legal · Defensoría del Pueblo · "
    "Demostración interactiva — Ciencia de Datos"
    "</p>",
    unsafe_allow_html=True,
)

import streamlit as st
import pandas as pd
import numpy as np
import time


# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================

st.set_page_config(
    page_title="Simulador IA - URAB",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Simulador del Ciclo de Vida de IA - URAB")

st.caption(
    "Entrenamiento · Refinamiento · Validación · "
    "Despliegue · Operaciones de ML · Evolución"
)

st.info(
    "La simulación representa de forma gráfica y dinámica cómo "
    "evoluciona la solución de IA desde la preparación de datos "
    "hasta su operación y monitoreo."
)


# ==========================================================
# CONFIGURACIÓN DE LA SIMULACIÓN
# ==========================================================

st.sidebar.header("⚙️ Configuración de la simulación")

num_pqrsd = st.sidebar.slider(
    "PQRSD utilizadas",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

calidad_datos = st.sidebar.slider(
    "Calidad inicial de los datos",
    min_value=0.60,
    max_value=1.00,
    value=0.82,
    step=0.01
)

iteraciones_max = st.sidebar.slider(
    "Máximo de ciclos de refinamiento",
    min_value=1,
    max_value=10,
    value=5
)

nivel_deriva = st.sidebar.slider(
    "Drift esperado en producción",
    min_value=0.00,
    max_value=0.30,
    value=0.08,
    step=0.01
)

st.sidebar.divider()

# ==========================================================
# CONTROL DE TIEMPO
# ==========================================================

st.sidebar.subheader("⏱️ Tiempo de ejecución")

duracion_simulacion = st.sidebar.slider(
    "Duración aproximada de la simulación",
    min_value=5,
    max_value=60,
    value=20,
    step=5,
    format="%d segundos"
)

st.sidebar.caption(
    "El tiempo seleccionado se distribuye entre las diferentes "
    "fases y ciclos de refinamiento."
)

st.sidebar.divider()

# ==========================================================
# RANGOS Y METAS DE LOS COMPONENTES
# ==========================================================

st.sidebar.subheader("📐 Rangos de los componentes")

st.sidebar.caption(
    "Define el rango permitido de cada componente durante la simulación "
    "y la meta mínima que debe alcanzar para ser aceptado."
)


def configurar_componente(nombre, rango_default, meta_default, clave):

    with st.sidebar.expander(nombre, expanded=False):

        rango = st.slider(
            "Rango de simulación (%)",
            min_value=0.0,
            max_value=100.0,
            value=(float(rango_default[0]), float(rango_default[1])),
            step=1.0,
            key=f"rango_{clave}"
        )

        meta = st.number_input(
            "Meta mínima de aceptación (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(meta_default),
            step=1.0,
            key=f"meta_{clave}"
        )

    return (rango[0] / 100, rango[1] / 100), meta / 100


rango_m1, meta_m1 = configurar_componente(
    "M1 · Extracción",
    (70, 100),
    90,
    "m1_extraccion"
)

rango_m2_exactitud, meta_m2_exactitud = configurar_componente(
    "M2 · Exactitud",
    (65, 100),
    90,
    "m2_exactitud"
)

rango_m2_sensibilidad, meta_m2_sensibilidad = configurar_componente(
    "M2 · Sensibilidad de urgencias",
    (85, 100),
    99,
    "m2_sensibilidad"
)

rango_m4_precision, meta_m4_precision = configurar_componente(
    "M4 · Precisión",
    (65, 100),
    85,
    "m4_precision"
)

rango_m4_sensibilidad, meta_m4_sensibilidad = configurar_componente(
    "M4 · Sensibilidad",
    (65, 100),
    90,
    "m4_sensibilidad"
)

rango_m6, meta_m6 = configurar_componente(
    "M6 · Aceptación",
    (45, 100),
    70,
    "m6_aceptacion"
)


RANGOS_COMPONENTES = {
    "M1 Extracción": rango_m1,
    "M2 Exactitud": rango_m2_exactitud,
    "M2 Sensibilidad de urgencias": rango_m2_sensibilidad,
    "M4 Precisión": rango_m4_precision,
    "M4 Sensibilidad": rango_m4_sensibilidad,
    "M6 Aceptación": rango_m6
}


UMBRALES = {
    "M1 Extracción": meta_m1,
    "M2 Exactitud": meta_m2_exactitud,
    "M2 Sensibilidad de urgencias": meta_m2_sensibilidad,
    "M4 Precisión": meta_m4_precision,
    "M4 Sensibilidad": meta_m4_sensibilidad,
    "M6 Aceptación": meta_m6
}


# Advertir cuando una meta está por encima del máximo configurado.
metas_imposibles = [
    nombre
    for nombre, meta in UMBRALES.items()
    if meta > RANGOS_COMPONENTES[nombre][1]
]

if metas_imposibles:
    st.sidebar.warning(
        "La meta supera el máximo del rango en: "
        + ", ".join(metas_imposibles)
    )



# ==========================================================
# FUNCIONES
# ==========================================================

def limitar(valor, minimo=0, maximo=1):
    return max(minimo, min(maximo, valor))


def limitar_componente(nombre, valor):
    minimo, maximo = RANGOS_COMPONENTES[nombre]
    return limitar(valor, minimo, maximo)


def pausa(tiempo_base):
    """
    Pausa proporcional a la duración configurada.
    """
    time.sleep(tiempo_base)


def simular_metricas_iniciales(calidad):

    # Convertir la calidad (0.60 - 1.00) a un factor normalizado (0 - 1).
    factor_calidad = limitar(
        (calidad - 0.60) / 0.40,
        0,
        1
    )

    def valor_en_rango(nombre):

        minimo, maximo = RANGOS_COMPONENTES[nombre]

        # La calidad desplaza el resultado hacia la parte alta del rango.
        valor_base = minimo + (maximo - minimo) * factor_calidad

        # Pequeña variación aleatoria para que cada ejecución sea diferente.
        amplitud = maximo - minimo
        variacion = np.random.uniform(
            -amplitud * 0.08,
            amplitud * 0.08
        )

        return limitar(
            valor_base + variacion,
            minimo,
            maximo
        )

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

    # M1 - Ajuste fino
    nuevas["M1 Extracción"] = limitar_componente(
        "M1 Extracción",
        nuevas["M1 Extracción"]
        + np.random.uniform(0.008, 0.025)
        + feedback * 0.005
    )

    # M2 - Ajuste fino
    nuevas["M2 Exactitud"] = limitar_componente(
        "M2 Exactitud",
        nuevas["M2 Exactitud"]
        + np.random.uniform(0.012, 0.035)
        + feedback * 0.006
    )

    # Sensibilidad de urgencias
    nuevas["M2 Sensibilidad de urgencias"] = limitar_componente(
        "M2 Sensibilidad de urgencias",
        nuevas["M2 Sensibilidad de urgencias"]
        + np.random.uniform(0.006, 0.022)
        + feedback * 0.004
    )

    # M4 - Calibración semántica
    nuevas["M4 Precisión"] = limitar_componente(
        "M4 Precisión",
        nuevas["M4 Precisión"]
        + np.random.uniform(0.010, 0.030)
    )

    nuevas["M4 Sensibilidad"] = limitar_componente(
        "M4 Sensibilidad",
        nuevas["M4 Sensibilidad"]
        + np.random.uniform(0.010, 0.030)
    )

    # M6 - RAG + ajuste de instrucciones
    nuevas["M6 Aceptación"] = limitar_componente(
        "M6 Aceptación",
        nuevas["M6 Aceptación"]
        + np.random.uniform(0.015, 0.045)
        + feedback * 0.008
    )

    return nuevas


# ==========================================================
# TABLA DE MÉTRICAS
# ==========================================================

def tabla_metricas(metricas):

    filas = []

    for nombre, valor in metricas.items():

        objetivo = UMBRALES[nombre]

        filas.append({
            "Componente": nombre,
            "Resultado": round(valor * 100, 2),
            "Meta": round(objetivo * 100, 2),
            "Estado":
                "✅ Cumple"
                if valor >= objetivo
                else "⚠️ Refinar"
        })

    return pd.DataFrame(filas)


# ==========================================================
# RESULTADOS DETALLADOS POR CICLO
# ==========================================================

def tabla_resultados_ciclo(registro_ciclo):

    filas = []

    for nombre, objetivo in UMBRALES.items():

        resultado_componente = float(
            registro_ciclo[nombre]
        )

        meta_porcentaje = objetivo * 100

        filas.append({
            "Componente": nombre,
            "Resultado (%)": round(
                resultado_componente,
                2
            ),
            "Meta configurada (%)": round(
                meta_porcentaje,
                2
            ),
            "Estado": (
                "✅ Cumple"
                if resultado_componente >= meta_porcentaje
                else "⚠️ Refinar"
            )
        })

    return pd.DataFrame(filas)


# ==========================================================
# DIAGRAMA DINÁMICO
# ==========================================================

def construir_diagrama(etapa_activa=None):

    normal = "#F2F2F2"
    activo = "#FFD966"
    completado = "#C6E0B4"

    orden = [
        "datos",
        "preparacion",
        "modelos",
        "evaluacion",
        "refinamiento",
        "human",
        "criterios",
        "deploy",
        "integracion",
        "operacion",
        "mlops",
        "feedback"
    ]

    def color(etapa):

        if etapa_activa is None:
            return normal

        if etapa == etapa_activa:
            return activo

        try:

            indice_actual = orden.index(etapa_activa)
            indice_etapa = orden.index(etapa)

            if indice_etapa < indice_actual:
                return completado

        except ValueError:
            pass

        return normal


    return f"""
    digraph URAB {{

        graph [
            rankdir=LR,
            bgcolor="transparent",
            pad="0.4",
            nodesep="0.40",
            ranksep="0.60",
            splines=ortho
        ]

        node [
            shape=box,
            style="rounded,filled",
            fontname="Arial",
            fontsize=10,
            margin="0.16"
        ]

        edge [
            fontname="Arial",
            fontsize=9,
            arrowsize=0.8,
            penwidth=1.4
        ]


        A [
            label="PQRSD históricas\\nIRIS + VisionWeb",
            fillcolor="{color('datos')}"
        ]


        B [
            label="Preparación y consolidación\\nde datos",
            fillcolor="{color('preparacion')}"
        ]


        C [
            label="ADAPTACIÓN DE MODELOS\\n\\nM1 · Ajuste fino\\nM2 · Ajuste fino\\nM4 · Vectores semánticos\\nM6 · RAG",
            fillcolor="{color('modelos')}"
        ]


        D [
            label="Evaluación\\nMétricas de desempeño",
            fillcolor="{color('evaluacion')}"
        ]


        E [
            label="REFINAMIENTO\\n\\nM1 + M2 · Ajuste fino\\nM4 · Calibración semántica\\nM6 · RAG + ajuste de instrucciones",
            fillcolor="{color('refinamiento')}"
        ]


        F [
            label="Validación humana\\nValidación profesional URAB",
            fillcolor="{color('human')}"
        ]


        G [
            label="¿Cumple criterios\\nde aceptación?",
            shape=diamond,
            fillcolor="{color('criterios')}"
        ]


        H [
            label="Despliegue\\na producción",
            fillcolor="{color('deploy')}"
        ]


        I [
            label="M7 · Interoperabilidad\\nIRIS ↔ IA ↔ VisionWeb",
            fillcolor="{color('integracion')}"
        ]


        J [
            label="Operación integral\\nde PQRSD",
            fillcolor="{color('operacion')}"
        ]


        K [
            label="Operaciones de ML\\nVersionamiento · Monitoreo\\nDrift · Trazabilidad",
            fillcolor="{color('mlops')}"
        ]


        L [
            label="Retroalimentación profesional\\n+ nuevos datos",
            fillcolor="{color('feedback')}"
        ]


        A -> B
        B -> C
        C -> D

        D -> E
        E -> F
        F -> G

        G -> H [
            label=" Cumple"
        ]

        G -> D [
            label=" Refinar",
            style=dashed
        ]

        H -> I
        I -> J
        J -> K
        K -> L

        L -> D [
            label=" Nuevo ciclo",
            style=dashed
        ]
    }}
    """


# ==========================================================
# ESTADO DE SESIÓN
# ==========================================================

if "resultado" not in st.session_state:
    st.session_state.resultado = None


# ==========================================================
# BOTONES
# ==========================================================

col1, col2, col3 = st.columns([1.4, 1, 4])

with col1:

    ejecutar = st.button(
        "▶ Ejecutar simulación",
        type="primary",
        use_container_width=True
    )

with col2:

    if st.button(
        "🔄 Reiniciar",
        use_container_width=True
    ):

        st.session_state.resultado = None
        st.rerun()


# ==========================================================
# ÁREA DINÁMICA
# ==========================================================

st.divider()

st.subheader("🔄 Flujo de ejecución")

estado_texto = st.empty()

grafico_dinamico = st.empty()

barra_progreso = st.progress(0)

metricas_dinamicas = st.empty()


# ==========================================================
# EJECUCIÓN DE LA SIMULACIÓN
# ==========================================================

if ejecutar:

    np.random.seed()

    # ------------------------------------------------------
    # CÁLCULO DE TIEMPO
    # ------------------------------------------------------

    etapas_estimadas = 12 + iteraciones_max * 4

    tiempo_por_evento = (
        duracion_simulacion / etapas_estimadas
    )

    historial = []

    desplegado = False
    necesita_reentrenamiento = False

    feedback_acumulado = 0

    # ======================================================
    # 1. DATOS HISTÓRICOS
    # ======================================================

    estado_texto.info(
        "📥 Recuperando PQRSD históricas desde IRIS y VisionWeb..."
    )

    grafico_dinamico.graphviz_chart(
        construir_diagrama("datos"),
        use_container_width=True
    )

    barra_progreso.progress(5)

    pausa(tiempo_por_evento)


    # ======================================================
    # 2. PREPARACIÓN
    # ======================================================

    estado_texto.info(
        "🧹 Consolidando, depurando y preparando los datos..."
    )

    grafico_dinamico.graphviz_chart(
        construir_diagrama("preparacion"),
        use_container_width=True
    )

    pqrsd_validas = int(
        num_pqrsd * calidad_datos
    )

    pqrsd_rechazadas = (
        num_pqrsd - pqrsd_validas
    )

    barra_progreso.progress(12)

    pausa(tiempo_por_evento)


    # ======================================================
    # 3. ADAPTACIÓN DE MODELOS
    # ======================================================

    estado_texto.info(
        "🧠 Adaptando los modelos de IA al contexto de la URAB..."
    )

    grafico_dinamico.graphviz_chart(
        construir_diagrama("modelos"),
        use_container_width=True
    )

    metricas = simular_metricas_iniciales(
        calidad_datos
    )

    metricas_dinamicas.dataframe(
        tabla_metricas(metricas),
        use_container_width=True,
        hide_index=True
    )

    barra_progreso.progress(20)

    pausa(tiempo_por_evento)


    # ======================================================
    # CICLOS DE REFINAMIENTO
    # ======================================================

    for ciclo in range(
        1,
        iteraciones_max + 1
    ):

        # --------------------------------------------------
        # EVALUACIÓN
        # --------------------------------------------------

        estado_texto.warning(
            f"🔬 Ciclo {ciclo}: evaluando desempeño de los modelos..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("evaluacion"),
            use_container_width=True
        )

        pausa(tiempo_por_evento)


        # --------------------------------------------------
        # REFINAMIENTO
        # --------------------------------------------------

        estado_texto.warning(
            f"⚙️ Ciclo {ciclo}: ejecutando refinamiento..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("refinamiento"),
            use_container_width=True
        )

        pausa(tiempo_por_evento)


        # --------------------------------------------------
        # HUMAN IN THE LOOP
        # --------------------------------------------------

        estado_texto.warning(
            f"👤 Ciclo {ciclo}: profesionales URAB validando resultados..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("human"),
            use_container_width=True
        )

        promedio = np.mean(
            list(metricas.values())
        )

        errores_estimados = int(
            pqrsd_validas *
            (1 - promedio)
        )

        correcciones = int(
            errores_estimados *
            np.random.uniform(
                0.65,
                0.90
            )
        )

        feedback_acumulado += (
            correcciones /
            max(pqrsd_validas, 1)
        )

        pausa(tiempo_por_evento)


        # --------------------------------------------------
        # CRITERIOS
        # --------------------------------------------------

        estado_texto.warning(
            f"🎯 Ciclo {ciclo}: verificando criterios de aceptación..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("criterios"),
            use_container_width=True
        )

        registro = {
            "Ciclo": ciclo
        }

        for k, v in metricas.items():
            registro[k] = round(
                v * 100,
                2
            )

        registro[
            "Correcciones profesionales"
        ] = correcciones

        historial.append(registro)

        metricas_dinamicas.dataframe(
            tabla_metricas(metricas),
            use_container_width=True,
            hide_index=True
        )

        progreso_actual = min(
            20 + int(
                ciclo /
                iteraciones_max *
                50
            ),
            70
        )

        barra_progreso.progress(
            progreso_actual
        )

        pausa(tiempo_por_evento)


        # --------------------------------------------------
        # ¿CUMPLE?
        # --------------------------------------------------

        if cumple_criterios(metricas):

            desplegado = True

            estado_texto.success(
                f"✅ Ciclo {ciclo}: criterios de aceptación alcanzados."
            )

            break


        # --------------------------------------------------
        # NUEVO REFINAMIENTO
        # --------------------------------------------------

        metricas = refinar_modelos(
            metricas,
            feedback_acumulado
        )


    # ======================================================
    # DESPLIEGUE
    # ======================================================

    produccion = []

    if desplegado:

        estado_texto.success(
            "🚀 Desplegando modelos y agentes en producción..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("deploy"),
            use_container_width=True
        )

        barra_progreso.progress(75)

        pausa(tiempo_por_evento)


        # ==================================================
        # M7 INTEROPERABILIDAD
        # ==================================================

        estado_texto.success(
            "🔗 Activando interoperabilidad con IRIS y VisionWeb..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("integracion"),
            use_container_width=True
        )

        barra_progreso.progress(80)

        pausa(tiempo_por_evento)


        # ==================================================
        # OPERACIÓN
        # ==================================================

        estado_texto.success(
            "📨 Solución operando sobre nuevas PQRSD..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("operacion"),
            use_container_width=True
        )

        barra_progreso.progress(85)

        pausa(tiempo_por_evento)


        # ==================================================
        # OPERACIONES DE ML
        # ==================================================

        estado_texto.info(
            "📡 Operaciones de ML monitoreando desempeño y drift..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("mlops"),
            use_container_width=True
        )

        metricas_prod = metricas.copy()

        for periodo in range(1, 7):

            deriva_periodo = (
                nivel_deriva *
                periodo / 6
            )

            ruido = np.random.uniform(
                0.001,
                0.008
            )

            exactitud_prod = limitar_componente(
                "M2 Exactitud",
                metricas_prod["M2 Exactitud"]
                - deriva_periodo
                - ruido
            )

            aceptacion_prod = limitar_componente(
                "M6 Aceptación",
                metricas_prod["M6 Aceptación"]
                - deriva_periodo * 0.70
            )

            produccion.append({
                "Periodo": periodo,
                "M2 Exactitud": round(
                    exactitud_prod * 100,
                    2
                ),
                "M6 Aceptación": round(
                    aceptacion_prod * 100,
                    2
                ),
                "Drift": round(
                    deriva_periodo * 100,
                    2
                )
            })

            pausa(
                tiempo_por_evento / 2
            )


        ultimo = produccion[-1]

        if (
            ultimo["M2 Exactitud"] < UMBRALES["M2 Exactitud"] * 100
            or ultimo["M6 Aceptación"] < UMBRALES["M6 Aceptación"] * 100
            or ultimo["Drift"] > 10
        ):

            necesita_reentrenamiento = True


        barra_progreso.progress(92)


        # ==================================================
        # RETROALIMENTACIÓN
        # ==================================================

        estado_texto.info(
            "🔄 Incorporando retroalimentación profesional y nuevos datos..."
        )

        grafico_dinamico.graphviz_chart(
            construir_diagrama("feedback"),
            use_container_width=True
        )

        pausa(tiempo_por_evento)


    else:

        estado_texto.error(
            "❌ No se alcanzaron todos los criterios. "
            "La versión no será promovida a producción."
        )


    # ======================================================
    # FINALIZACIÓN
    # ======================================================

    barra_progreso.progress(100)

    if desplegado:

        estado_texto.success(
            "✅ Simulación finalizada: "
            "la solución fue desplegada y monitoreada."
        )

    grafico_dinamico.graphviz_chart(
        construir_diagrama(
            "feedback"
            if desplegado
            else "criterios"
        ),
        use_container_width=True
    )


    st.session_state.resultado = {
        "metricas": metricas,
        "historial": historial,
        "desplegado": desplegado,
        "produccion": produccion,
        "retraining": necesita_reentrenamiento,
        "validas": pqrsd_validas,
        "rechazadas": pqrsd_rechazadas
    }


# ==========================================================
# RESULTADOS
# ==========================================================

resultado = st.session_state.resultado

if resultado:

    st.divider()

    st.header("📊 Resultados de la simulación")


    # ======================================================
    # RESUMEN
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "PQRSD analizadas",
        f"{num_pqrsd:,}"
    )

    c2.metric(
        "Datos aptos",
        f"{resultado['validas']:,}"
    )

    c3.metric(
        "Ciclos ejecutados",
        len(resultado["historial"])
    )

    c4.metric(
        "Estado",
        "Producción"
        if resultado["desplegado"]
        else "Refinamiento"
    )


    # ======================================================
    # MÉTRICAS
    # ======================================================

    st.subheader("🎯 Métricas finales")

    st.dataframe(
        tabla_metricas(
            resultado["metricas"]
        ),
        use_container_width=True,
        hide_index=True
    )


    # ======================================================
    # RESULTADOS DE LOS COMPONENTES POR CICLO
    # ======================================================

    df_historial = pd.DataFrame(
        resultado["historial"]
    )

    if not df_historial.empty:

        st.subheader(
            "🔬 Resultados de los componentes por ciclo"
        )

        st.caption(
            "Selecciona un ciclo para consultar el resultado obtenido "
            "por cada componente frente a la meta configurada."
        )

        ciclos_disponibles = (
            df_historial["Ciclo"]
            .astype(int)
            .tolist()
        )

        ciclo_seleccionado = st.selectbox(
            "Ciclo de refinamiento",
            options=ciclos_disponibles,
            index=len(ciclos_disponibles) - 1,
            format_func=lambda ciclo: f"Ciclo {ciclo}",
            key="ciclo_resultados_componentes"
        )

        registro_ciclo = (
            df_historial[
                df_historial["Ciclo"] == ciclo_seleccionado
            ]
            .iloc[0]
        )

        tabla_ciclo = tabla_resultados_ciclo(
            registro_ciclo
        )

        total_componentes = len(UMBRALES)
        componentes_cumplen = int(
            (tabla_ciclo["Estado"] == "✅ Cumple").sum()
        )

        col_estado_ciclo, col_correcciones = st.columns(2)

        col_estado_ciclo.metric(
            "Componentes que cumplen",
            f"{componentes_cumplen} de {total_componentes}"
        )

        col_correcciones.metric(
            "Correcciones profesionales",
            int(
                registro_ciclo[
                    "Correcciones profesionales"
                ]
            )
        )

        st.dataframe(
            tabla_ciclo,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Resultado (%)": st.column_config.NumberColumn(
                    "Resultado (%)",
                    format="%.2f %%"
                ),
                "Meta configurada (%)": st.column_config.NumberColumn(
                    "Meta configurada (%)",
                    format="%.2f %%"
                )
            }
        )

        with st.expander(
            "📋 Ver comparativo de todos los ciclos",
            expanded=False
        ):

            columnas_comparativo = [
                "Ciclo",
                "M1 Extracción",
                "M2 Exactitud",
                "M2 Sensibilidad de urgencias",
                "M4 Precisión",
                "M4 Sensibilidad",
                "M6 Aceptación",
                "Correcciones profesionales"
            ]

            st.dataframe(
                df_historial[columnas_comparativo],
                use_container_width=True,
                hide_index=True
            )


        # ==================================================
        # EVOLUCIÓN
        # ==================================================

        st.subheader(
            "📈 Evolución del refinamiento"
        )

        columnas = [
            "M1 Extracción",
            "M2 Exactitud",
            "M2 Sensibilidad de urgencias",
            "M4 Precisión",
            "M4 Sensibilidad",
            "M6 Aceptación"
        ]

        st.line_chart(
            df_historial
            .set_index("Ciclo")[columnas]
        )


    # ======================================================
    # PRODUCCIÓN
    # ======================================================

    if resultado["desplegado"]:

        st.subheader(
            "📡 Monitoreo en producción"
        )

        df_prod = pd.DataFrame(
            resultado["produccion"]
        )

        st.dataframe(
            df_prod,
            use_container_width=True,
            hide_index=True
        )

        st.line_chart(
            df_prod.set_index("Periodo")[
                [
                    "M2 Exactitud",
                    "M6 Aceptación",
                    "Drift"
                ]
            ]
        )

        if resultado["retraining"]:

            st.warning(
                "⚠️ El monitoreo de ML detectó degradación o drift. "
                "Se recomienda iniciar un nuevo ciclo "
                "de refinamiento y validación."
            )

        else:

            st.success(
                "✅ La solución mantiene un desempeño "
                "estable dentro de los criterios definidos."
            )
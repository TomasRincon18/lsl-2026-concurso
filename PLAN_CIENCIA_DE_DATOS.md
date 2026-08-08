# PLAN CIENCIA DE DATOS — Legal Strategy Lab 2026

## CALENDARIO REAL
- **Hoy:** 17 de julio (Día 1)
- **Entrega escrita:** 30 de julio (Día 13)
- **Fase oral (pitch):** 31 jul – 18 ago (20 días extra)

## ESTRATEGIA
**No hay tiempo para prototipado completo.** Tu entregable es un **diseño conceptual y arquitectónico detallado** con especificaciones, diagramas y justificaciones técnicas para cada módulo. Si sobra tiempo, haz un PoC mínimo del clasificador M2 (es el corazón del sistema).

---

## DÍAS 1–2: SETUP E INVESTIGACIÓN (Jul 17–18)

### Setup técnico

```bash
python -m venv lsl-env
source lsl-env/bin/activate
pip install torch transformers datasets accelerate evaluate
pip install spacy sentence-transformers scikit-learn pandas numpy
python -m spacy download es_core_news_lg
pip install fastapi uvicorn pydantic
pip install sqlalchemy psycopg2-binary alembic
pip install chromadb
pip install streamlit plotly
pip install mlflow evidently
```

### Repositorio

```bash
git init lsl-2026
cd lsl-2026
mkdir -p {docs/{diagramas,especificaciones},notebooks,src,data}
```

### Lectura obligatoria (prioridad máxima)

| Documento | Enfocarse en |
|---|---|
| Caso (RFP) | Secciones 2, 3, 4, 5, 6 |
| NIST AI RMF 1.0 | Core functions: Govern, Map, Measure, Manage |
| ISO/IEC 42001:2023 | Estructura del sistema de gestión de IA |
| OECD "Governing with AI" (2024) | Secciones sobre sector público |

### Investigación rápida (1-2 horas por tema)

| Tema | Qué decidir |
|---|---|
| **Modelo NLP español** | ¿BETO o RoBERTa-es para clasificación? BETO es más ligero y está probado en tareas legales → **recomendado: BETO** |
| **LLM open-source** | ¿Llama 3 (8B), Mistral (7B) o Qwen 2.5 (7B)? Para sector público, soberanía de datos → self-hosted. Mistral 7B es el más eficiente para CPU → **recomendado: Mistral 7B** |
| **Embeddings** | `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` para similitud semántica multilingüe. Suficiente para M4 |
| **OCR** | Tesseract LSTM español. Preprocesamiento con OpenCV (deskew, binarización adaptativa) |
| **Vector DB** | ChromaDB (liviano, sin infraestructura extra). Alternativa: pgvector en PostgreSQL |
| **Mensajería** | RabbitMQ para integración IRIS/VisionWeb (estándar en gobierno) |
| **Dashboard** | Streamlit (rápido de prototipar). Mencionar Power BI como opción enterprise |

---

## DÍAS 2–3: ANÁLISIS DEL MACROPROCESO (Jul 18–19)

### Entregables

1. **Diagrama AS-IS** del macroproceso actual:
   ```
   Recepción (web/email/físico/campo) → Verificación legibilidad/completitud 
   → Clasificación inicial (Asesoría/Queja/Mediación/Conciliación) 
   → Análisis de competencia → Asignación interna → Gestión defensorial 
   → Cierre → Archivo (IRIS + VisionWeb)
   ```

2. **Mapeo de los 5 problemas críticos** y cómo cada módulo los ataca:

| Problema | Módulo(s) que lo resuelven |
|---|---|
| Volumen y saturación operativa (~300/día) | M1 (ingesta automática), M2 (clasificación automática), M6 (respuestas automatizables) |
| Riesgo jurídico por represamiento | M2 (priorización), M3 (SLAs y alertas) |
| Duplicidad IRIS/VisionWeb y re-trabajo | M7 (integración y anti-doble registro) |
| Duplicidad de peticiones (hasta 10 veces) | M4 (detección de duplicados) |
| Peticionarios recurrentes sin historial | M5 (historial unificado) |

3. **Diagrama TO-BE** con IA integrada (hacer después del diseño de módulos en Días 4-6)

---

## DÍAS 3–5: DISEÑO DE ARQUITECTURA (Jul 19–21)

### Arquitectura lógica (diagrama de capas)

```
┌──────────────────────────────────────────────────┐
│            CAPA DE PRESENTACIÓN                   │
│   Dashboard (Streamlit) + API Gateway (FastAPI)  │
├──────────────────────────────────────────────────┤
│            CAPA DE SERVICIOS                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │
│  │  M1  │ │  M2  │ │  M3  │ │  M4  │            │
│  │Recepc│ │Clasif│ │Asign │ │Dedup │            │
│  └──────┘ └──────┘ └──────┘ └──────┘            │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐            │
│  │  M5  │ │  M6  │ │  M7  │ │  M8  │            │
│  │Histor│ │GenAI │ │Intero│ │Analit│            │
│  └──────┘ └──────┘ └──────┘ └──────┘            │
├──────────────────────────────────────────────────┤
│         CAPA DE INTEGRACIÓN (M7)                  │
│   RabbitMQ ──── IRIS API ──── VisionWeb API      │
├──────────────────────────────────────────────────┤
│            CAPA DE DATOS                          │
│  PostgreSQL │ ChromaDB (vectores) │ Elasticsearch│
├──────────────────────────────────────────────────┤
│         CAPA DE SEGURIDAD                         │
│   RBAC │ OAuth2/JWT │ TLS 1.3 │ AES-256 │ Logs  │
└──────────────────────────────────────────────────┘
```

### Stack tecnológico final

| Capa | Tecnología | Justificación |
|---|---|---|
| Backend | FastAPI (Python) | Alto rendimiento, async, OpenAPI automático |
| NLP Clasificación | BETO fine-tuned (`dccuchile/bert-base-spanish-wwm-uncased`) | SOTA en español, probado en dominio legal |
| NER | spaCy (`es_core_news_lg`) + fine-tuning | Madurez, pipeline integrado |
| Embeddings | Sentence-Transformers (`paraphrase-multilingual-mpnet-base-v2`) | Similitud semántica probada, multilingüe |
| LLM | Mistral 7B (self-hosted vía Ollama/vLLM) | Open-source, soberanía de datos, eficiente |
| RAG | LangChain + ChromaDB | Framework estándar, vector DB liviano |
| OCR | Tesseract LSTM (`spa`) + OpenCV | Open-source, sin costo, buen rendimiento |
| BD Transaccional | PostgreSQL + pgvector | Robusto, transaccional + vectorial |
| Búsqueda | Elasticsearch | Full-text search escalable |
| Mensajería | RabbitMQ | Estándar empresarial, confiable |
| MLOps | MLflow + DVC + Evidently AI | Trazabilidad completa |
| Dashboard | Streamlit (PoC) + Power BI (prod) | Prototipado rápido + enterprise |
| Infra | Docker + Docker Compose | Portabilidad, consistencia |
| Seguridad | OAuth2/JWT, TLS 1.3, AES-256 | Estándares de industria |

---

## DÍAS 4–7: DISEÑO DETALLADO DE MÓDULOS M1-M8 (Jul 20–23)

> **Producir una especificación de 1-2 páginas por módulo con diagrama de flujo, componentes, tecnologías y métricas esperadas.**

### M1 — Recepción Inteligente

**Pipeline:**
```
Web → JSON ─────────┐
Email → Parser ─────┤
PDF → OCR(Tesseract)─┼──→ NER(spaCy) ──→ Validación completitud ──→ Radicado
Imagen → OCR ────────┤
Formulario campo ────┘
```

**Componentes:**
- **API Gateway:** Endpoints REST para upload (multipart), email webhook, JSON
- **OCR Engine:** Tesseract con preprocesamiento OpenCV (deskew, binarización adaptativa, eliminación de ruido). Modelo `spa` (español). CER esperado <5% en documentos limpios
- **NER Pipeline:** spaCy fine-tuned. Entidades: nombre, tipo_doc, num_doc, direccion, telefono, email, hecho, pretension
- **Validador de completitud:** Reglas declarativas. Si falta campo crítico → respuesta automática solicitando info
- **Generador de radicado:** URAB-{YYYYMMDD}-{SEQ:06}

**Métricas:** Tasa de extracción correcta >90%, Tasa de detección de datos faltantes >95%

---

### M2 — Clasificación y Triaje

**Pipeline:**
```
Texto → BETO fine-tuned → [Asesoría | Queja | Mediación | Conciliación]
                          → [Sub-temas: multi-etiqueta]
                          → Reglas urgencia → Score 1-5
                          → Reglas prioridad → Flag binario
```

**Componentes:**
- **Clasificador primario:** BETO fine-tuned con cabeza de clasificación 4 clases. Softmax. Entrenamiento con ~1000 ejemplos etiquetados
- **Sub-clasificador:** Mismo backbone BETO, cabeza multi-etiqueta (una petición puede tener múltiples temas). ~12 etiquetas. Binary cross-entropy
- **Scorer de urgencia:** Sistema de reglas (no ML). Keywords + patrones NER. Niveles: 1=baja, 5=crítica. Criterios validados por Derecho
- **Priorizador:** Determinístico. Si el texto contiene indicadores de sujeto de especial protección → flag automático. Reglas basadas en catálogo D3 de Derecho
- **Evaluación de equidad:** Equal opportunity, demographic parity (si hay datos de género/región). Plan de mitigación si se detecta sesgo

**Métricas esperadas:** Accuracy >85%, F1 por clase >0.80, Tasa de falsos negativos en urgencia <1%

---

### M3 — Asignación y Enrutamiento

**Pipeline:**
```
[Tipo + Sub-tema] → Matriz de competencia → Entidad competente
                                              → Si Defensoría: Recomendador de ruta interna
                                              → Si externa: Notificación de traslado
```

**Componentes:**
- **Matriz de competencia:** Reglas declarativas basadas en D4 de Derecho. Tabla: (tipo, sub-tema) → entidad + dirección + contacto
- **Recomendador de ruta:** Híbrido: reglas base (por tipo y carga actual) + scoring ML si hay historial de asignaciones exitosas
- **Bandejas de trabajo:** API REST con estados: pendiente, asignado, en_gestión, escalado, cerrado. Colas por profesional y por URAB
- **Monitor SLA:** Tiempos: ingreso→asignación (<4h), asignación→gestión (<24h), gestión→cierre (<15 días hábiles). Alertas a 80% y 100% del plazo

---

### M4 — Anti-Duplicación

**Pipeline:**
```
Nueva petición → Sentence-Transformer embedding → Cosine similarity vs BD
                                                    → Si ≥85% + mismo CC + misma pretensión
                                                       → Sugerir acumulación al profesional
```

**Componentes:**
- **Vectorizador:** Sentence-Transformer modelo multilingüe. Embeddings 768-dim almacenados en ChromaDB
- **Motor de similitud:** Cosine similarity contra top-K más cercanos (K=10). Filtro adicional: mismo número de documento + misma pretensión (extraída vía NER)
- **Umbral configurable:** 85% por defecto. Validado jurídicamente (D8 de Derecho). Ajustable por administrador
- **UI de acumulación:** El profesional ve: petición nueva, petición existente, % similitud, campos coincidentes. Puede: aceptar acumulación, rechazar (con motivo), marcar como relacionado sin acumular
- **Métricas:** Precision >90%, Recall >85%, Falso positivo <5%

---

### M5 — Peticionarios Recurrentes

**Pipeline:**
```
Número de identificación → Elasticsearch → Historial consolidado
                                          → Sugerencia de respuesta (respuestas previas + templates)
```

**Componentes:**
- **Índice Elasticsearch:** Campos: CC, radicados, fechas, tipo, sub_tema, estado, profesional, respuestas (texto), constancias
- **API de consulta:** GET /ciudadano/{cc}/historial. Respuesta paginada. Filtros por fecha, tipo, estado
- **Sugerencia de respuesta:** Buscar respuestas previas del mismo ciudadano + templates institucionales (D6 de Derecho) para el tipo de caso. Mostrar como sugerencia al profesional

---

### M6 — Asistente Generativo (RAG + LLM)

**Arquitectura RAG:**
```
Pregunta/Petición
    │
    ▼
Embedding (consulta) ──→ ChromaDB (base de conocimiento)
    │                        │
    │                    Top-K chunks relevantes
    │                        │
    ▼                        ▼
Prompt template + Contexto recuperado
    │
    ▼
Mistral 7B (self-hosted, Ollama)
    │
    ▼
Borrador de respuesta
    │
    ▼
UI de validación humana (Streamlit)
    ├── Profesional: edita / aprueba / rechaza
    │
    ▼
    ├── Aprobado → Envío
    └── Rechazado → Log + descarte
```

**Base de conocimiento (ChromaDB):**
- Normativa aplicable (CONPES 4144, Ley 1581, CPACA, fragmentos relevantes)
- Jurisprudencia (sentencias clave sobre debido proceso, derechos fundamentales, IA)
- Templates institucionales (D6 de Derecho)
- Respuestas previas anonimizadas (patrones de respuesta exitosos)

**Prompt engineering:**
```
Eres un asistente de la Defensoría del Pueblo de Colombia. Tu función es redactar 
borradores de respuesta para revisión de un profesional. Reglas:
1. Usa lenguaje claro, respetuoso y ciudadano. Evita tecnicismos innecesarios.
2. Cita la normativa aplicable cuando corresponda.
3. NO inventes información. Si no hay base suficiente, indícalo.
4. NO tomes decisiones vinculantes. El profesional siempre revisa y aprueba.
5. Identifica señales de riesgo (amenazas, menores, VBG, discapacidad) y márcalas.

Contexto: {documentos_recuperados}
Petición del ciudadano: {texto_peticion}
Historial del ciudadano: {historial}

Redacta un borrador de respuesta:
```

**Respuestas automatizables (M6-automático):**
- Solo para consultas del catálogo D5 (Derecho): "¿cuál es mi radicado?", "¿quién me atiende?", "reenvío de constancia", "¿estado de mi caso?"
- Estas NO pasan por RAG completo; usan templates con datos de BD. Se registran como "respuesta automática"
- Log inmutable: timestamp, consulta, respuesta, datos usados

**Sistema de alertas (M6-alertas):**
- Detección de patrones de riesgo en tiempo real durante ingesta
- Keywords + NER + reglas de Derecho
- Disparadores: amenaza, desaparición, menor de edad, VBG, discapacidad, riesgo inminente
- Acción: flag de prioridad en BD + notificación push al profesional asignado + entrada en dashboard de alertas

**Logs de auditoría (inmutables):**
- Tabla `audit_log`: id, timestamp, caso_id, profesional_id, prompt_completo, respuesta_generada, respuesta_final (tras edición), decisión (aprobado/rechazado), tiempo_revisión
- Append-only. No se puede modificar ni eliminar
- Acceso solo para auditoría

---

### M7 — Interoperabilidad

**Estrategia anti-doble registro:**
- El nuevo sistema es el **único punto de entrada** de peticiones
- Al crear un caso, se propaga a IRIS y VisionWeb **simultáneamente** (no secuencial)
- Si una API falla → evento se reencola en RabbitMQ con reintentos exponenciales
- Log de sincronización: cada evento enviado/recibido con timestamp y estado

**Diagrama de secuencia:**
```
Sistema ──→ Crear caso (POST /casos)
    │
    ├──→ RabbitMQ: publica evento "caso.creado"
    │       │
    │       ├──→ IRIS Consumer ──→ IRIS API ──→ OK/KO ──→ Log
    │       └──→ VisionWeb Consumer ──→ VisionWeb API ──→ OK/KO ──→ Log
    │
    └──→ BD local: INSERT caso
```

**Contratos de API (simulados):**

IRIS:
```
POST   /api/casos              → Crear caso en IRIS
PUT    /api/casos/{id}/estado  → Actualizar estado
GET    /api/casos/{id}         → Consultar caso
```

VisionWeb:
```
POST   /api/v1/expedientes     → Crear expediente
PUT    /api/v1/expedientes/{id}→ Actualizar
GET    /api/v1/expedientes/{id}→ Consultar
```

**Mapeo de campos críticos:**

| Sistema | IRIS | VisionWeb | Tipo de sincronización |
|---|---|---|---|
| radicado | numero_radicado | codigo_expediente | Bidireccional |
| estado | estado_tramite | fase_procesal | Bidireccional |
| profesional_asignado | funcionario_id | responsable_id | Bidireccional |
| fecha_ingreso | fecha_radicacion | fecha_creacion | Sistema → IRIS/VW |
| fecha_cierre | fecha_archivo | fecha_finalizacion | Bidireccional |

---

### M8 — Analítica

**Dashboard 1 — Carga temática:**
- Distribución por tipo (pie chart)
- Tendencia semanal/mensual de ingresos (line chart)
- Top 10 sub-temas (bar chart)
- Filtros: rango de fechas, tipo, sub-tema

**Dashboard 2 — Cuellos de botella:**
- Tiempo promedio por etapa (ingreso→asignación, asignación→gestión, gestión→cierre) (gauge/bar)
- Top 5 entidades externas con mayor demora en respuesta
- Carga por profesional (bar chart)
- Casos vencidos o próximos a vencer (table + alerts)

**Dashboard 3 — Recurrencia y duplicidad:**
- Tasa de duplicación diaria/mensual (%)
- Top 10 peticionarios recurrentes (table)
- Evolución temporal de duplicidad (line chart)

**Dashboard 4 — Equidad:**
- Distribución de tiempos de respuesta por género (si disponible)
- Distribución por grupo de especial protección
- Tasa de resolución por sub-tema y grupo poblacional
- Alertas de disparidad significativa

**Capa de investigación institucional:**
- Datos agregados y anonimizados (k-anonymity ≥ 5)
- Vistas materializadas con agregaciones: por mes, tipo, sub-tema, región, entidad
- Acceso: solo rol "investigador". Auditoría de consultas
- Cumplimiento Ley 1581/2012: sin datos identificables

---

### MLOps

| Componente | Herramienta | Qué hace |
|---|---|---|
| Versionamiento de código | Git + GitHub | Código fuente de modelos y pipelines |
| Versionamiento de datos | DVC | Datasets etiquetados, versionados, trazables |
| Versionamiento de modelos | MLflow Model Registry | Modelos con tag de versión, métricas, artefactos |
| Experiment tracking | MLflow | Hiperparámetros, métricas, artefactos de cada experimento |
| Data drift | Evidently AI | Distribución de features en producción vs entrenamiento |
| Prediction drift | Evidently AI | Distribución de predicciones en el tiempo |
| Performance monitoring | Evidently AI | Precisión, recall, F1 en producción (con ground truth de feedback) |
| Feedback loop | API endpoint | Profesionales reportan errores → datos etiquetados para reentrenamiento |
| Política de actualización | Procedimiento documentado | Solicitud → Evaluación → Aprobación Comité IA → Implementación → Changelog |

---

## DÍAS 7–9: PRODUCCIÓN DE DIAGRAMAS (Jul 23–25)

### Diagramas obligatorios

1. **Arquitectura lógica** — Capas del sistema (como el ASCII arriba, versión visual)
2. **Arquitectura de datos** — Modelo entidad-relación con tablas principales: casos, ciudadanos, profesionales, asignaciones, respuestas, audit_log, eventos_sincronizacion
3. **Integración IRIS/VisionWeb** — Diagrama de secuencia (publicador → RabbitMQ → consumidores → APIs)
4. **Seguridad** — Diagrama de componentes: API Gateway → Auth Service (OAuth2/JWT) → RBAC → Microservicios. Flujos de autenticación y autorización
5. **Macroproceso TO-BE** — Diagrama de flujo con actores: Ciudadano → M1 → M2 → M4 → M3 → Profesional → M6 → M7 → M8
6. **Pipeline MLOps** — Ciclo: Datos → Entrenamiento → Validación → Registro → Despliegue → Monitoreo → Feedback → Reentrenamiento
7. **Pipeline RAG (M6)** — Flujo: Consulta → Embedding → Retrieval → Prompt → LLM → Borrador → Revisión humana → Envío/Rechazo

**Herramientas sugeridas:** draw.io (gratuito), Lucidchart, o Mermaid (código en Markdown). Exportar como PNG/SVG para el anexo.

---

## DÍAS 8–11: REDACCIÓN DE SECCIONES DEL DOCUMENTO (Jul 24–27)

### Secciones que escribes TÚ

| Sección | Contenido |
|---|---|
| **6. Diseño técnico** (~7 págs) | Arquitectura lógica, de datos, integración, seguridad. Descripción de M1-M8. Stack con justificación. MLOps |
| **5. Análisis del macroproceso** (con Derecho, ~2 págs tuyas) | AS-IS detallado, 5 problemas críticos mapeados a módulos, TO-BE con IA |
| **9. Matriz de riesgos** (parte técnica, ~1 pág) | Fallas técnicas → operacionales, medidas de mitigación |
| **Anexo B: Especificaciones técnicas** (ilimitado) | Diagramas, contratos de API (OpenAPI), modelo de datos, plan de pruebas, métricas de rendimiento esperadas, plan MLOps |

### Estructura sugerida para sección 6 (Diseño técnico):

1. Visión general de la arquitectura
2. Arquitectura lógica (capas)
3. Arquitectura de datos
4. Arquitectura de integración (IRIS/VisionWeb)
5. Arquitectura de seguridad
6. Stack tecnológico
7. Módulo M1: Recepción Inteligente
8. Módulo M2: Clasificación y Triaje
9. Módulo M3: Asignación y Enrutamiento
10. Módulo M4: Anti-Duplicación
11. Módulo M5: Peticionarios Recurrentes
12. Módulo M6: Asistente Generativo
13. Módulo M7: Interoperabilidad
14. Módulo M8: Analítica
15. MLOps y gobierno técnico

**IMPORTANTE:** No dediques más de 2 párrafos por módulo. La descripción detallada va en el Anexo B. En la sección 6 solo concepto, componentes clave y una métrica.

---

## DÍAS 11–13: REVISIÓN Y PULIDO (Jul 27–30)

- Revisar que todos los diagramas estén referenciados en el texto
- Verificar coherencia entre secciones jurídicas (Derecho) y técnicas (tú)
- Formato APA 7ª ed. en citas técnicas (NIST, ISO, papers)
- Verificar que el Anexo B esté completo y bien organizado

---

## SI SOBRA TIEMPO: PoC MÍNIMO (Días 8-10 si adelantas)

### PoC M2 — Clasificador (el más importante)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name = "dccuchile/bert-base-spanish-wwm-uncased"
# Fine-tuning simulado con 50-100 ejemplos sintéticos
classifier = pipeline("text-classification", model=model_name)

# Demo
ejemplos = [
    "Necesito saber cómo puedo solicitar una tutela para mi hijo",
    "Denuncio que en la cárcel La Picota no me dan acceso a medicamentos",
    "Solicito mediación con mi empleador por despido injustificado",
]
for texto in ejemplos:
    print(classifier(texto))
```

Si llegas a entrenar con ejemplos reales de las categorías D1, puedes incluir capturas de pantalla del notebook como evidencia en el anexo. Esto suma puntos en "Nivel de Innovación" (criterio de 20 puntos).

---

## CALENDARIO DS VISUAL

```
DÍA:  1  2  3  4  5  6  7  8  9  10 11 12 13
      J  V  S  D  L  M  M  J  V  S  D  L  M
      |--|--|--|--|--|--|--|--|--|--|--|--|--|
SETUP ██|  |  |  |  |  |  |  |  |  |  |  |  |
INVEST ██|██|  |  |  |  |  |  |  |  |  |  |  |
AS-IS  |██|██|  |  |  |  |  |  |  |  |  |  |  |
ARQUIT |  |  |██|██|██|  |  |  |  |  |  |  |  |
MODULOS|  |  |  |██|██|██|██|  |  |  |  |  |  |
DIAGRAM|  |  |  |  |  |  |██|██|██|  |  |  |  |
REDACC |  |  |  |  |  |  |  |██|██|██|██|  |  |
PULIDO |  |  |  |  |  |  |  |  |  |  |██|██|  |
ENTREGA|  |  |  |  |  |  |  |  |  |  |  |  |██|
```

---

## ENTREGABLES QUE EXIGES A DERECHO

| # | Qué | Deadline | Úsalo para |
|---|---|---|---|
| D1 | 4 categorías + ejemplos | Día 2 | M2 clasificación |
| D2 | Sub-temas (~12) | Día 2 | M2 sub-clasificación |
| D3 | Sujetos de protección especial | Día 3 | M2 priorización |
| D4 | Matriz de competencias | Día 4 | M3 enrutamiento |
| D5 | Consultas automatizables | Día 4 | M6 respuestas automáticas |
| D6 | Templates de respuesta (10-20) | Día 5 | M6 RAG |
| D7 | Criterios de urgencia | Día 3 | M2 scoring + M6 alertas |
| D8 | Umbral de duplicación | Día 5 | M4 threshold |
| D9 | Roles RBAC | Día 5 | Seguridad |

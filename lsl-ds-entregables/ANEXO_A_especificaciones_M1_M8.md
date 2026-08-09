# Anexo A — Especificaciones técnicas detalladas M1–M8

> **Referenciado desde:** §4.2 (diagrama TO-BE) y §5.3 (descripción de módulos) del borrador principal.

---

## A.1 Diagrama TO-BE completo

```
                          CIUDADANO
                    envía petición por
                web / email / físico / campo
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                     M1 — RECEPCIÓN INTELIGENTE                   │
│                                                                  │
│  ● OCR (Tesseract LSTM spa + OpenCV): convierte escaneados       │
│    en texto. Preprocesamiento: deskew, binarización adaptativa.  │
│  ● NER (spaCy es_core_news_lg fine-tuned): extrae nombre,       │
│    tipo_doc, num_doc, direccion, telefono, email, hecho,         │
│    pretension, entidad_referida, anexos, canal, fecha            │
│  ● Validador de completitud: reglas declarativas                 │
│       ├── Faltan datos → Respuesta automática con plantilla      │
│       └── OK → Genera radicado URAB-YYYYMMDD-NNNNNN              │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   M4 — ANTI-DUPLICACIÓN                          │
│                                                                  │
│  ● Vectorizador: Sentence-Transformers → embedding 768-dim      │
│  ● Cosine similarity vs top-K (K=10) más cercanos en BD         │
│  ● Filtro: mismo CC + misma pretensión (NER de M1)              │
│  ● Umbral configurable: 85% por defecto (validado D8)           │
│       ├── ≥85% → UI de acumulación al profesional               │
│       └── <85% → Pasa a M2                                       │
│                                                                  │
│  ⚠️  El profesional ve lado a lado las dos peticiones,           │
│     campos coincidentes resaltados. Decide: acumular /           │
│     rechazar (con motivo) / marcar relacionado.                  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                  M2 — CLASIFICACIÓN Y TRIAJE                     │
│                                                                  │
│  Clasificador primario: BETO fine-tuned + Softmax 4 clases:     │
│     Asesoría | Queja | Solicitud de Mediación | Conciliación    │
│                                                                  │
│  Sub-clasificador: mismo backbone BETO, cabeza multi-etiqueta   │
│     ~12 sub-temas. Binary cross-entropy.                        │
│                                                                  │
│  Scorer de urgencia (reglas, NO ML): keywords + patrones NER    │
│     Nivel 1 (baja) → 5 (crítica). Criterios D7 de Derecho.     │
│                                                                  │
│  Priorizador (determinístico): cruza texto con catálogo D3.     │
│     Flag automático si sujeto de especial protección.           │
│                                                                  │
│  ⚠️  El profesional de URAB valida/corrige antes de avanzar.    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│               M3 — ASIGNACIÓN Y ENRUTAMIENTO                     │
│                                                                  │
│  Matriz de competencia: (tipo, sub-tema) → entidad + datos      │
│     Alimentada por D4. Reglas declarativas, actualizables.       │
│       ├── No Defensoría → Notificación de traslado automática   │
│       └── Defensoría → Recomendador de ruta interna              │
│                                                                  │
│  Recomendador: reglas base (tipo + regional) + scoring opcional │
│     basado en historial de asignaciones exitosas.                │
│                                                                  │
│  Bandejas: API REST. Estados: pendiente, asignado, en_gestión,  │
│     escalado, cerrado. Colas por profesional y URAB.             │
│                                                                  │
│  Monitor SLA: ingreso→asignación <4h, asignación→gestión <24h,  │
│     gestión→cierre <15 días hábiles. Alertas 80% y 100%.        │
│                                                                  │
│  ⚠️  El profesional confirma la entidad competente.              │
│     La IA sugiere, NUNCA decide competencia.                    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│            PROFESIONAL DEFENSORIAL GESTIONA EL CASO              │
│                                                                  │
│  M5 — Historial unificado:                                       │
│     Elasticsearch indexa: CC, radicados, fechas, tipos,         │
│     sub-temas, estados, profesional, respuestas.                │
│     GET /ciudadano/{cc}/historial → <500ms. Filtros.           │
│     Sugiere respuestas previas + templates D6.                  │
│                                                                  │
│  M6 — Asistente generativo RAG:                                  │
│     ┌──────────────────────────────────────────┐                │
│     │ Consulta → Embedding → ChromaDB (top-K)  │                │
│     │    │                                      │                │
│     │    ▼                                      │                │
│     │ Prompt = instrucciones + documentos       │                │
│     │         + petición + historial             │                │
│     │    │                                      │                │
│     │    ▼                                      │                │
│     │ Mistral 7B (self-hosted) → borrador       │                │
│     │    │                                      │                │
│     │    ▼                                      │                │
│     │ Profesional: revisa / edita / rechaza     │                │
│     │ Todo en logs inmutables                   │                │
│     └──────────────────────────────────────────┘                │
│                                                                  │
│  ⚠️  Respuesta automática SOLO para catálogo D5.                │
│     El profesional SIEMPRE revisa, edita y firma.               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                M7 — INTEROPERABILIDAD                            │
│                                                                  │
│  RabbitMQ: publica evento caso.{creado,actualizado,cerrado}     │
│     ├── Consumer IRIS → IRIS API → OK/KO → Log                  │
│     └── Consumer VisionWeb → VisionWeb API → OK/KO → Log        │
│                                                                  │
│  Reintentos: backoff exponencial (1s, 2s, 4s, 8s, 16s, 32s)    │
│  Tras 6 fallos → alerta administrador.                           │
│                                                                  │
│  RPA como contingencia si no hay API de escritura.              │
│                                                                  │
│  Mapeo canónico de campos:                                       │
│     radicado ↔ numero_radicado (IRIS) ↔ codigo_expediente (VW) │
│     estado ↔ estado_tramite (IRIS) ↔ fase_procesal (VW)         │
│     profesional ↔ funcionario_id (IRIS) ↔ responsable_id (VW)   │
│                                                                  │
│  Bitácora inmutable: timestamp, destino, payload, resultado,    │
│     número de reintentos. Conciliación diaria automática.       │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   M8 — ANALÍTICA                                 │
│                                                                  │
│  Dashboard 1 — Carga temática:                                   │
│     Distribución tipos (pie), tendencia semanal (line),         │
│     top 10 sub-temas (bar). Filtros: fecha, tipo, regional.     │
│                                                                  │
│  Dashboard 2 — Cuellos de botella:                               │
│     Tiempos promedio por etapa. Top 5 entidades lentas.         │
│     Carga por profesional. Casos vencidos (table + alerts).    │
│                                                                  │
│  Dashboard 3 — Recurrencia y duplicidad:                         │
│     Tasa duplicación diaria/mensual. Top 10 recurrentes.        │
│     Evolución temporal.                                          │
│                                                                  │
│  Dashboard 4 — Equidad:                                          │
│     Distribución tiempos por género, grupo especial protección. │
│     Alertas disparidad >5%.                                      │
│                                                                  │
│  Capa investigación: k-anonymity ≥5. Rol "investigador"         │
│     con aprobación del Comité IA. Consultas auditadas.          │
└──────────────────────────────────────────────────────────────────┘
```

---

## A.2 M1 — Recepción Inteligente

**Pipeline:** Web (JSON) / Email (parser) / PDF (OCR Tesseract + preprocesamiento OpenCV) / Imagen (OCR) / Formulario campo → NER (spaCy) → Validación completitud → Radicado.

**Componentes:**
- **API Gateway (FastAPI):** endpoints REST para upload multipart, webhook de email, JSON. Rate limiting por IP. Timeout 30s. Autenticación JWT.
- **OCR Engine:** Tesseract LSTM con modelo `spa` (español). OpenCV: deskew (corrección de inclinación), binarización adaptativa (mejora contraste), eliminación de ruido. CER esperado <5% en documentos limpios, <10% en baja calidad.
- **NER Pipeline:** spaCy `es_core_news_lg` con fine-tuning para dominio Defensoría. Entidades: `PER` (nombre), `TIPO_DOC`, `NUM_DOC`, `DIR`, `TEL`, `EMAIL`, `HECHO`, `PRETENSION`, `ENTIDAD_REF`, `ANEXOS`, `CANAL`, `FECHA`.
- **Validador de completitud:** reglas declarativas configurables por administrador. Campos críticos: nombre, número de documento, descripción del hecho. Si falta → respuesta automática con plantilla solicitando info. Máximo 3 intentos de solicitud; al tercero, el caso se escala a revisión humana.
- **Generador de radicado:** formato URAB-{YYYYMMDD}-{SEQ:06}. Contador atómico por día. Ejemplo: URAB-20260115-000342.

**Métrica principal:** tasa de extracción correcta de entidades ≥90% (medida sobre conjunto gold de 200 documentos etiquetados).

---

## A.3 M2 — Clasificación y Triaje

**Pipeline:** Texto normalizado → BETO fine-tuned (clasificación primaria 4 clases) → Sub-clasificador multi-etiqueta (~12 etiquetas) → Scorer urgencia (reglas) → Priorizador (D3) → Sugerencia al profesional → Validación humana.

**Componentes:**
- **Clasificador primario:** `dccuchile/bert-base-spanish-wwm-uncased` con cabeza de clasificación (4 neuronas + Softmax). Entrenado con ~1000 ejemplos etiquetados (Fase 0). Hiperparámetros: learning rate 2e-5, batch size 16, 3 épocas, weight decay 0.01, warmup 10% de pasos. Early stopping con paciencia de 2 épocas.
- **Sub-clasificador multi-etiqueta:** mismo backbone BETO, cabeza con ~12 neuronas + sigmoid. Binary cross-entropy loss. Una petición puede activar múltiples sub-temas simultáneamente.
- **Scorer de urgencia:** sistema determinístico basado en reglas (no ML, auditable). Diccionario de keywords y patrones NER por nivel, validado jurídicamente (D7). Niveles: 1 (baja), 2 (media-baja), 3 (media), 4 (alta), 5 (crítica — riesgo vital). Los patrones de nivel 5 incluyen: "amenaza de muerte", "desaparición forzada", "menor en peligro", "violencia sexual", "riesgo inminente".
- **Priorizador:** cruza texto + NER con catálogo D3. Si detecta pertenencia a grupo de especial protección → flag binario de prioridad. Los grupos incluyen: NNA, mujeres VBG, personas con discapacidad, adultos mayores, desplazados, minorías étnicas, población privada de libertad, migrantes.
- **Evaluación de equidad:** métricas Equal Opportunity, Demographic Parity y False Negative Rate segmentadas (ver Anexo F).

**Métricas objetivo:** accuracy ≥90%, F1 por clase ≥0.85, recall urgencias ≥99% (umbral asimétrico). Ninguna clase por debajo de F1 0.80.

---

## A.4 M3 — Asignación y Enrutamiento

**Pipeline:** [Tipo + Sub-tema] → Matriz de competencia → Entidad determinada → Si Defensoría: Recomendador ruta → Bandeja profesional con SLA.

**Componentes:**
- **Matriz de competencia:** tabla PostgreSQL: (tipo, sub-tema) → entidad + dirección + contacto + normativa_aplicable. Alimentada y validada por Derecho (D4). Actualizable sin deploy. Si la entidad no es la Defensoría, el sistema genera automáticamente oficio de traslado con todos los datos del caso.
- **Recomendador de ruta interna:** reglas base: tipo de caso + regional destino + carga actual del profesional. Fase 2+: scoring ML opcional basado en historial de asignaciones exitosas (tiempo de cierre, satisfacción). Distribución balanceada de carga.
- **Bandejas de trabajo:** API REST. Estados: `pendiente` → `asignado` → `en_gestion` → `escalado` → `cerrado`. Filtros: por profesional, URAB, tipo, urgencia, antigüedad. Ordenamiento por prioridad.
- **Monitor SLA:** tiempos máximos configurables — ingreso→asignación: 4h, asignación→inicio_gestión: 24h, inicio→cierre: 15 días hábiles. Alertas: amarilla al 80% del plazo, roja al 100%. Escalamiento automático al superior jerárquico si se vence.

**Métrica objetivo:** tiempo ingreso→asignación ≤15 min en p90, ≤4h en p99.

---

## A.5 M4 — Anti-Duplicación

**Pipeline:** Texto petición → Sentence-Transformer embedding (768-dim) → Cosine similarity vs top-10 en pgvector → Filtro CC + pretensión → Si ≥85% → UI acumulación → Profesional decide.

**Componentes:**
- **Vectorizador:** `paraphrase-multilingual-mpnet-base-v2` de Sentence-Transformers. Embeddings 768 dimensiones. Almacenados en pgvector dentro de PostgreSQL (sin BD vectorial separada).
- **Motor de similitud:** índice IVFFlat en pgvector para búsqueda aproximada rápida. Cosine similarity contra los K=10 vecinos más cercanos. Filtro post-recuperación: mismo número de documento (extraído por NER en M1) + misma pretensión (NER).
- **Umbral configurable:** 85% por defecto. Validado jurídicamente (D8). Ajustable por administrador con registro de cambio en log de auditoría. Si la similitud supera el umbral Y coincide CC Y coincide pretensión → sugerencia de acumulación.
- **UI de decisión:** vista lado a lado: petición nueva, petición existente, % similitud, campos coincidentes resaltados en amarillo. Botones: "Acumular" (requiere motivo), "Rechazar" (requiere motivo), "Marcar como relacionado sin acumular". Todo registrado en bitácora M4 (timestamp, profesional, decisión, motivo).

**Métrica objetivo:** precision sugerencias ≥85%, recall duplicados ≥90%, falsos positivos ≤15%, falsos negativos ≤10%.

---

## A.6 M5 — Peticionarios Recurrentes

**Pipeline:** Número de identificación → Elasticsearch → Historial consolidado → Sugerencias de respuesta.

**Componentes:**
- **Índice Elasticsearch:** documentos indexados por número de documento. Campos: CC, radicados (array), fechas (array), tipos, sub-temas, estados, profesional_asignado, respuestas (texto completo), constancias. Sharding por regional para rendimiento.
- **API de consulta:** `GET /ciudadano/{cc}/historial?fecha_inicio=&fecha_fin=&tipo=&estado=`. Respuesta paginada (20 resultados por página). Orden cronológico inverso. Tiempo objetivo <500ms (p95).
- **Sugerencia de respuesta:** busca respuestas previas emitidas al mismo ciudadano para el mismo tipo de caso + templates institucionales del catálogo D6. Muestra hasta 3 sugerencias como referencia. El profesional elige si usar alguna como base.

**Métrica objetivo:** tiempo de consulta <500ms (p95), disponibilidad del índice 99.9%.

---

## A.7 M6 — Asistente Generativo (RAG + LLM)

**Arquitectura RAG completa:**

1. **Ingesta de conocimiento (Fase 2):** se indexan en ChromaDB fragmentos de ~500 tokens con solapamiento de 100 tokens: normativa aplicable (CONPES 4144, Ley 1581, CPACA, Ley 1755), jurisprudencia relevante (Corte Constitucional, Consejo de Estado), templates institucionales del catálogo D6, y respuestas previas exitosas anonimizadas.
2. **Recuperación (Retrieval):** la petición del ciudadano se convierte en embedding con el mismo modelo de M4. Se recuperan los top-5 fragmentos más relevantes de ChromaDB por cosine similarity.
3. **Prompt engineering:** se construye un prompt estructurado con: (a) instrucciones de sistema ("Eres un asistente de la Defensoría del Pueblo..."), (b) reglas estrictas (no inventar, lenguaje ciudadano, citar normativa real, no decidir), (c) contexto recuperado de ChromaDB, (d) texto de la petición, (e) historial relevante del ciudadano (M5).
4. **Generación:** Mistral 7B Instruct v0.2, self-hosted vía Ollama/vLLM en servidores de la Defensoría. Parámetros: temperature 0.3 (baja creatividad = menos alucinaciones), max_tokens 1024, top_p 0.9. Los datos NUNCA salen de la infraestructura de la Defensoría (soberanía de datos, CONPES 4144).
5. **Validación humana:** el borrador se presenta en una interfaz con tres acciones: (a) "Aprobar y enviar", (b) "Editar" (abre editor de texto con diff visual), (c) "Rechazar" (requiere motivo). Toda interacción se registra en tabla `audit_log` (append-only): timestamp, caso_id, profesional_id, prompt_completo, respuesta_generada, respuesta_final, tiempo_revisión, decisión.

**Modo automático (catálogo D5):** para el conjunto cerrado de consultas definidas por Derecho —"¿cuál es mi número de radicado?", "¿quién es mi profesional asignado?", "reenvío de constancia de radicación", "¿estado actual de mi caso?"— el sistema responde con plantillas precargadas que se completan con datos de PostgreSQL. No pasan por el LLM. Se registran como "respuesta automática D5" en logs.

**Sistema de alertas integrado:** durante la ingesta (M1) y clasificación (M2), M6 ejecuta en paralelo un detector de patrones de riesgo que busca: amenazas explícitas, desaparición forzada, menores de edad en situación de peligro, violencia basada en género activa, discapacidad con riesgo inminente. Si detecta → flag de prioridad en BD + notificación push al profesional + entrada inmediata en dashboard de alertas M8.

**Métrica objetivo:** tasa de aceptación de borradores (aprobados sin edición o con ediciones menores) ≥70%, tiempo de generación <10 segundos (p95).

---

## A.8 M7 — Interoperabilidad (IRIS / VisionWeb)

**Estrategia anti-doble registro:** el nuevo sistema es el único punto de entrada de peticiones. Al ocurrir un evento de ciclo de vida (`caso.creado`, `caso.actualizado`, `caso.cerrado`), el backend publica un mensaje en el exchange `defensoria.casos` de RabbitMQ con routing key según el tipo de evento. Dos colas independientes (`iris.sync` y `visionweb.sync`) reciben copia del mensaje. Consumidores independientes transforman el payload al formato específico de cada API y realizan la llamada HTTP.

**Manejo de fallos:**
- RabbitMQ confirmations: cada mensaje requiere ACK del consumidor. Si el consumidor falla (NACK) o hay timeout → el mensaje se reencola automáticamente.
- Backoff exponencial entre reintentos: 1s, 2s, 4s, 8s, 16s, 32s. Máximo 6 reintentos.
- Dead Letter Queue: tras agotar reintentos, el mensaje va a una cola especial que dispara alerta al administrador. Un operador revisa y puede reprocesar manualmente.
- Conciliación diaria automática: un job programado compara el estado de cada caso entre el sistema nuevo, IRIS y VisionWeb. Las discrepancias se registran y se notifican.

**Bitácora inmutable:** tabla `sync_log` (PostgreSQL, append-only): id, timestamp, caso_id, sistema_destino, tipo_evento, payload, response_code, response_body, reintentos, estado (success/failed), error_message.

**RPA como contingencia:** si IRIS o VisionWeb no exponen API de escritura, se despliega un robot de software (RPA) que automatiza la digitación en la interfaz web del sistema legado. El RPA se versiona, audita y monitorea igual que una API. Es una capa de último recurso, no la solución primaria.

**Métrica objetivo:** tasa de sincronización exitosa en primer intento ≥99.5%, latencia de sincronización <5 segundos (p95).

---

## A.9 M8 — Analítica

**Dashboard 1 — Carga temática:** gráfico de torta (distribución por tipo), línea (tendencia semanal y mensual de ingresos), barras horizontales (top 10 sub-temas). Filtros interactivos: rango de fechas, tipo, sub-tema, regional. Actualización: tiempo real (WebSocket, latencia <1 min).

**Dashboard 2 — Cuellos de botella:** medidores tipo gauge (tiempo promedio ingreso→asignación, asignación→gestión, gestión→cierre). Barras (top 5 entidades externas con mayor demora en respuesta). Tabla (carga por profesional, color por ocupación). Tabla de casos vencidos o próximos a vencer con alertas visuales (rojo/amarillo/verde). Filtros por profesional, regional, rango de fechas.

**Dashboard 3 — Recurrencia y duplicidad:** línea (tasa de duplicación diaria y mensual), tabla (top 10 peticionarios recurrentes con contador de casos), línea (evolución temporal de duplicidad). Indicador numérico grande: % de peticiones duplicadas este mes.

**Dashboard 4 — Equidad:** barras agrupadas (tiempo promedio de respuesta por género), barras (distribución de tipos por grupo de especial protección), tabla de alertas de disparidad (>5% de diferencia entre grupos). Filtro por período. Reporte exportable a PDF para el Comité de IA.

**Capa de investigación institucional:** vistas materializadas en PostgreSQL con agregaciones por mes, tipo, sub-tema, regional, entidad y grupo poblacional. k-anonymity ≥5 (garantizado por restricción SQL: no se retorna ninguna celda con menos de 5 individuos). Acceso: solo rol "investigador", previa aprobación del Comité de IA. Cada consulta registrada en log de auditoría. Propósito exclusivo: investigación académica e institucional sobre patrones de vulneración de derechos. Cumplimiento Ley 1581/2012 y Ley 1712/2014.

**Métrica objetivo:** dashboards actualizados en tiempo real (latencia <1 minuto desde el evento). Disponibilidad de dashboards 99.5%.

---

## A.10 MLOps — Pipeline de mantenimiento de modelos

| Componente | Herramienta | Descripción |
|---|---|---|
| Versionamiento de código | Git + GitHub | Código fuente de modelos, pipelines y configuración |
| Versionamiento de datos | DVC | Datasets etiquetados versionados. Remoto: bucket S3/GCS |
| Versionamiento de modelos | MLflow Model Registry | Modelos con tag de versión, métricas, parámetros, artefactos. Stages: Staging → Production → Archived |
| Experiment tracking | MLflow Tracking | Hiperparámetros, métricas, artefactos de cada experimento. Comparación visual |
| Data drift | Evidently AI | Compara distribución de features en producción vs entrenamiento. Estadísticos: KS, Wasserstein, Jensen-Shannon |
| Prediction drift | Evidently AI | Compara distribución de predicciones en el tiempo. Alerta si cambio significativo |
| Performance monitoring | Evidently AI | Accuracy, recall, F1 sobre muestra etiquetada por feedback humano. Reporte semanal automático |
| Feedback loop | API endpoint `POST /feedback` | Profesional reporta: {caso_id, prediccion_original, correccion, motivo}. Datos acumulados para reentrenamiento |
| Política de actualización | Procedimiento documentado | Solicitud → Evaluación (métricas en test set) → Aprobación Comité IA → Staging (1 semana) → Producción → Changelog |

---

## A.11 Plan de pruebas detallado

| Tipo | Alcance | Herramienta | Criterio de aceptación | Frecuencia |
|---|---|---|---|---|
| Unitarias | Cada función aislada: OCR, NER, validador, reglas urgencia, cosine similarity, tokenizador | pytest | Cobertura >80%. Todos los tests pasan. | Cada commit (CI) |
| Integración | Flujo M1→M4→M2→M3. M7→IRIS mock, M7→VisionWeb mock. M6→ChromaDB→Mistral | pytest + docker-compose | Flujo completo sin errores. Assertions sobre estados intermedios. | Cada sprint |
| Aceptación | Profesionales URAB reales con 50 casos etiquetados. Encuesta de usabilidad SUS. | Script de testing manual + formulario | SUS score >70. Tiempo de tarea <2x manual. Satisfacción >80%. | Antes de cada fase |
| Equidad | Equal Opportunity, Demographic Parity, FN Rate por género/regional/grupo. Segmentación con mínimo 30 casos. | Evidently AI + pytest custom | Disparidad <5% para todos los grupos. Disparate Impact >0.80. | Antes de despliegue + trimestral |
| Carga | 300 peticiones/día simuladas. Picos de 500/día. Medir p95 latencia, uso CPU/RAM, tasa de error. | Locust / k6 | p95 API <500ms. Tasa error <0.1%. CPU <80%. | Antes de producción |
| Seguridad | OWASP Top 10. Inyección SQL, XSS, CSRF. TLS 1.3 verificado. Acceso no autorizado a endpoints. Simulación caída IRIS. | OWASP ZAP + scripts manuales | 0 vulnerabilidades críticas o altas. TLS 1.3 confirmado. RBAC intacto. | Antes de producción + semestral |

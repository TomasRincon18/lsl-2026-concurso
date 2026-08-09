# Anexo 05 — Arquitectura técnica: especificaciones M1–M8, stack, integración, seguridad, MLOps, infraestructura cloud y pruebas

> **Referenciado desde:** §5 del cuerpo del documento.
> **Contiene:** §B.1 Especificaciones detalladas M1–M8, §B.2 Stack tecnológico completo con justificación y licencias, §B.3 Modelo de datos, §B.4 Integración IRIS/VisionWeb, §B.5 Seguridad cloud y continuidad, §B.6 MLOps, §B.7 Infraestructura cloud y plataforma de agentes de IA, §B.8 Plan de pruebas.

---

## B.1 Especificaciones técnicas detalladas de módulos M1–M8

### M1 — Recepción Inteligente

**Pipeline:** entrada multicanal (JSON web, email parser, PDF/imagen vía OCR, formulario campo) → OCR Tesseract LSTM `spa` + preprocesamiento OpenCV (deskew, binarización adaptativa, eliminación de ruido) → NER spaCy `es_core_news_lg` fine-tuned (entidades: `PER`, `TIPO_DOC`, `NUM_DOC`, `DIR`, `TEL`, `EMAIL`, `HECHO`, `PRETENSION`, `ENTIDAD_REF`, `ANEXOS`, `CANAL`, `FECHA`) → Validador de completitud (reglas declarativas configurables: campos críticos nombre, documento, hecho, pretensión) → Si faltan datos: respuesta automática con plantilla solicitando información (máx. 3 intentos, luego escala a revisión humana) → Si OK: genera radicado `URAB-YYYYMMDD-NNNNNN` con contador atómico diario.

**Componentes cloud:** API Gateway gestiona rate limiting, autenticación JWT y enrutamiento. OCR y NER se ejecutan como funciones serverless o contenedores en la nube corporativa, escalando automáticamente con el volumen de ingesta. **Métrica:** extracción correcta de entidades ≥90% (medida sobre conjunto gold de 200 documentos). CER <5% en documentos limpios, <10% en baja calidad.

---

### M2 — Clasificación y Triaje

**Pipeline:** texto normalizado → BETO `dccuchile/bert-base-spanish-wwm-uncased` fine-tuned (clasificación primaria 4 clases con Softmax) → Sub-clasificador multi-etiqueta (~12 sub-temas, binary cross-entropy, mismo backbone) → Scorer de urgencia: sistema de reglas determinístico con diccionario de keywords y patrones NER por nivel (1=baja a 5=crítica/riesgo vital, validado D7). Nivel 5 incluye: "amenaza de muerte", "desaparición forzada", "menor en peligro", "violencia sexual", "riesgo inminente" → Priorizador: cruza texto con catálogo D3 de sujetos de especial protección (NNA, mujeres VBG, discapacidad, adultos mayores, desplazados, minorías étnicas, PPL, migrantes) → flag binario de prioridad.

**Entrenamiento:** dataset ~1000 casos etiquetados en Fase 0. Hiperparámetros: learning rate 2e-5, batch size 16, 3 épocas, weight decay 0.01, warmup 10%, early stopping paciencia=2. **Métricas:** accuracy ≥90%, F1 por clase ≥0.85 (ninguna <0.80), recall urgencias ≥99% (umbral asimétrico calibrado en Fase 2 con conjunto gold de 200 casos de riesgo vital etiquetados por juristas URAB).

**Evaluación de equidad:** Equal Opportunity, Demographic Parity y False Negative Rate segmentados por género (cuando declarado voluntariamente), regional, grupo de especial protección y canal. Ver Anexo 08.

---

### M3 — Asignación y Enrutamiento

**Pipeline:** [tipo + sub-tema] → Matriz de competencia PostgreSQL (tabla: tipo, sub-tema, entidad, dirección, contacto, normativa; alimentada D4, actualizable sin deploy) → Si no es Defensoría: generación automática de oficio de traslado con todos los datos → Si es Defensoría: Recomendador de ruta (reglas base: tipo + regional + carga actual; Fase 2+: scoring ML opcional por historial de asignaciones exitosas).

**Bandejas:** API REST con estados `pendiente → asignado → en_gestion → escalado → cerrado`. Filtros por profesional, URAB, tipo, urgencia, antigüedad. Ordenamiento por prioridad. **Monitor SLA:** ingreso→asignación 4h, asignación→inicio_gestión 24h, inicio→cierre 15 días hábiles. Alertas: amarilla 80% plazo, roja 100%. Escalamiento automático al superior al vencer. **Métrica:** tiempo ingreso→asignación ≤15 min en p90, ≤4h en p99.

---

### M4 — Anti-Duplicación

**Pipeline:** texto → Sentence-Transformers `paraphrase-multilingual-mpnet-base-v2` → embedding 768-dim → Cosine similarity (índice IVFFlat en pgvector) vs top-10 vecinos → Filtro: mismo CC (NER M1) + misma pretensión (NER M1) → Si ≥85% similitud + matching: sugerencia de acumulación.

**UI de decisión:** vista side-by-side (petición nueva vs existente, % similitud, campos coincidentes resaltados). Acciones: "Acumular" (requiere motivo), "Rechazar" (requiere motivo), "Marcar relacionado sin acumular". Todo registrado en bitácora M4 (timestamp, profesional, decisión, motivo). Umbral 85% configurable por administrador con registro de cambio en log. **Métricas:** precision sugerencias ≥85%, recall duplicados ≥90%, FP ≤15%, FN ≤10%.

---

### M5 — Peticionarios Recurrentes

**Pipeline:** nº cédula → Elasticsearch (índice por CC: radicados, fechas, tipos, sub-temas, estados, profesional, respuestas texto completo) → historial paginado (20 resultados/pág, orden cronológico inverso) → sugerencias: respuestas previas del mismo ciudadano + templates D6 aplicables al tipo de caso.

**API:** `GET /ciudadano/{cc}/historial?fecha_inicio=&fecha_fin=&tipo=&estado=`. Sharding por regional. **Métrica:** tiempo de consulta <500ms (p95), disponibilidad del índice 99.9%.

---

### M6 — Asistente Generativo RAG + LLM

**Arquitectura en cloud corporativa:**

1. **Ingesta de conocimiento (Fase 2):** ChromaDB indexa fragmentos de ~500 tokens (solapamiento 100 tokens) de: normativa (CONPES 4144, Ley 1581, CPACA, Ley 1755), jurisprudencia (Corte Constitucional, Consejo de Estado), templates D6, respuestas previas exitosas anonimizadas.
2. **Recuperación:** embedding de la consulta → top-5 fragmentos por cosine similarity en ChromaDB.
3. **Prompt engineering:** instrucciones de sistema + reglas (no inventar, lenguaje ciudadano, citar normativa real, no decidir) + contexto recuperado + petición + historial M5.
4. **Generación:** Mistral 7B Instruct v0.2 ejecutado en la nube corporativa. Parámetros: temperature 0.3, max_tokens 1024, top_p 0.9.
5. **Validación humana:** UI con tres acciones: "Aprobar y enviar" / "Editar" (diff visual) / "Rechazar" (motivo obligatorio). Log inmutable: prompt, respuesta cruda, respuesta final, profesional, timestamp, tiempo de revisión.

**Modo automático (catálogo D5):** consultas preaprobadas por Derecho —estado del radicado, profesional asignado, reenvío de constancia— respondidas con plantillas desde BD, sin pasar por LLM. Marcadas como "respuesta automática D5" en logs.

**Sistema de alertas integrado:** detector en paralelo durante M1+M2 busca: amenazas explícitas, desaparición forzada, menores en peligro, VBG activa, discapacidad con riesgo inminente. Si detecta → flag prioridad + push al profesional + entrada en dashboard M8.

**Métricas:** borradores aceptados sin corrección mayor ≥70%, tiempo generación <10s (p95).

---

### M7 — Interoperabilidad IRIS/VisionWeb

**Estrategia cloud-native:** el nuevo sistema es único punto de entrada. Backend publica evento `caso.{creado,actualizado,cerrado}` en el message broker cloud. Dos consumidores independientes transforman payload al formato de cada API legada y realizan la llamada HTTP.

**Manejo de fallos:** ACK del consumidor. Si NACK o timeout → reencolado automático con backoff exponencial (1s, 2s, 4s, 8s, 16s, 32s). Máx. 6 reintentos. Dead Letter Queue con alerta al administrador. Reproceso manual disponible.

**RPA como contingencia:** si IRIS o VisionWeb no exponen API de escritura (Banco Q10), robot de software versionado, auditado y monitoreado que automatiza la digitación en la interfaz web del sistema legado. Capa de último recurso.

**Modelo canónico:** mapeo documentado de campos equivalentes: `radicado` ↔ `numero_radicado` (IRIS) ↔ `codigo_expediente` (VisionWeb); `estado` ↔ `estado_tramite` (IRIS) ↔ `fase_procesal` (VisionWeb); `profesional_asignado` ↔ `funcionario_id` (IRIS) ↔ `responsable_id` (VisionWeb).

**Bitácora inmutable:** tabla `sync_log` (append-only): id, timestamp, caso_id, sistema_destino, tipo_evento, payload, response_code, response_body, reintentos, estado, error_message. Conciliación diaria automática comparando estados entre los tres sistemas.

**Métricas:** sincronización exitosa en primer intento ≥99.5%, latencia <5s (p95).

---

### M8 — Analítica

**Dashboard 1 — Carga temática:** gráfico torta (distribución por tipo), línea (tendencia semanal/mensual), barras (top 10 sub-temas). Filtros: fecha, tipo, sub-tema, regional. WebSocket, latencia <1 min.

**Dashboard 2 — Cuellos de botella:** gauges (tiempos promedio por etapa), barras (top 5 entidades con mayor demora), tabla (carga por profesional con semaforización), tabla de casos vencidos/próximos a vencer.

**Dashboard 3 — Recurrencia y duplicidad:** línea (tasa duplicación), tabla (top 10 recurrentes), indicador numérico (% duplicados del mes).

**Dashboard 4 — Equidad:** barras agrupadas (tiempos por género), distribución por grupo de especial protección, alertas de disparidad >5%. Filtro por período. Exportable PDF.

**Capa de investigación institucional:** vistas materializadas PostgreSQL, k-anonymity ≥5 (restricción SQL: sin celdas con <5 individuos). Acceso solo rol "investigador" con aprobación del Comité de IA. Cada consulta auditada. Propósito exclusivo: investigación académica e institucional sobre patrones de vulneración de derechos. Cumplimiento Ley 1581/2012 y Ley 1712/2014.

---

## B.2 Stack tecnológico completo

| Capa | Tecnología | Versión | Justificación | Alternativas | Licencia |
|---|---|---|---|---|---|
| **Plataforma cloud** | IaaS/PaaS corporativa (AWS/Azure/GCP o GovCloud MinTIC) | — | Orquestación unificada de agentes de IA, administración de versiones, monitoreo, escalabilidad automática, delegación de infraestructura | On-premise (mayor carga operativa para la Defensoría) | Comercial / Gubernamental |
| Backend API | **FastAPI** (Python) | ≥0.110 | Alto rendimiento async, OpenAPI 3.0 automático, ecosistema IA nativo, validación Pydantic | Django REST, Flask | MIT |
| Clasificación NLP | **BETO** (`dccuchile/bert-base-spanish-wwm-uncased`) fine-tuned | Base | Entrenado en español por U. de Chile. 110M parámetros. Whole Word Masking. Probado en dominio legal. | RoBERTa-es (más pesado), Multilingual BERT (no optimizado) | MIT |
| NER | **spaCy** (`es_core_news_lg`) + fine-tuning | ≥3.7 | Pipeline NLP más maduro para español. Inferencia rápida. Componentes integrados (tokenización, POS, NER). | Stanza, Flair | MIT |
| Embeddings | **Sentence-Transformers** (`paraphrase-multilingual-mpnet-base-v2`) | ≥2.2 | Optimizado para similitud semántica. 50+ idiomas. 768-dim balancea precisión/eficiencia. | BETO embeddings, LASER | Apache 2.0 |
| LLM generativo | **Mistral 7B** (Instruct v0.2) | 7B params | Mejor relación calidad/eficiencia en 7B. Apache 2.0. Ejecutado en nube corporativa (no expone datos a APIs externas). | Llama 3 8B, Qwen 2.5 7B | Apache 2.0 |
| RAG | **LangChain + ChromaDB** | LangChain ≥0.1, ChromaDB ≥0.4 | Framework estándar RAG. ChromaDB ligera, embebible, open-source. | LlamaIndex + Qdrant | MIT / Apache 2.0 |
| OCR | **Tesseract LSTM** (`spa`) + **OpenCV** | Tesseract 5.x, OpenCV 4.x | CER <5% en docs limpios. Sin costo. OpenCV para preprocesamiento. | Google Cloud Vision (costo, datos externos) | Apache 2.0 |
| BD transaccional + vectorial | **PostgreSQL + pgvector** (cloud-managed) | PG 15+, pgvector 0.5+ | Estándar sector público. ACID. pgvector evita BD vectorial separada. | MySQL, MongoDB + Pinecone | PostgreSQL License |
| Búsqueda textual | **Elasticsearch** (cloud-managed) | 8.x | Búsquedas <500ms. Agregaciones para dashboards. Analizador español. | OpenSearch, Solr | Elastic License 2.0 |
| Mensajería | **RabbitMQ** (cloud-managed) o equivalente cloud-native (SQS, Pub/Sub) | 3.12+ | Garantía de entrega, ACK, colas persistentes, reintentos, DLQ. | Kafka (sobredimensionado) | MPL 2.0 / Cloud |
| MLOps | **MLflow + DVC + Evidently AI** | MLflow 2.x, DVC 3.x, Evidently 0.3+ | Versionamiento de modelos/datos + monitoreo de drift + reportes automáticos de equidad. | W&B, Neptune, Great Expectations | Apache 2.0 |
| Dashboard | **Streamlit** (piloto) → **Power BI** (producción) | Streamlit ≥1.28 | Prototipado rápido en Python. Power BI ya usado en sector público. | Grafana, Tableau | Apache 2.0 / Microsoft |
| Seguridad | **OAuth2/JWT + TLS 1.3 + AES-256 + WAF** | — | Autenticación sin estado. Cifrado estándar militar. WAF cloud contra ataques web. | SAML, mTLS | Estándares IETF |

**Criterios de selección:** (1) 100% de componentes de IA son open-source con licencias permisivas → sin costo de licenciamiento. (2) Soberanía de datos garantizada contractualmente: los modelos se ejecutan en la nube corporativa bajo control del contratista, sin exposición a APIs externas. (3) Stack 100% Python facilita transferencia de conocimiento en Fase 4. (4) Infraestructura cloud-managed delegada al contratista → la Defensoría no administra servidores.

---

## B.3 Modelo de datos (resumen)

**Entidades principales:** `ciudadanos` (tipo_doc, num_doc, nombre, dirección, teléfono, email, grupo_especial_proteccion), `casos` (radicado, tipo, urgencia, prioridad, estado, canal, texto_original, pretensión, entidad_referida, timestamps), `asignaciones` (caso_id, profesional_id, tipo_asignacion, timestamp), `respuestas` (caso_id, tipo_respuesta —automática_D5/manual/RAG—, texto_borrador_llm, texto_final, profesional_id, timestamp_revisión), `sync_log` (caso_id, sistema_destino, tipo_evento, payload, response, reintentos, estado), `audit_log` (usuario_id, accion, entidad_afectada, entidad_id, datos_previos, datos_nuevos, ip, timestamp), `feedback` (caso_id, prediccion_original, correccion_humana, motivo, profesional_id, timestamp).

---

## B.4 Integración IRIS/VisionWeb (detalle)

**Contratos de API simulados (OpenAPI 3.0):**

```
IRIS:
  POST   /api/casos               → Crear caso
  PUT    /api/casos/{id}/estado   → Actualizar estado
  GET    /api/casos/{id}          → Consultar caso

VisionWeb:
  POST   /api/v1/expedientes      → Crear expediente
  PUT    /api/v1/expedientes/{id} → Actualizar
  GET    /api/v1/expedientes/{id} → Consultar
```

**Mapeo de campos críticos:**

| Sistema nuevo | IRIS | VisionWeb | Tipo sincronización |
|---|---|---|---|
| radicado | numero_radicado | codigo_expediente | Bidireccional |
| estado | estado_tramite | fase_procesal | Bidireccional |
| profesional_asignado | funcionario_id | responsable_id | Bidireccional |
| fecha_ingreso | fecha_radicacion | fecha_creacion | Sistema → IRIS/VW |
| fecha_cierre | fecha_archivo | fecha_finalizacion | Bidireccional |

---

## B.5 Seguridad cloud y continuidad (§4.5)

**Modelo de responsabilidad compartida:**
- **Proveedor cloud:** seguridad física de data centers, virtualización, red, protección DDoS, cifrado de discos, cumplimiento certificaciones (ISO 27001, SOC 2).
- **Contratista:** seguridad de aplicación (OWASP Top 10), gestión de identidades y accesos (RBAC + OAuth2/JWT), cifrado de datos en tránsito (TLS 1.3), logs de auditoría, backups, gestión de vulnerabilidades (SCA/SAST en CI/CD), respuesta a incidentes.

**RBAC (4 roles):** URAB (recepción, clasificación, validación inicial), Profesional defensorial (gestión de casos asignados, revisión borradores M6), Auditor (solo lectura: logs, métricas, bitácoras), Administrador (configuración del sistema, sin acceso a logs de auditoría, sin acceso a datos de casos).

**Continuidad:** backups automáticos diarios (RPO≤24h). Restauración en ≤4h (RTO). Plan de contingencia ante indisponibilidad de IRIS/VisionWeb: cola de mensajes local con persistencia, acuse diferido al ciudadano, operación sin degradación del sistema propio. Pruebas de recuperación semestrales.

**Anonimización:** la URAB establece lineamientos para que los datos usados en entrenamiento, despliegue y aprendizaje de modelos sean anonimizados antes de su procesamiento. Los datos se gestionan dentro del entorno cloud empresarial controlado, disponibles únicamente para la Defensoría. Cláusula contractual explícita de prohibición de usos secundarios.

---

## B.6 MLOps (§4.6)

| Componente | Herramienta | Descripción |
|---|---|---|
| Versionamiento código | Git + GitHub | Código fuente, pipelines, configuración |
| Versionamiento datos | DVC | Datasets etiquetados versionados. Remoto: bucket cloud (S3/GCS). |
| Versionamiento modelos | MLflow Model Registry | Modelos con tag de versión, métricas, parámetros, artefactos. Stages: Staging → Production → Archived |
| Experiment tracking | MLflow Tracking | Hiperparámetros, métricas, artefactos. Comparación visual de experimentos. |
| Data drift | Evidently AI | Distribución features producción vs entrenamiento. KS, Wasserstein, Jensen-Shannon. |
| Prediction drift | Evidently AI | Distribución de predicciones en el tiempo. Alerta si cambio significativo. |
| Performance monitoring | Evidently AI | Accuracy, recall, F1 sobre muestra de feedback humano. Reporte semanal automático. |
| Feedback loop | API `POST /feedback` | Profesional reporta: {caso_id, prediccion_original, correccion, motivo}. Alimenta reentrenamiento. |
| Política de actualización | Procedimiento documentado | Solicitud → Evaluación (métricas test set) → Aprobación Comité IA → Staging (1 sem) → Producción → Changelog. Modelos NUNCA se actualizan sin aprobación. |

---

## B.7 Infraestructura cloud y plataforma de agentes de IA `[validar]`

| Entorno | Capacidad estimada | Propósito |
|---|---|---|
| Desarrollo | 4 vCPU, 16 GB RAM, 100 GB SSD | Desarrollo y pruebas unitarias. Modelos pequeños (BETO) caben en CPU. |
| Staging | 8 vCPU, 32 GB RAM, 250 GB SSD, 1 GPU T4 (opcional) | Pruebas de integración, carga y equidad pre-producción. |
| Producción — Piloto | 8+ vCPU, 32+ GB RAM, 500 GB SSD, 1 GPU T4 (16 GB VRAM) | Operación URAB Bogotá. GPU para inferencia de Mistral 7B en tiempo razonable. |
| Producción — Nacional | 16+ vCPU, 64+ GB RAM, 2 TB SSD + backup, 2 GPU T4 (alta disponibilidad) | Cobertura nacional con redundancia. Auto-scaling configurado. |

La plataforma cloud permite escalar recursos vertical (más CPU/RAM/GPU) y horizontalmente (más instancias) según la demanda, sin interrupción del servicio. El contratista administra la infraestructura, aplica parches de seguridad, monitorea disponibilidad 24/7 y garantiza los SLA contractuales (disponibilidad ≥99.5%, latencia API <500ms p95).

---

## B.8 Plan de pruebas

| Tipo | Alcance | Herramienta | Criterio de aceptación | Frecuencia |
|---|---|---|---|---|
| Unitarias | Cada función aislada: OCR, NER, validador, reglas urgencia, cosine similarity, tokenizador | pytest | Cobertura >80%. Todos los tests pasan. | Cada commit (CI) |
| Integración | Flujo M1→M4→M2→M3. M7→IRIS mock, M7→VisionWeb mock. M6→ChromaDB→Mistral | pytest + docker-compose | Flujo completo sin errores. Assertions sobre estados intermedios. | Cada sprint |
| Aceptación | Profesionales URAB con 50 casos etiquetados. Encuesta SUS. | Testing manual + formulario | SUS >70. Tiempo tarea <2x manual. Satisfacción >80%. | Antes de cada fase |
| Equidad | Equal Opportunity, Demographic Parity, FNR por género/regional/grupo. Mín. 30 casos. | Evidently AI + pytest custom | Disparidad <5% todos los grupos. Disparate Impact >0.80. | Antes de despliegue + trimestral |
| Carga | 300 peticiones/día, picos 500. Medir p95 latencia, CPU/RAM, tasa error. | Locust / k6 | p95 API <500ms. Tasa error <0.1%. CPU <80%. | Antes de producción |
| Seguridad | OWASP Top 10. SQL injection, XSS, CSRF. TLS 1.3. Acceso no autorizado. Simulación caída IRIS. | OWASP ZAP + manual | 0 vulnerabilidades críticas/altas. TLS 1.3. RBAC intacto. | Antes de producción + semestral |

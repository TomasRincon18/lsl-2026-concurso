# Especificaciones técnicas — Ciencia de Datos

> Destinatario: Equipo de Derecho, para integrar en el documento de fase escrita.
> Puntos cubiertos: 4, 5, 8, 9, 10, 12 del índice.
> Formato: Arial 12, espacio sencillo, márgenes 1.5 cm, tamaño carta, APA 7.ª ed.
> [validar]: pendiente de confirmación con mentoría.
> Referencias (§): Caso oficial URAB (RFP). [Corchetes]: insumos del equipo.

---

## 4. Modelo TO-BE y alcance del piloto (diseño técnico viable)

### 4.1 Diagnóstico del proceso actual (AS-IS)

El macroproceso de atención y trámite de quejas en la Defensoría del Pueblo opera de forma predominantemente manual. La URAB recibe unas 300 peticiones diarias por canales diversos sin normalización (formulario web, correo electrónico en formato libre, correspondencia física, jornadas de campo). Cada petición atraviesa cinco etapas dependientes de intervención humana: (A) recepción y verificación manual de legibilidad y completitud, con radicado creado a mano; (B) clasificación manual en las cuatro categorías jurídicas (Asesoría, Queja, Solicitud de Mediación, Solicitud de Conciliación) sin criterios uniformes ni visibilidad del historial del peticionario; (C) asignación manual a profesionales con doble registro en IRIS y VisionWeb, sistemas que no se comunican entre sí (§2.4.3); (D) gestión defensorial sin apoyo documental automatizado, con el profesional investigando y redactando cada respuesta desde cero; y (E) cierre con riesgo de archivo en una sola plataforma, perdiendo trazabilidad.

Cinco problemas estructurales se derivan de este diagnóstico: (1) saturación operativa por clasificación manual (~15 minutos por caso), que resulta en represamiento crónico y respuestas fuera de términos legales; (2) riesgo jurídico por ausencia de priorización automática, donde casos de riesgo vital (amenazas, desapariciones, menores en peligro, violencia basada en género) pueden quedar rezagados entre consultas rutinarias; (3) doble digitación IRIS/VisionWeb que genera retrabajo, errores e inconsistencias entre plataformas; (4) duplicidad de peticiones no detectada, donde un mismo ciudadano puede presentar la misma queja múltiples veces generando respuestas redundantes o contradictorias; y (5) ausencia de historial unificado por ciudadano, abordándose cada nueva petición como si fuera la primera.

### 4.2 Modelo TO-BE

El proceso rediseñado inserta los ocho módulos solicitados (§3, M1–M8) como una capa de asistencia que automatiza tareas repetitivas y apoya, nunca reemplaza, la toma de decisiones del profesional defensorial. En cada punto donde el sistema produce una clasificación, sugerencia o borrador, existe un mecanismo explícito de validación humana antes de que la decisión surta efectos jurídicos, según lo exigido en §5.4.

| Etapa | AS-IS (hoy) | TO-BE (con IA y cloud) | Mód. | Punto de decisión humana |
|---|---|---|---|---|
| A. Recepción | Funcionario recibe, transcribe a mano, verifica legibilidad, crea radicado manual (~15 min). Errores de digitación frecuentes. | Sistema recibe por API/email/OCR. NER extrae datos automáticamente. Validador detecta faltantes y responde al ciudadano. Radicado semiautomático. | M1 | Valida datos extraídos y confirma radicado |
| B. Triage | Clasificación manual en 4 categorías sin criterios uniformes, sin historial del peticionario. ~30 casos/día por funcionario. | IA sugiere tipo, sub-tema(s), urgencia (1–5) y flag de prioridad. M5 muestra historial unificado. Profesional valida o corrige. | M2, M5 | Valida/corrige clasificación y nivel de urgencia |
| C. Reparto | Asignación manual. Doble registro en IRIS y VisionWeb. Sin monitoreo de tiempos ni alertas de vencimiento. | M3 recomienda entidad y ruta. Un solo registro. M7 sincroniza simultáneamente. SLAs visibles con alertas. | M3, M7 | Confirma competencia de la entidad y ruta de asignación |
| D. Gestión | Profesional investiga y redacta desde cero. Sin apoyo documental. Respuestas inconsistentes entre profesionales. | M6 (RAG) genera borrador basado en normativa real. M5 muestra historial y respuestas previas. Profesional edita y firma. | M6, M5 | Revisa, edita y firma la respuesta. La IA solo redacta borrador |
| E. Cierre | Verificación manual. Archivo con riesgo de quedar en una sola plataforma. Sin trazabilidad. | M7 sincroniza cierre simultáneo en IRIS y VisionWeb. Bitácora inmutable. M8 actualiza dashboards. | M7, M8 | Inicia el cierre tras verificar cumplimiento |

Las decisiones que nunca se automatizan son: evaluación de competencia de la entidad (M3), priorización final de casos de riesgo vital (M2/M6), respuesta de fondo al peticionario (M6 solo redacta borrador), corrección de errores de deduplicación (M4) y cierre del caso (M7). En todos estos puntos la IA asiste o sugiere; la decisión vinculante es exclusivamente humana. El fundamento jurídico de cada una se detalla a continuación:

| Decisión | La IA solo... | El humano siempre... | Fundamento |
|---|---|---|---|
| Competencia de la entidad (M3) | Sugiere direccionamiento según matriz D4 | Confirma o corrige la entidad competente | Debido proceso (CP art. 29). La competencia es decisión de fondo |
| Priorización de riesgo vital (M2/M6) | Asigna score de urgencia y flag de alerta | Determina la prioridad final. El umbral asimétrico prefiere falsos positivos sobre falsos negativos | Derecho a la vida e integridad (CP arts. 11–12) |
| Respuesta de fondo (M6) | Redacta borrador basado en normativa real recuperada por RAG | Revisa, edita, corrige y firma | Debido proceso (CP art. 29). Derecho de petición (CP art. 23) |
| Corrección de duplicación (M4) | Sugiere acumulación si supera umbral de similitud | Decide si acumula, rechaza o marca como relacionado. Justifica por escrito | Seguridad jurídica. Dos casos distintos acumulados vulneran el acceso a la justicia |
| Archivo y cierre (M7/M8) | Sincroniza el cierre en IRIS y VisionWeb | Verifica cumplimiento de todos los pasos e inicia el cierre | Ley 594 de 2000 (gestión documental) |

### 4.3 Mapeo problema → solución

| Problema crítico | Módulo(s) | Cómo lo resuelve |
|---|---|---|
| Volumen y saturación (~300/día) | M1, M2, M6 | Automatiza recepción, extracción de datos y clasificación. El profesional pasa de digitar a supervisar. |
| Riesgo jurídico por falta de priorización | M2, M3 | Score de urgencia (1–5) con reglas auditables, detección automática de sujetos de especial protección, SLAs visibles con alertas. |
| Doble registro IRIS/VisionWeb | M7 | Capa de orquestación con modelo canónico: único punto de entrada, sincronización bidireccional simultánea, bitácora de cada operación. |
| Duplicidad de peticiones | M4 | Comparación semántica mediante embeddings y cosine similarity. Si ≥85% de similitud + mismo CC + misma pretensión: sugerencia de acumulación al profesional. |
| Peticionarios sin historial | M5 | Índice unificado Elasticsearch. Historial completo del ciudadano consultable por cédula en menos de 500ms. |

### 4.4 Alcance del piloto en URAB

El piloto se implementa en la URAB de Bogotá (~300 peticiones/día, 8–10 profesionales, 8 semanas de operación controlada en la Fase 3). Entran en el piloto los módulos M1, M2, M3, M4, M5 y M6 con validación humana en todos los puntos de decisión (§5.4), M7 con integración mínima IRIS/VisionWeb requerida por §4.2, y M8 con el Dashboard 1 de carga temática. Se difieren al escalamiento progresivo otras Unidades de Análisis fuera de Bogotá, la integración con Carpeta Ciudadana Digital (gov.co) como componente opcional de M7 (el Banco de Preguntas indica que el proponente puede proponer un mecanismo de acuse de recibo y consulta de estado), y la foliación electrónica con firma de índice bajo estándares AGN, ofrecida como diferenciador a partir de §4.3 y la gestión documental de §5.1 (Banco Q8: no es requisito mínimo). Las métricas y obligaciones de la Fase 3 se comprometen en el piloto URAB; la analítica institucional se habilita sobre los datos del piloto y se extiende con el escalamiento.

Criterios de salida del piloto: precisión de clasificación ≥90%, recall de urgencias/riesgo vital ≥99%, detección de duplicados ≥85% recall, tiempo ingreso→asignación ≤4h (p90), disponibilidad del sistema ≥99.5% mensual. Si la precisión cae por debajo de 75% no se escala sin reentrenar.

---

## 5. Arquitectura técnica de la solución

### 5.1 Decisión de arquitectura: nube corporativa con capa de orquestación

La solución se despliega sobre una plataforma corporativa en nube para la administración de agentes de inteligencia artificial, operada por el contratista o un proveedor autorizado bajo los lineamientos de seguridad, administración y gobernanza definidos por la Defensoría del Pueblo. Esta modalidad es la más adecuada por cuatro razones:

**Orquestación unificada de modelos.** La plataforma permite utilizar, versionar y administrar simultáneamente diferentes modelos de IA, tanto los desarrollados específicamente para la Defensoría (BETO fine-tuned para clasificación, modelos NER propios) como modelos fundacionales de terceros (Mistral 7B para generación de borradores, Sentence-Transformers para embeddings semánticos), bajo un mismo marco corporativo de seguridad, control de accesos y trazabilidad de ejecuciones.

**Delegación de infraestructura.** Los requerimientos de infraestructura, mantenimiento, seguridad física, escalabilidad automática y soporte técnico 24/7 se delegan en el contratista o proveedor autorizado. Esto libera a la Defensoría de la carga operativa de administrar servidores, actualizar dependencias, escalar recursos ante picos de demanda y mantener la continuidad del servicio. El contratista asume los niveles de servicio (SLA) de disponibilidad ≥99.5%, tiempo de respuesta de API <500ms (p95) y recuperación ante desastres con RPO≤24h y RTO≤4h.

**Integración y sincronización optimizadas.** El despliegue en nube ofrece condiciones de conectividad, disponibilidad y latencia para la integración con IRIS y VisionWeb, así como para la sincronización bidireccional mediante la capa de orquestación con modelo canónico de datos. Los eventos de ciclo de vida del caso (creado, actualizado, cerrado) se publican en colas de mensajería cloud-native que garantizan la entrega y la trazabilidad de cada sincronización hacia los sistemas legados.

**Protección de datos bajo modelo contractual.** En materia de tratamiento de datos personales (Ley 1581 de 2012), la plataforma opera bajo un modelo de protección definido contractualmente: la Defensoría es la responsable del tratamiento y el contratista actúa como encargado con instrucciones documentadas. Los datos se procesan dentro de un entorno empresarial controlado, con cifrado AES-256 en reposo y TLS 1.3 en tránsito, acceso segmentado por roles RBAC, y logs inmutables de auditoría. La URAB establece lineamientos para la anonimización de los datos utilizados en procesos de entrenamiento, despliegue y aprendizaje de modelos, de modo que estos se gestionen exclusivamente para los fines misionales de la organización y no estén disponibles para terceros.

Frente al problema de IRIS vs. VisionWeb, dos sistemas sin comunicación entre sí (§2.4.3), mientras §4.2 exige evitar dobles registros, la capa de orquestación opera sobre la infraestructura cloud manteniendo un registro único con modelo canónico de datos y sincronización bidireccional. Esta decisión cumple §4.2 (evitar doble registro), reduce el riesgo del §2.4.3 (archivo en una sola plataforma), y alimenta la trazabilidad requerida por §5.4. Si los sistemas legados no ofrecen API de escritura (Banco Q10), se despliega RPA como capa de contingencia.

### 5.2 Arquitectura lógica

```
[ Capa de acceso ]  Bandejas URAB · Bandejas profesionales · Dashboards (M8)
  Acceso web seguro (HTTPS/TLS 1.3) · Autenticación OAuth2/JWT
──────────────────────────────────────────────────────────────────────────────
[ Capa de orquestación ] API Gateway cloud-native · Message Broker · Workflow ingreso→cierre
  Bitácora inmutable · Orquestador de modelos de IA
──────────────────────────────────────────────────────────────────────────────
[ Plataforma de agentes de IA en nube corporativa ]
  ● Motor M2, Clasificación y triaje (BETO fine-tuned)
  ● Motor M4, Anti-duplicación (Sentence-Transformers + cosine similarity)
  ● Motor M6, Asistente generativo RAG (ChromaDB + Mistral 7B)
  ● Motor M5, Historial unificado (Elasticsearch)
  ● Motor M1, OCR (Tesseract) + NER (spaCy)
  ● Administración: versionamiento, monitoreo, drift, feedback loop
──────────────────────────────────────────────────────────────────────────────
[ Modelo canónico de datos ] PostgreSQL + pgvector (cloud-managed)
──────────────────────────────────────────────────────────────────────────────
[ Capa de integración ] Conectores → IRIS · VisionWeb · gov.co (opcional)
  RPA como contingencia
──────────────────────────────────────────────────────────────────────────────
[ Seguridad transversal cloud ] RBAC · OAuth2/JWT · TLS 1.3 · AES-256
  Logs inmutables · WAF · DDoS protection · Backup automático
```

### 5.3 Stack tecnológico

La plataforma cloud corporativa permite la administración unificada de los siguientes modelos y servicios. Todos los componentes de IA son de código abierto con licencias permisivas (MIT, Apache 2.0), sin costo de licenciamiento. La plataforma administra las distintas versiones de estos modelos, tanto los desarrollados por el contratista como los modelos fundacionales de terceros, bajo un mismo marco de seguridad y gobernanza.

| Capa | Tecnología | Justificación principal | Licencia |
|---|---|---|---|
| Plataforma cloud | IaaS/PaaS corporativa (AWS/Azure/GCP o GovCloud MinTIC) | Orquestación unificada de agentes de IA, administración de versiones, monitoreo, escalabilidad automática, delegación de infraestructura | Comercial / Gubernamental |
| Backend / API | FastAPI (Python) ≥0.110 | Alto rendimiento async, documentación OpenAPI 3.0 automática, ecosistema IA nativo, validación Pydantic | MIT |
| Clasificación NLP | BETO (dccuchile/bert-base-spanish-wwm-uncased) fine-tuned | Entrenado en español por U. de Chile. 110M parámetros. Whole Word Masking. Probado en dominio legal. Más ligero que RoBERTa-es | MIT |
| Extracción de entidades (NER) | spaCy (es_core_news_lg) + fine-tuning ≥3.7 | Pipeline NLP más maduro para español. Inferencia rápida. Componentes integrados: tokenización, POS tagging, NER | MIT |
| Similitud semántica | Sentence-Transformers (paraphrase-multilingual-mpnet-base-v2) ≥2.2 | Optimizado para similitud semántica en 50+ idiomas. 768-dim balancea precisión/eficiencia de almacenamiento | Apache 2.0 |
| LLM generativo | Mistral 7B (Instruct v0.2) | Mejor relación calidad/eficiencia entre modelos open-source de 7B parámetros. Ejecutado en nube corporativa: datos no salen a APIs externas | Apache 2.0 |
| RAG | LangChain ≥0.1 + ChromaDB ≥0.4 | Framework estándar RAG. ChromaDB es base de datos vectorial ligera, embebible, open-source | MIT / Apache 2.0 |
| OCR | Tesseract LSTM (spa) + OpenCV 4.x | CER <5% en documentos limpios. OpenCV para preprocesamiento (deskew, binarización). Sin costo de licencia | Apache 2.0 |
| BD transaccional + vectorial | PostgreSQL 15+ + pgvector 0.5+ (cloud-managed) | Estándar sector público colombiano. ACID. pgvector evita base de datos vectorial separada, simplificando la arquitectura | PostgreSQL License |
| Búsqueda textual | Elasticsearch 8.x (cloud-managed) | Búsquedas <500ms. Agregaciones para dashboards. Analizador configurable para español | Elastic License 2.0 |
| Mensajería | RabbitMQ 3.12+ o equivalente cloud-native | Garantía de entrega con ACK, colas persistentes en disco, reintentos configurables, Dead Letter Queue | MPL 2.0 |
| MLOps | MLflow 2.x + DVC 3.x + Evidently AI 0.3+ | Versionamiento de modelos y datos, monitoreo de drift, reportes automáticos de equidad | Apache 2.0 |
| Dashboard | Streamlit ≥1.28 (piloto) → Power BI (producción) | Prototipado rápido en Python puro. Power BI ya usado en sector público colombiano | Apache 2.0 / Microsoft |
| Seguridad | OAuth2/JWT + TLS 1.3 + AES-256 + WAF | Autenticación sin estado, cifrado en tránsito (última versión) y reposo (estándar militar), protección contra ataques web | Estándares IETF |

**Infraestructura cloud estimada** [validar]: entorno de desarrollo con 4 vCPU, 16 GB RAM, 100 GB SSD. Piloto en producción con 8+ vCPU, 32+ GB RAM, 500 GB SSD, 1 GPU T4 (16 GB VRAM) para inferencia de Mistral 7B. Cobertura nacional con 16+ vCPU, 64+ GB RAM, 2 TB SSD + backup, 2 GPU T4 en alta disponibilidad con auto-scaling.

### 5.4 Descripción funcional de módulos

M1, Recepción Inteligente. Recibe peticiones por todos los canales, aplica OCR a documentos escaneados o fotografiados, extrae automáticamente los datos del ciudadano mediante NER, verifica completitud de campos obligatorios (nombre, documento de identidad, descripción del hecho, pretensión), y genera radicado único. Si se detectan datos faltantes, el sistema responde automáticamente al ciudadano solicitando la información complementaria con plantillas institucionales. Métrica objetivo: tasa de extracción correcta de entidades ≥90%.

M2, Clasificación y Triaje. Clasifica la petición en las 4 categorías jurídicas mediante un modelo BETO con fine-tuning. Un sub-clasificador multi-etiqueta asigna los sub-temas aplicables (~12). Un sistema de reglas determinístico y auditable, no de caja negra, asigna nivel de urgencia en escala 1 a 5 según los criterios jurídicos del equipo de Derecho. Un priorizador cruza el texto con el catálogo de sujetos de especial protección constitucional y asigna flags de alerta. El profesional de URAB valida o corrige toda clasificación. Métrica objetivo: accuracy ≥90%, recall en urgencias/riesgo vital ≥99% (umbral asimétrico).

M3, Asignación y Enrutamiento. Determina la entidad competente mediante matriz de reglas tipo+sub-tema (alimentada y validada por el equipo de Derecho). Si la Defensoría es competente, recomienda ruta interna según carga y perfil del profesional. Bandejas de trabajo con estados y monitoreo de SLA (ingreso→asignación <4h, gestión→cierre <15 días hábiles) con alertas automáticas al 80% y 100% del plazo. Métrica objetivo: tiempo ingreso→asignación ≤15 min en el 90% de los casos.

M4, Anti-Duplicación. Convierte el texto de la petición en un embedding semántico de 768 dimensiones y lo compara vía cosine similarity contra los casos existentes en la base de datos. Si la similitud supera el 85% y coinciden el documento de identidad y la pretensión del ciudadano, el sistema sugiere acumulación al profesional mediante una interfaz que muestra ambas peticiones lado a lado con los campos coincidentes resaltados. El profesional decide con justificación escrita. Métrica objetivo: precisión de sugerencias ≥85%, recall de duplicados ≥90%.

M5, Peticionarios Recurrentes. Índice Elasticsearch que permite consultar por número de cédula el historial completo de peticiones de un ciudadano (radicados, fechas, tipos, estados, profesionales asignados, respuestas emitidas) en menos de 500ms. El sistema sugiere además respuestas previas y plantillas institucionales aplicables al caso. Métrica objetivo: tiempo de consulta <500ms (p95).

M6, Asistente Generativo (RAG + LLM). Opera en dos modos. Para consultas complejas, el sistema recupera fragmentos relevantes de la base de conocimiento (normativa, jurisprudencia, plantillas institucionales, respuestas previas anonimizadas) mediante ChromaDB, los inyecta en un prompt con instrucciones estrictas, no inventar, lenguaje ciudadano, no decidir, y Mistral 7B, ejecutándose en la nube corporativa, genera un borrador. El profesional siempre revisa, edita y firma. Para consultas simples del catálogo previamente aprobado por el equipo de Derecho (estado del radicado, profesional asignado, reenvío de constancia), el sistema responde automáticamente con plantillas sin pasar por el LLM. Adicionalmente, M6 incorpora un detector de patrones de riesgo en tiempo real (amenazas, desapariciones, menores en peligro, VBG) que notifica inmediatamente al profesional y dispara alertas en el dashboard. Métrica objetivo: borradores aceptados sin corrección mayor ≥70%, tiempo de generación <10s.

M7, Interoperabilidad. Elimina la doble digitación. El nuevo sistema es el único punto de entrada de peticiones. Cada evento de ciclo de vida se publica en el message broker cloud y dos consumidores independientes replican simultáneamente a IRIS y VisionWeb. Reintentos con backoff exponencial ante fallos (1s, 2s, 4s, 8s, 16s, 32s). Tras 6 fallos, alerta al administrador. RPA como contingencia si los sistemas legados no ofrecen API de escritura. Bitácora inmutable de cada sincronización. Conciliación diaria automática entre los tres sistemas. Métrica objetivo: sincronización exitosa ≥99.5%.

M8, Analítica. Cuatro dashboards que transforman datos operativos en información para la toma de decisiones: (1) carga temática, distribución por tipo, tendencias, top 10 sub-temas, (2) cuellos de botella, tiempos por etapa, carga por profesional, casos vencidos, (3) recurrencia y duplicidad, y (4) equidad, desagregada por género, región y grupo de especial protección, con alertas de disparidad significativa. Incluye una capa de investigación institucional con datos anonimizados (k-anonymity ≥5) y acceso restringido a rol "investigador" previa aprobación del Comité de IA. Métrica objetivo: dashboards actualizados en tiempo real, latencia <1 minuto desde el evento.

### 5.5 Integración IRIS/VisionWeb

El modelo canónico de datos mapea los campos equivalentes entre los tres sistemas: radicado ↔ numero_radicado (IRIS) ↔ codigo_expediente (VisionWeb); estado ↔ estado_tramite (IRIS) ↔ fase_procesal (VisionWeb); profesional_asignado ↔ funcionario_id (IRIS) ↔ responsable_id (VisionWeb). La sincronización es bidireccional para todos los campos críticos.

Las APIs simuladas bajo OpenAPI 3.0 son POST /api/casos, PUT /api/casos/{id}/estado y GET /api/casos/{id} para IRIS, y POST /api/v1/expedientes, PUT /api/v1/expedientes/{id} y GET /api/v1/expedientes/{id} para VisionWeb. El modelo de datos incluye las entidades ciudadanos, casos, asignaciones, respuestas, sync_log (bitácora inmutable de sincronización), audit_log (logs inmutables de auditoría) y feedback (correcciones humanas para reentrenamiento).

### 5.6 Seguridad, MLOps y pruebas

**Seguridad y protección de datos (§4.5).** El modelo de seguridad opera bajo el esquema de responsabilidad compartida de la plataforma cloud corporativa: el proveedor cloud garantiza la seguridad física, de red y de virtualización; el contratista implementa los controles a nivel de aplicación y datos. Cuatro roles de acceso (RBAC): URAB, Profesional defensorial, Auditor y Administrador, este último sin acceso a logs de auditoría, en cumplimiento del principio de mínimo privilegio. Autenticación OAuth2/JWT sin estado. Cifrado TLS 1.3 en tránsito y AES-256 en reposo. Logs inmutables (append-only) con backup automático diario a almacenamiento externo. Plan de contingencia ante indisponibilidad de IRIS/VisionWeb con cola de mensajes local y acuse diferido al ciudadano. El contratista garantiza contractualmente la anonimización de los datos utilizados en entrenamiento, despliegue y aprendizaje de modelos, operando dentro de un entorno empresarial controlado y disponible únicamente para la Defensoría.

**MLOps (§4.6).** Versionamiento integral: Git (código), DVC (datasets etiquetados), MLflow Model Registry (modelos con métricas, parámetros y artefactos). Monitoreo de drift de datos y predicciones mediante Evidently AI con reportes automáticos. Canal de retroalimentación humana: API donde los profesionales reportan errores de clasificación; esos datos etiquetados alimentan el siguiente ciclo de reentrenamiento. Política de actualización controlada: solicitud → evaluación técnica → aprobación del Comité de IA → staging → producción con changelog. Los modelos nunca se actualizan sin aprobación explícita.

**Plan de pruebas.** Pruebas unitarias (cada componente aislado), de integración (flujos M1→M4→M2→M3 y M7→IRIS/VisionWeb), de aceptación (profesionales URAB con casos reales), de equidad (Equal Opportunity, Demographic Parity y False Negative Rate segmentados), de carga (simulación de 300 peticiones/día con picos de 500), y de seguridad (pentesting, revisión TLS, simulación de indisponibilidad).

---

## 8. Cambio sociotécnico, enfoque diferencial y pruebas de equidad

### 8.1 Cambio sociotécnico (§5.3)

La introducción de IA en el macroproceso de la Defensoría transforma la forma en que los funcionarios trabajan y cómo los ciudadanos interactúan con la institución. La siguiente tabla identifica las nuevas capacidades, las conductas que se habilitan, los impactos disruptivos que deben anticiparse y las decisiones de gobernanza que los mitigan:

| Capacidad nueva | Conducta que cambia | Riesgo a anticipar | Decisión de gobernanza |
|---|---|---|---|
| Lectura y clasificación masiva (~300 peticiones/día en minutos) | El profesional pasa de clasificar manualmente a supervisar la IA. Dedica más tiempo a casos complejos y menos a tareas repetitivas. | Sobre-automatización: tentación de delegar decisiones que requieren juicio humano (priorización, competencia). | Lista taxativa de decisiones nunca automatizables (§4.2). Human-in-the-loop obligatorio en todos los puntos de decisión. |
| Vista unificada del historial por ciudadano (M5) | Atender peticionarios recurrentes con contexto completo en segundos. Respuestas más coherentes y personalizadas entre distintas interacciones. | Privacidad por concentración de historial: todos los casos de un ciudadano visibles en un solo punto. | Principio de minimización: solo se muestra lo necesario para el caso actual. Roles de acceso diferenciados. Consentimiento informado. |
| Borradores de respuesta generados por IA (M6) | Redactar respuestas en minutos en lugar de horas. El profesional edita y personaliza en lugar de empezar desde cero. | Confianza excesiva en la IA: omitir la revisión humana obligatoria, asumir que el borrador es correcto. | Revisión y firma humana registrada en logs inmutables. UI con fricción deliberada (confirmación explícita, tiempo mínimo de visualización). |
| Monitoreo y analítica en tiempo real (M8) | Visibilizar patrones de carga, cuellos de botella y disparidades entre grupos poblacionales que antes eran invisibles. | Datos agregados que podrían amplificar barreras o estigmatizar grupos si se usan sin contexto. | Enfoque diferencial en dashboards. Privacidad (k-anonymity ≥5). Reportes públicos de equidad. |
| Interoperabilidad IRIS/VisionWeb (M7) | Eliminar la doble digitación. Un solo registro, dos plataformas actualizadas simultáneamente. | Resistencia al cambio organizacional. Posible percepción de redundancia del nuevo sistema. | Gestión de cambio desde Fase 0, alineada con MIPG e ISO/IEC 42001:2023. Capacitación mínima de 20 profesionales (§6.1). |

La estrategia de gestión de cambio incluye sesiones de sensibilización sobre IA en el sector público, manuales de rol con procedimientos claros, y mesa de ayuda durante el piloto y los primeros seis meses de operación (§6.4).

### 8.2 Pruebas de equidad algorítmica (§5.2)

En el contexto de la Defensoría del Pueblo, cuya misión constitucional es proteger los derechos humanos de toda la población, con énfasis en los grupos más vulnerables, un sesgo algorítmico no es un error técnico: es una vulneración del derecho fundamental a la igualdad (Art. 13 CP). La solución incorpora pruebas de equidad como gate de calidad obligatorio antes de cada despliegue.

**Métricas utilizadas.** Equal Opportunity (diferencia en tasa de aciertos positivos entre grupos), Demographic Parity (diferencia en proporción de predicciones entre grupos), Disparate Impact Ratio (cociente entre el grupo con peor y mejor rendimiento, debe ser >0.80), y False Negative Rate por grupo (el error más grave: omitir un caso urgente más en unos grupos que en otros).

**Segmentación.** Género (solo cuando el ciudadano lo proporciona voluntariamente, nunca inferido), regional/departamento, grupo de especial protección (NNA, mujeres VBG, discapacidad, adultos mayores, desplazados, minorías étnicas, población privada de libertad, migrantes), y canal de ingreso. Si una muestra tiene menos de 30 casos, esa segmentación no se reporta.

**Niveles de alerta y protocolo de actuación:**

| Disparidad detectada | Acción |
|---|---|
| <3% de diferencia entre grupos | Verde. Aceptable. Monitoreo continuo. |
| 3–5% o diferencia de precisión >5 puntos entre subgrupos | Amarillo. Revisión técnica. Análisis de causas. No detiene despliegue. |
| 5–10% o cociente de falsos negativos >1.5 | Naranja. Escalar al Comité de IA en 5 días. Activar mitigación: rebalanceo de datos, threshold tuning o adversarial debiasing. Detener despliegue para el grupo afectado. |
| >10% de diferencia | Rojo. Suspender el módulo para todos los grupos. Investigación urgente. Notificar al Defensor Delegado. |

**Ejemplo de activación en un escenario del piloto.** En una evaluación trimestral con 5.000 peticiones, si el accuracy para hombres es 91% frente a 84% para mujeres (diferencia de 7 pp, nivel naranja) y la tasa de falsos negativos en urgencias es 1.2% para hombres frente a 3.5% para mujeres (cociente de 2.92, nivel rojo), se suspende M2 para decisiones de urgencia que afecten a mujeres y se activa mitigación inmediata.

**Estrategias de mitigación disponibles.** (1) Rebalanceo del dataset: recolectar y etiquetar más ejemplos del grupo subrepresentado (1–2 semanas). (2) Threshold tuning: ajustar el umbral de decisión para el grupo afectado igualando tasas de error (2–3 días). (3) Adversarial debiasing: entrenar un adversario que intente predecir el grupo y penalizar al modelo principal si acierta (2–4 semanas). (4) Revisión humana reforzada: doble revisión para el grupo impactado como contención inmediata mientras se aplican las soluciones técnicas.

**Monitoreo continuo.** Evidently AI genera reportes trimestrales automáticos de equidad desagregados por género, regional, grupo de especial protección, canal de ingreso y sub-tema. El Comité de IA recibe un reporte específico mensual de False Negative Rate para grupos de especial protección. La regla de despliegue es inviolable: ningún modelo se despliega en producción sin haber pasado las pruebas de equidad con nivel verde, o excepcionalmente amarillo con plan de mitigación aprobado y fecha límite. Niveles naranja o rojo bloquean el despliegue.

**Salvaguardas institucionales.** Validación manual de todos los rechazos automáticos, revisión de casos de riesgo vital exclusivamente por un funcionario, formatos accesibles para personas con discapacidad, prohibición absoluta de automatizar decisiones de fondo.

---

## 9. Matriz de riesgos, SPI, corrupción y daño antijurídico (§5.5)

Se identifican 12 riesgos en tres familias: T (técnica), O (operacional) y J (jurídica). La matriz que sigue incluye para cada riesgo su mitigación y frecuencia de monitoreo. Los riesgos R3 (falso negativo en urgencias) y R5 (sesgo algorítmico) se detallan con mayor profundidad por su criticidad para los derechos fundamentales.

| ID | F. | Riesgo | Mitigación principal | Monitoreo |
|---|---|---|---|---|
| R1 | T | Caída de conectividad o indisponibilidad de IRIS/VisionWeb que genera represamiento (§2.4.2) | Colas resilientes cloud, modo offline con acuse diferido, plan de contingencia documentado | Semanal |
| R2 | T | Error de integración: doble registro o archivo en una sola plataforma (§2.4.3) | Modelo canónico + sincronización bidireccional + conciliación diaria automática | Diaria |
| R3 | T | Falso negativo en clasificación de urgencias: no detección de riesgo vital | Umbral asimétrico calibrado para recall ≥99%, revisión humana de casos sin flag, reentrenamiento ante cualquier fallo | Diaria |
| R4 | T | Falso positivo en deduplicación: acumulación inadecuada de casos diferentes | Umbral 85% configurable + coincidencia CC + pretensión. Justificación escrita obligatoria del profesional | Semanal |
| R5 | T/O | Sesgo algorítmico que amplifica exclusiones (género, discapacidad, juventud, etnia) | Pruebas de equidad pre-despliegue, 4 niveles de alerta con protocolo graduado, adversarial debiasing | Cada release + trimestral |
| R6 | O | Dependencia excesiva del sistema, pérdida de supervisión humana (§5.4) | Lista taxativa de decisiones nunca automatizables. Human-in-the-loop obligatorio. UI con fricción en puntos críticos | Semanal |
| R7 | O | Omisiones o uso indebido por profesionales (carga incorrecta, falta de revisión) | Capacitación desde Fase 0 con certificación, roles con mínimo privilegio, auditoría de actividad | Mensual |
| R8 | J | Incumplimiento de términos legales (CPACA, Ley 1755/2015, derecho de petición) | Dashboards M8 con semaforización, alertas M3 al 80% y 100% del plazo, escalamiento en cadena | Diaria |
| R9 | J | Vulneración de privacidad o tratamiento inadecuado de datos sensibles (Ley 1581/2012) | Defensoría responsable, contratista encargado con instrucciones contractuales. AES-256 + TLS 1.3 + anonimización. Evaluación de impacto (AIA) | Trimestral |
| R10 | J | Falta de trazabilidad algorítmica (Directiva Conjunta 007/2025) | Ficha de Transparencia Algorítmica alineada con NIST AI RMF 1.0. Logs inmutables con registro de cada decisión | Trimestral |
| R11 | T/O | Alucinación del LLM generando información falsa en respuesta oficial | Arquitectura RAG: solo genera sobre documentos reales de ChromaDB. Revisión humana obligatoria. Solo D5 automático | Semanal |
| R12 | T | Incidente de ciberseguridad con exposición de datos sensibles [antecedente DOC_1] | Seguridad cloud bajo responsabilidad compartida. RBAC + OAuth2 + cifrado + pentesting + equipo de respuesta | Mensual |

**Detalle de riesgos críticos.** R3 (falso negativo en urgencias): probabilidad baja con el umbral asimétrico calibrado, pero impacto crítico. Un falso negativo en riesgo vital implica daño antijurídico por omisión y vulneración de derechos fundamentales (vida, integridad), con posible responsabilidad patrimonial del Estado (CP art. 90). La mitigación principal es el umbral asimétrico calibrado con un conjunto gold de 200 casos etiquetados por juristas de la URAB, revisión humana de todo caso sin flag de urgencia en las primeras 4 horas, y reentrenamiento inmediato ante cualquier falso negativo real. R5 (sesgo algorítmico): probabilidad media, impacto alto. Su materialización equivale a una denegación de acceso a la justicia por origen o condición. Se mitiga con las pruebas de equidad como gate obligatorio de despliegue y los 4 niveles de alerta con protocolo graduado descritos en §8.2.

---

## 10. Plan de trabajo por fases y entregables (§6)

El proyecto se organiza en 5 fases secuenciales con criterios de salida verificables, desplegadas sobre la plataforma cloud corporativa. Duración total: 32 semanas de ejecución más 12 meses de garantía y evolución [validar].

| Fase | Dur. | Objetivo | Entregables clave | Criterio de aceptación |
|---|---|---|---|---|
| F0. Alistamiento y diagnóstico | 4 sem | Diagnosticar el AS-IS y preparar los datos | Flujograma validado, dataset etiquetado (~1000 casos), taxonomía, línea base de métricas, configuración inicial del entorno cloud | Diagnóstico y taxonomía aprobados por el comité del proyecto |
| F1. Diseño de arquitectura e integración | 8 sem | Definir la arquitectura cloud y la estrategia de integración con IRIS/VisionWeb | Arquitectura objetivo, diagrama de integración, modelo canónico de datos, especificación de seguridad cloud, diseño de la plataforma de agentes de IA | Arquitectura validada con equipos de sistemas legados |
| F2. Construcción de módulos IA | 12 sem | Desarrollar, entrenar y probar los módulos core en el entorno cloud | Prototipos M1–M6 desplegados en cloud de desarrollo. Informe de desempeño sobre conjunto gold. Pruebas de equidad superadas | Métricas ≥ metas (§12). Sin disparidad >5% en equidad |
| F3. Implementación, capacitación y operación inicial | 8 sem | Desplegar el piloto en producción cloud, capacitar y operar en modo supervisado | Sistema en producción, 100% profesionales capacitados, dashboards M8, mesa de ayuda, informe comparativo sistema vs. manual | Métricas del piloto en umbrales. Satisfacción ≥80% |
| F4. Gobernanza y mejora continua | 12+ meses | Operación autónoma, transferencia y evolución controlada | Comité de IA operando, reportes periódicos de métricas y equidad, transferencia de conocimiento al equipo interno | Equipo interno autónomo ≥3 meses. Auditoría sin hallazgos críticos |

**Carta Gantt:** F0 (semanas 1–4) → F1 (5–12) → F2 (13–24) → F3 (25–32) → F4 (33 en adelante).

**Presupuesto estimado a 3 años** [validar], basado en referencias de SECOP IA.xlsx, con infraestructura cloud como servicio gestionado por el contratista:

| Rubro | Año 1 | Año 2 | Año 3 | Total |
|---|---|---|---|---|
| Implementación | $575 M | $60 M | $60 M | $695 M |
| Licencias | $0 | $0 | $0 | $0 |
| Infraestructura cloud | $125 M | $50 M | $50 M | $225 M |
| Capacitación | $55 M | $10 M | $10 M | $75 M |
| Evolución (reentrenamiento, auditorías) | $30 M | $50 M | $60 M | $140 M |
| **Total** | **$785 M** | **$170 M** | **$180 M** | **$1.135 M** |

Las licencias suman cero porque el 100% del stack de IA es open-source (MIT, Apache 2.0). El 55% de la inversión se concentra en el año 1 (implementación intensiva). Los años 2 y 3 cubren soporte, evolución y transferencia. El evento de cotización en Fase 0 validará los supuestos unitarios antes de la firma del contrato. Pago por hitos verificables: 15% a la firma, 10% al diagnóstico aprobado, 15% a la arquitectura validada, 25% a los módulos IA aprobados, 20% al piloto en operación, 10% a la cobertura de 6 regionales, y 5% a la transferencia completada.

---

## 12. Métricas y línea base del piloto (§4.4)

La línea base se levanta durante la Fase 0 (actualmente no existen mediciones automatizadas; el Banco Q18 confirma que el proceso tarda varios días y no se mide formalmente). Los valores AS-IS son estimaciones basadas en el caso que deben refinarse con los datos reales del diagnóstico [validar].

| # | Indicador | Línea base (est.) | Meta piloto | Umbral de alerta | Frecuencia |
|---|---|---|---|---|---|
| M1 | Tiempo de clasificación sugerida (M2) | Varias horas–2 días (manual, sin medición) | ≤15 min en 90% (p90) | p90 >30 min | Diaria |
| M2 | Precisión de clasificación, accuracy (M2) | ~80% (humano, con fatiga) | ≥90% global; ≥90% subclasificación | <85% o caída >3 puntos | Semanal |
| M3 | Recall de urgencias / riesgo vital (M2) | No medido | ≥99% (falso negativo ≈0) | Cualquier FN real | Diaria |
| M4 | Precisión de sugerencias de duplicados (M4) | No hay sistema | ≥85% | <70% | Semanal |
| M5 | Recall de duplicados (M4) | <30% (muestreo manual) | ≥90% | <80% | Semanal |
| M6 | Reducción de reprocesos de reparto | Línea base F0 | ≥50% de reducción | <20% | Mensual |
| M7 | Cumplimiento de tiempos internos | No sólido | ≥90% de peticiones en plazo | <80% | Mensual |
| M8 | Tiempo ingreso→asignación (M3) | ~2 días hábiles | ≤4h en 90% (p90) | Desvío >+50% | Semanal |
| M9 | Tiempo ingreso→primera respuesta | 15–20 días hábiles | ≤10 días hábiles en 90% (p90) | >15 días | Mensual |
| M10 | Extracción correcta de entidades (M1) | ~70–80% (digitación manual) | ≥90% campos obligatorios | <85% | Semanal |
| M11 | Borradores M6 sin corrección mayor | No aplica | ≥90% consultas simples | Conflictivas >5% | Semanal |
| M12 | Disponibilidad del sistema | No aplica | ≥99.5% mensual | <99% | Tiempo real |
| M13 | Sincronización IRIS/VisionWeb (M7) | 0% (sin integración) | ≥99.5% | <99% | Tiempo real |
| M14 | Tasa de error en OCR (M1) | No medido | <5% docs limpios, <10% baja calidad | >10% / >15% | Semanal |
| M15 | Equal Opportunity por género (M2) | No medido | <5% de diferencia | >5% | Trimestral |
| M16 | Disparate Impact Ratio | No medido | >0.80 | <0.80 | Trimestral |
| M17 | Satisfacción del profesional URAB | No aplica | ≥80% (encuesta trimestral) | <70% | Trimestral |

**Plan de medición.** Las métricas operativas (M1, M8, M9) se miden en tiempo real desde los logs del sistema y se visualizan en M8 Dashboard 2. Las de calidad de IA (M2–M5, M10, M11) se calculan semanalmente con MLflow y Evidently AI sobre el conjunto gold y los datos de feedback humano. Las de infraestructura (M12–M14) se monitorean con Prometheus y Grafana en tiempo real. Las de equidad (M15, M16) se evalúan trimestralmente con Evidently AI. La satisfacción (M17) se mide con formulario integrado en el sistema al cierre de cada caso.

**Metodología de umbral asimétrico para riesgo vital.** El costo de un falso negativo en casos de riesgo vital (desapariciones, amenazas, menores en peligro, VBG activa) no es comparable al de un falso positivo: el primero implica daño antijurídico y vulneración de derechos fundamentales (§2.4.2 + §5.5); el segundo representa un costo operativo manejable (revisión adicional de ~15 minutos). Por esta razón, el clasificador M2 se calibra deliberadamente para ser hipersensible a indicadores de riesgo vital. El procedimiento es el siguiente: en la Fase 0, los juristas de la URAB etiquetan un conjunto gold de al menos 200 peticiones con indicadores reales de riesgo vital. En la Fase 2, durante el fine-tuning de BETO, se entrena un clasificador binario adicional para la clase "riesgo vital" y se ajusta el umbral de decisión (threshold) hacia abajo para alcanzar una sensibilidad (recall) ≥99%. Esto incrementa los falsos positivos, pero de forma controlada.

La siguiente tabla ilustra el trade-off con datos estimados:

| Escenario | Threshold | Recall riesgo vital | Falsos positivos/día | Costo operativo diario |
|---|---|---|---|---|
| Umbral estándar (simétrico) | 0.50 | 92% | ~5 casos | ~25 min extra |
| **Umbral asimétrico (propuesto)** | **0.15** | **99.5%** | **~18 casos** | **~90 min extra** |
| Umbral extremo | 0.05 | 99.9% | ~45 casos | ~225 min (inviable) |

El punto óptimo propuesto es el umbral asimétrico con recall 99.5%, que genera aproximadamente 18 falsos positivos diarios y 90 minutos adicionales de revisión. Este costo operativo es aceptable frente al beneficio de detectar prácticamente todos los casos de riesgo vital. El monitoreo es diario (cualquier falso negativo real activa revisión inmediata y análisis de causa raíz), mensual (recalculo del trade-off precisión/recall) y trimestral (informe al Comité de IA con recomendación de ajuste).

---

*Borrador preparado por el equipo de Ciencia de Datos para integración en el documento de fase escrita. Este documento consolida las especificaciones técnicas correspondientes a los puntos 4, 5, 8, 9, 10 y 12 del índice en un único entregable para el equipo de Derecho.*

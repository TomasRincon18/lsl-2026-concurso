# 5. Arquitectura técnica de la solución

## 5.1 Cuatro planos de arquitectura (§4.1)

La arquitectura se organiza en cuatro planos exigidos por el numeral 4.1 del caso: lógico (motores de IA y capa de orquestación), de datos (modelo canónico y almacenamiento), de integración (conexión con IRIS y VisionWeb) y de seguridad (control de acceso, cifrado, continuidad). Cada plano se detalla en las subsecciones siguientes. Esta separación permite auditar y mantener cada capa de forma independiente y asegura que los requisitos de §5.4 (supervisión humana, trazabilidad) y §4.2 (evitar doble registro) se cumplan desde el diseño.

## 5.2 Plano lógico: motores de IA y capa de orquestación

El sistema separa cuatro motores con responsabilidades definidas y no solapadas, más una capa transversal de orquestación que registra cada decisión y mantiene la trazabilidad exigida por §5.4:

**Motor de clasificación (M2).** BETO fine-tuned clasifica cada petición en las 4 categorías jurídicas y asigna sub-temas mediante un clasificador multi-etiqueta. Un sistema de reglas determinístico, no de caja negra, asigna el nivel de urgencia (1 a 5) según los criterios del equipo de Derecho. Un priorizador detecta sujetos de especial protección constitucional. Este motor no decide: el profesional de URAB valida toda clasificación antes de que el caso avance.

**Motor de similitud y deduplicación (M4).** Sentence-Transformers convierte el texto en un embedding de 768 dimensiones. La cosine similarity contra los casos existentes, combinada con la coincidencia de documento de identidad y pretensión, detecta duplicados. El profesional recibe una sugerencia con ambas peticiones lado a lado y decide si acumula, con justificación escrita obligatoria.

**Componente generativo (M6).** Mistral 7B, ejecutándose en la nube corporativa y sin exponer datos a APIs externas, genera borradores de respuesta mediante arquitectura RAG. ChromaDB recupera fragmentos de normativa, jurisprudencia y plantillas institucionales. El profesional siempre revisa, edita y firma. Solo el catálogo D5 de consultas simples se responde sin pasar por el LLM. Un detector de patrones de riesgo (amenazas, desapariciones, menores, VBG) opera en paralelo.

**Capa de orquestación y auditoría.** API Gateway (FastAPI), Message Broker (RabbitMQ cloud-native) y Workflow de ciclo de vida (ingreso a cierre) coordinan los motores anteriores. Una bitácora inmutable (append-only) registra cada transición de estado, cada clasificación sugerida y cada decisión humana. Esta capa es la que permite reconstruir, ante una auditoría, qué hizo el sistema, con qué datos y quién tomó la decisión final en cada caso.

```
[ Capa de acceso ]  Bandejas URAB · Bandejas profesionales · Dashboards (M8)
  HTTPS/TLS 1.3 · OAuth2/JWT

[ Capa de orquestación y auditoría ] API Gateway · Message Broker · Workflow · Bitácora inmutable

[ Motores de IA ]
  · Motor de clasificación (M2): BETO fine-tuned + reglas de urgencia + priorizador
  · Motor de similitud (M4): Sentence-Transformers + cosine similarity
  · Componente generativo (M6): ChromaDB + Mistral 7B (RAG)
  · Motor de historial (M5): Elasticsearch
  · Motor de ingesta (M1): OCR (Tesseract) + NER (spaCy)

[ Modelo canónico de datos ] PostgreSQL + pgvector

[ Integración ] Conectores → IRIS · VisionWeb · gov.co (opcional) · RPA como contingencia

[ Seguridad transversal ] RBAC · OAuth2/JWT · TLS 1.3 · AES-256 · WAF · Logs inmutables
```

## 5.3 Plano de datos

Todos los datos del macroproceso convergen en un modelo canónico unificado sobre PostgreSQL 15+ con la extensión pgvector, que permite almacenar en la misma base tanto los datos transaccionales (casos, ciudadanos, asignaciones, respuestas) como los vectores semánticos (embeddings) usados por M4 para detectar duplicados y por M6 para buscar en la base de conocimiento. Esto elimina la necesidad de una base de datos vectorial separada y simplifica la arquitectura.

El flujo de datos entre motores es el siguiente: M1 ingesta la petición, extrae entidades con NER y escribe el caso en el modelo canónico. M4 consulta los embeddings almacenados en pgvector para verificar duplicidad. M2 lee el texto del caso, produce la clasificación y la escribe de vuelta. M3 consulta la matriz de competencia y asigna el caso. M5 indexa en Elasticsearch para búsquedas rápidas por cédula. M6 recupera documentos de ChromaDB y genera el borrador. M7 orquesta la sincronización de estados hacia IRIS y VisionWeb. M8 consulta vistas materializadas para los dashboards.

Los datos utilizados para entrenar, desplegar y reentrenar modelos son anonimizados antes de cualquier procesamiento, en cumplimiento de la Ley 1581 de 2012 y los lineamientos de protección de datos personales de la Defensoría. Las entidades del modelo incluyen: ciudadanos, casos, asignaciones, respuestas, sync_log (bitácora de sincronización), audit_log (logs de auditoría) y feedback (correcciones humanas para reentrenamiento).

## 5.4 Plano de integración: el nudo IRIS/VisionWeb

### Contexto de los sistemas legados

**IRIS** es el sistema de gestión documental y de correspondencia de la Defensoría, resultado de una transición tecnológica desde el sistema Orfeo. Esta migración ha implicado retos de estabilización de la plataforma, integración con otras herramientas institucionales y apropiación por parte de los usuarios, en el marco del Plan de Transformación Digital de la Entidad. IRIS gestiona el radicado, reparto, trámite y archivo de los documentos electrónicos, y es la plataforma de trabajo cotidiano para los profesionales defensoriales.

**VisionWeb** es el sistema misional de estadísticas y seguimiento. Cumple un papel crítico en proyectos como "Contribución en la Construcción de Ciudadanía de las Víctimas del Conflicto Armado Nacional", donde la Delegada requiere verificar, cargar, controlar y consolidar evidencias para asegurar la calidad y oportunidad de los datos. Esto fortalece la trazabilidad de los procesos, la rendición de cuentas y la capacidad institucional de proteger los derechos de las víctimas y comunidades campesinas. La información en VisionWeb debe ser veraz, completa y oportuna para evitar inconsistencias, facilitar decisiones basadas en datos confiables y respaldar la transparencia en el uso de los recursos.

Ambos sistemas, sin embargo, no se comunican entre sí (§2.4.3). Cada caso se digita dos veces. El cierre puede quedar registrado en una sola plataforma. No hay trazabilidad cruzada.

### Solución propuesta: capa de orquestación con modelo canónico

El equipo propone una capa de orquestación con registro único y modelo canónico de datos, que opera como único punto de entrada de peticiones y sincroniza bidireccionalmente hacia IRIS y VisionWeb. Cuando ocurre un evento de ciclo de vida (creación, actualización, cierre), el message broker cloud publica el evento y dos consumidores independientes replican simultáneamente a cada plataforma. Una bitácora inmutable registra cada sincronización: qué dato se replicó, a qué sistema, cuándo y con qué resultado. La conciliación diaria automática compara estados entre los tres sistemas y alerta ante cualquier discrepancia.

Se evaluó la alternativa de reducir uno de los dos sistemas a consulta (lectura), manteniendo solo uno como escritura. Esta opción se descartó porque: (i) VisionWeb cumple funciones misionales de estadística y rendición de cuentas que no pueden delegarse en IRIS, cuyo diseño está orientado a gestión documental; (ii) IRIS es la plataforma de trabajo diario de los profesionales y no puede operar en modo solo lectura; (iii) §4.2 exige consistencia de estados entre ambas plataformas, no la eliminación de una de ellas. La capa de orquestación respeta la función de cada sistema y resuelve el problema de doble registro sin eliminar ninguna plataforma.

### Propiedad intelectual y coexistencia

La solución no entra en conflicto con la propiedad intelectual de los sistemas legados. Los datos y registros son de la Defensoría del Pueblo. Los modelos de IA entrenados (BETO fine-tuned para clasificación, modelos NER, embeddings) se entregan a la Entidad con licencia perpetua e irrevocable. Las plataformas base utilizadas (BETO, Mistral 7B, Sentence-Transformers, spaCy, Tesseract) son de código abierto con licencias MIT y Apache 2.0, que permiten expresamente el uso, modificación y redistribución sin restricciones. La capa de orquestación es desarrollo a medida del contratista y se transfiere en la Fase 4. Si los sistemas legados no ofrecen API de escritura (Banco Q10), se despliega RPA como contingencia, automatizando la digitación en la interfaz web sin modificar el sistema legado.

## 5.5 Plano de seguridad y continuidad (§4.5)

### Control de acceso por roles

El sistema implementa cuatro roles de acceso (RBAC), justificados por la sensibilidad de los datos que trata el macroproceso: peticiones que versan sobre salud, niñez, violencia basada en género, desplazamiento forzado, origen étnico y orientación sexual. Los roles son: (1) URAB, con acceso a recepción, clasificación y validación inicial de los casos que ingresan; (2) Profesional defensorial, con acceso a los casos que tiene asignados y a la revisión de borradores de M6; (3) Auditor, con acceso de solo lectura a logs, métricas y bitácoras; (4) Administrador, con acceso a la configuración del sistema pero sin acceso a logs de auditoría ni a datos de casos, en cumplimiento del principio de mínimo privilegio. Este diseño está alineado con la política de seguridad de la información de la Defensoría del Pueblo.

### Cifrado y protección de datos

Toda comunicación entre el navegador y el servidor, y entre los servicios internos, se cifra con TLS 1.3. Los datos en reposo (bases de datos, backups, logs) se cifran con AES-256. Estos estándares están alineados con la política de protección de datos personales de la Defensoría. El contratista actúa como encargado del tratamiento, con instrucciones documentadas y prohibición contractual de usos secundarios. Los datos utilizados para entrenamiento y reentrenamiento de modelos son anonimizados antes de cualquier procesamiento. La evaluación de impacto en protección de datos (AIA) se integra al plan de pruebas de equidad (§8.2).

### Trazabilidad y logs

Toda acción sobre el sistema queda registrada en logs inmutables (append-only): creación de caso, clasificación, asignación, edición de borrador, aprobación de respuesta, consulta de historial, sincronización con IRIS/VisionWeb. Cada entrada incluye timestamp, usuario, acción, dirección IP y resultado. Los logs se respaldan diariamente a almacenamiento externo. El administrador del sistema no tiene acceso de escritura a los logs de auditoría.

### Antecedente: incidente de seguridad de noviembre de 2025

El 21 de noviembre de 2025, la Defensoría del Pueblo identificó un incidente de seguridad digital en la aplicación "Doña Juana le Responde", con accesos no autorizados que comprometieron información institucional. La entidad activó su equipo técnico en coordinación con el Equipo de Respuesta a Emergencias Cibernéticas de Colombia (ColCERT) y recibió soporte especializado de Microsoft. Se rindió informe ante la Superintendencia de Industria y Comercio y la Fiscalía General de la Nación. Como medidas preventivas, la Defensoría recomendó cambiar y fortalecer contraseñas, activar doble factor de autenticación, evitar enlaces o archivos de fuentes desconocidas y verificar comunicaciones a través de canales oficiales.

Este antecedente demuestra que el riesgo de ciberseguridad es material y concreto para la Entidad. Las siguientes decisiones de arquitectura responden directamente a las lecciones de este incidente: autenticación con doble factor para todos los roles, monitoreo continuo de actividad con alertas de anomalías, equipo de respuesta a incidentes con protocolo documentado (detección, contención, erradicación, recuperación), pruebas de penetración y red teaming periódicas, análisis de vulnerabilidades (SCA/SAST) integrado en el pipeline de CI/CD, y capacitación obligatoria en seguridad para todo el personal que use el sistema.

### Continuidad del servicio

Ante la indisponibilidad de IRIS o VisionWeb (riesgo identificado en §2.4.2), el sistema mantiene una cola de mensajes local con persistencia en disco. Los eventos de sincronización se acumulan localmente y se despachan cuando la conectividad se recupera. El sistema propio sigue operando sin degradación. Se entrega un acuse de recibo diferido al ciudadano. Los objetivos de recuperación son: RPO menor o igual a 24 horas (backups diarios), RTO menor o igual a 4 horas (tiempo máximo para restaurar el servicio). Se realizan pruebas de recuperación semestrales. La disponibilidad del sistema se compromete al 99.5% mensual.

## 5.6 Decisión de infraestructura: nube corporativa

La solución se despliega sobre una plataforma corporativa en nube para administración de agentes de IA, operada por el contratista. Esta decisión no obedece a una preferencia tecnológica sino a dos requisitos del caso que ninguna alternativa on-premise puede satisfacer con la misma garantía:

**Sensibilidad de la información tratada.** Las peticiones que recibe la Defensoría contienen datos sensibles (salud, niñez, VBG, desplazamiento, origen étnico, orientación sexual) clasificados como tales por la Ley 1581 de 2012. La arquitectura cloud corporativa permite que estos datos se procesen dentro de un entorno empresarial controlado, con cifrado AES-256 en reposo y TLS 1.3 en tránsito, acceso segmentado por roles y logs inmutables. Los datos nunca salen a APIs externas: todos los modelos de IA (BETO, Mistral 7B, Sentence-Transformers, spaCy) se ejecutan dentro del perímetro de la nube corporativa. La Defensoría es la responsable del tratamiento y el contratista actúa como encargado con instrucciones documentadas y prohibición contractual de usos secundarios. La opción preferente es GovCloud del MinTIC, en línea con el CONPES 4144 de 2025 sobre soberanía de datos. Como alternativa evaluada se contempla nube comercial (AWS, Azure, GCP) con cláusulas contractuales reforzadas de residencia y jurisdicción de los datos. La decisión final se toma en la Fase 0 según el Q7 del Banco de Preguntas.

**Continuidad del servicio.** El macroproceso de atención y trámite de quejas no puede interrumpirse: los ciudadanos ejercen su derecho de petición (CP art. 23) y los casos de riesgo vital no admiten demora. La nube corporativa ofrece escalabilidad automática ante picos de demanda, balanceo de carga entre instancias redundantes, backups automatizados con RPO menor o igual a 24 horas, y restauración en menos de 4 horas (RTO). El contratista asume contractualmente estos niveles de servicio (SLA de disponibilidad mayor o igual a 99.5%, latencia de API menor a 500ms en p95). Una arquitectura on-premise exigiría que la Defensoría adquiriera, mantuviera y operara servidores físicos con redundancia geográfica, un costo y una carga operativa que el modelo cloud delega en el contratista.

## 5.7 Stack tecnológico

La plataforma cloud corporativa administra de forma unificada los siguientes modelos y servicios. Todos los componentes de IA son de código abierto con licencias permisivas (MIT, Apache 2.0), sin costo de licenciamiento.

| Capa | Tecnología | Justificación | Licencia |
|---|---|---|---|
| Cloud | IaaS/PaaS corporativa (preferente GovCloud MinTIC) | Orquestación de agentes IA, versionamiento, monitoreo, escalabilidad, soberanía de datos | Comercial / Gubernamental |
| API | FastAPI (Python) 0.110+ | Async, OpenAPI 3.0 automático, ecosistema IA nativo | MIT |
| Clasificación | BETO (dccuchile/bert-base-spanish-wwm-uncased) fine-tuned | Español, 110M params, WWM, probado en dominio legal | MIT |
| NER | spaCy (es_core_news_lg) + fine-tuning 3.7+ | Pipeline NLP maduro en español, inferencia rápida | MIT |
| Embeddings | Sentence-Transformers (paraphrase-multilingual-mpnet-base-v2) | Similitud semántica, 50+ idiomas, 768-dim | Apache 2.0 |
| LLM | Mistral 7B (Instruct v0.2) | Mejor calidad/eficiencia en 7B, ejecución cloud sin exponer datos | Apache 2.0 |
| RAG | LangChain + ChromaDB | Framework estándar, BD vectorial ligera y embebible | MIT / Apache 2.0 |
| OCR | Tesseract LSTM (spa) + OpenCV | CER menor a 5% docs limpios, sin costo | Apache 2.0 |
| BD | PostgreSQL 15+ + pgvector | Estándar sector público, transaccional + vectorial unificado | PostgreSQL |
| Búsqueda | Elasticsearch 8.x | Menos de 500ms, agregaciones, analizador español | Elastic 2.0 |
| Mensajería | RabbitMQ 3.12+ o cloud-native | ACK, persistencia, reintentos, DLQ | MPL 2.0 |
| MLOps | MLflow + DVC + Evidently AI | Versionamiento integral, drift, reportes de equidad | Apache 2.0 |
| Dashboard | Streamlit (piloto) → Power BI (prod) | Python puro, Power BI usado en sector público | Apache 2.0 / Microsoft |
| Seguridad | OAuth2/JWT + TLS 1.3 + AES-256 + WAF | Sin estado, cifrado estándar, protección web | IETF |

Infraestructura estimada [validar]: desarrollo 4 vCPU, 16 GB RAM, 100 GB SSD. Piloto 8+ vCPU, 32 GB RAM, 500 GB SSD, 1 GPU T4 (16 GB VRAM) para Mistral 7B. Nacional 16+ vCPU, 64 GB RAM, 2 TB SSD, 2 GPU T4 en alta disponibilidad con auto-scaling.

## 5.8 MLOps (§4.6)

El mantenimiento de los modelos de IA en producción se rige por cuatro componentes, alineados con el numeral 4.6 del caso:

**Versionamiento.** Git para el código fuente de modelos y pipelines. DVC (Data Version Control) para los datasets etiquetados, garantizando que se pueda reconstruir exactamente con qué datos se entrenó cada versión de un modelo. MLflow Model Registry para los modelos entrenados, con registro de métricas, hiperparámetros y artefactos. Stages: Staging, Production, Archived.

**Evaluación de deriva (drift).** Evidently AI compara periódicamente la distribución de los datos que llegan en producción contra la distribución de los datos de entrenamiento. Si detecta una divergencia significativa (cambio en el lenguaje de las peticiones, aparición de nuevos tipos de casos, modificación en los patrones de urgencia), genera una alerta automática. También monitorea la distribución de predicciones en el tiempo para detectar degradación silenciosa del modelo.

**Canal de retroalimentación humana.** Una API (POST /feedback) permite que los profesionales reporten errores de clasificación: corrigen el tipo de caso, el sub-tema o el nivel de urgencia asignado por el sistema, e indican el motivo. Estos datos etiquetados por humanos se acumulan y alimentan el siguiente ciclo de reentrenamiento. Son la fuente de ground truth más valiosa para mejorar el modelo con datos reales del dominio.

**Política de actualización controlada.** Los modelos no se actualizan sin un procedimiento explícito: solicitud formal de cambio, evaluación técnica del nuevo modelo sobre el conjunto de prueba (métricas deben igualar o superar a la versión en producción), aprobación del Comité de IA, despliegue en staging durante al menos una semana con monitoreo, y solo entonces pase a producción. Cada actualización queda registrada en un changelog con la fecha, las métricas comparativas y la aprobación del Comité. Los datos de entrenamiento deben estar anonimizados antes de cualquier procesamiento.

## 5.9 Módulos

M1, Recepción. OCR sobre escaneados, NER extrae campos obligatorios (nombre, CC, hecho, pretensión), validador detecta faltantes y responde al ciudadano, genera radicado URAB-YYYYMMDD-NNNNNN. Meta: extracción mayor o igual a 90%.

M2, Clasificación y Triaje. BETO fine-tuned clasifica en 4 tipos; sub-clasificador multi-etiqueta asigna unos 12 sub-temas; reglas determinísticas asignan urgencia 1 a 5; priorizador cruza con catálogo D3 de sujetos de especial protección. Profesional URAB valida todo. Meta: accuracy mayor o igual a 90%, recall urgencias mayor o igual a 99%.

M3, Asignación. Matriz tipo+sub-tema → entidad (D4). Bandejas con SLA: ingreso a asignación menor a 4h, gestión a cierre menor a 15dh. Alertas al 80% y 100%. Meta: 15 min o menos en p90.

M4, Anti-Duplicación. Embedding 768-dim, cosine similarity, umbral 85% + mismo CC + misma pretensión. UI side-by-side. Profesional justifica por escrito. Meta: precisión mayor o igual a 85%, recall mayor o igual a 90%.

M5, Historial. Elasticsearch: GET /ciudadano/{cc}/historial menor a 500ms. Sugiere respuestas previas + templates D6. Meta: menor a 500ms p95.

M6, Asistente RAG. Modo RAG: ChromaDB recupera normativa y jurisprudencia, Mistral 7B genera borrador, profesional edita/firma. Modo automático D5: plantillas sin LLM para consultas simples. Detector de riesgo en tiempo real. Meta: aceptación mayor o igual a 70%, generación menor a 10s.

M7, Interoperabilidad. Único punto de entrada. Eventos al message broker, replicación simultánea a IRIS/VisionWeb. Backoff exponencial (1s a 32s), 6 intentos máx. RPA si no hay API. Bitácora inmutable. Meta: sincronización mayor o igual a 99.5%.

M8, Analítica. Dashboards: (1) carga temática, (2) cuellos de botella, (3) recurrencia/duplicidad, (4) equidad. Capa institucional con k-anonymity mayor o igual a 5, acceso rol investigador. Meta: latencia menor a 1 min.

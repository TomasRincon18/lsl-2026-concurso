# Borrador Integrado — Secciones Técnicas para el Escrito 1 (Equipo Ciencia de Datos → Equipo Derecho)

> **Destinatario:** Equipo de Derecho, para integrar en el documento `CONCURSO_LEGALTECH_-_ESCRITO_INTENTO_1.docx`.
> **Cubre los puntos del índice:** 4 (Modelo TO-BE y piloto), 5 (Arquitectura técnica), 8 (Cambio sociotécnico, enfoque diferencial y pruebas de equidad), 9 (Matriz de riesgos), 10 (Plan de trabajo por fases), 12 (Métricas y línea base).
> **Referencias a secciones (§):** remiten al Caso oficial URAB (RFP). Referencias entre corchetes: insumos del equipo (Matriz SGIA, SECOP, flujogramas, DOC_1).
> **Valores `[validar]`:** propuestas que el equipo debe ajustar con la mentoría antes de la entrega final.
> **Formato final del escrito:** Arial 12, interlineado 1, APA 7.ª edición.

---

## 4. Modelo TO-BE y alcance del piloto (diseño técnico viable)

### 4.1 Diagnóstico del proceso actual (AS-IS)

El macroproceso actual de atención y trámite de quejas en la Defensoría del Pueblo opera de forma predominantemente manual. Según el caso (§2.2–§2.4), la URAB recibe aproximadamente 300 peticiones diarias por canales diversos (formulario web, correo electrónico en formato libre, correspondencia física, jornadas de campo). Cada petición pasa por un flujo que podemos resumir en cinco etapas, todas dependientes de intervención humana:

| Etapa | Cómo opera hoy | Problema principal |
|---|---|---|
| **A. Recepción** | Ingreso multicanal sin normalización. Un funcionario verifica legibilidad y completitud, crea el radicado a mano, y transcribe los datos del ciudadano. | Errores de digitación, omisión de campos, lentitud (~15 min por caso). |
| **B. Triage en URAB** | Clasificación manual en Asesoría / Queja / Solicitud de Mediación / Solicitud de Conciliación. Evaluación de competencia sin apoyo automatizado. Sin visibilidad del historial del peticionario. | ~30 casos/día por funcionario. Casos urgentes se mezclan con consultas rutinarias. Sin criterios uniformes de clasificación. |
| **C. Reparto y gestión** | Asignación manual a profesionales. Registro duplicado en IRIS y VisionWeb, sistemas que no se comunican entre sí (§2.4.3). Seguimiento manual de tiempos. | Doble digitación, retrabajo, inconsistencias entre plataformas, sin alertas de vencimiento. |
| **D. Gestión defensorial** | El profesional investiga, coordina con la entidad competente y redacta la respuesta desde cero. Actualiza manualmente el estado en ambas plataformas. | Sin apoyo documental automatizado. Respuestas inconsistentes entre profesionales. |
| **E. Cierre** | Verificación manual, archivo con riesgo de quedar registrado en una sola plataforma (§2.4.3). | Pérdida de trazabilidad, imposibilidad de auditoría integral. |

Los cinco problemas estructurales que identificamos en este AS-IS son:

1. **Volumen y saturación operativa** (~300 peticiones/día, clasificación manual ~15 min/caso). El resultado es represamiento crónico y respuestas fuera de términos legales.
2. **Riesgo jurídico por falta de priorización.** Sin sistema automático, casos de riesgo vital (amenazas, desapariciones, menores, VBG) pueden quedar rezagados entre consultas rutinarias.
3. **Duplicidad de registro IRIS/VisionWeb.** Cada caso se digita dos veces en sistemas desconectados, generando retrabajo e inconsistencias.
4. **Duplicidad de peticiones no detectada.** Un mismo ciudadano puede presentar la misma queja múltiples veces sin que el sistema lo identifique, generando respuestas redundantes o contradictorias.
5. **Peticionarios recurrentes sin trazabilidad.** No existe un historial unificado por ciudadano; cada nueva petición se aborda como si fuera la primera.

### 4.2 Marco del rediseño (TO-BE)

El objeto de la convocatoria es la solución integral de IA y gobernanza para el macroproceso, con implementación piloto en la URAB e integración con IRIS y VisionWeb (§2.2). El proceso rediseñado inserta los ocho módulos solicitados (§3, M1–M8) como una capa de asistencia que automatiza tareas repetitivas y apoya —nunca reemplaza— la toma de decisiones del profesional defensorial.

| Etapa del macroproceso | Cambio esperado con la solución | Módulos responsables |
|---|---|---|
| **A. Recepción** | Ingesta multicanal normalizada con OCR para documentos escaneados y extracción automática de datos del ciudadano mediante NER (nombre, CC, dirección, pretensión). Detección de información faltante y solicitud automática al ciudadano. Radicado semiautomático con validación. | M1 |
| **B. Triage en URAB** | Clasificación del tipo de caso (4 categorías) y sub-tema (~12 sub-temas) asistida por IA con sugerencia de prioridad, nivel de urgencia (1–5) y detección de sujetos de especial protección constitucional. Validación humana antes de la asignación. Historial unificado visible en el mismo paso. | M2, M5 |
| **C. Reparto y gestión** | Bandejas de trabajo por rol con recomendación de entidad competente (matriz tipo+subtema → entidad). Si la Defensoría es competente, el sistema sugiere ruta interna según carga y perfil. Indicadores de tiempo por segmento con alertas automáticas. | M3, M7 |
| **D. Gestión defensorial** | Apoyo con borradores de respuesta generados por IA (RAG: la IA consulta normativa y jurisprudencia antes de redactar). El profesional siempre revisa, edita y aprueba. Alertas de patrones de riesgo para elevación inmediata a prioridad. | M6, M5 |
| **E. Cierre** | Sincronización simultánea del estado final en IRIS y VisionWeb con bitácora de trazabilidad. Consolidación del expediente y alimentación de dashboards de analítica. | M7, M8 |

> **Referencia visual:** El flujograma AS-IS / TO-BE se incorpora como anexo (ver `FLUJOGRAMAS.pptx` → diagrama TO-BE). El diagrama detallado con la secuencia completa de módulos está en el Anexo B de este borrador.

### 4.3 Mapeo problema → solución

| Problema crítico | Módulo(s) | Cómo lo resuelve |
|---|---|---|
| Volumen y saturación (~300/día) | M1, M2, M6 | Automatiza recepción, extracción de datos y clasificación. El profesional pasa de digitar a supervisar. |
| Riesgo jurídico por represamiento | M2, M3 | Sistema de priorización con score de urgencia (1–5). Alertas de SLA visibles. Detección automática de sujetos de especial protección. |
| Doble registro IRIS/VisionWeb | M7 | Capa de orquestación con modelo canónico: un solo punto de entrada, sincronización bidireccional simultánea. Bitácora de cada sincronización. |
| Duplicidad de peticiones | M4 | Comparación semántica automática (embeddings + cosine similarity). Si ≥85% similitud + mismo CC + misma pretensión → sugerencia de acumulación al profesional. |
| Peticionarios sin historial | M5 | Índice unificado de búsqueda por cédula. Historial completo del ciudadano en <500ms. |

### 4.4 Alcance del piloto en URAB

- **Entran en el piloto:** módulos **M1, M2, M3, M4, M5, M6** con validación humana en todos los puntos de decisión (§5.4), módulo **M7** con integración mínima IRIS/VisionWeb requerida por §4.2, y módulo **M8** con tableros básicos de operación (Dashboard 1: carga temática).
- **Se difieren al escalamiento:** otras Unidades de Análisis fuera de Bogotá, integración con Carpeta Ciudadana Digital (gov.co) como componente opcional de M7 (Banco de Preguntas: el proponente puede proponer mecanismo de acuse de recibo y consulta de estado), foliación electrónica con firma de índice bajo estándares AGN (Banco Q8: no es requisito mínimo; se ofrece como diferenciador a partir de §4.3 y gestión documental §5.1).
- **Regional piloto:** una regional de alto volumen (Bogotá).
- **Volumen:** ~300 peticiones/día durante el piloto.
- **Usuarios:** 8–10 profesionales de URAB + 2 administradores.
- **Duración total del piloto:** 8 semanas de operación controlada (dentro de la Fase 3, ver §10).
- **Criterios de salida del piloto:** precisión de clasificación ≥90%, recall de urgencias ≥99%, detección de duplicados ≥85% recall, tiempo ingreso→asignación ≤4h (p90), disponibilidad ≥99.5% mensual. Si precisión cae por debajo de 75% no se escala sin reentrenar.

---

## 5. Arquitectura técnica de la solución

### 5.1 Decisión de arquitectura: capa de orquestación con modelo canónico

Frente al problema de IRIS vs. VisionWeb —dos sistemas sin comunicación entre sí (§2.4.3), mientras §4.2 exige evitar dobles registros— el equipo propone una **capa de orquestación con registro único y modelo canónico de datos, con sincronización bidireccional y mecanismo de resolución de conflictos**. Justificación:

- Cumple §4.2: un solo punto de entrada elimina la doble digitación. Mantiene consistencia de estados (radicado, asignación, gestión, cierre) entre los tres sistemas.
- Reduce el riesgo del §2.4.3 (archivo en una sola plataforma) al centralizar el estado maestro y replicarlo.
- Alimenta la gobernanza §5.4 al dejar trazabilidad total de cada sincronización (qué, cuándo, por quién, con qué resultado).
- Es neutral tecnológicamente (§7.1) y compatible con que IRIS siga operando como plataforma de gestión documental y VisionWeb como sistema misional de estadísticas.

> Esta decisión se desarrolla en coordinación con la estrategia jurídica para no entrar en conflicto con la cláusula de propiedad intelectual del anexo contractual.

### 5.2 Arquitectura lógica (diagrama de capas)

El sistema se organiza en cinco capas, cada una con responsabilidades bien definidas:

```
[ Capa de acceso ]  Bandejas URAB · Bandejas profesionales · Tableros analítica (M8)
─────────────────────────────────────────────────────────────────────────────
[ Capa de orquestación ]  API Gateway (FastAPI) · RabbitMQ (colas de mensajería)
                          Workflow ingreso→cierre · Bitácora de sincronización
─────────────────────────────────────────────────────────────────────────────
[ Motores de IA ]
    · M1 — OCR (Tesseract + OpenCV) + NER (spaCy fine-tuned)
    · M2 — Clasificación y triaje (BETO fine-tuned + reglas de urgencia)
    · M4 — Anti-duplicación (Sentence-Transformers + cosine similarity)
    · M5 — Historial unificado (Elasticsearch)
    · M6 — Asistente generativo RAG (LangChain + ChromaDB + Mistral 7B)
[ Modelo canónico de datos ]  PostgreSQL + pgvector (esquema unificado)
─────────────────────────────────────────────────────────────────────────────
[ Integración ]  Conectores → IRIS · VisionWeb · gov.co (opcional)
                 RPA como capa de contingencia si APIs legadas no ofrecen escritura
─────────────────────────────────────────────────────────────────────────────
[ Seguridad transversal ]  OAuth2/JWT · RBAC (4 roles) · TLS 1.3 · AES-256
                           Logs inmutables (append-only) · Contingencia offline
```

Esta separación permite escalar cada capa de forma independiente y facilita el mantenimiento y la evolución futura del sistema.

### 5.3 Stack tecnológico

| Capa | Tecnología | Justificación principal | Licencia |
|---|---|---|---|
| Backend / API | **FastAPI** (Python) | Alto rendimiento, async nativo, documentación OpenAPI automática, ecosistema de IA nativo | MIT |
| Clasificación NLP | **BETO** (`dccuchile/bert-base-spanish-wwm-uncased`) fine-tuned | Modelo transformer entrenado específicamente en español por la Universidad de Chile. Más ligero que RoBERTa. Probado en dominio legal. | MIT |
| Extracción de entidades (NER) | **spaCy** (`es_core_news_lg`) + fine-tuning | Pipeline maduro para español. Extrae nombres, CC, direcciones, pretensiones del texto libre. | MIT |
| Similitud semántica | **Sentence-Transformers** (`paraphrase-multilingual-mpnet-base-v2`) | Convierte textos en vectores de 768 dimensiones. Cosine similarity entre embeddings permite comparar significados, no solo palabras. | Apache 2.0 |
| LLM generativo | **Mistral 7B** (self-hosted vía Ollama/vLLM) | Código abierto, soberanía de datos (nada sale de la Defensoría), eficiente en recursos. | Apache 2.0 |
| RAG (búsqueda + generación) | **LangChain + ChromaDB** | LangChain es el framework estándar para RAG. ChromaDB es vector DB ligera, sin infraestructura extra. | MIT / Apache 2.0 |
| OCR | **Tesseract LSTM** (`spa`) + **OpenCV** | Reconocimiento de caracteres en español con preprocesamiento de imagen. CER <5% en documentos limpios. | Apache 2.0 |
| BD transaccional + vectorial | **PostgreSQL + pgvector** | Robusto, estándar en sector público. pgvector evita tener BD separada para vectores semánticos. | PostgreSQL License |
| Búsqueda textual | **Elasticsearch** | Índice de búsqueda escalable para historial por cédula, palabras clave, filtros combinados. Respuesta <500ms. | Elastic License 2.0 |
| Mensajería | **RabbitMQ** | Garantiza entrega de eventos entre el nuevo sistema e IRIS/VisionWeb. Reintentos, confirmaciones, colas de contingencia. | Mozilla Public License 2.0 |
| MLOps | **MLflow + DVC + Evidently AI** | Versionamiento de modelos, datos y experimentos. Monitoreo de drift (datos y predicciones) en producción. | Apache 2.0 |
| Dashboard | **Streamlit** (piloto) → **Power BI** (producción) | Prototipado rápido para el piloto. Power BI ya se usa en el sector público colombiano. | Apache 2.0 / Microsoft |
| Infraestructura | **Docker + Docker Compose** | Contenedores portables, idénticos en desarrollo y producción. Escalamiento horizontal. | Apache 2.0 |
| Seguridad | **OAuth2/JWT + TLS 1.3 + AES-256** | Autenticación sin estado, cifrado en tránsito (última versión) y en reposo (estándar militar). | Estándares abiertos |

### 5.4 Arquitectura de datos

- **Ingesta multicanal normalizada:** formulario web (JSON estructurado), correo electrónico (parser de texto libre + adjuntos), documentos escaneados (OCR con Tesseract + preprocesamiento OpenCV: deskew, binarización adaptativa, eliminación de ruido), cargue manual asistido. Controles de calidad y detección de datos faltantes en el punto de ingreso (§4.3).
- **Almacenamiento en tres capas:** (i) área cruda para datos originales sin transformar, (ii) capa canónica con el modelo de datos unificado PostgreSQL, (iii) índices semánticos (embeddings) en pgvector para clasificación, deduplicación y búsqueda RAG.
- **Gobernanza de datos:** perfilamiento de calidad en la Fase 0, normalización de taxonomías (tipos de trámite, sub-temas, entidades competentes), trazabilidad del origen de cada dato (§4.3). Los datos sensibles según la Ley 1581 de 2012 reciben tratamiento reforzado.

### 5.5 Arquitectura de integración (IRIS / VisionWeb)

- **Capa de integración primaria:** APIs / ETL-ELT cuando existan endpoints factibles en IRIS y VisionWeb. Se usa RabbitMQ como bus de mensajería: el nuevo sistema publica un evento (`caso.creado`, `caso.actualizado`, `caso.cerrado`) y dos consumidores independientes replican a cada plataforma simultáneamente.
- **RPA como capa de contingencia:** si los sistemas legados no ofrecen API de escritura (Banco Q10), se despliega automatización robótica de procesos (RPA) para eliminar la doble digitación manual como plan B. Esta capa se documenta, versiona y audita igual que las APIs.
- **Modelo canónico:** mapea campos y estados equivalentes entre las tres plataformas. Ejemplo: `radicado` (sistema nuevo) ↔ `numero_radicado` (IRIS) ↔ `codigo_expediente` (VisionWeb). La orquestación mantiene el estado maestro y replica cambios.
- **Bitácora inmutable:** cada sincronización registra qué dato se replicó, a qué sistema, cuándo, iniciada por quién, con qué resultado (éxito/fallo) y número de reintentos. Esta bitácora alimenta la auditoría (§5.4 del caso) y la matriz de riesgos.
- **Reintentos con backoff exponencial:** si una API externa falla (timeout, error 5xx), el mensaje se reencola con esperas progresivas: 1s, 2s, 4s, 8s, 16s, 32s. Tras 6 reintentos fallidos, se genera alerta al administrador.

### 5.6 Arquitectura de seguridad y continuidad (§4.5)

- **Control de acceso por roles (RBAC):** cuatro perfiles definidos con el equipo de Derecho (D9): (1) URAB — recepción, clasificación y validación inicial; (2) Profesional defensorial — gestión de casos asignados, revisión de borradores M6; (3) Auditor — acceso solo lectura a logs, métricas y bitácoras; (4) Administrador — configuración del sistema, sin acceso a logs de auditoría. Principio de mínimo privilegio en todos los roles.
- **Autenticación:** OAuth2 con JWT (JSON Web Tokens). Sin estado en el servidor. Tokens con tiempo de expiración configurable y renovación segura.
- **Cifrado:** TLS 1.3 para todas las comunicaciones en tránsito. AES-256 para datos en reposo (bases de datos, backups, logs). El antecedente del incidente de ciberseguridad de noviembre de 2025 [DOC_1] refuerza la necesidad de estos controles.
- **Logs inmutables (append-only):** cada acción sobre el sistema (creación de caso, clasificación, asignación, edición de borrador, aprobación de respuesta, consulta de historial) se registra con timestamp, usuario, acción, IP de origen y resultado. Solo se puede añadir información, nunca modificar ni borrar. Separación de roles: el administrador del sistema no tiene acceso de escritura a los logs de auditoría. Backup diario automático a almacenamiento externo.
- **Plan de contingencia ante indisponibilidad de IRIS/VisionWeb** (fallo crítico del §2.4.2): cola de mensajes local con persistencia en disco. Si los sistemas externos no responden, los eventos se acumulan localmente y se despachan cuando se recupera la conectividad. Acuse de recibo diferido al ciudadano. El sistema propio sigue operando sin degradación.
- **Respaldo y recuperación:** `[validar]` objetivos de recuperación propuestos: RPO ≤24 horas (pérdida máxima de datos), RTO ≤4 horas (tiempo máximo para restaurar el servicio). Pruebas de recuperación semestrales.

### 5.7 MLOps y operación de modelos (§4.6)

- **Versionamiento integral:** Git para código fuente. DVC (Data Version Control) para datasets etiquetados. MLflow Model Registry para modelos entrenados con sus métricas, parámetros y artefactos. Trazabilidad completa: dado un modelo en producción, se puede reconstruir exactamente con qué datos y configuración se entrenó.
- **Monitoreo de drift:** Evidently AI genera reportes automáticos comparando la distribución de datos en producción vs. entrenamiento (data drift) y la distribución de predicciones en el tiempo (prediction drift). Alertas si la divergencia supera umbrales definidos.
- **Canal de retroalimentación humana:** API endpoint donde los profesionales reportan errores de clasificación. Cada corrección se registra con el caso, la predicción original, la corrección humana y el motivo. Estos datos etiquetados alimentan el siguiente ciclo de reentrenamiento.
- **Política de actualización controlada:** solicitud formal de cambio → evaluación técnica (métricas sobre datos de prueba) → aprobación del Comité de IA → implementación en ambiente de staging → validación → despliegue en producción con registro en changelog. Los modelos nunca se actualizan sin aprobación explícita.

### 5.8 Plan de pruebas

| Tipo | ¿Qué se prueba? | Frecuencia |
|---|---|---|
| Unitarias | Cada función aislada: OCR, NER, validador de completitud, reglas de urgencia | Cada cambio de código |
| Integración | Flujo completo: M1→M4→M2→M3. M7→IRIS, M7→VisionWeb | Al final de cada sprint |
| Aceptación | Profesionales reales de URAB prueban el sistema con casos reales. Se mide satisfacción y se recoge feedback | Antes de cada entrega de fase |
| Equidad (fairness) | Equal Opportunity, Demographic Parity y False Negative Rate segmentados por género, regional y grupo de especial protección | Antes de cada despliegue + trimestral |
| Carga | Simular 300 peticiones/día y picos de 500. Medir latencia p95 y uso de recursos | Antes de puesta en producción |
| Seguridad | Pruebas de penetración, revisión de configuración TLS, intentos de acceso no autorizado, simulación de indisponibilidad de IRIS/VisionWeb | Antes de producción + semestral |

### 5.9 Descripción de módulos (resumen)

> Las especificaciones detalladas de cada módulo —incluyendo diagramas de flujo, componentes internos, contratos de API y métricas de rendimiento— se encuentran en el Anexo B: Especificaciones Técnicas. A continuación, un resumen funcional.

**M1 — Recepción Inteligente.** Recibe peticiones por todos los canales y las normaliza. El OCR (Tesseract) convierte documentos escaneados en texto; el NER (spaCy) extrae datos estructurados (nombre, tipo y número de documento, dirección, teléfono, email, relato de los hechos, pretensión). Un validador de completitud verifica campos obligatorios: si falta información crítica, el sistema responde automáticamente al ciudadano solicitándola. Si los datos están completos, se genera un radicado único (URAB-YYYYMMDD-NNNNNN) y se inicia el flujo. **Métrica:** tasa de extracción correcta de entidades ≥90%.

**M2 — Clasificación y Triaje.** Es el corazón inteligente del sistema. Sobre el texto de la petición, un modelo BETO con fine-tuning clasifica el tipo de caso en las 4 categorías jurídicas. Un segundo clasificador multi-etiqueta asigna sub-temas (~12). En paralelo, un sistema de reglas —no de IA, sino determinístico y auditable— evalúa el nivel de urgencia (escala 1 a 5) basándose en los criterios D7 del equipo de Derecho. Finalmente, un priorizador cruza el texto con el catálogo de sujetos de especial protección constitucional (D3) y asigna flags de alerta. **Métrica:** accuracy ≥90%, F1 por clase ≥0.80, recall en urgencias/riesgo vital ≥99%.

**M3 — Asignación y Enrutamiento.** La matriz de competencia (D4) determina la entidad responsable según tipo y sub-tema. Si no es la Defensoría, el sistema genera automáticamente la notificación de traslado. Si es competente, un recomendador híbrido (reglas + scoring) sugiere la ruta interna óptima según carga y perfil del profesional. Bandejas de trabajo con estados (pendiente → asignado → en_gestión → escalado → cerrado) y monitoreo de SLA con alertas al 80% y 100% del plazo. **Métrica:** tiempo ingreso→asignación ≤15 minutos en el 90% de los casos.

**M4 — Anti-Duplicación.** Antes de crear un nuevo caso, el texto de la petición se convierte en un vector semántico (embedding de 768 dimensiones) mediante Sentence-Transformers. Se compara vía cosine similarity contra los K casos más cercanos en la base de datos. Si la similitud supera el 85% y coincide el número de documento y la pretensión, el sistema sugiere acumulación al profesional, quien decide con una interfaz que muestra ambas peticiones lado a lado con los campos coincidentes resaltados. **Métrica:** precision de sugerencias ≥85%, recall de duplicados ≥90%.

**M5 — Peticionarios Recurrentes.** Al ingresar un número de cédula, Elasticsearch devuelve en menos de 500ms el historial completo de peticiones de ese ciudadano: radicados, fechas, tipos, estados, profesionales asignados y respuestas emitidas. El sistema sugiere además respuestas previas y templates institucionales (D6) aplicables al caso actual. **Métrica:** tiempo de consulta de historial <500ms (p95).

**M6 — Asistente Generativo (RAG + LLM).** Es el módulo de apoyo a la redacción de respuestas. Funciona en dos modos:

- *Modo RAG completo (consultas complejas):* la petición del ciudadano se convierte en embedding y se buscan en ChromaDB los fragmentos más relevantes de la base de conocimiento (normativa, jurisprudencia, templates D6, respuestas previas anonimizadas). Esos fragmentos se inyectan en un prompt junto con la petición, el historial del ciudadano e instrucciones estrictas (no inventar, no decidir, lenguaje ciudadano). Mistral 7B —ejecutándose en servidores propios de la Defensoría, sin enviar datos a terceros— genera un borrador que el profesional revisa, edita y aprueba.
- *Modo automático (catálogo D5):* para consultas simples preaprobadas por Derecho ("¿cuál es mi radicado?", "¿quién atiende mi caso?", "reenvío de constancia") el sistema responde automáticamente con plantillas que se llenan con datos de la base de datos, sin pasar por el LLM.

En ambos modos, cada interacción queda registrada en logs inmutables: prompt completo, respuesta generada, respuesta final tras edición, profesional responsable y timestamp. Además, M6 incorpora un sistema de alertas que detecta en tiempo real patrones de riesgo (amenazas, desapariciones, menores, VBG) y notifica inmediatamente al profesional. **Métrica:** tasa de aceptación de borradores sin corrección mayor ≥70%; tiempo de generación <10 segundos.

**M7 — Interoperabilidad.** Elimina la doble digitación. El nuevo sistema es el único punto de entrada de peticiones. Cada evento (creación, actualización, cierre) se publica en RabbitMQ y dos consumidores independientes replican simultáneamente a IRIS y VisionWeb. Si una API externa falla, el evento se reencola automáticamente. RPA como contingencia si no hay APIs de escritura disponibles. **Métrica:** tasa de sincronización exitosa ≥99.5%.

**M8 — Analítica.** Cuatro dashboards que transforman datos operativos en información para la toma de decisiones: (1) Carga temática — distribución por tipo, tendencias, top sub-temas; (2) Cuellos de botella — tiempos por etapa, carga por profesional, casos vencidos; (3) Recurrencia y duplicidad — tasa de duplicación, peticionarios frecuentes; (4) Equidad — distribución por género, grupo de especial protección, alertas de disparidad >5%. Adicionalmente, una capa de investigación institucional con datos anonimizados (k-anonymity ≥5) y acceso restringido a rol "investigador". **Métrica:** dashboards actualizados en tiempo real, latencia <1 minuto desde el evento.

---

## 8. Cambio sociotécnico, enfoque diferencial y pruebas de equidad (§5.2, §5.3)

### 8.1 Cambio sociotécnico

La introducción de IA en el macroproceso de la Defensoría no es solo un cambio tecnológico: transforma la forma en que los funcionarios trabajan y cómo los ciudadanos interactúan con la institución. Identificamos las siguientes dinámicas:

| (i) Capacidades nuevas | (ii) Conductas habilitadas / cambiadas | (iii) Impactos disruptivos a anticipar | (iv) Decisiones de gobernanza |
|---|---|---|---|
| Lectura y clasificación masiva (~300 peticiones/día en minutos) | El profesional pasa de clasificar manualmente caso por caso a supervisar y validar clasificaciones automáticas. Dedica más tiempo a casos complejos. | Riesgo de sobre-automatización: tentación de automatizar decisiones que requieren juicio humano | Lista taxativa de decisiones NUNCA automatizables (ver §8.4). Human-in-the-loop obligatorio. |
| Vista unificada del historial por ciudadano | Atender peticionarios recurrentes con contexto completo en segundos. Respuestas más coherentes y personalizadas. | Privacidad por concentración de historial: todos los casos de un ciudadano visibles en un solo lugar | Principio de minimización: solo se muestra lo necesario para el caso actual. Roles de acceso diferenciados. |
| Borradores de respuesta generados por IA (M6) | Redactar respuestas en minutos en lugar de horas. El profesional edita y personaliza en lugar de empezar desde cero. | Riesgo de que el profesional asuma respuestas sin revisar adecuadamente (confianza excesiva en la IA) | Revisión humana obligatoria y registrada. El profesional siempre firma. Bitácora de cada borrador generado. |
| Monitoreo y analítica en tiempo real (M8) | Evidenciar patrones de carga, cuellos de botella y disparidades entre grupos poblacionales que antes eran invisibles | Datos agregados que podrían amplificar barreras o estigmatizar grupos poblacionales si se usan sin contexto | Enfoque diferencial en la analítica. Controles de privacidad (k-anonymity). Publicación de reportes de equidad. |
| Interoperabilidad IRIS/VisionWeb (M7) | Eliminar la doble digitación. Un solo registro, dos plataformas actualizadas. | Resistencia al cambio organizacional. Posible percepción de redundancia del nuevo sistema. | Gestión del cambio alineada con MIPG y articulada con ISO/IEC 42001:2023. Capacitación desde la Fase 0. |

### 8.2 Gestión de cambio organizacional

La estrategia incluye gestión de cambio desde la Fase 0 (§6.0) y un plan de capacitación para al menos 20 profesionales (§6.1). Componentes: sesiones de sensibilización sobre IA en el sector público, manuales de rol con procedimientos claros (qué hace el sistema, qué decide el humano), mesa de ayuda durante el piloto y los primeros 6 meses de operación (§6.4). El proceso sigue el Modelo Integrado de Planeación y Gestión (MIPG) y se articula con la ISO/IEC 42001:2023 para adaptar la cultura organizacional.

### 8.3 Pruebas de equidad algorítmica

Los sistemas de inteligencia artificial, si no se diseñan y monitorean cuidadosamente, pueden reproducir e incluso amplificar sesgos presentes en los datos de entrenamiento. En el contexto de la Defensoría del Pueblo —cuya misión constitucional es proteger los derechos humanos de toda la población, con énfasis en los grupos más vulnerables— un sesgo algorítmico no es solo un error técnico: es una vulneración del derecho a la igualdad (Art. 13 CP). Por ello, la solución incorpora desde su diseño un marco de pruebas de equidad con monitoreo continuo.

**Principio metodológico:** las pruebas de equidad se incorporan como pruebas antes del despliegue dentro del plan de pruebas de la Fase 2 (§6.3 del caso). No son un anexo separado, sino un gate de calidad obligatorio.

**Métricas de equidad utilizadas:**

| Métrica | ¿Qué mide? | Ejemplo de sesgo que detecta |
|---|---|---|
| **Equal Opportunity** (Igualdad de Oportunidad) | ¿El modelo clasifica con la misma precisión a todos los grupos? | Si acierta el 90% de quejas de hombres pero solo 70% de mujeres |
| **Demographic Parity** (Paridad Demográfica) | ¿El modelo asigna cada categoría en proporciones similares entre grupos? | Si clasifica como "Queja" al 40% de hombres y solo 15% de mujeres |
| **Disparate Impact Ratio** | Cociente entre la tasa del grupo menos favorecido y el más favorecido | Ratio <0.80 se considera impacto desproporcionado |
| **False Negative Rate por grupo** | ¿Deja pasar más casos urgentes sin marcar en unos grupos que en otros? | Si 5% de FN en desplazados vs 0.5% en el resto |

**Segmentación:** género (cuando el dato lo proporciona voluntariamente el ciudadano, nunca inferido), regional/departamento, grupo de especial protección (cuando detectable por el texto), canal de ingreso. Si una muestra tiene menos de 30 casos, esa segmentación no se reporta para evitar conclusiones no estadísticamente significativas.

**Umbrales de alerta y protocolo de mitigación:**

| Disparidad detectada | Acción |
|---|---|
| <3% de diferencia entre grupos | Aceptable. Monitoreo continuo. |
| 3–5% de diferencia o diferencia de precisión >5 puntos entre subgrupos | Alerta amarilla. Revisión por el equipo técnico. Análisis de causas. |
| 5–10% de diferencia o cociente de falsos negativos >1.5 | Alerta naranja. Se escala al Comité de IA. Protocolo de mitigación: rebalanceo del dataset, threshold tuning, o adversarial debiasing. |
| >10% de diferencia | Alerta roja. Se suspende el despliegue del módulo para decisiones que afecten a ese grupo. Investigación inmediata. |

**Estrategias de mitigación disponibles:** (1) rebalanceo del dataset añadiendo más ejemplos del grupo subrepresentado, (2) ajuste del umbral de decisión por grupo (threshold tuning) para igualar tasas de error, (3) adversarial debiasing —técnica de entrenamiento que obliga al modelo a clasificar bien sin poder distinguir el grupo de pertenencia—, y (4) revisión humana obligatoria reforzada para los grupos afectados hasta que se resuelva el sesgo.

**Monitoreo continuo:**

| Variable | Métrica | Frecuencia | Responsable | Herramienta |
|---|---|---|---|---|
| Género | Equal Opportunity, Demographic Parity | Trimestral | Equipo MLOps | Evidently AI |
| Regional | Accuracy por departamento | Trimestral | Equipo MLOps | Evidently AI |
| Grupo de especial protección | False Negative Rate | Mensual | Comité de IA | Evidently AI + reporte manual |
| Canal de ingreso | Accuracy por canal | Trimestral | Equipo MLOps | Evidently AI |
| Sub-tema | F1 score por sub-tema | Trimestral | Equipo MLOps | Evidently AI |

**Salvaguardas institucionales:** validación manual de todos los rechazos automáticos del sistema; revisión de casos de riesgo vital exclusivamente por un funcionario, nunca por el sistema; formatos y lectura accesibles para personas con discapacidad; prohibición absoluta de automatizar decisiones de fondo (§5.4).

### 8.4 Decisiones que nunca se automatizan (supervisión humana significativa §5.4)

| Decisión | Módulo | Mecanismo de control |
|---|---|---|
| Evaluación de competencia de la entidad para conocer el caso | M3 | Decisión humana. La IA solo sugiere direccionamiento según la matriz D4. |
| Priorización de casos de riesgo vital (desapariciones, amenazas, niñez en peligro) | M2, M6 | Alerta automática, pero la prioridad final la asigna el funcionario. Umbral asimétrico: el sistema está calibrado para preferir falsos positivos (exceso de alertas) sobre falsos negativos (omitir un riesgo real). |
| Respuesta de fondo al peticionario | M6 | La IA solo redacta borrador. Revisión, edición y firma exclusivamente humanas. |
| Corrección de errores de deduplicación y decisiones de archivo | M4 | Revisión humana obligatoria. El profesional justifica por escrito cada acumulación o rechazo de acumulación. |
| Cierre del caso | M7, M8 | Validación humana del cumplimiento de todos los pasos antes de la sincronización final con IRIS/VisionWeb. |

---

## 9. Matriz de riesgos (SPI, corrupción y daño antijurídico) — §5.5

### 9.1 Categorización

Identificamos los riesgos en tres familias, alineadas con los requerimientos del caso:

| Familia | Sigla | Alcance |
|---|---|---|
| **Técnica** | T | Fallas de infraestructura, conectividad, integración, precisión de modelos |
| **Operacional** | O | Uso indebido, dependencia excesiva, omisiones humanas, resistencia al cambio |
| **Jurídica** | J | Incumplimiento de términos legales, vulneración de privacidad, falta de trazabilidad, daño antijurídico |

Cada riesgo incluye mitigación, evidencia de control y frecuencia de monitoreo. La matriz completa (con probabilidad e impacto inherente y residual según metodología DAFP) se presenta en el Anexo A, basada en `Matriz_SGIA_ISO42001.xlsx` (hoja "2. Matriz SGIA") que contiene 23+ riesgos graduados.

### 9.2 Matriz de riesgos consolidada

| ID | Familia | Riesgo | Mitigación / control | Evidencia | Monitoreo |
|---|---|---|---|---|---|
| R1 | T | Fallo de conectividad o caída de IRIS/VisionWeb que genera represamiento (§2.4.2) | Colas resilientes (RabbitMQ con persistencia), modo offline con acuse diferido, plan de contingencia documentado (§5.6) | Logs de colas, bitácora de fallos, dashboard de estado M7 | Semanal |
| R2 | T | Error de integración: doble registro o archivo en una sola plataforma (§2.4.3) | Modelo canónico + sincronización bidireccional + verificación automática de consistencia de estados | Bitácora de sincronización M7, reportes de conciliación diaria | Diaria |
| R3 | T | Falso negativo en clasificación de urgencias: no detección de riesgo vital (desapariciones, amenazas, niñez en peligro) | Umbral asimétrico (priorizar recall ≥99% sobre precisión), supervisión humana de todos los casos sin flag de urgencia, revisión de alto riesgo por funcionario | Datasets gold etiquetados por juristas URAB, métricas de recall diarias, protocolo de revisión ante cualquier falso negativo | Diaria |
| R4 | T | Falso positivo en deduplicación: fragmentación o acumulación inadecuada de casos diferentes | Umbral configurable (85% por defecto, ajustable), validación humana obligatoria con justificación escrita de cada decisión de acumulación, regla adicional de coincidencia de CC + pretensión | Bitácora de acumulación M4 con motivo de aceptación/rechazo | Semanal |
| R5 | T/O | Sesgo algorítmico que amplifica exclusiones (género, discapacidad, juventud, etnia, origen) | Pruebas de equidad obligatorias antes de cada despliegue (§8.3), revisión por subgrupo, plan de mitigación con 4 niveles de alerta, XAI (Explainable AI) para trazabilidad de decisiones | Reportes trimestrales de Evidently AI, actas del Comité de IA | Cada release + trimestral |
| R6 | O | Dependencia excesiva del sistema: "automatizar de más", falta de supervisión humana significativa (§5.4) | Human-in-the-loop obligatorio en todos los puntos de decisión. Lista taxativa de decisiones NUNCA automatizables (§8.4). Límites explícitos de M6: solo borradores, nunca respuesta final automática. | Logs de revisión humana, registro de firmas, tiempos de revisión por caso | Semanal |
| R7 | O | Omisiones o uso indebido por parte de profesionales (cargue manual de información incorrecta, omisión de revisión de borrador) | Capacitación desde Fase 0 (§6.1/§6.3), roles y permisos con principio de menor privilegio, auditoría de actividad por usuario, procedimientos documentados por rol | Plan de capacitación, registro de accesos, manuales de rol | Mensual |
| R8 | J | Incumplimiento de términos legales (derecho de petición, CPACA) por retraso en el flujo | Tableros de tiempos M8 con semaforización, alertas automáticas M3 al 80% y 100% del plazo, escalamiento en cadena, responsable definido por caso | Indicadores M3/M8, reportes de cumplimiento de SLA | Diaria |
| R9 | J | Vulneración de privacidad o tratamiento inadecuado de datos sensibles (salud, niñez, VBG, desaparición, origen étnico) | Defensoría = responsable del tratamiento, proveedor = encargado con instrucciones documentadas (§5.1 y §5.4 + Ley 1581/2012). Cifrado AES-256 + TLS 1.3. Evaluación de impacto (AIA) integrada al plan de pruebas de equidad. | Registros de consentimiento/autorización, AIA documentada, logs de acceso a datos sensibles | Trimestral |
| R10 | J | Falta de trazabilidad que impide explicar decisiones automatizadas (transparencia algorítmica — Directiva 007/2025) | Ficha de Transparencia Algorítmica de diseño propio alineada con la Directiva 007/2025 y NIST AI RMF 1.0 (Q9). Logs inmutables. Registro de explicación para cada decisión automatizada. | Fichas por sistema (SDA), logs de auditoría | Trimestral |
| R11 | T/O | Falla del asistente generativo (M6): respuesta falsa, invención de normativa (alucinación), decisión de fondo errónea | Arquitectura RAG: el LLM solo genera basándose en documentos reales recuperados de ChromaDB. Prompt con instrucciones estrictas anti-alucinación. Revisión humana obligatoria con registro. Solo consultas del catálogo D5 se responden automáticamente. | Bitácora de respuestas generadas (prompt, respuesta cruda, respuesta final editada, profesional responsable) | Semanal |
| R12 | T | Incidente de ciberseguridad con exposición de datos personales y sensibles | Controles de acceso (RBAC + OAuth2/JWT), cifrado en tránsito y reposo, monitoreo de actividad, equipo de respuesta a incidentes, pruebas de penetración y red teaming periódicas (cf. Matriz SGIA riesgos 4–7) | Reportes de pentest, simulacros de incidentes, plan de respuesta documentado | Mensual |

> **Garantía de alineación jurídica:** la propuesta técnica se construye en paralelo al marco jurídico del equipo de Derecho, asegurando que cada riesgo identificado en esta matriz tenga su correlato en el régimen de responsabilidad por daño antijurídico (CP art. 90), en el contrato anexo y en el modelo de gobernanza §5.4.

---

## 10. Plan de trabajo por fases y entregables (§6)

### 10.1 Estructura general

El proyecto se organiza en 5 fases secuenciales con criterios de salida verificables. Cada fase es prerrequisito de la siguiente. Duración total propuesta: 32 semanas de ejecución más 12 meses de garantía y evolución. `[validar]` duraciones con el cronograma oficial del caso.

```
Fase 0: Alistamiento y diagnóstico (4 semanas)
   │
Fase 1: Diseño de arquitectura e integración (8 semanas)
   │
Fase 2: Construcción de módulos IA (12 semanas)
   │
Fase 3: Implementación, capacitación y operación inicial (8 semanas)
   │
Fase 4: Gobernanza y mejora continua (continua, mínimo 12 meses de garantía)
```

### 10.2 Detalle por fase

**Fase 0 — Alistamiento y diagnóstico (4 semanas)**
- **Objetivo:** Entender el estado real del macroproceso, preparar los datos y sentar las bases de la arquitectura.
- **Actividades clave:** levantamiento de datos AS-IS de IRIS/VisionWeb (volúmenes, patrones, tiempos por etapa), etiquetado del dataset inicial con apoyo de juristas de la URAB (~1000 peticiones etiquetadas con tipo, sub-tema y urgencia), inventario de canales y puntos de falla, auditoría de infraestructura existente, definición de taxonomías (tipos, sub-temas, entidades), y plan de gestión de cambio y capacitación.
- **Entregables:** flujograma AS-IS y TO-BE validado, dataset etiquetado (~200 ejemplos por categoría), taxonomía propuesta validada por URAB, línea base de métricas levantada, plan de gestión de cambio.
- **Criterio de aceptación:** diagnóstico aprobado por el comité del proyecto. Taxonomía validada. Línea base documentada.

**Fase 1 — Diseño de arquitectura e integración (8 semanas)**
- **Objetivo:** Definir la arquitectura objetivo y la estrategia de integración con los sistemas legados.
- **Actividades clave:** diseño detallado de la arquitectura de capas, modelo canónico de datos, diagrama de integración con IRIS y VisionWeb (incluyendo mapeo de campos y contratos de API), diseño de seguridad (accesos, roles, cifrado, logs), diseño de continuidad y contingencia, evaluación de la opción Carpeta Ciudadana Digital (gov.co) con decisión argumentada.
- **Entregables:** documento de arquitectura objetivo, diagrama de integración, matriz de interoperabilidad, especificación de seguridad y continuidad, decisión documentada sobre gov.co.
- **Criterio de aceptación:** arquitectura validada con los equipos de sistemas legados. Matriz de interoperabilidad firmada por las partes.

**Fase 2 — Construcción de módulos IA (12 semanas)**
- **Objetivo:** Desarrollar y probar los módulos core con IA.
- **Actividades clave:** fine-tuning de BETO para M2 con el dataset etiquetado en Fase 0, desarrollo de M1 (OCR, NER, validador, radicado), M4 (embeddings, cosine similarity, umbral), M5 (índice Elasticsearch, API de historial), y prototipo de M6 (RAG con base de conocimiento inicial). Plan de pruebas completo: unitarias, integración, usabilidad, estrés, sesgos (equidad).
- **Entregables:** prototipos funcionales de M1, M2, M4, M5 y M6 (modo básico), informe de desempeño sobre el conjunto de prueba gold, informe de pruebas de equidad superadas.
- **Criterio de aceptación:** métricas de M2/M4/M5 sobre el conjunto de prueba iguales o superiores a las metas definidas en §12. Pruebas de equidad sin disparidad >5%.

**Fase 3 — Implementación, capacitación y operación inicial (8 semanas)**
- **Objetivo:** Desplegar el piloto en la URAB, capacitar a los profesionales y comenzar la operación controlada.
- **Actividades clave:** plan de despliegue y adopción, capacitación por roles para el 100% de los profesionales de la URAB, desarrollo de tableros de analítica M8 (operación y derechos), protocolo de incidentes, mesa de ayuda, puesta en producción en modo supervisado (las primeras 4 semanas el sistema opera en paralelo al proceso manual para comparación y ajuste).
- **Entregables:** sistema piloto URAB en operación, 100% de profesionales capacitados, tableros M8 operativos, protocolo de incidentes activo, informe de comparación sistema vs. manual.
- **Criterio de aceptación:** métricas del piloto dentro de los umbrales definidos en §12. Satisfacción de profesionales ≥80%.

**Fase 4 — Gobernanza y mejora continua (continua, mínimo 12 meses de garantía `[validar]`)**
- **Objetivo:** Consolidar la operación autónoma, transferir el conocimiento y asegurar la evolución controlada del sistema.
- **Actividades clave:** operación del Comité de IA con roles definidos (propietario del sistema, dueño de datos, responsable misional), monitoreo continuo de métricas y drift, reentrenamiento programado y bajo demanda, plan de actualización controlada, auditoría interna y externa periódica, transferencia de conocimiento al equipo interno de la Defensoría (train-the-trainer, documentación completa, soporte decreciente).
- **Entregables:** modelo de gobierno operando, informes periódicos de métricas y equidad, plan de actualización documentado, documentación completa transferida, equipo interno autónomo.
- **Criterio de aceptación:** Comité de IA sesionando regularmente. Métricas estables dentro de umbrales. Auditoría interna sin hallazgos críticos. Equipo interno opera sin asistencia externa durante al menos 3 meses consecutivos.

### 10.3 Cronograma resumido de hitos `[validar]`

| Hito | Fase | Semana |
|---|---|---|
| Diagnóstico y dataset etiquetado aprobados | F0 | Semana 4 |
| Arquitectura validada con sistemas legados | F1 | Semana 12 |
| Módulos IA superan pruebas de desempeño y equidad | F2 | Semana 24 |
| Piloto URAB en operación, 100% profesionales capacitados | F3 | Semana 32 |
| Primera auditoría de equidad superada | F4 | Semana 44 |
| Transferencia de conocimiento completada | F4 | Mes 18+ |

### 10.4 Modelo de costos (referencia) `[validar]`

El modelo de costos a 3 años se construye discriminando: implementación (costo único), licencias, operación y soporte, infraestructura, capacitación y gestión de cambio, y evolución (mejoras, reentrenamiento, auditorías). Los supuestos unitarios se validan en la Fase 0 con un evento de cotización. Referencia de mercado en `SECOP IA.xlsx`. Presupuesto total estimado: ≈$1.125 M COP a 3 años `[validar]`, distribuido aproximadamente en 55% año 1 (implementación intensiva), 22.5% año 2 y 22.5% año 3 (soporte y evolución).

---

## 12. Métricas y línea base del piloto (§4.4)

### 12.1 Metodología

La línea base se levanta durante la Fase 0. Actualmente no existen registros automatizados de los indicadores propuestos (Banco Q18 confirma que el proceso tarda varios días y no se mide formalmente). Los valores AS-IS son estimaciones basadas en el caso y deben refinarse con los datos reales del diagnóstico. Las metas del piloto están calibradas para ser ambiciosas pero alcanzables en la Fase 3. Valores `[validar]`.

### 12.2 Cuadro de indicadores

| # | Indicador | Definición / Módulo | Línea base (estimada) | Meta piloto | Umbral de alerta | Frecuencia |
|---|---|---|---|---|---|---|
| M1 | Tiempo de clasificación sugerida | De radicado a sugerencia de clasificación por M2 | Varias horas–2 días (manual, sin medición formal) | ≤15 min en 90% de peticiones (p90) | p90 >30 min | Diaria |
| M2 | Precisión de clasificación (accuracy) | Acierto de la categoría entre las 4 clases jurídicas (M2) | ~80% (humano, con fatiga) | ≥90% global; ≥90% subclasificación | <85% o caída >3 puntos | Semanal |
| M3 | Exhaustividad en urgencias (recall) | Porcentaje de casos de riesgo vital detectados (M2) | No medido | ≥99% (falso negativo ≈ 0) | Cualquier falso negativo real | Diaria |
| M4 | Precisión de sugerencias de duplicados | De los duplicados sugeridos, cuántos realmente lo son (M4) | No hay sistema | ≥85% | <70% | Semanal |
| M5 | Recall de duplicados | De los duplicados reales, cuántos detecta el sistema (M4) | <30% (muestreo manual) | ≥90% | <80% | Semanal |
| M6 | Falsos positivos en deduplicación | Sugerencias de duplicado incorrectas (M4) | No hay | ≤15% | >20% | Semanal |
| M7 | Falsos negativos en deduplicación | Duplicados reales no detectados (M4) | >70% | ≤10% | >15% | Semanal |
| M8 | Reducción de reprocesos de reparto | Reasignaciones por error o duplicación | Línea base F0 | ≥50% de reducción | <20% de reducción | Mensual |
| M9 | Cumplimiento de tiempos internos | % de peticiones con gestión terminada antes del plazo | No robusto | ≥90% de peticiones en tiempo | <80% | Mensual |
| M10 | Tiempo ingreso→asignación | Desde la recepción hasta la bandeja del profesional (M3) | ~2 días hábiles | ≤4 horas en 90% de casos | Desvío >+50% | Semanal |
| M11 | Tiempo ingreso→primera respuesta | Días hábiles hasta que el ciudadano recibe respuesta (M3, M6) | 15–20 días hábiles | ≤10 días hábiles en 90% de casos | >15 días | Mensual |
| M12 | Tasa de extracción correcta de entidades | Campos del ciudadano correctamente extraídos (M1) | ~70–80% (digitación manual con errores) | ≥90% para campos obligatorios | <85% | Semanal |
| M13 | Precisión del asistente generativo | Borradores M6 que no requirieron corrección mayor | No aplica | ≥90% para consultas de trámite simples | Alertas diarias por revisiones conflictivas | Semanal |
| M14 | Disponibilidad del sistema | % del tiempo operativo | No aplica | ≥99.5% mensual | <99% | Tiempo real |
| M15 | Tasa de sincronización IRIS/VisionWeb | Eventos replicados exitosamente sin reintentos (M7) | 0% (no hay integración) | ≥99.5% | <99% | Tiempo real |
| M16 | Tasa de error en OCR | Caracteres mal reconocidos en documentos escaneados (M1) | No medido | <5% en documentos limpios | >10% | Semanal |
| M17 | Equal Opportunity por género | Diferencia en tasa de aciertos entre grupos de género (M2) | No medido | <5% de diferencia | >5% o cociente FN >1.5 | Trimestral |
| M18 | Disparate Impact Ratio | Rendimiento del peor grupo / mejor grupo (todos los módulos) | No medido | >0.80 | <0.80 | Trimestral |
| M19 | Satisfacción del profesional URAB | Encuesta trimestral | No aplica | ≥80% | <70% | Trimestral |

### 12.3 Metodología para umbral asimétrico de riesgo vital

El costo de un falso negativo en casos con riesgo vital (desapariciones, amenazas, niñez en peligro) no es comparable al de un falso positivo: el primero involucra daño antijurídico y vulneración de derechos fundamentales (§2.4.2 + §5.5), mientras que el segundo representa un costo operativo (revisión adicional). Por esta razón, el equipo propone una metodología de **umbral asimétrico**:

- Durante la Fase 0, los juristas de la URAB etiquetan un conjunto *gold* de peticiones, identificando aquellas con riesgo vital real.
- Para la clase "riesgo vital", el clasificador M2 se calibra con sensibilidad (recall) objetivo de **99–100%**, aceptando un incremento controlado de falsos positivos como costo operativo aceptable.
- Se monitorea el trade-off precisión/recall de forma continua. Cualquier falso negativo de esta clase activa revisión inmediata, análisis de causa raíz y, si es necesario, reentrenamiento del modelo (§5.7 MLOps).
- El reporte de este indicador incluye: (i) línea base de clasificación levantada en F0, (ii) métrica de calidad por nivel de urgencia y por población de enfoque diferencial (§8.3), y (iii) plan de reajuste cuando se active el umbral de alerta.

### 12.4 Mecanismo de medición y reporte

| Grupo de métricas | Herramienta | Frecuencia | Responsable | Visualización |
|---|---|---|---|---|
| Operativas (M1–M5, M8–M11) | Logs del sistema + PostgreSQL | Tiempo real | Equipo MLOps | M8 — Dashboard 2 |
| Calidad IA (M6–M7, M12–M13) | MLflow + Evidently AI | Semanal automático | Equipo MLOps | M8 — Reporte de calidad |
| Infraestructura (M14–M15) | Prometheus + Grafana | Tiempo real | Equipo de Infraestructura | Dashboard de operaciones |
| Equidad (M17–M18) | Evidently AI | Trimestral automático | MLOps + Comité de IA | M8 — Dashboard 4 |
| Satisfacción (M19) | Formulario integrado en el sistema | Trimestral | URAB / Defensoría | Reporte al Comité de IA |

---

## Anexos referenciados

- **Anexo A — Matriz de riesgos completa (23+ riesgos graduados con DAFP):** `Matriz_SGIA_ISO42001.xlsx` (hoja "2. Matriz SGIA").
- **Anexo B — Especificaciones técnicas detalladas:** descripción completa de cada módulo M1–M8 con diagramas de flujo, componentes, contratos de API (OpenAPI), modelo de datos, plan MLOps y métricas de rendimiento esperadas. Diagramas en `FLUJOGRAMAS.pptx`.
- **Anexo C — Estudio de mercado y referencias de precios:** `SECOP IA.xlsx` (insumo del modelo económico §7.2).
- **Anexo F — Ficha de Transparencia Algorítmica:** alineada con la Directiva Conjunta 007 de 2025 y el marco NIST AI RMF 1.0.

> *Borrador integrado por el equipo de Ciencia de Datos a partir del caso oficial URAB (RFP), los planes técnicos, la matriz SGIA ISO 42001, los flujogramas y el borrador previo del Escrito Intento 1. Las celdas `[validar]` deben confirmarse con la mentoría antes de la entrega final. Este texto está listo para ser copiado, adaptado y organizado por el equipo de Derecho en la estructura final del documento.*

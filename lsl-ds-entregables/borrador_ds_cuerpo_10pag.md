# Borrador — Secciones Técnicas Ciencia de Datos (Cuerpo ≈10 págs + Anexos)

> **Destinatario:** Equipo de Derecho, para integrar en el documento `CONCURSO_LEGALTECH_-_ESCRITO_INTENTO_1.docx`.
> **Extensión objetivo en el cuerpo:** ~10 páginas. Todo el detalle adicional se remite a los anexos A–F, que no cuentan para el límite de 25 páginas.
> **Formato:** Arial 12, espacio sencillo, márgenes 1.5 cm, tamaño carta, APA 7.ª ed.
> **Referencias a secciones (§):** Caso oficial URAB (RFP). `[validar]` = pendiente de mentoría.
>
> **Mapa de anexos para el equipo de Derecho:**
>
> | Anexo | Contenido | Referenciado desde |
> |---|---|---|
> | **Anexo A** | Especificaciones detalladas M1–M8: pipeline, componentes, métricas, tecnologías por módulo | §5.3 |
> | **Anexo B** | Stack tecnológico completo con justificación y licencias | §5.2 |
> | **Anexo C** | Matriz de riesgos completa (12 riesgos con probabilidad, impacto, causa, efecto, responsable) | §9 |
> | **Anexo D** | Plan de trabajo detallado: carta Gantt, actividades por fase, presupuesto por rubro | §10 |
> | **Anexo E** | Métricas completas: 19 indicadores con línea base, meta, umbral de alerta, frecuencia, herramienta y metodología de umbral asimétrico | §12 |
> | **Anexo F** | Pruebas de equidad: protocolo completo, métricas, niveles de alerta, estrategias de mitigación, tabla de monitoreo | §8.2 |

---

## 4. Modelo TO-BE y alcance del piloto (~1.5 págs)

### 4.1 Diagnóstico del proceso actual

El macroproceso de atención y trámite de quejas en la Defensoría del Pueblo opera hoy de forma predominantemente manual. La URAB recibe ~300 peticiones diarias por canales diversos sin normalización (web, correo electrónico, físico, jornadas de campo). Una petición típica atraviesa cinco etapas, todas dependientes de intervención humana: (A) recepción y verificación manual de legibilidad, (B) clasificación manual del tipo de caso entre cuatro categorías jurídicas sin apoyo automatizado ni visibilidad del historial del peticionario, (C) asignación manual a profesionales con doble registro en IRIS y VisionWeb —sistemas que no se comunican entre sí (§2.4.3)—, (D) gestión defensorial sin apoyo documental automatizado, y (E) cierre con riesgo de archivo en una sola plataforma.

De este diagnóstico se derivan cinco problemas estructurales: (1) saturación operativa por clasificación manual (~15 min/caso), que resulta en represamiento crónico; (2) riesgo jurídico por ausencia de priorización automática de casos de riesgo vital; (3) doble digitación IRIS/VisionWeb que genera retrabajo e inconsistencias; (4) duplicidad de peticiones no detectada; y (5) ausencia de historial unificado por ciudadano.

### 4.2 Modelo TO-BE

El proceso rediseñado inserta los ocho módulos solicitados (§3, M1–M8) como una capa de asistencia que automatiza tareas repetitivas y apoya —nunca reemplaza— la toma de decisiones del profesional. En cada punto donde el sistema produce una clasificación, sugerencia o borrador, existe un mecanismo explícito de validación humana antes de que la decisión surta efectos jurídicos (§5.4).

| Etapa | Cambio con la solución | Módulos | ¿Quién decide? |
|---|---|---|---|
| **A. Recepción** | Ingesta multicanal normalizada con OCR para documentos escaneados y extracción automática de datos (NER). Detección de faltantes con respuesta automática al ciudadano. Radicado semiautomático. | M1 | Humano (valida datos extraídos) |
| **B. Triage** | Clasificación asistida por IA del tipo, sub-tema, nivel de urgencia (1–5) y detección de sujetos de especial protección. Historial unificado visible. | M2, M5 | **Humano** (valida/corrige la clasificación) |
| **C. Reparto** | Recomendación de entidad competente y ruta interna según carga. Un solo registro, sincronización automática con IRIS y VisionWeb. Alertas de SLA. | M3, M7 | **Humano** (confirma competencia y ruta) |
| **D. Gestión** | Asistente generativo (RAG) produce borrador de respuesta basado en normativa real. El profesional siempre revisa, edita y firma. Alertas de riesgo. | M6, M5 | **Humano** (revisa, edita, firma) |
| **E. Cierre** | Sincronización simultánea en IRIS y VisionWeb con bitácora. Dashboards de analítica actualizados. | M7, M8 | Humano (inicia el cierre) |

Las decisiones que **nunca** se automatizan son: evaluación de competencia de la entidad, priorización final de riesgo vital, respuesta de fondo al ciudadano, corrección de errores de duplicación y cierre del caso. En todos estos puntos la IA solo sugiere o asiste; la decisión vinculante es exclusivamente humana.

### 4.3 Mapeo problema → solución

| Problema | Módulo(s) | Mecanismo |
|---|---|---|
| Volumen y saturación (~300/día) | M1, M2, M6 | Automatiza recepción, extracción y clasificación. El profesional supervisa en lugar de digitar. |
| Riesgo jurídico por falta de priorización | M2, M3 | Score de urgencia (1–5), detección de sujetos de especial protección, SLAs con alertas automáticas. |
| Doble registro IRIS/VisionWeb | M7 | Capa de orquestación con modelo canónico: único punto de entrada, sincronización bidireccional simultánea. |
| Duplicidad de peticiones no detectada | M4 | Embeddings semánticos + cosine similarity ≥85% + mismo CC + misma pretensión → sugerencia de acumulación. |
| Peticionarios sin historial unificado | M5 | Índice Elasticsearch con historial completo consultable por cédula en <500ms. |

### 4.4 Alcance del piloto

El piloto se implementa en la URAB de Bogotá (~300 peticiones/día, 8–10 profesionales, 8 semanas de operación controlada en la Fase 3). Incluye M1, M2, M3, M4, M5 y M6 con validación humana en todos los puntos de decisión, M7 con integración mínima IRIS/VisionWeb (§4.2) y M8 con el Dashboard 1 de carga temática. Se difieren al escalamiento: otras regionales, integración con Carpeta Ciudadana Digital (gov.co) como opción complementaria, y foliación electrónica bajo estándares AGN (ofrecida como diferenciador). Criterios de salida: precisión de clasificación ≥90%, recall de urgencias ≥99%, detección de duplicados ≥85% recall, tiempo ingreso→asignación ≤4h (p90), disponibilidad ≥99.5% mensual.

> **Diagrama TO-BE completo:** Anexo A (§A.1). Flujograma AS-IS/TO-BE: `FLUJOGRAMAS.pptx`.

---

## 5. Arquitectura técnica de la solución (~4 págs)

### 5.1 Decisión de arquitectura

Frente al problema de IRIS vs. VisionWeb —dos sistemas sin comunicación (§2.4.3) que exigen doble digitación— el equipo propone una **capa de orquestación con modelo canónico de datos y sincronización bidireccional**. Un solo punto de entrada mantiene el estado maestro del caso y replica cambios simultáneamente a ambas plataformas mediante RabbitMQ. Cada sincronización queda registrada en una bitácora inmutable (qué, cuándo, por quién, con qué resultado). Si los sistemas legados no ofrecen API de escritura (Banco Q10), se despliega RPA como capa de contingencia. Esta decisión cumple §4.2 (evitar doble registro), reduce el riesgo de archivo en una sola plataforma (§2.4.3), y alimenta la trazabilidad requerida por §5.4.

### 5.2 Arquitectura lógica y stack tecnológico

El sistema se organiza en cinco capas con responsabilidades separadas:

```
[ Capa de acceso ]       Bandejas URAB · Bandejas profesionales · Dashboards (M8)
─────────────────────────────────────────────────────────────────────────────
[ Capa de orquestación ] API Gateway (FastAPI) · RabbitMQ · Workflow ingreso→cierre
─────────────────────────────────────────────────────────────────────────────
[ Motores de IA ]        M1 (OCR+NER) · M2 (BETO fine-tuned) · M4 (embeddings)
                         M5 (Elasticsearch) · M6 (RAG: ChromaDB + Mistral 7B)
─────────────────────────────────────────────────────────────────────────────
[ Modelo canónico ]      PostgreSQL + pgvector (transaccional + vectorial)
─────────────────────────────────────────────────────────────────────────────
[ Integración ]          Conectores → IRIS · VisionWeb · gov.co (opcional)
[ Seguridad transversal ] OAuth2/JWT · RBAC · TLS 1.3 · AES-256 · Logs inmutables
```

**Stack tecnológico resumido** (detalle completo con justificaciones y licencias en Anexo B):

| Capa | Tecnología principal |
|---|---|
| Backend | FastAPI (Python) |
| Clasificación NLP | BETO (`dccuchile/bert-base-spanish-wwm-uncased`) fine-tuned |
| Extracción de entidades (NER) | spaCy (`es_core_news_lg`) + fine-tuning |
| Similitud semántica | Sentence-Transformers (`paraphrase-multilingual-mpnet-base-v2`) |
| LLM generativo | Mistral 7B (self-hosted, soberanía de datos) |
| RAG | LangChain + ChromaDB |
| OCR | Tesseract LSTM (`spa`) + OpenCV |
| BD transaccional + vectorial | PostgreSQL + pgvector |
| Búsqueda textual | Elasticsearch |
| Mensajería | RabbitMQ |
| MLOps | MLflow + DVC + Evidently AI |
| Dashboard | Streamlit (piloto) → Power BI (producción) |
| Infraestructura | Docker + Docker Compose |
| Seguridad | OAuth2/JWT + TLS 1.3 + AES-256 |

Todos los componentes de IA son de código abierto con licencias permisivas (MIT, Apache 2.0), lo que garantiza soberanía tecnológica, ausencia de costos de licenciamiento por uso, y cumplimiento de los lineamientos de infraestructura de gobierno (GovCloud u on-prem según CONPES 4144).

### 5.3 Descripción de módulos (resumen)

> **Las especificaciones detalladas de cada módulo —pipeline completo, componentes internos, métricas de rendimiento y justificación tecnológica— se encuentran en el Anexo A.** A continuación se presenta la función de cada módulo y su aporte al macroproceso.

**M1 — Recepción Inteligente.** Recibe peticiones por todos los canales, aplica OCR a documentos escaneados, extrae automáticamente los datos del ciudadano (NER), verifica completitud, y genera radicado único. Si faltan datos críticos, responde automáticamente al ciudadano solicitándolos. **Métrica objetivo:** tasa de extracción correcta de entidades ≥90%.

**M2 — Clasificación y Triaje.** Clasifica la petición en las 4 categorías jurídicas y asigna sub-temas mediante un modelo BETO con fine-tuning. Un sistema de reglas deterministicas —auditable, no de caja negra— asigna nivel de urgencia (1–5) según los criterios jurídicos del equipo de Derecho. Un priorizador detecta automáticamente sujetos de especial protección constitucional y asigna flags de alerta. El profesional de URAB valida o corrige toda clasificación antes de que el caso avance. **Métrica objetivo:** accuracy ≥90%, recall en urgencias ≥99% (umbral asimétrico: se prioriza no omitir ningún riesgo vital así se generen falsos positivos).

**M3 — Asignación y Enrutamiento.** Determina la entidad competente mediante una matriz de reglas tipo+sub-tema (alimentada por el equipo de Derecho). Si es externa, genera notificación de traslado. Si es la Defensoría, recomienda ruta interna según carga y perfil. Bandejas de trabajo con estados y monitoreo de SLA con alertas al 80% y 100% del plazo. **Métrica objetivo:** tiempo ingreso→asignación ≤15 min en el 90% de los casos.

**M4 — Anti-Duplicación.** Convierte el texto en un vector semántico (embedding) y lo compara contra la base de datos. Si la similitud supera el 85% y coinciden el documento de identidad y la pretensión, sugiere acumulación al profesional, quien decide con justificación escrita. **Métrica objetivo:** precisión de sugerencias ≥85%, recall de duplicados ≥90%.

**M5 — Peticionarios Recurrentes.** Índice Elasticsearch que devuelve en <500ms el historial completo de peticiones de un ciudadano: radicados, tipos, estados, respuestas emitidas. **Métrica objetivo:** tiempo de consulta <500ms (p95).

**M6 — Asistente Generativo (RAG + LLM).** Opera en dos modos. Para consultas complejas: el sistema recupera fragmentos relevantes de la base de conocimiento (normativa, jurisprudencia, templates) mediante ChromaDB, los inyecta en un prompt junto con la petición e instrucciones estrictas (no inventar, lenguaje ciudadano, el profesional siempre decide), y Mistral 7B —ejecutándose en servidores propios— genera un borrador que el profesional revisa, edita y firma. Para consultas simples del catálogo D5 ("estado de mi radicado", "quién me atiende") se usan plantillas predefinidas sin pasar por el LLM. Cada interacción queda registrada en logs inmutables. **Métrica objetivo:** borradores aceptados sin corrección mayor ≥70%, tiempo de generación <10s.

**M7 — Interoperabilidad.** Elimina la doble digitación. El nuevo sistema publica eventos en RabbitMQ y dos consumidores replican simultáneamente a IRIS y VisionWeb. Reintentos con backoff exponencial ante fallos. RPA como contingencia si no hay APIs. Bitácora inmutable de cada sincronización. **Métrica objetivo:** sincronización exitosa ≥99.5%.

**M8 — Analítica.** Cuatro dashboards en tiempo real: (1) carga temática, (2) cuellos de botella y cumplimiento de SLA, (3) recurrencia y duplicidad, (4) equidad desagregada por género, región y grupo poblacional. Capa de investigación institucional con datos anonimizados (k-anonymity ≥5) y acceso restringido. **Métrica objetivo:** dashboards actualizados con latencia <1 minuto.

### 5.4 Seguridad, integración y MLOps

**Seguridad (§4.5).** Cuatro roles RBAC definidos con el equipo de Derecho: URAB, Profesional, Auditor y Administrador —este último sin acceso a logs de auditoría—. Autenticación OAuth2/JWT sin estado. Cifrado TLS 1.3 en tránsito y AES-256 en reposo. Logs inmutables (append-only) con backup diario externo. Plan de contingencia ante indisponibilidad de IRIS/VisionWeb con cola local y acuse diferido. Respaldo con RPO≤24h y RTO≤4h `[validar]`.

**Integración IRIS/VisionWeb.** APIs/ETL-ELT como vía primaria; RPA como contingencia. Modelo canónico que mapea campos equivalentes: `radicado` ↔ `numero_radicado` (IRIS) ↔ `codigo_expediente` (VisionWeb). Reintentos: 1s, 2s, 4s, 8s, 16s, 32s. Tras 6 fallos → alerta al administrador. Conciliación diaria automática entre sistemas.

**MLOps (§4.6).** Versionamiento integral: Git (código), DVC (datasets), MLflow (modelos con métricas y parámetros). Monitoreo de drift de datos y predicciones con Evidently AI. Canal de feedback humano: API donde profesionales reportan errores → esos datos alimentan el siguiente reentrenamiento. Política de actualización controlada: solicitud → evaluación → aprobación del Comité de IA → staging → producción con changelog. Los modelos nunca se actualizan sin aprobación explícita.

### 5.5 Plan de pruebas

| Tipo | Objeto | Frecuencia |
|---|---|---|
| Unitarias | Cada función aislada (OCR, NER, validador, reglas) | Cada cambio |
| Integración | Flujo M1→M4→M2→M3. M7→IRIS/VisionWeb | Por sprint |
| Aceptación | Profesionales URAB prueban con casos reales | Antes de cada fase |
| Equidad | Equal Opportunity y Demographic Parity segmentados | Antes de despliegue + trimestral |
| Carga | 300 peticiones/día, picos de 500 | Antes de producción |
| Seguridad | Pentesting, TLS, acceso no autorizado, indisponibilidad | Antes de producción + semestral |

---

## 8. Cambio sociotécnico, enfoque diferencial y pruebas de equidad (~1.5 págs)

### 8.1 Cambio sociotécnico (§5.3)

La introducción de IA transforma la forma de trabajo. Identificamos las siguientes dinámicas:

| Capacidad nueva | Conducta que cambia | Riesgo a anticipar | Decisión de gobernanza |
|---|---|---|---|
| Clasificación masiva (~300/día en minutos) | El profesional pasa de clasificar manualmente a supervisar la IA. Dedica más tiempo a casos complejos. | Sobre-automatización: tentación de delegar decisiones que requieren juicio humano | Lista taxativa de decisiones NUNCA automatizables (§4.2). Human-in-the-loop obligatorio. |
| Historial unificado por ciudadano (M5) | Atender peticionarios recurrentes con contexto completo. Respuestas coherentes. | Concentración de datos personales que incrementa el riesgo de privacidad | Minimización: solo se muestra lo necesario. Roles de acceso diferenciados. |
| Borradores de respuesta (M6) | Redactar en minutos. El profesional edita en lugar de crear desde cero. | Confianza excesiva: omitir la revisión humana obligatoria | Revisión y firma humana registrada en logs. Bitácora de cada borrador. |
| Analítica en tiempo real (M8) | Visibilizar patrones de carga, cuellos y disparidades antes invisibles | Datos agregados que podrían estigmatizar grupos si se usan sin contexto | Enfoque diferencial en dashboards. Privacidad (k-anonymity ≥5). |
| Interoperabilidad IRIS/VisionWeb (M7) | Eliminar la doble digitación | Resistencia al cambio organizacional | Gestión de cambio desde Fase 0, alineada con MIPG e ISO/IEC 42001:2023. |

La gestión de cambio incluye sesiones de sensibilización, manuales de rol y mesa de ayuda desde la Fase 0, con capacitación para al menos 20 profesionales (§6.1).

### 8.2 Pruebas de equidad algorítmica (§5.2)

En el contexto de la Defensoría del Pueblo, un sesgo algorítmico no es solo un error técnico: es una vulneración del derecho a la igualdad (Art. 13 CP). El sistema incorpora pruebas de equidad como gate de calidad obligatorio antes de cada despliegue, integradas al plan de pruebas de la Fase 2 (§6.3).

**Métricas.** Se evalúa Equal Opportunity, Demographic Parity, Disparate Impact Ratio y False Negative Rate, segmentando por género (solo cuando el dato lo proporciona voluntariamente el ciudadano), regional, grupo de especial protección y canal de ingreso. Si una muestra tiene menos de 30 casos, esa segmentación no se reporta.

**Umbrales de alerta y protocolo:**

| Disparidad detectada | Acción |
|---|---|
| <3% entre grupos | Aceptable. Monitoreo continuo. |
| 3–5% o diferencia de precisión >5 puntos | Alerta amarilla. Revisión técnica. Análisis de causas. |
| 5–10% o cociente de falsos negativos >1.5 | Alerta naranja. Comité de IA. Mitigación: rebalanceo, threshold tuning o adversarial debiasing. |
| >10% | Alerta roja. Suspensión del módulo para decisiones que afecten a ese grupo. |

**Monitoreo.** Evidently AI genera reportes trimestrales automáticos. El Comité de IA recibe un reporte mensual específico de False Negative Rate para grupos de especial protección.

**Salvaguardas.** Validación manual de todos los rechazos automáticos, revisión de riesgo vital solo por funcionario, formatos accesibles para personas con discapacidad, prohibición absoluta de automatizar decisiones de fondo.

> **Protocolo completo de pruebas de equidad:** Anexo F (métricas detalladas, niveles de alerta con ejemplo numérico, estrategias de mitigación, tabla de monitoreo por variable y frecuencia).

---

## 9. Matriz de riesgos — SPI, corrupción y daño antijurídico (~1 pág)

Se identifican 12 riesgos organizados en tres familias: T (técnica), O (operacional) y J (jurídica). La matriz completa con probabilidad, impacto, causa raíz, efecto detallado y responsable se encuentra en el Anexo C (basada en `Matriz_SGIA_ISO42001.xlsx`).

| ID | Familia | Riesgo | Mitigación principal | Monitoreo |
|---|---|---|---|---|
| R1 | T | Caída de conectividad o indisponibilidad de IRIS/VisionWeb (§2.4.2) | Colas resilientes (RabbitMQ), modo offline con acuse diferido, plan de contingencia | Semanal |
| R2 | T | Doble registro o archivo en una sola plataforma (§2.4.3) | Modelo canónico + sincronización bidireccional + conciliación diaria automática | Diaria |
| R3 | T | Falso negativo en urgencias: no detección de riesgo vital | Umbral asimétrico (recall ≥99%), revisión humana de casos sin flag, reentrenamiento ante cualquier fallo | Diaria |
| R4 | T | Falso positivo en deduplicación: acumulación de casos distintos | Umbral configurable (85%) + coincidencia de CC + pretensión. Justificación escrita obligatoria del profesional | Semanal |
| R5 | T/O | Sesgo algorítmico que amplifica exclusiones | Pruebas de equidad pre-despliegue, 4 niveles de alerta, adversarial debiasing si es necesario | Cada release + trimestral |
| R6 | O | Dependencia excesiva del sistema, falta de supervisión humana (§5.4) | Human-in-the-loop obligatorio. Lista taxativa de decisiones NUNCA automatizables. | Semanal |
| R7 | O | Omisiones o uso indebido por profesionales | Capacitación desde Fase 0, roles con mínimo privilegio, auditoría de actividad por usuario | Mensual |
| R8 | J | Incumplimiento de términos legales (CPACA, derecho de petición) | Tableros M8 con semaforización. Alertas M3 al 80% y 100% del plazo. Escalamiento en cadena. | Diaria |
| R9 | J | Vulneración de privacidad o tratamiento inadecuado de datos sensibles (Ley 1581/2012) | Defensoría = responsable, proveedor = encargado. AES-256 + TLS 1.3. Evaluación de impacto (AIA). | Trimestral |
| R10 | J | Falta de trazabilidad algorítmica (Directiva 007/2025) | Ficha de Transparencia alineada con NIST AI RMF 1.0. Logs inmutables. | Trimestral |
| R11 | T/O | Alucinación del LLM generando información falsa en respuesta | Arquitectura RAG: solo genera sobre documentos reales. Revisión humana obligatoria. Solo D5 automático. | Semanal |
| R12 | T | Incidente de ciberseguridad con exposición de datos sensibles | RBAC + OAuth2/JWT + cifrado + pentesting periódico + equipo de respuesta a incidentes | Mensual |

> **Matriz de riesgos completa:** Anexo C.

---

## 10. Plan de trabajo por fases y entregables (~1 pág)

El proyecto se organiza en 5 fases secuenciales con criterios de salida verificables. Duración total: 32 semanas de ejecución más 12 meses de garantía y evolución `[validar]`.

| Fase | Duración | Objetivo | Entregables clave | Criterio de aceptación |
|---|---|---|---|---|
| **F0. Alistamiento** | 4 sem | Diagnosticar el AS-IS y preparar datos | Flujograma validado, dataset etiquetado (~1000 casos), taxonomía, línea base de métricas | Diagnóstico y taxonomía aprobados por el comité |
| **F1. Diseño** | 8 sem | Definir arquitectura e integración | Arquitectura objetivo, diagrama de integración IRIS/VisionWeb, especificación de seguridad | Arquitectura validada con sistemas legados |
| **F2. Construcción IA** | 12 sem | Desarrollar y probar módulos core | Prototipos M1, M2, M4, M5, M6. Informe de desempeño y equidad | Métricas ≥ metas §12. Equidad sin disparidad >5% |
| **F3. Implementación** | 8 sem | Desplegar piloto URAB y capacitar | Sistema en operación, 100% profesionales capacitados, tableros M8, mesa de ayuda | Métricas del piloto dentro de umbrales. Satisfacción ≥80% |
| **F4. Gobernanza** | 12+ meses | Operación autónoma y mejora continua | Comité de IA operando, reportes periódicos, transferencia de conocimiento | Equipo interno autónomo ≥3 meses. Auditoría sin hallazgos críticos |

**Modelo de costos de referencia** (basado en `SECOP IA.xlsx`, `[validar]`): ≈$1.125 M COP a 3 años, distribuidos en ~55% año 1 (implementación), ~22.5% año 2 y ~22.5% año 3 (soporte y evolución). Se discrimina: implementación (costo único), licencias, operación/soporte, infraestructura, capacitación y evolución. Pago por hitos verificables, no por tiempo.

> **Plan de trabajo detallado:** Anexo D (actividades por fase, carta Gantt, presupuesto por rubro, hitos de pago).

---

## 12. Métricas y línea base del piloto (~1 pág)

La línea base se levanta en la Fase 0 (actualmente no existen mediciones automatizadas; Banco Q18 confirma que el proceso tarda varios días). Los valores AS-IS son estimaciones del caso `[validar]`.

| # | Indicador | Línea base (est.) | Meta piloto | Umbral de alerta | Frec. |
|---|---|---|---|---|---|
| M1 | Tiempo clasificación sugerida (M2) | Varias horas–2 días (manual) | ≤15 min en 90% (p90) | p90 >30 min | Diaria |
| M2 | Precisión clasificación (accuracy M2) | ~80% (humano, con fatiga) | ≥90% | <85% | Semanal |
| M3 | Recall urgencias/riesgo vital (M2) | No medido | ≥99% (falso negativo ≈0) | Cualquier FN real | Diaria |
| M4 | Precisión sugerencias duplicados (M4) | No hay | ≥85% | <70% | Semanal |
| M5 | Recall duplicados (M4) | <30% (manual aleatorio) | ≥90% | <80% | Semanal |
| M6 | Reducción reprocesos de reparto | Línea base F0 | ≥50% | <20% | Mensual |
| M7 | Cumplimiento tiempos internos | No robusto | ≥90% peticiones en plazo | <80% | Mensual |
| M8 | Tiempo ingreso→asignación (M3) | ~2 días hábiles | ≤4h en 90% (p90) | >+50% desvío | Semanal |
| M9 | Tiempo ingreso→primera respuesta | 15–20 días hábiles | ≤10 días hábiles (p90) | >15 días | Mensual |
| M10 | Extracción correcta entidades (M1) | ~70–80% (digitación) | ≥90% | <85% | Semanal |
| M11 | Borradores M6 sin corrección mayor | No aplica | ≥90% consultas simples | Conflictivas >5% | Semanal |
| M12 | Disponibilidad del sistema | No aplica | ≥99.5% mensual | <99% | Tiempo real |
| M13 | Sincronización IRIS/VisionWeb (M7) | 0% (sin integración) | ≥99.5% | <99% | Tiempo real |
| M14 | Tasa error OCR (M1) | No medido | <5% docs limpios | >10% | Semanal |
| M15 | Equal Opportunity por género (M2) | No medido | <5% diferencia | >5% | Trimestral |
| M16 | Disparate Impact Ratio | No medido | >0.80 | <0.80 | Trimestral |
| M17 | Satisfacción profesional URAB | No aplica | ≥80% | <70% | Trimestral |

**Metodología de umbral asimétrico para riesgo vital.** El costo de un falso negativo en casos de riesgo vital no es comparable al de un falso positivo: el primero implica daño antijurídico y vulneración de derechos fundamentales, el segundo solo un costo operativo. Durante la Fase 0, los juristas de la URAB etiquetan un conjunto *gold* de peticiones con riesgo vital real. El clasificador M2 se calibra con sensibilidad (recall) objetivo de 99–100%, aceptando un incremento controlado de falsos positivos. Cualquier falso negativo de esta clase activa revisión inmediata, análisis de causa raíz y reentrenamiento si es necesario.

> **Métricas detalladas:** Anexo E (metodología completa de cada indicador, plan de medición con herramientas, responsables y dashboards).

---

## Referencia de anexos

| Anexo | Contenido | Extensión aprox. |
|---|---|---|
| **Anexo A** | Especificaciones técnicas M1–M8 con pipeline, componentes, métricas y justificación tecnológica por módulo. Incluye diagrama TO-BE completo (§A.1). | ~8 págs |
| **Anexo B** | Stack tecnológico completo: 14 tecnologías con justificación detallada, licencia, alternativas evaluadas y criterio de selección. | ~2 págs |
| **Anexo C** | Matriz de riesgos completa con 12 riesgos. Cada uno: probabilidad, impacto, causa raíz, efecto detallado, mitigación, evidencia de control, responsable y frecuencia de monitoreo. | ~4 págs |
| **Anexo D** | Plan de trabajo detallado: actividades por fase, carta Gantt, presupuesto discriminado por rubro (implementación, licencias, infraestructura, capacitación, evolución) y tabla de hitos de pago. | ~3 págs |
| **Anexo E** | Métricas detalladas: metodología de cada indicador, definición operativa, fórmula de cálculo, herramienta de medición, responsable, dashboard asociado y protocolo de umbral asimétrico con ejemplo numérico. | ~3 págs |
| **Anexo F** | Pruebas de equidad: protocolo completo con definición de métricas (Equal Opportunity, Demographic Parity, Disparate Impact, False Negative Rate por grupo), 4 niveles de alerta con ejemplos numéricos, estrategias de mitigación (rebalanceo, threshold tuning, adversarial debiasing), y tabla de monitoreo por variable, métrica, frecuencia y responsable. | ~2 págs |

---

*Borrador preparado por el equipo de Ciencia de Datos para integración en el documento de fase escrita. Las secciones en el cuerpo ocupan ~10 páginas. El detalle completo se encuentra en los Anexos A–F, que no cuentan para el límite de 25 páginas del cuerpo del documento. `[validar]` = pendiente de confirmación con mentoría.*

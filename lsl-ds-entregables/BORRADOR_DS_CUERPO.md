# Borrador DS — Cuerpo del documento (~10 págs)

> **Destinatario:** Equipo de Derecho, para integrar en el documento de fase escrita.
> **Puntos cubiertos:** 4, 5, 8, 9, 10, 12 del índice.
> **Formato:** Arial 12, espacio sencillo, márgenes 1.5 cm, tamaño carta, APA 7.ª ed.
> **[validar]:** pendiente de confirmación con mentoría.
> **Referencias (§):** Caso oficial URAB (RFP). [Corchetes]: insumos del equipo.
>
> ### Mapa de anexos para el equipo de Derecho
>
> | Anexo | Contenido | Referenciado desde |
> |---|---|---|
> | **Anexo 04** | Modelo TO-BE: diagrama completo, flujo detallado por etapa, mapeo problema→solución, tabla de decisiones no automatizables | §4 |
> | **Anexo 05** | Arquitectura técnica: especificaciones M1–M8, stack tecnológico, modelo de datos, integración IRIS/VisionWeb, seguridad, MLOps, infraestructura cloud, plan de pruebas | §5 |
> | **Anexo 08** | Pruebas de equidad: protocolo completo, métricas, 4 niveles de alerta con ejemplos, estrategias de mitigación, monitoreo continuo | §8.2 |
> | **Anexo 09** | Matriz de riesgos completa: 12 riesgos con probabilidad, impacto, causa, efecto, mitigación, evidencia, responsable y frecuencia | §9 |
> | **Anexo 10** | Plan de trabajo detallado: carta Gantt, actividades semana a semana, presupuesto discriminado por rubro y fase, hitos de pago | §10 |
> | **Anexo 12** | Métricas detalladas: 17 indicadores con fórmula, herramienta, dashboard, y metodología de umbral asimétrico con ejemplo numérico | §12 |

---

## 4. Modelo TO-BE y alcance del piloto (diseño técnico viable) (~1.5 págs)

### 4.1 Diagnóstico del proceso actual (AS-IS)

El macroproceso de atención y trámite de quejas en la Defensoría del Pueblo opera de forma predominantemente manual. La URAB recibe aproximadamente 300 peticiones diarias por canales diversos sin normalización (formulario web, correo electrónico en formato libre, correspondencia física, jornadas de campo). Cada petición atraviesa cinco etapas dependientes de intervención humana: (A) recepción y verificación manual de legibilidad y completitud, con radicado creado a mano; (B) clasificación manual en las cuatro categorías jurídicas (Asesoría, Queja, Solicitud de Mediación, Solicitud de Conciliación) sin criterios uniformes ni visibilidad del historial del peticionario; (C) asignación manual a profesionales con doble registro en IRIS y VisionWeb, sistemas que no se comunican entre sí (§2.4.3); (D) gestión defensorial sin apoyo documental automatizado, con el profesional investigando y redactando cada respuesta desde cero; y (E) cierre con riesgo de archivo en una sola plataforma, perdiendo trazabilidad.

Cinco problemas estructurales se derivan de este diagnóstico: (1) saturación operativa por clasificación manual (~15 minutos por caso), que resulta en represamiento crónico y respuestas fuera de términos legales; (2) riesgo jurídico por ausencia de priorización automática, donde casos de riesgo vital (amenazas, desapariciones, menores en peligro, violencia basada en género) pueden quedar rezagados entre consultas rutinarias; (3) doble digitación IRIS/VisionWeb que genera retrabajo, errores e inconsistencias entre plataformas; (4) duplicidad de peticiones no detectada, donde un mismo ciudadano puede presentar la misma queja múltiples veces generando respuestas redundantes o contradictorias; y (5) ausencia de historial unificado por ciudadano, abordándose cada nueva petición como si fuera la primera.

### 4.2 Modelo TO-BE

El proceso rediseñado inserta los ocho módulos solicitados (§3, M1–M8) como una capa de asistencia que automatiza tareas repetitivas y apoya —nunca reemplaza— la toma de decisiones del profesional defensorial. En cada punto donde el sistema produce una clasificación, sugerencia o borrador, existe un mecanismo explícito de validación humana antes de que la decisión surta efectos jurídicos, en cumplimiento de §5.4.

| Etapa | Cambio con la solución | Módulos | ¿Quién decide? |
|---|---|---|---|
| **A. Recepción** | Ingesta multicanal normalizada con OCR para documentos escaneados y extracción automática de datos del ciudadano mediante NER. Detección de información faltante con respuesta automática al ciudadano. Radicado semiautomático con validación. | M1 | Humano (valida datos extraídos) |
| **B. Triage en URAB** | Clasificación asistida por IA del tipo de caso (4 categorías), sub-tema (~12), nivel de urgencia (1–5) y detección de sujetos de especial protección constitucional. Historial unificado del peticionario visible en el mismo paso. Validación humana antes de continuar. | M2, M5 | **Humano** (valida/corrige clasificación) |
| **C. Reparto y gestión** | Recomendación de entidad competente mediante matriz tipo+sub-tema. Si es la Defensoría, el sistema sugiere ruta interna según carga y perfil. Bandejas de trabajo con indicadores de tiempo por segmento y alertas automáticas. | M3, M7 | **Humano** (confirma competencia y asignación) |
| **D. Gestión defensorial** | Asistente generativo con arquitectura RAG que consulta normativa, jurisprudencia y plantillas antes de redactar. El profesional siempre revisa, edita y firma. Alertas de patrones de riesgo para elevación inmediata a prioridad. | M6, M5 | **Humano** (revisa, edita, firma) |
| **E. Cierre** | Sincronización simultánea del estado final en IRIS y VisionWeb con bitácora de trazabilidad. Consolidación del expediente y alimentación de dashboards de analítica. | M7, M8 | Humano (inicia el cierre) |

Las decisiones que nunca se automatizan son: evaluación de competencia de la entidad (M3), priorización final de casos de riesgo vital (M2/M6), respuesta de fondo al peticionario (M6 solo redacta borrador), corrección de errores de deduplicación (M4) y cierre del caso (M7). En todos estos puntos la IA asiste o sugiere; la decisión vinculante es exclusivamente humana.

### 4.3 Mapeo problema → solución

| Problema crítico | Módulo(s) | Cómo lo resuelve |
|---|---|---|
| Volumen y saturación (~300/día) | M1, M2, M6 | Automatiza recepción, extracción de datos y clasificación. El profesional pasa de digitar a supervisar. |
| Riesgo jurídico por falta de priorización | M2, M3 | Score de urgencia (1–5) con reglas auditables, detección automática de sujetos de especial protección, SLAs visibles con alertas. |
| Doble registro IRIS/VisionWeb | M7 | Capa de orquestación con modelo canónico: único punto de entrada, sincronización bidireccional simultánea, bitácora de cada operación. |
| Duplicidad de peticiones | M4 | Comparación semántica mediante embeddings y cosine similarity. Si ≥85% de similitud + mismo CC + misma pretensión: sugerencia de acumulación al profesional. |
| Peticionarios sin historial | M5 | Índice unificado Elasticsearch. Historial completo del ciudadano consultable por cédula en menos de 500ms. |

### 4.4 Alcance del piloto en URAB

El piloto se implementa en la URAB de Bogotá (~300 peticiones/día, 8–10 profesionales, 8 semanas de operación controlada en la Fase 3). Entran en el piloto los módulos M1, M2, M3, M4, M5 y M6 con validación humana en todos los puntos de decisión (§5.4), M7 con integración mínima IRIS/VisionWeb requerida por §4.2, y M8 con el Dashboard 1 de carga temática. Se difieren al escalamiento progresivo otras Unidades de Análisis fuera de Bogotá, la integración con Carpeta Ciudadana Digital (gov.co) como componente opcional de M7 —el Banco de Preguntas indica que el proponente puede proponer un mecanismo de acuse de recibo y consulta de estado—, y la foliación electrónica con firma de índice bajo estándares AGN, ofrecida como diferenciador a partir de §4.3 y la gestión documental de §5.1 (Banco Q8: no es requisito mínimo). Las métricas y obligaciones de la Fase 3 se comprometen en el piloto URAB; la analítica institucional se habilita sobre los datos del piloto y se extiende con el escalamiento.

Criterios de salida del piloto: precisión de clasificación ≥90%, recall de urgencias/riesgo vital ≥99%, detección de duplicados ≥85% recall, tiempo ingreso→asignación ≤4h (p90), disponibilidad del sistema ≥99.5% mensual. Si la precisión cae por debajo de 75% no se escala sin reentrenar.

> **Diagrama TO-BE completo, flujo detallado por etapa y tabla de decisiones no automatizables:** Anexo 04.

---

## 5. Arquitectura técnica de la solución (~4 págs)

### 5.1 Decisión de arquitectura: nube corporativa con capa de orquestación

La solución se despliega sobre una **plataforma corporativa en nube para la administración de agentes de inteligencia artificial**, operada por el contratista o un proveedor autorizado bajo los lineamientos de seguridad, administración y gobernanza definidos por la Defensoría del Pueblo. Esta modalidad se identifica como la alternativa más adecuada por cuatro razones:

**Orquestación unificada de modelos.** La plataforma permite utilizar, versionar y administrar simultáneamente diferentes modelos de IA —tanto los desarrollados específicamente para la Defensoría (BETO fine-tuned para clasificación, modelos NER propios) como modelos fundacionales de terceros (Mistral 7B para generación de borradores, Sentence-Transformers para embeddings semánticos)— bajo un mismo marco corporativo de seguridad, control de accesos y trazabilidad de ejecuciones.

**Delegación de infraestructura.** Los requerimientos de infraestructura, mantenimiento, seguridad física, escalabilidad automática y soporte técnico 24/7 se delegan en el contratista o proveedor autorizado, liberando a la Defensoría de la carga operativa de administrar servidores, actualizar dependencias, escalar recursos ante picos de demanda y mantener la continuidad del servicio. El contratista asume los niveles de servicio (SLA) de disponibilidad ≥99.5%, tiempo de respuesta de API <500ms (p95) y recuperación ante desastres con RPO≤24h y RTO≤4h.

**Integración y sincronización optimizadas.** El despliegue en nube ofrece mejores condiciones de conectividad, disponibilidad y latencia para la integración con IRIS y VisionWeb, así como para la sincronización bidireccional mediante la capa de orquestación con modelo canónico de datos. Los eventos de ciclo de vida del caso (`creado`, `actualizado`, `cerrado`) se publican en colas de mensajería cloud-native que garantizan la entrega y la trazabilidad de cada sincronización hacia los sistemas legados.

**Protección de datos bajo modelo contractual.** En materia de tratamiento de datos personales (Ley 1581 de 2012), la plataforma opera bajo un modelo robusto de protección definido contractualmente: la Defensoría es la responsable del tratamiento y el contratista actúa como encargado con instrucciones documentadas. Los datos se procesan dentro de un entorno empresarial controlado, con cifrado AES-256 en reposo y TLS 1.3 en tránsito, acceso segmentado por roles RBAC, y logs inmutables de auditoría. La URAB establece lineamientos para la anonimización de los datos utilizados en procesos de entrenamiento, despliegue y aprendizaje de modelos, garantizando que estos se gestionen exclusivamente para los fines misionales de la organización y no estén disponibles para terceros.

Frente al problema de IRIS vs. VisionWeb —dos sistemas sin comunicación entre sí (§2.4.3), mientras §4.2 exige evitar dobles registros—, la capa de orquestación opera sobre la infraestructura cloud manteniendo un registro único con modelo canónico de datos y sincronización bidireccional. Esta decisión cumple §4.2 (evitar doble registro), reduce el riesgo del §2.4.3 (archivo en una sola plataforma), y alimenta la trazabilidad requerida por §5.4. Si los sistemas legados no ofrecen API de escritura (Banco Q10), se despliega RPA como capa de contingencia.

### 5.2 Arquitectura lógica

```
[ Capa de acceso ]       Bandejas URAB · Bandejas profesionales · Dashboards (M8)
                         Acceso web seguro (HTTPS/TLS 1.3) · Autenticación OAuth2/JWT
──────────────────────────────────────────────────────────────────────────────────
[ Capa de orquestación ] API Gateway cloud-native · Message Broker · Workflow ingreso→cierre
                         Bitácora inmutable · Orquestador de modelos de IA
──────────────────────────────────────────────────────────────────────────────────
[ Plataforma de agentes de IA en nube corporativa ]
    ● Motor M2 — Clasificación y triaje (BETO fine-tuned)
    ● Motor M4 — Anti-duplicación (Sentence-Transformers + cosine similarity)
    ● Motor M6 — Asistente generativo RAG (ChromaDB + Mistral 7B)
    ● Motor M5 — Historial unificado (Elasticsearch)
    ● Motor M1 — OCR (Tesseract) + NER (spaCy)
    ● Administración: versionamiento, monitoreo, drift, feedback loop
──────────────────────────────────────────────────────────────────────────────────
[ Modelo canónico de datos ] PostgreSQL + pgvector (cloud-managed)
──────────────────────────────────────────────────────────────────────────────────
[ Capa de integración ] Conectores → IRIS · VisionWeb · gov.co (opcional)
                        RPA como contingencia
──────────────────────────────────────────────────────────────────────────────────
[ Seguridad transversal cloud ] RBAC · OAuth2/JWT · TLS 1.3 · AES-256
                                Logs inmutables · WAF · DDoS protection · Backup automático
```

### 5.3 Stack tecnológico y plataforma de agentes de IA

La plataforma cloud corporativa permite la administración unificada de los siguientes modelos y servicios. El detalle completo de cada tecnología —incluyendo justificación, licencia, alternativas evaluadas y criterios de selección— se encuentra en el Anexo 05.

| Capa | Tecnología | Función |
|---|---|---|
| **Plataforma cloud** | Infraestructura como Servicio (IaaS) / Plataforma como Servicio (PaaS) corporativa | Orquestación de todos los agentes de IA, administración de versiones, monitoreo, escalabilidad |
| Backend / API | FastAPI (Python) | Gateway de servicios, endpoints REST documentados (OpenAPI 3.0) |
| Clasificación NLP | **BETO** (`dccuchile/bert-base-spanish-wwm-uncased`) fine-tuned | Clasificación primaria (4 categorías) y sub-clasificación multi-etiqueta (~12 sub-temas) |
| Extracción de entidades | **spaCy** (`es_core_news_lg`) + fine-tuning | NER: extrae nombre, CC, dirección, pretensión, entidad referida |
| Similitud semántica | **Sentence-Transformers** (`paraphrase-multilingual-mpnet-base-v2`) | Embeddings 768-dim para comparación de significados en detección de duplicados |
| LLM generativo | **Mistral 7B** (Instruct v0.2) — ejecutado en la nube corporativa | Asistente RAG: generación de borradores de respuesta |
| RAG | **LangChain + ChromaDB** | Recuperación de normativa y jurisprudencia + generación controlada |
| OCR | **Tesseract LSTM** (`spa`) + OpenCV | Conversión de documentos escaneados a texto |
| BD transaccional + vectorial | **PostgreSQL + pgvector** (cloud-managed) | Almacenamiento canónico + índices vectoriales para búsqueda semántica |
| Búsqueda textual | **Elasticsearch** (cloud-managed) | Índice de historial unificado por ciudadano |
| Mensajería | **RabbitMQ** (cloud-managed) o equivalente cloud-native | Publicación y consumo de eventos de sincronización IRIS/VisionWeb |
| MLOps | **MLflow + DVC + Evidently AI** | Versionamiento de modelos y datos, monitoreo de drift y rendimiento |
| Dashboard | **Streamlit** (piloto) → **Power BI** (producción) | Visualización de métricas operativas, calidad y equidad |

Todos los modelos de IA utilizados son de código abierto con licencias permisivas (MIT, Apache 2.0), lo que permite su uso, modificación y despliegue sin costos de licenciamiento. La plataforma cloud corporativa administra las diferentes versiones de estos modelos —tanto los desarrollados por el contratista como los modelos fundacionales de terceros— bajo un mismo marco de seguridad, control de acceso y gobernanza.

### 5.4 Descripción funcional de módulos

> Las especificaciones técnicas detalladas de cada módulo —incluyendo pipeline completo, componentes internos, tecnologías, métricas de rendimiento, modelo de datos, contratos de API y plan de pruebas— se encuentran en el Anexo 05. A continuación se presenta la función de cada módulo y su contribución al macroproceso.

**M1 — Recepción Inteligente.** Recibe peticiones por todos los canales, aplica OCR a documentos escaneados o fotografiados, extrae automáticamente los datos del ciudadano mediante NER, verifica completitud de campos obligatorios (nombre, documento de identidad, descripción del hecho, pretensión), y genera radicado único. Si se detectan datos faltantes, el sistema responde automáticamente al ciudadano solicitando la información complementaria con plantillas institucionales. **Métrica objetivo:** tasa de extracción correcta de entidades ≥90%.

**M2 — Clasificación y Triaje.** Clasifica la petición en las 4 categorías jurídicas mediante un modelo BETO con fine-tuning. Un sub-clasificador multi-etiqueta asigna los sub-temas aplicables (~12). Un sistema de reglas determinístico y auditable —no de caja negra— asigna nivel de urgencia en escala 1 a 5 según los criterios jurídicos del equipo de Derecho. Un priorizador cruza el texto con el catálogo de sujetos de especial protección constitucional y asigna flags de alerta. El profesional de URAB valida o corrige toda clasificación. **Métrica objetivo:** accuracy ≥90%, recall en urgencias/riesgo vital ≥99% (umbral asimétrico).

**M3 — Asignación y Enrutamiento.** Determina la entidad competente mediante matriz de reglas tipo+sub-tema (alimentada y validada por el equipo de Derecho). Si la Defensoría es competente, recomienda ruta interna según carga y perfil del profesional. Bandejas de trabajo con estados y monitoreo de SLA (ingreso→asignación <4h, gestión→cierre <15 días hábiles) con alertas automáticas al 80% y 100% del plazo. **Métrica objetivo:** tiempo ingreso→asignación ≤15 min en el 90% de los casos.

**M4 — Anti-Duplicación.** Convierte el texto de la petición en un embedding semántico de 768 dimensiones y lo compara vía cosine similarity contra los casos existentes en la base de datos. Si la similitud supera el 85% y coinciden el documento de identidad y la pretensión del ciudadano, el sistema sugiere acumulación al profesional mediante una interfaz que muestra ambas peticiones lado a lado con los campos coincidentes resaltados. El profesional decide con justificación escrita. **Métrica objetivo:** precisión de sugerencias ≥85%, recall de duplicados ≥90%.

**M5 — Peticionarios Recurrentes.** Índice Elasticsearch que permite consultar por número de cédula el historial completo de peticiones de un ciudadano (radicados, fechas, tipos, estados, profesionales asignados, respuestas emitidas) en menos de 500ms. El sistema sugiere además respuestas previas y plantillas institucionales aplicables al caso. **Métrica objetivo:** tiempo de consulta <500ms (p95).

**M6 — Asistente Generativo (RAG + LLM).** Opera en dos modos. Para consultas complejas, el sistema recupera fragmentos relevantes de la base de conocimiento (normativa, jurisprudencia, plantillas institucionales, respuestas previas anonimizadas) mediante ChromaDB, los inyecta en un prompt con instrucciones estrictas —no inventar, lenguaje ciudadano, no decidir— y Mistral 7B, ejecutándose en la nube corporativa, genera un borrador. El profesional siempre revisa, edita y firma. Para consultas simples del catálogo previamente aprobado por el equipo de Derecho (estado del radicado, profesional asignado, reenvío de constancia), el sistema responde automáticamente con plantillas sin pasar por el LLM. Adicionalmente, M6 incorpora un detector de patrones de riesgo en tiempo real (amenazas, desapariciones, menores en peligro, VBG) que notifica inmediatamente al profesional y dispara alertas en el dashboard. **Métrica objetivo:** borradores aceptados sin corrección mayor ≥70%, tiempo de generación <10s.

**M7 — Interoperabilidad.** Elimina la doble digitación. El nuevo sistema es el único punto de entrada de peticiones. Cada evento de ciclo de vida se publica en el message broker cloud y dos consumidores independientes replican simultáneamente a IRIS y VisionWeb. Reintentos con backoff exponencial ante fallos (1s, 2s, 4s, 8s, 16s, 32s). Tras 6 fallos, alerta al administrador. RPA como contingencia si los sistemas legados no ofrecen API de escritura. Bitácora inmutable de cada sincronización. Conciliación diaria automática entre los tres sistemas. **Métrica objetivo:** sincronización exitosa ≥99.5%.

**M8 — Analítica.** Cuatro dashboards que transforman datos operativos en información para la toma de decisiones: (1) carga temática —distribución por tipo, tendencias, top 10 sub-temas—, (2) cuellos de botella —tiempos por etapa, carga por profesional, casos vencidos—, (3) recurrencia y duplicidad, y (4) equidad —desagregada por género, región y grupo de especial protección, con alertas de disparidad significativa—. Incluye una capa de investigación institucional con datos anonimizados (k-anonymity ≥5) y acceso restringido a rol "investigador" previa aprobación del Comité de IA. **Métrica objetivo:** dashboards actualizados en tiempo real, latencia <1 minuto desde el evento.

### 5.5 Seguridad, MLOps y pruebas

**Seguridad y protección de datos (§4.5).** El modelo de seguridad opera bajo el esquema de responsabilidad compartida de la plataforma cloud corporativa: el proveedor cloud garantiza la seguridad física, de red y de virtualización; el contratista implementa los controles a nivel de aplicación y datos. Cuatro roles de acceso (RBAC): URAB, Profesional defensorial, Auditor y Administrador —este último sin acceso a logs de auditoría, en cumplimiento del principio de mínimo privilegio—. Autenticación OAuth2/JWT sin estado. Cifrado TLS 1.3 en tránsito y AES-256 en reposo. Logs inmutables (append-only) con backup automático diario a almacenamiento externo. Plan de contingencia ante indisponibilidad de IRIS/VisionWeb con cola de mensajes local y acuse diferido al ciudadano. El contratista garantiza contractualmente la anonimización de los datos utilizados en entrenamiento, despliegue y aprendizaje de modelos, operando dentro de un entorno empresarial controlado y disponible únicamente para la Defensoría.

**MLOps (§4.6).** Versionamiento integral: Git (código), DVC (datasets etiquetados), MLflow Model Registry (modelos con métricas, parámetros y artefactos). Monitoreo de drift de datos y predicciones mediante Evidently AI con reportes automáticos. Canal de retroalimentación humana: API donde los profesionales reportan errores de clasificación; esos datos etiquetados alimentan el siguiente ciclo de reentrenamiento. Política de actualización controlada: solicitud → evaluación técnica → aprobación del Comité de IA → staging → producción con changelog. Los modelos nunca se actualizan sin aprobación explícita.

**Plan de pruebas.** Pruebas unitarias (cada componente aislado), de integración (flujos M1→M4→M2→M3 y M7→IRIS/VisionWeb), de aceptación (profesionales URAB con casos reales), de equidad (Equal Opportunity, Demographic Parity y False Negative Rate segmentados), de carga (simulación de 300 peticiones/día con picos de 500), y de seguridad (pentesting, revisión TLS, simulación de indisponibilidad).

> **Especificaciones técnicas completas M1–M8, stack tecnológico detallado, modelo de datos, arquitectura de seguridad, MLOps y plan de pruebas:** Anexo 05.

---

## 8. Cambio sociotécnico, enfoque diferencial y pruebas de equidad (~1.5 págs)

### 8.1 Cambio sociotécnico (§5.3)

La introducción de IA en el macroproceso de la Defensoría transforma la forma en que los funcionarios trabajan y cómo los ciudadanos interactúan con la institución. La siguiente tabla identifica las nuevas capacidades, las conductas que se habilitan, los impactos disruptivos que deben anticiparse y las decisiones de gobernanza que los mitigan:

| Capacidad nueva | Conducta que cambia | Riesgo a anticipar | Decisión de gobernanza |
|---|---|---|---|
| Lectura y clasificación masiva (~300 peticiones/día en minutos) | El profesional pasa de clasificar manualmente a supervisar la IA. Dedica más tiempo a casos complejos y menos a tareas repetitivas. | Sobre-automatización: tentación de delegar decisiones que requieren juicio humano (priorización, competencia). | Lista taxativa de decisiones NUNCA automatizables (§4.2). Human-in-the-loop obligatorio en todos los puntos de decisión. |
| Vista unificada del historial por ciudadano (M5) | Atender peticionarios recurrentes con contexto completo en segundos. Respuestas más coherentes y personalizadas entre distintas interacciones. | Privacidad por concentración de historial: todos los casos de un ciudadano visibles en un solo punto. | Principio de minimización: solo se muestra lo necesario para el caso actual. Roles de acceso diferenciados. Consentimiento informado. |
| Borradores de respuesta generados por IA (M6) | Redactar respuestas en minutos en lugar de horas. El profesional edita y personaliza en lugar de empezar desde cero. | Confianza excesiva en la IA: omitir la revisión humana obligatoria, asumir que el borrador es correcto. | Revisión y firma humana registrada en logs inmutables. UI con fricción deliberada (confirmación explícita, tiempo mínimo de visualización). |
| Monitoreo y analítica en tiempo real (M8) | Visibilizar patrones de carga, cuellos de botella y disparidades entre grupos poblacionales que antes eran invisibles. | Datos agregados que podrían amplificar barreras o estigmatizar grupos si se usan sin contexto. | Enfoque diferencial en dashboards. Privacidad (k-anonymity ≥5). Reportes públicos de equidad. |
| Interoperabilidad IRIS/VisionWeb (M7) | Eliminar la doble digitación. Un solo registro, dos plataformas actualizadas simultáneamente. | Resistencia al cambio organizacional. Posible percepción de redundancia del nuevo sistema. | Gestión de cambio desde Fase 0, alineada con MIPG e ISO/IEC 42001:2023. Capacitación mínima de 20 profesionales (§6.1). |

La estrategia de gestión de cambio incluye sesiones de sensibilización sobre IA en el sector público, manuales de rol con procedimientos claros, y mesa de ayuda durante el piloto y los primeros seis meses de operación (§6.4).

### 8.2 Pruebas de equidad algorítmica (§5.2)

En el contexto de la Defensoría del Pueblo —cuya misión constitucional es proteger los derechos humanos de toda la población, con énfasis en los grupos más vulnerables— un sesgo algorítmico no es un error técnico: es una vulneración del derecho fundamental a la igualdad (Art. 13 CP). La solución incorpora pruebas de equidad como gate de calidad obligatorio antes de cada despliegue.

**Métricas utilizadas.** Equal Opportunity (diferencia en tasa de aciertos positivos entre grupos), Demographic Parity (diferencia en proporción de predicciones entre grupos), Disparate Impact Ratio (cociente entre el grupo con peor y mejor rendimiento, debe ser >0.80), y False Negative Rate por grupo (el error más grave: omitir un caso urgente más en unos grupos que en otros).

**Segmentación.** Género (solo cuando el ciudadano lo proporciona voluntariamente, nunca inferido), regional/departamento, grupo de especial protección (NNA, mujeres VBG, discapacidad, adultos mayores, desplazados, minorías étnicas, población privada de libertad, migrantes), y canal de ingreso. Si una muestra tiene menos de 30 casos, esa segmentación no se reporta.

**Niveles de alerta y protocolo de actuación:**

| Disparidad detectada | Acción |
|---|---|
| <3% de diferencia entre grupos | Verde — Aceptable. Monitoreo continuo. |
| 3–5% o diferencia de precisión >5 puntos entre subgrupos | Amarillo — Revisión técnica. Análisis de causas. No detiene despliegue. |
| 5–10% o cociente de falsos negativos >1.5 | Naranja — Escalar al Comité de IA en 5 días. Activar mitigación: rebalanceo de datos, threshold tuning o adversarial debiasing. Detener despliegue para el grupo afectado. |
| >10% de diferencia | Rojo — Suspender el módulo para TODOS los grupos. Investigación urgente. Notificar al Defensor Delegado. |

**Salvaguardas institucionales.** Validación manual de todos los rechazos automáticos, revisión de casos de riesgo vital exclusivamente por un funcionario, formatos accesibles para personas con discapacidad, prohibición absoluta de automatizar decisiones de fondo.

> **Protocolo completo de pruebas de equidad:** Anexo 08 (definiciones formales de métricas, niveles de alerta con ejemplo numérico, 4 estrategias de mitigación, plan de monitoreo continuo por variable, gate de despliegue).

---

## 9. Matriz de riesgos — SPI, corrupción y daño antijurídico (§5.5) (~1 pág)

Se identifican 12 riesgos en tres familias: T (técnica), O (operacional) y J (jurídica). La matriz completa con probabilidad, impacto, causa raíz, efecto detallado, responsable y evidencia de control se encuentra en el Anexo 09 (basada en `Matriz_SGIA_ISO42001.xlsx` hoja "2. Matriz SGIA").

| ID | F. | Riesgo | Mitigación principal | Monitoreo |
|---|---|---|---|---|
| R1 | T | Caída de conectividad o indisponibilidad de IRIS/VisionWeb que genera represamiento (§2.4.2) | Colas resilientes cloud, modo offline con acuse diferido, plan de contingencia documentado | Semanal |
| R2 | T | Error de integración: doble registro o archivo en una sola plataforma (§2.4.3) | Modelo canónico + sincronización bidireccional + conciliación diaria automática | Diaria |
| R3 | T | Falso negativo en clasificación de urgencias: no detección de riesgo vital | Umbral asimétrico calibrado para recall ≥99%, revisión humana de casos sin flag, reentrenamiento ante cualquier fallo | Diaria |
| R4 | T | Falso positivo en deduplicación: acumulación inadecuada de casos diferentes | Umbral 85% configurable + coincidencia CC + pretensión. Justificación escrita obligatoria del profesional | Semanal |
| R5 | T/O | Sesgo algorítmico que amplifica exclusiones (género, discapacidad, juventud, etnia) | Pruebas de equidad pre-despliegue, 4 niveles de alerta con protocolo graduado, adversarial debiasing | Cada release + trimestral |
| R6 | O | Dependencia excesiva del sistema, pérdida de supervisión humana significativa (§5.4) | Lista taxativa de decisiones NUNCA automatizables. Human-in-the-loop obligatorio. UI con fricción en puntos críticos | Semanal |
| R7 | O | Omisiones o uso indebido por profesionales (carga incorrecta, falta de revisión) | Capacitación desde Fase 0 con certificación, roles con mínimo privilegio, auditoría de actividad | Mensual |
| R8 | J | Incumplimiento de términos legales (CPACA, Ley 1755/2015, derecho de petición) | Dashboards M8 con semaforización, alertas M3 al 80% y 100% del plazo, escalamiento en cadena | Diaria |
| R9 | J | Vulneración de privacidad o tratamiento inadecuado de datos sensibles (Ley 1581/2012) | Defensoría = responsable, contratista = encargado con instrucciones contractuales. AES-256 + TLS 1.3 + anonimización. Evaluación de impacto (AIA) | Trimestral |
| R10 | J | Falta de trazabilidad algorítmica (Directiva Conjunta 007/2025) | Ficha de Transparencia Algorítmica alineada con NIST AI RMF 1.0. Logs inmutables con registro de cada decisión | Trimestral |
| R11 | T/O | Alucinación del LLM generando información falsa en respuesta oficial | Arquitectura RAG: solo genera sobre documentos reales de ChromaDB. Revisión humana obligatoria. Solo D5 automático. | Semanal |
| R12 | T | Incidente de ciberseguridad con exposición de datos sensibles [antecedente DOC_1] | Seguridad cloud bajo responsabilidad compartida. RBAC + OAuth2 + cifrado + pentesting + equipo de respuesta | Mensual |

> **Matriz de riesgos completa:** Anexo 09. Incluye probabilidad, impacto, causa raíz, efecto detallado, evidencia de control y responsable para cada riesgo.

---

## 10. Plan de trabajo por fases y entregables (§6) (~1 pág)

El proyecto se organiza en 5 fases secuenciales con criterios de salida verificables, desplegadas sobre la plataforma cloud corporativa. Duración total: 32 semanas de ejecución más 12 meses de garantía y evolución `[validar]`.

| Fase | Duración | Objetivo | Entregables clave | Criterio de aceptación |
|---|---|---|---|---|
| **F0. Alistamiento y diagnóstico** | 4 sem | Diagnosticar el AS-IS y preparar los datos | Flujograma validado, dataset etiquetado (~1000 casos), taxonomía, línea base de métricas, configuración inicial del entorno cloud | Diagnóstico y taxonomía aprobados por el comité del proyecto |
| **F1. Diseño de arquitectura e integración** | 8 sem | Definir la arquitectura cloud y la estrategia de integración con IRIS/VisionWeb | Arquitectura objetivo, diagrama de integración, modelo canónico de datos, especificación de seguridad cloud, diseño de la plataforma de agentes de IA | Arquitectura validada con equipos de sistemas legados |
| **F2. Construcción de módulos IA** | 12 sem | Desarrollar, entrenar y probar los módulos core en el entorno cloud | Prototipos M1–M6 desplegados en cloud de desarrollo. Informe de desempeño sobre conjunto gold. Pruebas de equidad superadas | Métricas ≥ metas (§12). Sin disparidad >5% en equidad |
| **F3. Implementación, capacitación y operación inicial** | 8 sem | Desplegar el piloto en producción cloud, capacitar y operar en modo supervisado | Sistema en producción, 100% profesionales capacitados, dashboards M8, mesa de ayuda, informe comparativo sistema vs. manual | Métricas del piloto en umbrales. Satisfacción ≥80% |
| **F4. Gobernanza y mejora continua** | 12+ meses | Operación autónoma, transferencia y evolución controlada | Comité de IA operando, reportes periódicos de métricas y equidad, transferencia de conocimiento al equipo interno | Equipo interno autónomo ≥3 meses. Auditoría sin hallazgos críticos |

**Modelo de costos de referencia** `[validar]`: ≈$1.125 M COP a 3 años, con la infraestructura cloud como servicio gestionado por el contratista incluida en el rubro de infraestructura y operación. Presupuesto discriminado en Anexo 10. Pago por hitos verificables, no por tiempo.

> **Plan de trabajo detallado:** Anexo 10 (actividades semana a semana, carta Gantt, presupuesto por rubro y fase, hitos de pago).

---

## 12. Métricas y línea base del piloto (§4.4) (~1 pág)

La línea base se levanta durante la Fase 0 (actualmente no existen mediciones automatizadas; el Banco Q18 confirma que el proceso tarda varios días y no se mide formalmente). Los valores AS-IS son estimaciones basadas en el caso que deben refinarse con los datos reales del diagnóstico `[validar]`.

| # | Indicador | Línea base (est.) | Meta piloto | Umbral de alerta | Frecuencia |
|---|---|---|---|---|---|
| M1 | Tiempo de clasificación sugerida (M2) | Varias horas–2 días (manual, sin medición) | ≤15 min en 90% (p90) | p90 >30 min | Diaria |
| M2 | Precisión de clasificación — accuracy (M2) | ~80% (humano, con fatiga) | ≥90% global; ≥90% subclasificación | <85% o caída >3 puntos | Semanal |
| M3 | Recall de urgencias / riesgo vital (M2) | No medido | ≥99% (falso negativo ≈0) | Cualquier FN real | Diaria |
| M4 | Precisión de sugerencias de duplicados (M4) | No hay sistema | ≥85% | <70% | Semanal |
| M5 | Recall de duplicados (M4) | <30% (muestreo manual) | ≥90% | <80% | Semanal |
| M6 | Reducción de reprocesos de reparto | Línea base F0 | ≥50% de reducción | <20% | Mensual |
| M7 | Cumplimiento de tiempos internos | No robusto | ≥90% de peticiones en plazo | <80% | Mensual |
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

**Metodología de umbral asimétrico para riesgo vital.** El costo de un falso negativo en casos de riesgo vital (desapariciones, amenazas, menores en peligro, VBG activa) no es comparable al de un falso positivo: el primero implica daño antijurídico y vulneración de derechos fundamentales (§2.4.2 + §5.5); el segundo representa un costo operativo manejable (revisión adicional de ~15 minutos). El clasificador M2 se calibra durante la Fase 2 con un conjunto gold etiquetado por juristas de la URAB, ajustando el umbral de decisión para alcanzar una sensibilidad (recall) ≥99% en la clase "riesgo vital", aceptando un incremento controlado de falsos positivos como costo operativo. Cualquier falso negativo de esta clase activa revisión inmediata, análisis de causa raíz y reentrenamiento si es necesario.

> **Métricas detalladas:** Anexo 12 (definición operativa con fórmula de cada indicador, plan de medición con herramientas, responsables y dashboards, metodología completa de umbral asimétrico con ejemplo numérico calibrado).

---

*Borrador preparado por el equipo de Ciencia de Datos para integración en el documento de fase escrita. Las secciones en el cuerpo ocupan ~10 páginas en formato Arial 12, espacio sencillo, márgenes 1.5 cm. El detalle completo se encuentra en los Anexos 04, 05, 08, 09, 10 y 12.*

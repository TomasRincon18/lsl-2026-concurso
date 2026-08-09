# Borrador DS — Cuerpo del documento (~10 pags)

> Destinatario: Equipo de Derecho, para integrar en el documento de fase escrita.
> Puntos cubiertos: 4, 5, 8, 9, 10, 12 del indice.
> Formato: Arial 12, espacio sencillo, margenes 1.5 cm, tamano carta, APA 7.a ed.
> [validar]: pendiente de confirmacion con mentoria.
> Referencias (par. mark): Caso oficial URAB (RFP). [Corchetes]: insumos del equipo.

### Mapa de anexos para el equipo de Derecho

| Anexo | Contenido | Referenciado desde |
|---|---|---|
| Anexo 04 | Modelo TO-BE: diagrama completo, flujo detallado por etapa, mapeo problema a solucion, tabla de decisiones no automatizables | par. 4 |
| Anexo 05 | Arquitectura tecnica: especificaciones M1 a M8, stack tecnologico, modelo de datos, integracion IRIS/VisionWeb, seguridad, MLOps, infraestructura cloud, plan de pruebas | par. 5 |
| Anexo 08 | Pruebas de equidad: protocolo completo, metricas, 4 niveles de alerta con ejemplos, estrategias de mitigacion, monitoreo continuo | par. 8.2 |
| Anexo 09 | Matriz de riesgos completa: 12 riesgos con probabilidad, impacto, causa, efecto, mitigacion, evidencia, responsable y frecuencia | par. 9 |
| Anexo 10 | Plan de trabajo detallado: carta Gantt, actividades semana a semana, presupuesto discriminado por rubro y fase, hitos de pago | par. 10 |
| Anexo 12 | Metricas detalladas: 17 indicadores con formula, herramienta, dashboard, y metodologia de umbral asimetrico con ejemplo numerico | par. 12 |

---

## 4. Modelo TO-BE y alcance del piloto (diseno tecnico viable) (~1.5 pags)

### 4.1 Diagnostico del proceso actual (AS-IS)

El macroproceso de atencion y tramite de quejas en la Defensoria del Pueblo opera de forma predominantemente manual. La URAB recibe unas 300 peticiones diarias por canales diversos sin normalizar: formulario web, correo electronico en formato libre, correspondencia fisica, jornadas de campo. Cada peticion atraviesa cinco etapas que dependen de intervencion humana: (A) recepcion y verificacion manual de legibilidad y completitud, con radicado creado a mano; (B) clasificacion manual en las cuatro categorias juridicas sin criterios uniformes ni visibilidad del historial del peticionario; (C) asignacion manual a profesionales con doble registro en IRIS y VisionWeb, sistemas que no se comunican entre si (par. 2.4.3); (D) gestion defensorial sin apoyo documental automatizado, donde el profesional investiga y redacta cada respuesta desde cero; y (E) cierre con riesgo de archivo en una sola plataforma, lo que implica perdida de trazabilidad.

De este diagnostico se derivan cinco problemas estructurales: (1) saturacion operativa por clasificacion manual, aproximadamente 15 minutos por caso, que produce represamiento cronico y respuestas fuera de terminos legales; (2) riesgo juridico por ausencia de priorizacion automatica, donde casos de riesgo vital (amenazas, desapariciones, menores en peligro, violencia basada en genero) pueden quedar rezagados entre consultas rutinarias; (3) doble digitacion IRIS/VisionWeb que genera retrabajo, errores e inconsistencias entre plataformas; (4) duplicidad de peticiones no detectada, donde un mismo ciudadano puede presentar la misma queja varias veces y recibir respuestas redundantes o contradictorias; y (5) ausencia de historial unificado por ciudadano, lo que obliga a abordar cada nueva peticion como si fuera la primera.

### 4.2 Modelo TO-BE

El proceso redisenado inserta los ocho modulos solicitados (par. 3, M1 a M8) como una capa de asistencia que automatiza tareas repetitivas y apoya, sin reemplazar, la toma de decisiones del profesional defensorial. En cada punto donde el sistema produce una clasificacion, sugerencia o borrador, hay un mecanismo explicito de validacion humana antes de que la decision surta efectos juridicos, segun lo exigido en par. 5.4.

| Etapa | Cambio con la solucion | Modulos | Quien decide |
|---|---|---|---|
| A. Recepcion | Ingesta multicanal normalizada con OCR para documentos escaneados y extraccion automatica de datos del ciudadano mediante NER. Deteccion de informacion faltante con respuesta automatica al ciudadano. Radicado semiautomatico con validacion. | M1 | Humano (valida datos extraidos) |
| B. Triage en URAB | Clasificacion asistida por IA del tipo de caso (4 categorias), sub-tema, nivel de urgencia (1 a 5) y deteccion de sujetos de especial proteccion constitucional. Historial unificado del peticionario visible en el mismo paso. Validacion humana antes de continuar. | M2, M5 | Humano (valida y corrige clasificacion) |
| C. Reparto y gestion | Recomendacion de entidad competente mediante matriz tipo mas sub-tema. Si es la Defensoria, el sistema sugiere ruta interna segun carga y perfil. Bandejas de trabajo con indicadores de tiempo por segmento y alertas automaticas. | M3, M7 | Humano (confirma competencia y asignacion) |
| D. Gestion defensorial | Asistente generativo con arquitectura RAG que consulta normativa, jurisprudencia y plantillas antes de redactar. El profesional siempre revisa, edita y firma. Alertas de patrones de riesgo para elevacion inmediata a prioridad. | M6, M5 | Humano (revisa, edita, firma) |
| E. Cierre | Sincronizacion simultanea del estado final en IRIS y VisionWeb con bitacora de trazabilidad. Consolidacion del expediente y alimentacion de dashboards de analitica. | M7, M8 | Humano (inicia el cierre) |

Las decisiones que nunca se automatizan son: evaluacion de competencia de la entidad (M3), priorizacion final de casos de riesgo vital (M2 y M6), respuesta de fondo al peticionario (M6 solo redacta borrador), correccion de errores de deduplicacion (M4) y cierre del caso (M7). En todos estos puntos la IA asiste o sugiere; la decision vinculante la toma exclusivamente un humano.

### 4.3 Mapeo problema a solucion

| Problema critico | Modulo(s) | Como lo resuelve |
|---|---|---|
| Volumen y saturacion (~300/dia) | M1, M2, M6 | Automatiza recepcion, extraccion de datos y clasificacion. El profesional pasa de digitar a supervisar. |
| Riesgo juridico por falta de priorizacion | M2, M3 | Score de urgencia (1 a 5) con reglas auditables, deteccion automatica de sujetos de especial proteccion, SLAs visibles con alertas. |
| Doble registro IRIS/VisionWeb | M7 | Capa de orquestacion con modelo canonico: unico punto de entrada, sincronizacion bidireccional simultanea, bitacora de cada operacion. |
| Duplicidad de peticiones | M4 | Comparacion semantica mediante embeddings y cosine similarity. Si la similitud supera el 85% y coinciden CC y pretension, el sistema sugiere acumulacion al profesional. |
| Peticionarios sin historial | M5 | Indice unificado Elasticsearch. Historial completo del ciudadano consultable por cedula en menos de 500ms. |

### 4.4 Alcance del piloto en URAB

El piloto se implementa en la URAB de Bogota (unas 300 peticiones/dia, 8 a 10 profesionales, 8 semanas de operacion controlada en la Fase 3). Entran en el piloto los modulos M1, M2, M3, M4, M5 y M6 con validacion humana en todos los puntos de decision (par. 5.4), M7 con integracion minima IRIS/VisionWeb requerida por par. 4.2, y M8 con el Dashboard 1 de carga tematica. Se difieren al escalamiento progresivo: otras Unidades de Analisis fuera de Bogota, la integracion con Carpeta Ciudadana Digital (gov.co) como componente opcional de M7 (el Banco de Preguntas indica que el proponente puede proponer un mecanismo de acuse de recibo y consulta de estado), y la foliacion electronica con firma de indice bajo estandares AGN, ofrecida como diferenciador a partir de par. 4.3 y la gestion documental de par. 5.1 (Banco Q8: no es requisito minimo). Las metricas y obligaciones de la Fase 3 se comprometen en el piloto URAB; la analitica institucional se habilita sobre los datos del piloto y se extiende con el escalamiento.

Criterios de salida del piloto: precision de clasificacion mayor o igual a 90%, recall de urgencias/riesgo vital mayor o igual a 99%, deteccion de duplicados mayor o igual a 85% recall, tiempo de ingreso a asignacion de maximo 4h (p90), disponibilidad del sistema mayor o igual a 99.5% mensual. Si la precision cae por debajo de 75% no se escala sin reentrenar.

> Diagrama TO-BE completo, flujo detallado por etapa y tabla de decisiones no automatizables: Anexo 04.

---

## 5. Arquitectura tecnica de la solucion (~4 pags)

### 5.1 Decision de arquitectura: nube corporativa con capa de orquestacion

La solucion se despliega sobre una plataforma corporativa en nube para la administracion de agentes de inteligencia artificial, operada por el contratista o un proveedor autorizado bajo los lineamientos de seguridad, administracion y gobernanza definidos por la Defensoria del Pueblo. Esta modalidad es la alternativa mas adecuada por cuatro razones:

**Orquestacion unificada de modelos.** La plataforma permite usar, versionar y administrar al mismo tiempo distintos modelos de IA (los desarrollados especificamente para la Defensoria, como BETO fine-tuned para clasificacion y modelos NER propios, y modelos fundacionales de terceros como Mistral 7B para generacion de borradores y Sentence-Transformers para embeddings semanticos), todo bajo un mismo marco corporativo de seguridad, control de accesos y trazabilidad de ejecuciones.

**Delegacion de infraestructura.** Los requerimientos de infraestructura, mantenimiento, seguridad fisica, escalabilidad automatica y soporte tecnico permanente se delegan en el contratista o proveedor autorizado. Esto libera a la Defensoria de la carga operativa de administrar servidores, actualizar dependencias, escalar recursos ante picos de demanda y mantener la continuidad del servicio. El contratista asume los niveles de servicio (SLA) de disponibilidad mayor o igual a 99.5%, tiempo de respuesta de API menor a 500ms (p95) y recuperacion ante desastres con RPO de 24h o menos y RTO de 4h o menos.

**Integracion y sincronizacion optimizadas.** El despliegue en nube ofrece mejores condiciones de conectividad, disponibilidad y latencia para la integracion con IRIS y VisionWeb, y para la sincronizacion bidireccional mediante la capa de orquestacion con modelo canonico de datos. Los eventos de ciclo de vida del caso (creado, actualizado, cerrado) se publican en colas de mensajeria cloud-native que garantizan la entrega y la trazabilidad de cada sincronizacion hacia los sistemas legados.

**Proteccion de datos bajo modelo contractual.** En materia de tratamiento de datos personales (Ley 1581 de 2012), la plataforma opera bajo un modelo de proteccion definido contractualmente: la Defensoria es la responsable del tratamiento y el contratista actua como encargado con instrucciones documentadas. Los datos se procesan dentro de un entorno empresarial controlado, con cifrado AES-256 en reposo y TLS 1.3 en transito, acceso segmentado por roles RBAC, y logs inmutables de auditoria. La URAB establece lineamientos para la anonimizacion de los datos usados en procesos de entrenamiento, despliegue y aprendizaje de modelos, de modo que estos se gestionen solo para los fines misionales de la organizacion y no esten disponibles para terceros.

Frente al problema de IRIS vs. VisionWeb (dos sistemas sin comunicacion entre si, par. 2.4.3, y par. 4.2 que exige evitar dobles registros), la capa de orquestacion opera sobre la infraestructura cloud manteniendo un registro unico con modelo canonico de datos y sincronizacion bidireccional. Esta decision cumple con par. 4.2 (evitar doble registro), reduce el riesgo del par. 2.4.3 (archivo en una sola plataforma), y alimenta la trazabilidad requerida por par. 5.4. Si los sistemas legados no ofrecen API de escritura (Banco Q10), se despliega RPA como capa de contingencia.

### 5.2 Arquitectura logica

```
[ Capa de acceso ]       Bandejas URAB . Bandejas profesionales . Dashboards (M8)
                         Acceso web seguro (HTTPS/TLS 1.3) . Autenticacion OAuth2/JWT
...............................................................................
[ Capa de orquestacion ] API Gateway cloud-native . Message Broker . Workflow ingreso a cierre
                         Bitacora inmutable . Orquestador de modelos de IA
...............................................................................
[ Plataforma de agentes de IA en nube corporativa ]
    o Motor M2: Clasificacion y triaje (BETO fine-tuned)
    o Motor M4: Anti-duplicacion (Sentence-Transformers + cosine similarity)
    o Motor M6: Asistente generativo RAG (ChromaDB + Mistral 7B)
    o Motor M5: Historial unificado (Elasticsearch)
    o Motor M1: OCR (Tesseract) + NER (spaCy)
    o Administracion: versionamiento, monitoreo, drift, feedback loop
...............................................................................
[ Modelo canonico de datos ] PostgreSQL + pgvector (cloud-managed)
...............................................................................
[ Capa de integracion ] Conectores a IRIS . VisionWeb . gov.co (opcional)
                        RPA como contingencia
...............................................................................
[ Seguridad transversal cloud ] RBAC . OAuth2/JWT . TLS 1.3 . AES-256
                                Logs inmutables . WAF . DDoS protection . Backup automatico
```

### 5.3 Stack tecnologico y plataforma de agentes de IA

La plataforma cloud corporativa permite la administracion unificada de los siguientes modelos y servicios. El detalle completo de cada tecnologia (justificacion, licencia, alternativas evaluadas y criterios de seleccion) esta en el Anexo 05.

| Capa | Tecnologia | Funcion |
|---|---|---|
| Plataforma cloud | Infraestructura como Servicio (IaaS) o Plataforma como Servicio (PaaS) corporativa | Orquestacion de todos los agentes de IA, administracion de versiones, monitoreo, escalabilidad |
| Backend / API | FastAPI (Python) | Gateway de servicios, endpoints REST documentados (OpenAPI 3.0) |
| Clasificacion NLP | BETO (dccuchile/bert-base-spanish-wwm-uncased) fine-tuned | Clasificacion primaria (4 categorias) y sub-clasificacion multi-etiqueta (~12 sub-temas) |
| Extraccion de entidades | spaCy (es_core_news_lg) + fine-tuning | NER: extrae nombre, CC, direccion, pretension, entidad referida |
| Similitud semantica | Sentence-Transformers (paraphrase-multilingual-mpnet-base-v2) | Embeddings 768-dim para comparacion de significados en deteccion de duplicados |
| LLM generativo | Mistral 7B (Instruct v0.2), ejecutado en la nube corporativa | Asistente RAG: generacion de borradores de respuesta |
| RAG | LangChain + ChromaDB | Recuperacion de normativa y jurisprudencia, generacion controlada |
| OCR | Tesseract LSTM (spa) + OpenCV | Conversion de documentos escaneados a texto |
| BD transaccional + vectorial | PostgreSQL + pgvector (cloud-managed) | Almacenamiento canonico e indices vectoriales para busqueda semantica |
| Busqueda textual | Elasticsearch (cloud-managed) | Indice de historial unificado por ciudadano |
| Mensajeria | RabbitMQ (cloud-managed) o equivalente cloud-native | Publicacion y consumo de eventos de sincronizacion IRIS/VisionWeb |
| MLOps | MLflow + DVC + Evidently AI | Versionamiento de modelos y datos, monitoreo de drift y rendimiento |
| Dashboard | Streamlit (piloto), Power BI (produccion) | Visualizacion de metricas operativas, calidad y equidad |

Todos los modelos de IA usados son de codigo abierto con licencias permisivas (MIT, Apache 2.0), lo que permite su uso, modificacion y despliegue sin costos de licenciamiento. La plataforma cloud corporativa administra las distintas versiones de estos modelos, tanto los desarrollados por el contratista como los modelos fundacionales de terceros, bajo un mismo marco de seguridad, control de acceso y gobernanza.

### 5.4 Descripcion funcional de modulos

> Las especificaciones tecnicas detalladas de cada modulo (pipeline completo, componentes internos, tecnologias, metricas de rendimiento, modelo de datos, contratos de API y plan de pruebas) estan en el Anexo 05. A continuacion se describe la funcion de cada modulo y su contribucion al macroproceso.

**M1: Recepcion Inteligente.** Recibe peticiones por todos los canales, aplica OCR a documentos escaneados o fotografiados, extrae automaticamente los datos del ciudadano mediante NER, verifica completitud de campos obligatorios (nombre, documento de identidad, descripcion del hecho, pretension) y genera radicado unico. Si se detectan datos faltantes, el sistema responde al ciudadano pidiendo la informacion complementaria con plantillas institucionales. **Metrica objetivo:** tasa de extraccion correcta de entidades mayor o igual a 90%.

**M2: Clasificacion y Triaje.** Clasifica la peticion en las 4 categorias juridicas mediante un modelo BETO con fine-tuning. Un sub-clasificador multi-etiqueta asigna los sub-temas aplicables. Un sistema de reglas deterministico y auditable, no de caja negra, asigna nivel de urgencia en escala 1 a 5 segun los criterios juridicos del equipo de Derecho. Un priorizador cruza el texto con el catalogo de sujetos de especial proteccion constitucional y marca flags de alerta. El profesional de URAB valida o corrige toda clasificacion. **Metrica objetivo:** accuracy mayor o igual a 90%, recall en urgencias/riesgo vital mayor o igual a 99% (umbral asimetrico).

**M3: Asignacion y Enrutamiento.** Determina la entidad competente mediante matriz de reglas tipo mas sub-tema (alimentada y validada por Derecho). Si la Defensoria es competente, recomienda ruta interna segun carga y perfil del profesional. Bandejas de trabajo con estados y monitoreo de SLA (ingreso a asignacion en menos de 4h, gestion a cierre en maximo 15 dias habiles) con alertas automaticas al 80% y 100% del plazo. **Metrica objetivo:** tiempo de ingreso a asignacion de 15 minutos o menos en el 90% de los casos.

**M4: Anti-Duplicacion.** Convierte el texto de la peticion en un embedding semantico de 768 dimensiones y lo compara via cosine similarity contra los casos existentes en la base de datos. Si la similitud supera el 85% y coinciden el documento de identidad y la pretension del ciudadano, el sistema sugiere acumulacion al profesional mediante una interfaz que muestra ambas peticiones lado a lado con los campos coincidentes resaltados. El profesional decide con justificacion escrita. **Metrica objetivo:** precision de sugerencias mayor o igual a 85%, recall de duplicados mayor o igual a 90%.

**M5: Peticionarios Recurrentes.** Indice Elasticsearch que permite consultar por numero de cedula el historial completo de peticiones de un ciudadano (radicados, fechas, tipos, estados, profesionales asignados, respuestas emitidas) en menos de 500ms. El sistema sugiere ademas respuestas previas y plantillas institucionales aplicables al caso. **Metrica objetivo:** tiempo de consulta menor a 500ms (p95).

**M6: Asistente Generativo (RAG + LLM).** Opera en dos modos. Para consultas complejas, el sistema recupera fragmentos relevantes de la base de conocimiento (normativa, jurisprudencia, plantillas institucionales, respuestas previas anonimizadas) mediante ChromaDB, los inyecta en un prompt con instrucciones estrictas (no inventar, lenguaje ciudadano, no decidir) y Mistral 7B, ejecutandose en la nube corporativa, genera un borrador. El profesional siempre revisa, edita y firma. Para consultas simples del catalogo previamente aprobado por Derecho (estado del radicado, profesional asignado, reenvio de constancia), el sistema responde con plantillas sin pasar por el LLM. M6 incorpora ademas un detector de patrones de riesgo en tiempo real (amenazas, desapariciones, menores en peligro, VBG) que notifica al profesional y dispara alertas en el dashboard. **Metrica objetivo:** borradores aceptados sin correccion mayor en al menos 70% de los casos, tiempo de generacion menor a 10s.

**M7: Interoperabilidad.** Elimina la doble digitacion. El nuevo sistema es el unico punto de entrada de peticiones. Cada evento de ciclo de vida se publica en el message broker cloud y dos consumidores independientes replican a IRIS y VisionWeb al mismo tiempo. Reintentos con backoff exponencial ante fallos (1s, 2s, 4s, 8s, 16s, 32s). Tras 6 fallos, alerta al administrador. RPA como contingencia si los sistemas legados no ofrecen API de escritura. Bitacora inmutable de cada sincronizacion. Conciliacion diaria automatica entre los tres sistemas. **Metrica objetivo:** sincronizacion exitosa mayor o igual a 99.5%.

**M8: Analitica.** Cuatro dashboards que transforman datos operativos en informacion para la toma de decisiones: (1) carga tematica (distribucion por tipo, tendencias, top 10 sub-temas), (2) cuellos de botella (tiempos por etapa, carga por profesional, casos vencidos), (3) recurrencia y duplicidad, (4) equidad (desagregada por genero, region y grupo de especial proteccion, con alertas de disparidad). Incluye una capa de investigacion institucional con datos anonimizados (k-anonymity mayor o igual a 5) y acceso restringido a rol investigador previa aprobacion del Comite de IA. **Metrica objetivo:** dashboards actualizados en tiempo real, latencia menor a 1 minuto desde el evento.

### 5.5 Seguridad, MLOps y pruebas

**Seguridad y proteccion de datos (par. 4.5).** El modelo de seguridad opera bajo el esquema de responsabilidad compartida de la plataforma cloud corporativa: el proveedor cloud garantiza la seguridad fisica, de red y de virtualizacion; el contratista implementa los controles a nivel de aplicacion y datos. Cuatro roles de acceso (RBAC): URAB, Profesional defensorial, Auditor y Administrador. Este ultimo no tiene acceso a logs de auditoria, segun el principio de minimo privilegio. Autenticacion OAuth2/JWT sin estado. Cifrado TLS 1.3 en transito y AES-256 en reposo. Logs inmutables (append-only) con backup automatico diario a almacenamiento externo. Plan de contingencia ante indisponibilidad de IRIS/VisionWeb con cola de mensajes local y acuse diferido al ciudadano. El contratista garantiza contractualmente la anonimizacion de los datos utilizados en entrenamiento, despliegue y aprendizaje de modelos, operando dentro de un entorno empresarial controlado y disponible unicamente para la Defensoria.

**MLOps (par. 4.6).** Versionamiento integral: Git (codigo), DVC (datasets etiquetados), MLflow Model Registry (modelos con metricas, parametros y artefactos). Monitoreo de drift de datos y predicciones mediante Evidently AI con reportes automaticos. Canal de retroalimentacion humana: API donde los profesionales reportan errores de clasificacion; esos datos etiquetados alimentan el siguiente ciclo de reentrenamiento. Politica de actualizacion controlada: solicitud, evaluacion tecnica, aprobacion del Comite de IA, staging, produccion con changelog. Los modelos nunca se actualizan sin aprobacion explicita.

**Plan de pruebas.** Pruebas unitarias (cada componente aislado), de integracion (flujos M1 a M4 a M2 a M3 y M7 a IRIS/VisionWeb), de aceptacion (profesionales URAB con casos reales), de equidad (Equal Opportunity, Demographic Parity y False Negative Rate segmentados), de carga (simulacion de 300 peticiones/dia con picos de 500), y de seguridad (pentesting, revision TLS, simulacion de indisponibilidad).

> Especificaciones tecnicas completas M1 a M8, stack tecnologico detallado, modelo de datos, arquitectura de seguridad, MLOps y plan de pruebas: Anexo 05.

---

## 8. Cambio sociotecnico, enfoque diferencial y pruebas de equidad (~1.5 pags)

### 8.1 Cambio sociotecnico (par. 5.3)

La introduccion de IA en el macroproceso de la Defensoria transforma la forma de trabajo de los funcionarios y la interaccion de los ciudadanos con la institucion. La siguiente tabla recoge las nuevas capacidades, las conductas que se habilitan, los impactos disruptivos y las decisiones de gobernanza que los mitigan:

| Capacidad nueva | Conducta que cambia | Riesgo a anticipar | Decision de gobernanza |
|---|---|---|---|
| Lectura y clasificacion masiva (~300 peticiones/dia en minutos) | El profesional pasa de clasificar manualmente a supervisar la IA. Dedica mas tiempo a casos complejos que a tareas repetitivas. | Sobre-automatizacion: tentacion de delegar decisiones que requieren juicio humano (priorizacion, competencia). | Lista taxativa de decisiones nunca automatizables (par. 4.2). Human-in-the-loop obligatorio en todos los puntos de decision. |
| Vista unificada del historial por ciudadano (M5) | Atender peticionarios recurrentes con contexto completo en segundos. Respuestas mas coherentes y personalizadas entre distintas interacciones. | Privacidad por concentracion de historial: todos los casos de un ciudadano visibles en un solo punto. | Principio de minimizacion: solo se muestra lo necesario para el caso actual. Roles de acceso diferenciados. Consentimiento informado. |
| Borradores de respuesta generados por IA (M6) | Redactar respuestas en minutos en lugar de horas. El profesional edita y personaliza en lugar de empezar desde cero. | Confianza excesiva en la IA: omitir la revision humana obligatoria, asumir que el borrador es correcto. | Revision y firma humana registrada en logs inmutables. UI con friccion deliberada (confirmacion explicita, tiempo minimo de visualizacion). |
| Monitoreo y analitica en tiempo real (M8) | Visibilizar patrones de carga, cuellos de botella y disparidades entre grupos poblacionales que antes eran invisibles. | Datos agregados que podrian amplificar barreras o estigmatizar grupos si se usan sin contexto. | Enfoque diferencial en dashboards. Privacidad (k-anonymity mayor o igual a 5). Reportes publicos de equidad. |
| Interoperabilidad IRIS/VisionWeb (M7) | Eliminar la doble digitacion. Un solo registro, dos plataformas actualizadas al mismo tiempo. | Resistencia al cambio organizacional. Posible percepcion de redundancia del nuevo sistema. | Gestion de cambio desde Fase 0, alineada con MIPG e ISO/IEC 42001:2023. Capacitacion minima de 20 profesionales (par. 6.1). |

La estrategia de gestion de cambio incluye sesiones de sensibilizacion sobre IA en el sector publico, manuales de rol con procedimientos claros, y mesa de ayuda durante el piloto y los primeros seis meses de operacion (par. 6.4).

### 8.2 Pruebas de equidad algoritmica (par. 5.2)

En el contexto de la Defensoria del Pueblo, cuya mision constitucional es proteger los derechos humanos de toda la poblacion con enfasis en los grupos mas vulnerables, un sesgo algoritmico no es un error tecnico: es una vulneracion del derecho fundamental a la igualdad (Art. 13 CP). La solucion incorpora pruebas de equidad como gate de calidad obligatorio antes de cada despliegue.

**Metricas utilizadas.** Equal Opportunity (diferencia en tasa de aciertos positivos entre grupos), Demographic Parity (diferencia en proporcion de predicciones entre grupos), Disparate Impact Ratio (cociente entre el grupo con peor y mejor rendimiento, debe ser mayor a 0.80), y False Negative Rate por grupo (el error mas grave: omitir un caso urgente mas en unos grupos que en otros).

**Segmentacion.** Genero (solo cuando el ciudadano lo proporciona voluntariamente, nunca inferido), regional/departamento, grupo de especial proteccion (NNA, mujeres VBG, discapacidad, adultos mayores, desplazados, minorias etnicas, poblacion privada de libertad, migrantes), y canal de ingreso. Si una muestra tiene menos de 30 casos, esa segmentacion no se reporta.

**Niveles de alerta y protocolo de actuacion:**

| Disparidad detectada | Accion |
|---|---|
| Menos de 3% de diferencia entre grupos | Verde. Aceptable. Monitoreo continuo. |
| 3 a 5% o diferencia de precision mayor a 5 puntos entre subgrupos | Amarillo. Revision tecnica. Analisis de causas. No detiene despliegue. |
| 5 a 10% o cociente de falsos negativos mayor a 1.5 | Naranja. Escalar al Comite de IA en 5 dias. Activar mitigacion: rebalanceo de datos, threshold tuning o adversarial debiasing. Detener despliegue para el grupo afectado. |
| Mas de 10% de diferencia | Rojo. Suspender el modulo para todos los grupos. Investigacion urgente. Notificar al Defensor Delegado. |

**Salvaguardas institucionales.** Validacion manual de todos los rechazos automaticos, revision de casos de riesgo vital exclusivamente por un funcionario, formatos accesibles para personas con discapacidad, prohibicion absoluta de automatizar decisiones de fondo.

> Protocolo completo de pruebas de equidad: Anexo 08 (definiciones formales de metricas, niveles de alerta con ejemplo numerico, 4 estrategias de mitigacion, plan de monitoreo continuo por variable, gate de despliegue).

---

## 9. Matriz de riesgos: SPI, corrupcion y dano antijuridico (par. 5.5) (~1 pag)

Se identifican 12 riesgos en tres familias: T (tecnica), O (operacional) y J (juridica). La matriz completa con probabilidad, impacto, causa raiz, efecto detallado, responsable y evidencia de control esta en el Anexo 09 (basada en Matriz_SGIA_ISO42001.xlsx hoja "2. Matriz SGIA").

| ID | F. | Riesgo | Mitigacion principal | Monitoreo |
|---|---|---|---|---|
| R1 | T | Caida de conectividad o indisponibilidad de IRIS/VisionWeb que genera represamiento (par. 2.4.2) | Colas resilientes cloud, modo offline con acuse diferido, plan de contingencia documentado | Semanal |
| R2 | T | Error de integracion: doble registro o archivo en una sola plataforma (par. 2.4.3) | Modelo canonico + sincronizacion bidireccional + conciliacion diaria automatica | Diaria |
| R3 | T | Falso negativo en clasificacion de urgencias: no deteccion de riesgo vital | Umbral asimetrico calibrado para recall mayor o igual a 99%, revision humana de casos sin flag, reentrenamiento ante cualquier fallo | Diaria |
| R4 | T | Falso positivo en deduplicacion: acumulacion inadecuada de casos diferentes | Umbral 85% configurable + coincidencia CC + pretension. Justificacion escrita obligatoria del profesional | Semanal |
| R5 | T/O | Sesgo algoritmico que amplifica exclusiones (genero, discapacidad, juventud, etnia) | Pruebas de equidad pre-despliegue, 4 niveles de alerta con protocolo graduado, adversarial debiasing | Cada release + trimestral |
| R6 | O | Dependencia excesiva del sistema, perdida de supervision humana (par. 5.4) | Lista taxativa de decisiones nunca automatizables. Human-in-the-loop obligatorio. UI con friccion en puntos criticos | Semanal |
| R7 | O | Omisiones o uso indebido por profesionales (carga incorrecta, falta de revision) | Capacitacion desde Fase 0 con certificacion, roles con minimo privilegio, auditoria de actividad | Mensual |
| R8 | J | Incumplimiento de terminos legales (CPACA, Ley 1755/2015, derecho de peticion) | Dashboards M8 con semaforizacion, alertas M3 al 80% y 100% del plazo, escalamiento en cadena | Diaria |
| R9 | J | Vulneracion de privacidad o tratamiento inadecuado de datos sensibles (Ley 1581/2012) | Defensoria como responsable, contratista como encargado con instrucciones contractuales. AES-256 + TLS 1.3 + anonimizacion. Evaluacion de impacto (AIA) | Trimestral |
| R10 | J | Falta de trazabilidad algoritmica (Directiva Conjunta 007/2025) | Ficha de Transparencia Algoritmica alineada con NIST AI RMF 1.0. Logs inmutables con registro de cada decision | Trimestral |
| R11 | T/O | Alucinacion del LLM generando informacion falsa en respuesta oficial | Arquitectura RAG: solo genera sobre documentos reales de ChromaDB. Revision humana obligatoria. Solo D5 automatico. | Semanal |
| R12 | T | Incidente de ciberseguridad con exposicion de datos sensibles [antecedente DOC_1] | Seguridad cloud bajo responsabilidad compartida. RBAC + OAuth2 + cifrado + pentesting + equipo de respuesta | Mensual |

> Matriz de riesgos completa: Anexo 09. Incluye probabilidad, impacto, causa raiz, efecto detallado, evidencia de control y responsable para cada riesgo.

---

## 10. Plan de trabajo por fases y entregables (par. 6) (~1 pag)

El proyecto se organiza en 5 fases secuenciales con criterios de salida verificables, desplegadas sobre la plataforma cloud corporativa. Duracion total: 32 semanas de ejecucion mas 12 meses de garantia y evolucion [validar].

| Fase | Duracion | Objetivo | Entregables clave | Criterio de aceptacion |
|---|---|---|---|---|
| F0. Alistamiento y diagnostico | 4 sem | Diagnosticar el AS-IS y preparar los datos | Flujograma validado, dataset etiquetado (~1000 casos), taxonomia, linea base de metricas, configuracion inicial del entorno cloud | Diagnostico y taxonomia aprobados por el comite del proyecto |
| F1. Diseno de arquitectura e integracion | 8 sem | Definir la arquitectura cloud y la estrategia de integracion con IRIS/VisionWeb | Arquitectura objetivo, diagrama de integracion, modelo canonico de datos, especificacion de seguridad cloud, diseno de la plataforma de agentes de IA | Arquitectura validada con equipos de sistemas legados |
| F2. Construccion de modulos IA | 12 sem | Desarrollar, entrenar y probar los modulos core en el entorno cloud | Prototipos M1 a M6 desplegados en cloud de desarrollo. Informe de desempeno sobre conjunto gold. Pruebas de equidad superadas | Metricas segun metas (par. 12). Sin disparidad mayor a 5% en equidad |
| F3. Implementacion, capacitacion y operacion inicial | 8 sem | Desplegar el piloto en produccion cloud, capacitar y operar en modo supervisado | Sistema en produccion, 100% profesionales capacitados, dashboards M8, mesa de ayuda, informe comparativo sistema vs. manual | Metricas del piloto en umbrales. Satisfaccion mayor o igual a 80% |
| F4. Gobernanza y mejora continua | 12+ meses | Operacion autonoma, transferencia y evolucion controlada | Comite de IA operando, reportes periodicos de metricas y equidad, transferencia de conocimiento al equipo interno | Equipo interno autonomo por 3+ meses. Auditoria sin hallazgos criticos |

**Modelo de costos de referencia** [validar]: aproximadamente $1.135 M COP a 3 anos, con la infraestructura cloud como servicio gestionado por el contratista incluida en el rubro de infraestructura y operacion. Presupuesto discriminado en Anexo 10. Pago por hitos verificables, no por tiempo.

> Plan de trabajo detallado: Anexo 10 (actividades semana a semana, carta Gantt, presupuesto por rubro y fase, hitos de pago).

---

## 12. Metricas y linea base del piloto (par. 4.4) (~1 pag)

La linea base se levanta durante la Fase 0. Actualmente no existen mediciones automatizadas; el Banco Q18 confirma que el proceso tarda varios dias y no se mide formalmente. Los valores AS-IS son estimaciones basadas en el caso que deben refinarse con los datos reales del diagnostico [validar].

| Num. | Indicador | Linea base (est.) | Meta piloto | Umbral de alerta | Frecuencia |
|---|---|---|---|---|---|
| M1 | Tiempo de clasificacion sugerida (M2) | Varias horas a 2 dias (manual, sin medicion) | 15 min o menos en 90% (p90) | p90 mayor a 30 min | Diaria |
| M2 | Precision de clasificacion, accuracy (M2) | ~80% (humano, con fatiga) | 90% o mas global; 90% o mas subclasificacion | menor a 85% o caida mayor a 3 puntos | Semanal |
| M3 | Recall de urgencias / riesgo vital (M2) | No medido | 99% o mas (falso negativo cercano a cero) | Cualquier FN real | Diaria |
| M4 | Precision de sugerencias de duplicados (M4) | No hay sistema | 85% o mas | menor a 70% | Semanal |
| M5 | Recall de duplicados (M4) | menor a 30% (muestreo manual) | 90% o mas | menor a 80% | Semanal |
| M6 | Reduccion de reprocesos de reparto | Linea base F0 | 50% o mas de reduccion | menor a 20% | Mensual |
| M7 | Cumplimiento de tiempos internos | No robusto | 90% o mas de peticiones en plazo | menor a 80% | Mensual |
| M8 | Tiempo ingreso a asignacion (M3) | ~2 dias habiles | 4h o menos en 90% (p90) | Desvio mayor a +50% | Semanal |
| M9 | Tiempo ingreso a primera respuesta | 15 a 20 dias habiles | 10 dias habiles o menos en 90% (p90) | mayor a 15 dias | Mensual |
| M10 | Extraccion correcta de entidades (M1) | ~70 a 80% (digitacion manual) | 90% o mas campos obligatorios | menor a 85% | Semanal |
| M11 | Borradores M6 sin correccion mayor | No aplica | 90% o mas consultas simples | Conflictivas mayor a 5% | Semanal |
| M12 | Disponibilidad del sistema | No aplica | 99.5% o mas mensual | menor a 99% | Tiempo real |
| M13 | Sincronizacion IRIS/VisionWeb (M7) | 0% (sin integracion) | 99.5% o mas | menor a 99% | Tiempo real |
| M14 | Tasa de error en OCR (M1) | No medido | menor a 5% docs limpios, menor a 10% baja calidad | mayor a 10% / mayor a 15% | Semanal |
| M15 | Equal Opportunity por genero (M2) | No medido | menor a 5% de diferencia | mayor a 5% | Trimestral |
| M16 | Disparate Impact Ratio | No medido | mayor a 0.80 | menor a 0.80 | Trimestral |
| M17 | Satisfaccion del profesional URAB | No aplica | 80% o mas (encuesta trimestral) | menor a 70% | Trimestral |

**Metodologia de umbral asimetrico para riesgo vital.** El costo de un falso negativo en casos de riesgo vital (desapariciones, amenazas, menores en peligro, VBG activa) no es comparable al de un falso positivo: el primero implica dano antijuridico y vulneracion de derechos fundamentales (par. 2.4.2 mas par. 5.5); el segundo representa un costo operativo manejable (revision adicional de unos 15 minutos). El clasificador M2 se calibra durante la Fase 2 con un conjunto gold etiquetado por juristas de la URAB, ajustando el umbral de decision para alcanzar una sensibilidad (recall) mayor o igual a 99% en la clase "riesgo vital", aceptando un incremento controlado de falsos positivos como costo operativo. Si se produce algun falso negativo de esta clase, se activa revision inmediata, analisis de causa raiz y reentrenamiento.

> Metricas detalladas: Anexo 12 (definicion operativa con formula de cada indicador, plan de medicion con herramientas, responsables y dashboards, metodologia completa de umbral asimetrico con ejemplo numerico calibrado).

---

*Borrador preparado por el equipo de Ciencia de Datos para integracion en el documento de fase escrita. Las secciones en el cuerpo ocupan ~10 paginas en formato Arial 12, espacio sencillo, margenes 1.5 cm. El detalle completo se encuentra en los Anexos 04, 05, 08, 09, 10 y 12.*

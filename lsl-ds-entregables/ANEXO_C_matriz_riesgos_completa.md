# Anexo C — Matriz de riesgos completa

> **Referenciado desde:** §9 del borrador principal.
> **Base:** `Matriz_SGIA_ISO42001.xlsx` (hoja "2. Matriz SGIA").

---

## R1 — Fallo de conectividad o indisponibilidad de IRIS/VisionWeb

| Campo | Valor |
|---|---|
| **ID** | R1 |
| **Familia** | T (Técnica) |
| **Riesgo** | Caída de conectividad o indisponibilidad de IRIS o VisionWeb que impide la sincronización y genera represamiento (§2.4.2) |
| **Probabilidad** | Media |
| **Impacto** | Alto |
| **Causa raíz** | Fallo de infraestructura de los sistemas legados, corte de red, mantenimiento no programado, ataque DDoS contra infraestructura externa |
| **Efecto** | Las peticiones siguen ingresando por el nuevo sistema pero no se sincronizan con IRIS/VisionWeb. Se acumula una cola de eventos pendientes. Si la caída se prolonga, los profesionales de otras áreas que solo usan IRIS no ven los casos nuevos. Riesgo de pérdida de trazabilidad si el sistema propio también falla antes de sincronizar. |
| **Mitigación** | Colas resilientes con persistencia en disco (RabbitMQ). Modo offline del sistema propio: sigue operando sin degradación. Acuse de recibo diferido al ciudadano. Plan de contingencia documentado con roles y tiempos de respuesta. Conciliación diaria automática que detecta y repara cualquier inconsistencia post-recuperación. |
| **Evidencia** | Logs de RabbitMQ (estado de colas, mensajes pendientes), bitácora de sincronización M7, dashboard de estado de integración en tiempo real |
| **Responsable** | Equipo de Infraestructura + Equipo Técnico (M7) |
| **Monitoreo** | Semanal (revisión de incidentes) + tiempo real (dashboard) |

---

## R2 — Error de integración: doble registro o archivo en una sola plataforma

| Campo | Valor |
|---|---|
| **ID** | R2 |
| **Familia** | T (Técnica) |
| **Riesgo** | Un caso queda registrado en un sistema pero no en el otro, o se duplica, violando §4.2 y el riesgo del §2.4.3 |
| **Probabilidad** | Media |
| **Impacto** | Medio |
| **Causa raíz** | Error en el mapeo de campos del modelo canónico, cambio no notificado en la API de IRIS/VisionWeb, timeout que deja el caso en estado indeterminado, bug en el consumidor de RabbitMQ |
| **Efecto** | Inconsistencia entre los tres sistemas. Un profesional que consulta IRIS ve un estado diferente al que ve en VisionWeb. Retrabajo manual para corregir. Riesgo de que un caso se archive en una plataforma pero quede abierto en la otra (§2.4.3). |
| **Mitigación** | Modelo canónico con mapeo de campos documentado y versionado. Sincronización bidireccional: el estado maestro está en el nuevo sistema; IRIS y VisionWeb son réplicas. Conciliación diaria automática: compara estados entre los tres sistemas y genera alerta ante cualquier discrepancia. Pruebas de integración con mocks de ambas APIs en CI/CD. |
| **Evidencia** | Bitácora de sincronización M7 (cada evento con timestamp, destino, payload, response), reportes de conciliación diaria, tests de integración en CI |
| **Responsable** | Equipo Técnico (M7) |
| **Monitoreo** | Diaria (conciliación automática) + tiempo real (dashboard M7) |

---

## R3 — Falso negativo en clasificación de urgencias

| Campo | Valor |
|---|---|
| **ID** | R3 |
| **Familia** | T (Técnica) |
| **Riesgo** | El clasificador M2 no detecta un caso de riesgo vital (desaparición, amenaza, niñez en peligro, VBG activa), el caso se encola como rutinario y el ciudadano sufre un perjuicio grave por la demora |
| **Probabilidad** | Baja (con umbral asimétrico calibrado) |
| **Impacto** | Crítico |
| **Causa raíz** | Redacción atípica de la petición que el modelo no reconoce como urgente. Palabras clave de riesgo expresadas de forma indirecta o en dialecto regional. Dataset de entrenamiento con subrepresentación de casos de riesgo vital en ciertas regiones o grupos. |
| **Efecto** | Daño antijurídico por omisión. Vulneración de derechos fundamentales (vida, integridad, libertad). Posible responsabilidad patrimonial del Estado (CP art. 90). Acciones de tutela contra la Defensoría. Pérdida de confianza en el sistema. |
| **Mitigación** | Umbral asimétrico: el clasificador se calibra para recall ≥99% en la clase "riesgo vital", aceptando un incremento de falsos positivos (que generan revisiones adicionales pero no daño). Conjunto gold etiquetado por juristas de URAB en Fase 0. Revisión humana de todos los casos sin flag de urgencia en las primeras 4 horas. Reentrenamiento inmediato ante cualquier falso negativo real. |
| **Evidencia** | Dataset gold etiquetado y versionado (DVC). Métricas diarias de recall por clase de urgencia. Protocolo documentado de actuación ante falso negativo. |
| **Responsable** | Equipo MLOps + Profesional URAB (revisión humana) |
| **Monitoreo** | Diaria (métricas recall urgencias) + inmediata (ante cualquier FN real detectado) |

---

## R4 — Falso positivo en deduplicación

| Campo | Valor |
|---|---|
| **ID** | R4 |
| **Familia** | T (Técnica) |
| **Riesgo** | El sistema sugiere acumular dos peticiones que en realidad son de ciudadanos diferentes o tratan asuntos distintos, fragmentando o mezclando casos incorrectamente |
| **Probabilidad** | Media |
| **Impacto** | Medio |
| **Causa raíz** | Alta similitud textual entre peticiones de naturaleza diferente (ej: dos quejas sobre salud en la misma EPS pero de personas distintas). Error en la extracción del número de documento por el NER. Umbral de similitud demasiado bajo. |
| **Efecto** | Si el profesional acepta la acumulación errónea: dos casos distintos se tratan como uno solo, uno de los ciudadanos no recibe respuesta. Si la rechaza correctamente: pérdida de tiempo del profesional, desconfianza en el sistema. |
| **Mitigación** | Umbral configurable (85% por defecto, ajustable con registro de cambio). Regla de coincidencia reforzada: mismo CC (extraído por NER y verificado) + misma pretensión. UI de decisión con vista lado a lado y campos coincidentes resaltados. Profesional debe justificar por escrito cada aceptación o rechazo. Bitácora de decisión M4 auditable. |
| **Evidencia** | Bitácora de acumulación M4 (profesional, timestamp, similitud, decisión, motivo). Métricas semanales de precisión/recall de sugerencias. |
| **Responsable** | Profesional URAB (decisión) + Equipo Técnico (calibración del umbral) |
| **Monitoreo** | Semanal |

---

## R5 — Sesgo algorítmico que amplifica exclusiones

| Campo | Valor |
|---|---|
| **ID** | R5 |
| **Familia** | T/O (Técnica/Operacional) |
| **Riesgo** | El modelo M2 (y potencialmente M4 y M6) tiene un desempeño sistemáticamente peor para ciertos grupos poblacionales (mujeres, población rural, minorías étnicas, personas con discapacidad, población LGBTIQ+), vulnerando el derecho a la igualdad (Art. 13 CP) |
| **Probabilidad** | Media |
| **Impacto** | Alto |
| **Causa raíz** | Dataset de entrenamiento que no representa adecuadamente la diversidad de la población colombiana. Patrones lingüísticos, dialectos y formas de expresión diferentes entre grupos. Sesgos históricos en los datos de entrenamiento originales de BETO. |
| **Efecto** | Ciudadanos de grupos vulnerables reciben peor servicio: sus quejas se clasifican incorrectamente, se subestima su urgencia, se generan peores borradores de respuesta. Esto equivale a una denegación de acceso a la justicia por origen o condición. Viola el enfoque diferencial exigido en §5.2. Genera responsabilidad estatal y deslegitima el sistema. |
| **Mitigación** | Pruebas de equidad obligatorias antes de cada despliegue (gate de calidad). 4 niveles de alerta con acciones graduadas. Estrategias técnicas: rebalanceo del dataset, threshold tuning por grupo, adversarial debiasing, revisión humana reforzada para grupos con sesgo detectado. Reportes públicos de equidad como transparencia algorítmica. |
| **Evidencia** | Reportes trimestrales de Evidently AI (métricas por subgrupo). Actas del Comité de IA. Dataset de entrenamiento documentado con distribución por variables demográficas (cuando disponibles). |
| **Responsable** | Equipo MLOps (medición) + Comité de IA (decisión) |
| **Monitoreo** | Cada release + trimestral (automático con Evidently AI) |

---

## R6 — Dependencia excesiva del sistema

| Campo | Valor |
|---|---|
| **ID** | R6 |
| **Familia** | O (Operacional) |
| **Riesgo** | Los profesionales delegan excesivamente en la IA, aprueban borradores sin revisar, aceptan clasificaciones sin verificar, y se pierde el juicio humano crítico que exige §5.4 |
| **Probabilidad** | Media |
| **Impacto** | Alto |
| **Causa raíz** | Presión por volumen de casos. Confianza excesiva en el sistema por buen desempeño inicial. Fatiga de revisión. Diseño de UI que facilita la aprobación sin fricción. |
| **Efecto** | Decisiones automatizadas de facto sin supervisión humana significativa. Violación del debido proceso (CP art. 29) y de los requisitos de §5.4. Respuestas erróneas enviadas a ciudadanos. |
| **Mitigación** | Lista taxativa de decisiones NUNCA automatizables (incluida en §4.2 del borrador principal). UI con fricción deliberada en puntos críticos: confirmación explícita, justificación escrita obligatoria, tiempo mínimo de visualización del borrador antes de poder aprobar. Logs inmutables de revisión humana. Capacitación desde Fase 0 sobre los límites de la IA. |
| **Evidencia** | Logs de revisión humana (timestamp de apertura del borrador, timestamp de aprobación, tiempo de revisión, ediciones realizadas). Registro de firmas. |
| **Responsable** | Profesional defensorial (responsabilidad individual) + URAB (supervisión) |
| **Monitoreo** | Semanal (tiempos de revisión, tasa de aprobación sin edición) |

---

## R7 — Omisiones o uso indebido por profesionales

| Campo | Valor |
|---|---|
| **ID** | R7 |
| **Familia** | O (Operacional) |
| **Riesgo** | Profesionales cometen errores al cargar información manualmente, omiten revisar borradores, o usan el sistema para fines no autorizados |
| **Probabilidad** | Media |
| **Impacto** | Medio |
| **Causa raíz** | Capacitación insuficiente, fatiga, error humano, desconocimiento de procedimientos |
| **Efecto** | Datos incorrectos en el sistema, respuestas erróneas o incompletas, posible violación de privacidad si se accede a casos sin autorización |
| **Mitigación** | Capacitación obligatoria desde Fase 0 con certificación. Manuales de rol con procedimientos paso a paso. Principio de mínimo privilegio: cada rol accede solo a lo necesario. Auditoría de actividad por usuario con alertas de patrones anómalos. Mesa de ayuda disponible durante todo el piloto. |
| **Evidencia** | Plan de capacitación documentado. Registros de acceso y actividad por usuario. Tickets de mesa de ayuda. |
| **Responsable** | URAB (capacitación y supervisión) + Equipo Técnico (controles de acceso) |
| **Monitoreo** | Mensual |

---

## R8 — Incumplimiento de términos legales por retraso

| Campo | Valor |
|---|---|
| **ID** | R8 |
| **Familia** | J (Jurídica) |
| **Riesgo** | Las peticiones no se responden dentro de los términos establecidos por el CPACA y la Ley 1755 de 2015, violando el derecho de petición (CP art. 23) |
| **Probabilidad** | Baja (con el sistema) |
| **Impacto** | Alto |
| **Causa raíz** | Cuello de botella en una etapa del flujo, sobrecarga de un profesional, caso complejo que excede el tiempo estimado, falla del sistema que retrasa la asignación |
| **Efecto** | Violación del derecho fundamental de petición. Silencio administrativo negativo. Posibles acciones de tutela. Responsabilidad disciplinaria del funcionario. |
| **Mitigación** | Tableros M8 con semaforización de tiempos (verde/amarillo/rojo). Alertas automáticas M3 al 80% y 100% del plazo. Escalamiento en cadena: profesional → superior → URAB → Defensor Delegado. Responsable definido por caso. Priorización automática de casos próximos a vencer. |
| **Evidencia** | Indicadores M3 y M8 (tiempos por etapa, tasa de cumplimiento). Registro de alertas y escalamientos. |
| **Responsable** | Profesional defensorial (gestión) + M3/M8 (monitoreo) |
| **Monitoreo** | Diaria (dashboard M8, alertas automáticas) |

---

## R9 — Vulneración de privacidad de datos sensibles

| Campo | Valor |
|---|---|
| **ID** | R9 |
| **Familia** | J (Jurídica) |
| **Riesgo** | Tratamiento inadecuado de datos sensibles (salud, niñez, VBG, desaparición, origen étnico, orientación sexual) en violación de la Ley 1581 de 2012 |
| **Probabilidad** | Baja |
| **Impacto** | Crítico |
| **Causa raíz** | Acceso no autorizado a datos sensibles por rol mal configurado. Datos sensibles visibles en logs o dashboards sin anonimizar. Uso de datos para fines distintos a la misión constitucional. Fuga por vulnerabilidad de seguridad. |
| **Efecto** | Violación del régimen de protección de datos personales. Sanciones de la Superintendencia de Industria y Comercio (multas de hasta 2.000 SMLMV). Acciones de hábeas data. Pérdida irreversible de confianza ciudadana. Riesgo para la seguridad física de víctimas si sus datos quedan expuestos. |
| **Mitigación** | Defensoría = responsable del tratamiento, proveedor = encargado con instrucciones documentadas. Cifrado AES-256 en reposo + TLS 1.3 en tránsito. Evaluación de impacto en protección de datos (AIA) integrada al plan de pruebas de equidad (Anexo F). Minimización: solo se recolectan los datos necesarios para la misión. Prohibición contractual de usos secundarios. Notificación obligatoria de brechas de seguridad a la SIC. |
| **Evidencia** | AIA documentada. Registros de consentimiento/autorización. Logs de acceso a datos sensibles. Cláusula contractual de tratamiento de datos. |
| **Responsable** | Oficial de Protección de Datos + Oficial de Seguridad de la Información |
| **Monitoreo** | Trimestral (auditoría de protección de datos) |

---

## R10 — Falta de trazabilidad algorítmica

| Campo | Valor |
|---|---|
| **ID** | R10 |
| **Familia** | J (Jurídica) |
| **Riesgo** | Imposibilidad de explicar cómo el sistema llegó a una decisión automatizada, incumpliendo la Directiva Conjunta 007 de 2025 sobre transparencia algorítmica |
| **Probabilidad** | Baja |
| **Impacto** | Medio |
| **Causa raíz** | Logs insuficientes o no estructurados. Falta de documentación del comportamiento del modelo. Imposibilidad de reconstruir el contexto de una decisión específica. |
| **Efecto** | Incumplimiento normativo (Directiva 007/2025). Imposibilidad de auditoría. Deslegitimación del sistema ante cuestionamientos ciudadanos o judiciales. |
| **Mitigación** | Ficha de Transparencia Algorítmica de diseño propio para cada sistema automatizado (M2, M4, M6), alineada con la Directiva 007/2025 y el marco NIST AI RMF 1.0 (Q9). Logs inmutables (append-only) con trazabilidad completa: dado un caso, se puede reconstruir exactamente qué datos entraron, qué predijo el modelo, con qué confianza, y quién tomó la decisión final. Registro de explicación en lenguaje natural para cada decisión automatizada. |
| **Evidencia** | Fichas de Transparencia por sistema (SDA). Logs de auditoría accesibles para el rol Auditor. |
| **Responsable** | Comité de IA (aprobación de fichas) + Equipo Técnico (implementación de logs) |
| **Monitoreo** | Trimestral (auditoría de transparencia algorítmica) |

---

## R11 — Alucinación del LLM en respuesta oficial

| Campo | Valor |
|---|---|
| **ID** | R11 |
| **Familia** | T/O (Técnica/Operacional) |
| **Riesgo** | El asistente generativo M6 (Mistral 7B) genera información falsa, cita normativa inexistente o toma posición de fondo en un borrador que, sin revisión adecuada, se envía al ciudadano |
| **Probabilidad** | Baja (con arquitectura RAG + revisión humana) |
| **Impacto** | Crítico |
| **Causa raíz** | Naturaleza probabilística de los LLM (generan texto estadísticamente probable, no factualmente correcto). Base de conocimiento incompleta o desactualizada. Profesional que aprueba sin revisar (ver R6). |
| **Efecto** | Respuesta oficial con información jurídicamente incorrecta o inventada. Desinformación al ciudadano. Posible perjuicio jurídico. Responsabilidad disciplinaria y patrimonial. Pérdida de credibilidad institucional. |
| **Mitigación** | Arquitectura RAG: el LLM solo genera basándose en documentos reales recuperados de ChromaDB (no "de memoria"). Prompt con instrucción explícita: "NO inventes información. Si no hay base suficiente, indícalo explícitamente. NO tomes decisiones vinculantes." Revisión humana obligatoria registrada en logs. Solo el catálogo D5 se responde automáticamente (sin LLM). Temperature baja (0.3) para reducir creatividad/alucinación. |
| **Evidencia** | Bitácora de respuestas generadas: prompt completo, respuesta cruda del LLM, respuesta final tras edición, profesional responsable, timestamp. |
| **Responsable** | Profesional defensorial (revisión y firma) + Equipo Técnico (RAG y prompt engineering) |
| **Monitoreo** | Semanal (revisión de bitácora, tasa de rechazo de borradores) |

---

## R12 — Incidente de ciberseguridad

| Campo | Valor |
|---|---|
| **ID** | R12 |
| **Familia** | T (Técnica) |
| **Riesgo** | Ataque informático que compromete la confidencialidad, integridad o disponibilidad del sistema y los datos personales que contiene |
| **Probabilidad** | Baja |
| **Impacto** | Crítico |
| **Causa raíz** | Vulnerabilidad no detectada en dependencias, configuración insegura, ataque de phishing a funcionarios, insider threat, explotación de día cero |
| **Efecto** | Exposición masiva de datos personales y sensibles. Paralización del sistema. Pérdida de datos. Sanciones legales y reputacionales. El antecedente del incidente de ciberseguridad de noviembre de 2025 [DOC_1] demuestra que este riesgo es real y material. |
| **Mitigación** | Controles de acceso (RBAC + OAuth2/JWT + MFA). Cifrado TLS 1.3 + AES-256. Monitoreo continuo de actividad con alertas de anomalías. Equipo de respuesta a incidentes con protocolo documentado (detección, contención, erradicación, recuperación, lecciones aprendidas). Pruebas de penetración y red teaming periódicas. Análisis de vulnerabilidades (SCA/SAST) en CI/CD. Capacitación anti-phishing para todo el personal. |
| **Evidencia** | Reportes de pentest, simulacros de incidentes, plan de respuesta documentado, registros de parches y actualizaciones de seguridad. |
| **Responsable** | Oficial de Seguridad de la Información + Equipo de Infraestructura |
| **Monitoreo** | Continuo (monitoreo de seguridad) + Mensual (revisión de vulnerabilidades) |

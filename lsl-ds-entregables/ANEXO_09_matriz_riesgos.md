# Anexo 09 — Matriz de riesgos completa

> **Referenciado desde:** §9 del cuerpo del documento.
> **Base:** `Matriz_SGIA_ISO42001.xlsx`.

---

## R1 — Caída de conectividad o indisponibilidad de IRIS/VisionWeb

| Campo | Valor |
|---|---|
| **ID** | R1 |
| **Familia** | T (Técnica) |
| **Probabilidad** | Media |
| **Impacto** | Alto |
| **Causa raíz** | Fallo de infraestructura de sistemas legados, corte de red, mantenimiento no programado, ataque DDoS |
| **Efecto** | Peticiones ingresan al nuevo sistema pero no se sincronizan. Cola de eventos pendientes. Si la caída se prolonga, profesionales de otras áreas que solo usan IRIS no ven casos nuevos. |
| **Mitigación** | Colas resilientes cloud con persistencia. Modo offline del sistema propio sin degradación. Acuse diferido al ciudadano. Plan de contingencia documentado. Conciliación diaria automática. |
| **Evidencia** | Logs del message broker, bitácora M7, dashboard de integración en tiempo real |
| **Responsable** | Equipo de Infraestructura + Equipo Técnico (M7) |
| **Monitoreo** | Semanal + tiempo real |

---

## R2 — Error de integración: doble registro o archivo en una sola plataforma

| Campo | Valor |
|---|---|
| **ID** | R2 |
| **Familia** | T (Técnica) |
| **Probabilidad** | Media |
| **Impacto** | Medio |
| **Causa raíz** | Error en mapeo de campos del modelo canónico, cambio no notificado en API externa, timeout que deja caso en estado indeterminado |
| **Efecto** | Inconsistencia entre sistemas. Retrabajo manual. Riesgo de archivo en una sola plataforma (§2.4.3). |
| **Mitigación** | Modelo canónico versionado. Sincronización bidireccional. Conciliación diaria automática. Tests de integración en CI/CD con mocks de ambas APIs. |
| **Evidencia** | Bitácora M7, reportes de conciliación, tests de integración |
| **Responsable** | Equipo Técnico (M7) |
| **Monitoreo** | Diaria |

---

## R3 — Falso negativo en clasificación de urgencias

| Campo | Valor |
|---|---|
| **ID** | R3 |
| **Familia** | T (Técnica) |
| **Probabilidad** | Baja (con umbral asimétrico) |
| **Impacto** | Crítico |
| **Causa raíz** | Redacción atípica, palabras de riesgo expresadas indirectamente o en dialecto regional, subrepresentación de casos de riesgo vital en el dataset |
| **Efecto** | Daño antijurídico por omisión. Vulneración de derechos fundamentales (vida, integridad). Responsabilidad patrimonial (CP art. 90). Acciones de tutela. |
| **Mitigación** | Umbral asimétrico calibrado para recall ≥99%. Conjunto gold etiquetado por juristas URAB en F0. Revisión humana de casos sin flag en 4h. Reentrenamiento inmediato ante cualquier FN real. |
| **Evidencia** | Dataset gold versionado (DVC), métricas diarias de recall, protocolo documentado de actuación |
| **Responsable** | Equipo MLOps + Profesional URAB |
| **Monitoreo** | Diaria + inmediata ante FN real |

---

## R4 — Falso positivo en deduplicación

| Campo | Valor |
|---|---|
| **ID** | R4 |
| **Familia** | T (Técnica) |
| **Probabilidad** | Media |
| **Impacto** | Medio |
| **Causa raíz** | Alta similitud textual entre casos distintos. Error en NER del CC. Umbral demasiado bajo. |
| **Efecto** | Casos distintos acumulados erróneamente → un ciudadano no recibe respuesta. O rechazo correcto → pérdida de tiempo, desconfianza. |
| **Mitigación** | Umbral 85% configurable + coincidencia CC + pretensión. UI side-by-side con campos resaltados. Justificación escrita obligatoria. Bitácora auditable. |
| **Evidencia** | Bitácora M4, métricas semanales de precisión/recall |
| **Responsable** | Profesional URAB + Equipo Técnico |
| **Monitoreo** | Semanal |

---

## R5 — Sesgo algorítmico que amplifica exclusiones

| Campo | Valor |
|---|---|
| **ID** | R5 |
| **Familia** | T/O (Técnica/Operacional) |
| **Probabilidad** | Media |
| **Impacto** | Alto |
| **Causa raíz** | Dataset no representativo de la diversidad colombiana. Patrones lingüísticos diferenciados. Sesgos históricos en datos de BETO. |
| **Efecto** | Grupos vulnerables reciben peor servicio. Denegación de acceso a la justicia por origen o condición. Viola enfoque diferencial (§5.2). |
| **Mitigación** | Pruebas de equidad pre-despliegue (gate obligatorio). 4 niveles de alerta. Rebalanceo, threshold tuning, adversarial debiasing. Revisión humana reforzada. |
| **Evidencia** | Reportes trimestrales Evidently AI, actas del Comité de IA, dataset documentado con distribución demográfica |
| **Responsable** | Equipo MLOps + Comité de IA |
| **Monitoreo** | Cada release + trimestral |

---

## R6 — Dependencia excesiva del sistema

| Campo | Valor |
|---|---|
| **ID** | R6 |
| **Familia** | O (Operacional) |
| **Probabilidad** | Media |
| **Impacto** | Alto |
| **Causa raíz** | Presión por volumen, confianza excesiva, fatiga de revisión, UI que facilita aprobación sin fricción |
| **Efecto** | Decisiones automatizadas de facto sin supervisión humana (§5.4). Violación del debido proceso. Respuestas erróneas enviadas. |
| **Mitigación** | Lista taxativa de decisiones NUNCA automatizables (§A04.4). UI con fricción deliberada. Logs de revisión humana. Capacitación desde F0. |
| **Evidencia** | Logs de revisión (tiempos, ediciones), registro de firmas |
| **Responsable** | Profesional defensorial + URAB |
| **Monitoreo** | Semanal |

---

## R7 — Omisiones o uso indebido por profesionales

| Campo | Valor |
|---|---|
| **ID** | R7 |
| **Familia** | O (Operacional) |
| **Probabilidad** | Media |
| **Impacto** | Medio |
| **Causa raíz** | Capacitación insuficiente, fatiga, error humano, desconocimiento de procedimientos |
| **Efecto** | Datos incorrectos en el sistema, respuestas erróneas, posible violación de privacidad |
| **Mitigación** | Capacitación obligatoria con certificación. Manuales de rol. Principio de mínimo privilegio. Auditoría de actividad por usuario. Mesa de ayuda. |
| **Evidencia** | Plan de capacitación, registros de acceso, tickets de mesa de ayuda |
| **Responsable** | URAB + Equipo Técnico |
| **Monitoreo** | Mensual |

---

## R8 — Incumplimiento de términos legales

| Campo | Valor |
|---|---|
| **ID** | R8 |
| **Familia** | J (Jurídica) |
| **Probabilidad** | Baja (con el sistema) |
| **Impacto** | Alto |
| **Causa raíz** | Cuello de botella en una etapa, sobrecarga de profesional, caso complejo, falla del sistema |
| **Efecto** | Violación del derecho de petición (CP art. 23). Silencio administrativo negativo. Tutela. Responsabilidad disciplinaria. |
| **Mitigación** | Dashboards M8 con semaforización. Alertas M3 al 80% y 100%. Escalamiento en cadena. Priorización de casos próximos a vencer. |
| **Evidencia** | Indicadores M3/M8, registro de alertas y escalamientos |
| **Responsable** | Profesional defensorial + M3/M8 |
| **Monitoreo** | Diaria |

---

## R9 — Vulneración de privacidad de datos sensibles

| Campo | Valor |
|---|---|
| **ID** | R9 |
| **Familia** | J (Jurídica) |
| **Probabilidad** | Baja |
| **Impacto** | Crítico |
| **Causa raíz** | Acceso no autorizado por rol mal configurado, datos visibles en logs sin anonimizar, fuga por vulnerabilidad, uso para fines no misionales |
| **Efecto** | Violación Ley 1581/2012. Sanciones SIC (hasta 2.000 SMLMV). Hábeas data. Pérdida irreversible de confianza. Riesgo físico para víctimas. |
| **Mitigación** | Defensoría = responsable, contratista = encargado contractual. AES-256 + TLS 1.3. Evaluación de impacto (AIA). Anonimización en entrenamiento. Prohibición contractual de usos secundarios. |
| **Evidencia** | AIA documentada, registros de consentimiento, logs de acceso a datos sensibles, cláusula contractual |
| **Responsable** | Oficial de Protección de Datos + Oficial de Seguridad |
| **Monitoreo** | Trimestral |

---

## R10 — Falta de trazabilidad algorítmica

| Campo | Valor |
|---|---|
| **ID** | R10 |
| **Familia** | J (Jurídica) |
| **Probabilidad** | Baja |
| **Impacto** | Medio |
| **Causa raíz** | Logs insuficientes, falta de documentación del modelo, imposibilidad de reconstruir contexto de una decisión |
| **Efecto** | Incumplimiento Directiva 007/2025. Imposibilidad de auditoría. Deslegitimación ante cuestionamientos judiciales. |
| **Mitigación** | Ficha de Transparencia Algorítmica (Directiva 007 + NIST AI RMF 1.0). Logs inmutables con trazabilidad completa. Registro de explicación de cada decisión automatizada. |
| **Evidencia** | Fichas SDA, logs de auditoría |
| **Responsable** | Comité de IA + Equipo Técnico |
| **Monitoreo** | Trimestral |

---

## R11 — Alucinación del LLM en respuesta oficial

| Campo | Valor |
|---|---|
| **ID** | R11 |
| **Familia** | T/O |
| **Probabilidad** | Baja (con RAG + revisión humana) |
| **Impacto** | Crítico |
| **Causa raíz** | Naturaleza probabilística de LLMs. Base de conocimiento incompleta. Profesional omite revisión (ver R6). |
| **Efecto** | Respuesta oficial con información falsa o normativa inventada. Perjuicio jurídico al ciudadano. Responsabilidad disciplinaria y patrimonial. |
| **Mitigación** | Arquitectura RAG: solo genera sobre documentos reales de ChromaDB. Prompt anti-alucinación. Revisión humana obligatoria. Solo D5 automático (sin LLM). Temperature 0.3. |
| **Evidencia** | Bitácora de respuestas: prompt, respuesta cruda LLM, respuesta final editada, profesional, timestamp |
| **Responsable** | Profesional defensorial + Equipo Técnico |
| **Monitoreo** | Semanal |

---

## R12 — Incidente de ciberseguridad

| Campo | Valor |
|---|---|
| **ID** | R12 |
| **Familia** | T (Técnica) |
| **Probabilidad** | Baja |
| **Impacto** | Crítico |
| **Causa raíz** | Vulnerabilidad en dependencias, configuración insegura, phishing, insider threat, día cero. El incidente de nov-2025 [DOC_1] demuestra que el riesgo es material. |
| **Efecto** | Exposición masiva de datos personales y sensibles. Paralización del sistema. Sanciones legales y reputacionales. |
| **Mitigación** | Seguridad cloud bajo responsabilidad compartida. RBAC + OAuth2 + MFA. TLS 1.3 + AES-256. WAF. Pentesting y red teaming periódicos. Equipo de respuesta a incidentes. SCA/SAST en CI/CD. Capacitación anti-phishing. |
| **Evidencia** | Reportes de pentest, simulacros, plan de respuesta, registros de parches |
| **Responsable** | Oficial de Seguridad + Equipo de Infraestructura |
| **Monitoreo** | Continuo + mensual |

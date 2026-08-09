# Especificaciones técnicas, Ciencia de Datos

## 4. Modelo TO-BE y alcance del piloto (diseño técnico viable)

El macroproceso descrito en el caso (§2.3) presenta cinco problemas estructurales que los módulos M1–M8 (§3) atacan directamente: (1) saturación operativa por clasificación manual, (2) falta de priorización de casos de riesgo vital, (3) doble digitación IRIS/VisionWeb, (4) duplicidad de peticiones no detectada, y (5) ausencia de historial unificado por ciudadano.

El TO-BE propuesto automatiza las tareas repetitivas y mantiene al profesional como decisor final en cada etapa (§5.4):

| Etapa | AS-IS (cf. §2.3) | TO-BE | Mód. | Decisión humana |
|---|---|---|---|---|
| A. Recepción | Ingreso multicanal sin normalizar, radicado manual | OCR + NER extraen datos, validan completitud, generan radicado semiautomático | M1 | Validación de datos extraídos |
| B. Triage | Clasificación manual sin criterios uniformes ni historial | BETO fine-tuned clasifica tipo, sub-tema y urgencia (1–5); priorizador detecta sujetos de especial protección; M5 muestra historial | M2, M5 | Validación/corrección de clasificación |
| C. Reparto | Asignación manual, doble registro IRIS/VisionWeb | M3 recomienda entidad y ruta; M7 sincroniza simultáneamente; SLAs con alertas al 80% y 100% | M3, M7 | Confirmación de competencia y ruta |
| D. Gestión | Sin apoyo documental, redacción desde cero | M6 (RAG) genera borrador sobre normativa recuperada de ChromaDB; profesional edita y firma | M6, M5 | Revisión, edición y firma |
| E. Cierre | Archivo con riesgo en una sola plataforma (§2.4.3) | M7 sincroniza simultáneamente IRIS y VisionWeb con bitácora inmutable; M8 alimenta dashboards | M7, M8 | Verificación e inicio del cierre |

La IA nunca decide en estos puntos: competencia de la entidad (M3), priorización final de riesgo vital (M2/M6), respuesta de fondo (M6 solo redacta borrador), corrección de duplicación (M4) y cierre del caso (M7). El fundamento jurídico de cada uno:

| Decisión | La IA | El humano | Fundamento |
|---|---|---|---|
| Competencia (M3) | Sugiere según matriz D4 | Confirma entidad | CP art. 29 |
| Priorización riesgo vital (M2/M6) | Asigna score y flag | Determina prioridad final | CP arts. 11–12 |
| Respuesta de fondo (M6) | Redacta borrador vía RAG | Revisa, edita, firma | CP arts. 23, 29 |
| Corrección duplicación (M4) | Sugiere acumulación si ≥85% | Decide y justifica por escrito | Seguridad jurídica |
| Archivo y cierre (M7/M8) | Sincroniza en IRIS/VisionWeb | Verifica e inicia cierre | Ley 594/2000 |

### 4.1 Mapeo problema → solución

| Problema | Mód. | Mecanismo |
|---|---|---|
| Volumen y saturación | M1, M2, M6 | Automatiza recepción, extracción y clasificación |
| Falta de priorización | M2, M3 | Score de urgencia (1–5) con reglas auditables, detección de sujetos de especial protección, SLAs con alertas |
| Doble registro IRIS/VisionWeb | M7 | Capa de orquestación con modelo canónico, sincronización bidireccional, bitácora inmutable |
| Duplicidad de peticiones | M4 | Embeddings semánticos + cosine similarity ≥85% + coincidencia CC + pretensión |
| Sin historial unificado | M5 | Elasticsearch, consulta por cédula <500ms |

### 4.2 Alcance del piloto

Piloto en URAB Bogotá: 8 semanas de operación controlada (Fase 3), 8–10 profesionales. Módulos incluidos: M1–M6 con validación humana, M7 con integración mínima IRIS/VisionWeb (§4.2), M8 con Dashboard 1 (carga temática). Diferidos al escalamiento: otras regionales, Carpeta Ciudadana Digital (gov.co, componente opcional de M7 según Banco de Preguntas), foliación electrónica bajo AGN (diferenciador, Q8).

Criterios de salida: precisión ≥90%, recall urgencias ≥99%, recall duplicados ≥85%, ingreso→asignación ≤4h (p90), disponibilidad ≥99.5% mensual. Precisión <75% detiene el escalamiento sin reentrenar.

---

## 5. Arquitectura técnica de la solución

### 5.1 Decisión de arquitectura

La solución se despliega sobre una plataforma corporativa en nube para administración de agentes de IA, operada por el contratista. Esto permite: (i) orquestar bajo un mismo marco de seguridad los modelos desarrollados (BETO fine-tuned, spaCy NER) y los fundacionales de terceros (Mistral 7B, Sentence-Transformers); (ii) delegar infraestructura, mantenimiento y escalabilidad al contratista, con SLA de disponibilidad ≥99.5%, latencia API <500ms (p95), RPO≤24h y RTO≤4h; (iii) operar la integración con IRIS y VisionWeb mediante colas de mensajería cloud-native con trazabilidad de cada sincronización; y (iv) proteger los datos bajo el modelo contractual de la Ley 1581/2012: Defensoría responsable, contratista encargado con instrucciones documentadas, cifrado AES-256 + TLS 1.3, RBAC, logs inmutables y anonimización de datos de entrenamiento.

La capa de orquestación mantiene un registro único con modelo canónico de datos y sincronización bidireccional, resolviendo el problema de doble registro (§2.4.3, §4.2). Si los sistemas legados no ofrecen API de escritura (Q10), se despliega RPA como contingencia.

### 5.2 Arquitectura lógica

```
[ Capa de acceso ] Bandejas URAB · Bandejas profesionales · Dashboards (M8)
 HTTPS/TLS 1.3 · OAuth2/JWT
──────────────────────────────────────────────────────────────
[ Capa de orquestación ] API Gateway · Message Broker · Workflow ingreso→cierre · Bitácora
──────────────────────────────────────────────────────────────
[ Plataforma de agentes de IA en nube corporativa ]
 ● M2: Clasificación y triaje (BETO fine-tuned)
 ● M4: Anti-duplicación (Sentence-Transformers + cosine similarity)
 ● M6: Asistente generativo RAG (ChromaDB + Mistral 7B)
 ● M5: Historial unificado (Elasticsearch)
 ● M1: OCR (Tesseract) + NER (spaCy)
 ● Administración: versionamiento, monitoreo, drift, feedback loop
──────────────────────────────────────────────────────────────
[ Modelo canónico de datos ] PostgreSQL + pgvector (cloud-managed)
──────────────────────────────────────────────────────────────
[ Integración ] Conectores → IRIS · VisionWeb · gov.co (opcional) · RPA
──────────────────────────────────────────────────────────────
[ Seguridad transversal ] RBAC · OAuth2/JWT · TLS 1.3 · AES-256 · WAF · Logs inmutables
```

### 5.3 Stack tecnológico

| Capa | Tecnología | Justificación | Licencia |
|---|---|---|---|
| Cloud | IaaS/PaaS corporativa (AWS/Azure/GCP o GovCloud) | Orquestación de agentes IA, versionamiento, monitoreo, escalabilidad | Comercial |
| API | FastAPI (Python) ≥0.110 | Async, OpenAPI 3.0 automático, ecosistema IA nativo | MIT |
| Clasificación | BETO (dccuchile/bert-base-spanish-wwm-uncased) fine-tuned | Español, 110M params, WWM, probado en dominio legal | MIT |
| NER | spaCy (es_core_news_lg) + fine-tuning ≥3.7 | Pipeline NLP maduro en español, inferencia rápida | MIT |
| Embeddings | Sentence-Transformers (paraphrase-multilingual-mpnet-base-v2) | Similitud semántica, 50+ idiomas, 768-dim | Apache 2.0 |
| LLM | Mistral 7B (Instruct v0.2) | Mejor calidad/eficiencia en 7B, ejecución cloud sin exponer datos | Apache 2.0 |
| RAG | LangChain + ChromaDB | Framework estándar, BD vectorial ligera y embebible | MIT / Apache 2.0 |
| OCR | Tesseract LSTM (spa) + OpenCV | CER <5% docs limpios, sin costo | Apache 2.0 |
| BD | PostgreSQL 15+ + pgvector | Estándar sector público, transaccional + vectorial unificado | PostgreSQL |
| Búsqueda | Elasticsearch 8.x | <500ms, agregaciones, analizador español | Elastic 2.0 |
| Mensajería | RabbitMQ 3.12+ o cloud-native | ACK, persistencia, reintentos, DLQ | MPL 2.0 |
| MLOps | MLflow + DVC + Evidently AI | Versionamiento integral, drift, reportes de equidad | Apache 2.0 |
| Dashboard | Streamlit (piloto) → Power BI (prod) | Python puro, Power BI usado en sector público | Apache 2.0 / Microsoft |
| Seguridad | OAuth2/JWT + TLS 1.3 + AES-256 + WAF | Sin estado, cifrado estándar, protección web | IETF |


### 5.4 Módulos

M1, Recepción. OCR sobre escaneados, NER extrae campos obligatorios (nombre, CC, hecho, pretensión), validador detecta faltantes y responde al ciudadano, genera radicado URAB-YYYYMMDD-NNNNNN. Meta: extracción ≥90%.

M2, Clasificación y Triaje. BETO fine-tuned clasifica en 4 tipos; sub-clasificador multi-etiqueta asigna ~12 sub-temas; reglas determinísticas asignan urgencia 1–5; priorizador cruza con catálogo D3 de sujetos de especial protección. Profesional URAB valida todo. Meta: accuracy ≥90%, recall urgencias ≥99%.

M3, Asignación. Matriz tipo+sub-tema → entidad (D4). Bandejas con SLA: ingreso→asignación <4h, gestión→cierre <15dh. Alertas al 80% y 100%. Meta: ≤15 min en p90.

M4, Anti-Duplicación. Embedding 768-dim, cosine similarity, umbral 85% + mismo CC + misma pretensión. UI side-by-side. Profesional justifica por escrito. Meta: precisión ≥85%, recall ≥90%.

M5, Historial. Elasticsearch: GET /ciudadano/{cc}/historial <500ms. Sugiere respuestas previas + templates D6. Meta: <500ms p95.

M6, Asistente RAG. Modo RAG: ChromaDB recupera normativa y jurisprudencia, Mistral 7B genera borrador, profesional edita/firma. Modo automático D5: plantillas sin LLM para consultas simples. Detector de riesgo en tiempo real. Meta: aceptación ≥70%, generación <10s.

M7, Interoperabilidad. Único punto de entrada. Eventos al message broker, replicación simultánea a IRIS/VisionWeb. Backoff exponencial (1s–32s), 6 intentos máx. RPA si no hay API. Bitácora inmutable. Meta: sincronización ≥99.5%.

M8, Analítica. Dashboards: (1) carga temática, (2) cuellos de botella, (3) recurrencia/duplicidad, (4) equidad. Capa institucional con k-anonymity ≥5, acceso rol investigador. Meta: latencia <1 min.

### 5.5 Integración y seguridad

Modelo canónico: radicado ↔ numero_radicado (IRIS) ↔ codigo_expediente (VisionWeb); estado y profesional sincronizados bidireccionalmente. APIs bajo OpenAPI 3.0. Seguridad (§4.5): responsabilidad compartida cloud, RBAC (4 roles), OAuth2/JWT, TLS 1.3, AES-256, logs append-only con backup diario, contingencia offline con acuse diferido. MLOps (§4.6): Git + DVC + MLflow, Evidently AI para drift y equidad, feedback loop humano, actualización controlada con aprobación del Comité de IA. Pruebas: unitarias, integración, aceptación, equidad, carga (300/día, picos 500), seguridad.

---

## 8. Cambio sociotécnico, enfoque diferencial y pruebas de equidad

### 8.1 Cambio sociotécnico (§5.3)

| Capacidad | Conducta que cambia | Riesgo | Gobernanza |
|---|---|---|---|
| Clasificación masiva | De digitar a supervisar IA | Sobre-automatización | Lista taxativa de decisiones no automatizables (§4), human-in-the-loop |
| Historial unificado (M5) | Contexto completo en segundos | Concentración de datos personales | Minimización, roles diferenciados, consentimiento |
| Borradores IA (M6) | De redactar a editar | Confianza excesiva, omisión de revisión | Revisión y firma humana registrada, UI con fricción |
| Analítica en tiempo real (M8) | Patrones visibles antes invisibles | Datos agregados sin contexto | k-anonymity ≥5, dashboards con enfoque diferencial |
| Interoperabilidad (M7) | Sin doble digitación | Resistencia al cambio | Gestión de cambio desde F0, MIPG, ISO 42001, 20+ profesionales capacitados |

La gestión de cambio incluye sensibilización, manuales de rol y mesa de ayuda durante el piloto y seis meses posteriores (§6.4).

### 8.2 Pruebas de equidad algorítmica (§5.2)

Un sesgo en este contexto vulnera el derecho a la igualdad (CP art. 13). Las pruebas de equidad son gate obligatorio de despliegue.

**Métricas:** Equal Opportunity, Demographic Parity, Disparate Impact Ratio (>0.80), False Negative Rate por grupo. Segmentación por género (declarado voluntariamente), regional, grupo de especial protección y canal de ingreso. Muestras con <30 casos no se reportan.

**Protocolo de alerta:**

| Disparidad | Acción |
|---|---|
| <3% | Verde. Monitoreo continuo. |
| 3–5% | Amarillo. Revisión técnica, no detiene despliegue. |
| 5–10% o FN cociente >1.5 | Naranja. Comité de IA en 5 días. Mitigación. Detener para el grupo afectado. |
| >10% | Rojo. Suspensión total, notificar al Defensor Delegado. |

**Ejemplo:** evaluación trimestral con 5.000 peticiones. Accuracy hombres 91%, mujeres 84% (diferencia 7 pp → naranja). FNR urgencias 1.2% vs. 3.5% (cociente 2.92 → rojo). Se suspende M2 para urgencias en mujeres.

**Mitigación:** (1) rebalanceo del dataset (1–2 sem), (2) threshold tuning por grupo (2–3 días), (3) adversarial debiasing (2–4 sem), (4) doble revisión humana como contención inmediata.

**Monitoreo:** Evidently AI genera reportes trimestrales automáticos. El Comité de IA recibe reporte mensual específico de FNR para grupos de especial protección. Regla de despliegue: sin pruebas de equidad superadas (nivel verde, o amarillo con plan aprobado y fecha límite), no hay despliegue. Salvaguardas: validación manual de rechazos, riesgo vital solo por funcionario, formatos accesibles, prohibición de automatizar decisiones de fondo.

---

## 9. Matriz de riesgos (§5.5)

12 riesgos en tres familias: T (técnica), O (operacional), J (jurídica).

| ID | F. | Riesgo | Mitigación | Monit. |
|---|---|---|---|---|
| R1 | T | Caída IRIS/VisionWeb (§2.4.2) | Colas resilientes, modo offline, acuse diferido, plan de contingencia | Sem. |
| R2 | T | Doble registro (§2.4.3) | Modelo canónico + sincronización bidireccional + conciliación diaria | Diaria |
| R3 | T | FN en urgencias | Umbral asimétrico recall ≥99%, revisión humana, reentrenamiento inmediato | Diaria |
| R4 | T | FP en deduplicación | Umbral 85% + CC + pretensión, justificación escrita | Sem. |
| R5 | T/O | Sesgo algorítmico | Pruebas de equidad gate obligatorio, 4 niveles, adversarial debiasing | Rel. + Trim. |
| R6 | O | Dependencia excesiva (§5.4) | Lista de no automatizables, human-in-the-loop, UI con fricción | Sem. |
| R7 | O | Uso indebido | Capacitación certificada, mínimo privilegio, auditoría | Mensual |
| R8 | J | Incumplimiento de términos | Semaforización M8, alertas M3, escalamiento en cadena | Diaria |
| R9 | J | Privacidad datos sensibles (Ley 1581) | Responsable/encargado contractual, AES-256 + TLS 1.3, anonimización, AIA | Trim. |
| R10 | J | Trazabilidad (Dir. 007/2025) | Ficha Transparencia NIST AI RMF, logs inmutables | Trim. |
| R11 | T/O | Alucinación LLM | RAG sobre documentos reales, revisión humana, solo D5 automático | Sem. |
| R12 | T | Ciberseguridad [DOC_1] | Cloud responsabilidad compartida, RBAC, cifrado, pentesting, equipo respuesta | Mensual |

**Detalle crítico.** R3: probabilidad baja (umbral calibrado), impacto crítico. FN en riesgo vital = daño antijurídico por omisión, vulneración de derechos fundamentales, responsabilidad patrimonial (CP art. 90). Mitigado con conjunto gold de 200 casos etiquetados por juristas URAB y revisión humana en <4h. R5: probabilidad media, impacto alto. Equivale a denegación de acceso a la justicia. Mitigado con pruebas de equidad como gate y protocolo graduado de §8.2.

---

## 10. Plan de trabajo por fases (§6)

5 fases secuenciales, 32 semanas de ejecución + 12 meses de garantía [validar]. Despliegue sobre plataforma cloud corporativa.

| Fase | Dur. | Objetivo | Entregables clave | Criterio de aceptación |
|---|---|---|---|---|
| F0. Diagnóstico | 4 s | AS-IS y preparación de datos | Flujograma, dataset (~1000 casos), taxonomía, línea base, tenant cloud | Dataset ≥200/categoría, taxonomía validada |
| F1. Diseño | 8 s | Arquitectura e integración | Arquitectura objetivo, modelo canónico, seguridad cloud, diseño de agentes IA | Arquitectura validada con sistemas legados |
| F2. Construcción IA | 12 s | Desarrollo y pruebas de módulos | Prototipos M1–M6 en cloud dev, informe desempeño gold, equidad superada | Métricas ≥§12, sin disparidad >5% |
| F3. Implementación | 8 s | Piloto, capacitación, operación supervisada | Sistema en producción, 100% capacitados, dashboards, mesa de ayuda | Métricas en umbrales, satisfacción ≥80% |
| F4. Gobernanza | 12+ m | Autonomía, transferencia, evolución | Comité IA operando, reportes periódicos, transferencia al equipo interno | Autonomía ≥3 meses, auditoría limpia |

**Presupuesto a 3 años** [validar] (millones COP, cf. SECOP IA.xlsx):

| Rubro | Año 1 | Año 2 | Año 3 | Total |
|---|---|---|---|---|
| Implementación | $575 M | $60 M | $60 M | $695 M |
| Licencias | $0 | $0 | $0 | $0 |
| Infraestructura cloud | $125 M | $50 M | $50 M | $225 M |
| Capacitación | $55 M | $10 M | $10 M | $75 M |
| Evolución | $30 M | $50 M | $60 M | $140 M |
| **Total** | **$785 M** | **$170 M** | **$180 M** | **$1.135 M** |

Licencias $0: 100% stack open-source. 55% de inversión en año 1. Pago por hitos verificables (15% firma, 10% diagnóstico, 15% arquitectura, 25% módulos IA, 20% piloto, 10% 6 regionales, 5% transferencia).

---

## 12. Métricas y línea base del piloto (§4.4)

Línea base en Fase 0 (Q18: no hay mediciones automatizadas). Valores AS-IS estimados [validar].

| # | Indicador | Línea base | Meta piloto | Umbral alerta | Free. |
|---|---|---|---|---|---|
| M1 | Tiempo clasificación (M2) | Horas–2 días | ≤15 min p90 | p90 >30 min | Diaria |
| M2 | Accuracy (M2) | ~80% | ≥90% | <85% | Sem. |
| M3 | Recall urgencias (M2) | No medido | ≥99% | Cualquier FN | Diaria |
| M4 | Precisión duplicados (M4) | No hay | ≥85% | <70% | Sem. |
| M5 | Recall duplicados (M4) | <30% | ≥90% | <80% | Sem. |
| M6 | Reducción reprocesos | Línea F0 | ≥50% | <20% | Mensual |
| M7 | Cumplimiento tiempos | No sólido | ≥90% | <80% | Mensual |
| M8 | Ingreso→asignación (M3) | ~2 dh | ≤4h p90 | Desvío >+50% | Sem. |
| M9 | Ingreso→1.ª respuesta | 15–20 dh | ≤10 dh p90 | >15 dh | Mensual |
| M10 | Extracción entidades (M1) | ~70–80% | ≥90% | <85% | Sem. |
| M11 | Borradores aceptados (M6) | N/A | ≥90% | Conflictivas >5% | Sem. |
| M12 | Disponibilidad | N/A | ≥99.5% | <99% | T. real |
| M13 | Sincronización (M7) | 0% | ≥99.5% | <99% | T. real |
| M14 | Error OCR (M1) | No medido | <5% / <10% | >10% / >15% | Sem. |
| M15 | Equal Opp. género (M2) | No medido | <5% dif. | >5% | Trim. |
| M16 | Disparate Impact | No medido | >0.80 | <0.80 | Trim. |
| M17 | Satisfacción URAB | N/A | ≥80% | <70% | Trim. |

**Medición:** operativas (M1, M8, M9) en tiempo real vía logs → M8 Dashboard 2; calidad IA (M2–M5, M10, M11) semanal con MLflow + Evidently AI sobre conjunto gold y feedback; infraestructura (M12–M14) con Prometheus + Grafana; equidad (M15, M16) trimestral con Evidently AI; satisfacción (M17) con formulario al cierre.

**Umbral asimétrico.** Un FN en riesgo vital (desaparición, amenaza, menor en peligro, VBG) es daño antijurídico y vulneración de derechos fundamentales; un FP cuesta ~15 min de revisión. El clasificador M2 se calibra para maximizar recall a costa de FP controlados. Procedimiento: Fase 0, juristas URAB etiquetan ≥200 casos gold de riesgo vital. Fase 2, se ajusta el threshold hacia abajo hasta recall ≥99%.

| Escenario | Threshold | Recall | FP/día | Costo diario |
|---|---|---|---|---|
| Simétrico | 0.50 | 92% | ~5 | ~25 min |
| **Asimétrico** | **0.15** | **99.5%** | **~18** | **~90 min** |
| Extremo | 0.05 | 99.9% | ~45 | ~225 min |

El punto óptimo (99.5% recall, ~18 FP/día, ~90 min extra) es operativamente viable. Monitoreo: diario (FN real → revisión inmediata), mensual (recalculo precisión/recall), trimestral (informe al Comité de IA con recomendación de ajuste).


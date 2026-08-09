# Anexo 04 — Modelo TO-BE: diagrama, flujo detallado y decisiones no automatizables

> **Referenciado desde:** §4 del cuerpo del documento.
> **Contiene:** §A.1 Diagrama TO-BE completo, §A.2 Flujo detallado por etapa, §A.3 Mapeo problema→solución ampliado, §A.4 Tabla de decisiones no automatizables.

---

## A04.1 Diagrama TO-BE completo

```
                          CIUDADANO
                    envía petición por
                web / email / físico / campo
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                     M1 — RECEPCIÓN INTELIGENTE                   │
│                                                                  │
│  ● OCR (Tesseract LSTM spa + OpenCV): convierte escaneados       │
│    en texto. Preprocesamiento: deskew, binarización adaptativa.  │
│  ● NER (spaCy fine-tuned): extrae nombre, tipo_doc, num_doc,    │
│    dirección, teléfono, email, hecho, pretensión, entidad_ref,  │
│    anexos, canal, fecha                                          │
│  ● Validador de completitud: reglas declarativas                 │
│       ├── Faltan datos → Respuesta automática con plantilla      │
│       └── OK → Genera radicado URAB-YYYYMMDD-NNNNNN              │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   M4 — ANTI-DUPLICACIÓN                          │
│                                                                  │
│  ● Vectorizador: Sentence-Transformers → embedding 768-dim      │
│  ● Cosine similarity vs top-K (K=10) más cercanos en BD         │
│  ● Filtro reforzado: mismo CC + misma pretensión (NER de M1)    │
│  ● Umbral configurable: 85% por defecto (validado D8)           │
│       ├── ≥85% + mismo CC + misma pretensión → UI acumulación   │
│       └── <85% → Pasa a M2                                       │
│                                                                  │
│  ⚠️  DECISIÓN HUMANA: El profesional ve ambas peticiones lado   │
│     a lado con campos resaltados. Justifica por escrito.         │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                  M2 — CLASIFICACIÓN Y TRIAJE                     │
│                                                                  │
│  Clasificador primario: BETO fine-tuned + Softmax 4 clases:     │
│     Asesoría | Queja | Solicitud de Mediación | Conciliación    │
│                                                                  │
│  Sub-clasificador: mismo backbone, cabeza multi-etiqueta        │
│     ~12 sub-temas. Binary cross-entropy.                        │
│                                                                  │
│  Scorer de urgencia (REGLAS, no ML): keywords + patrones NER    │
│     Nivel 1 (baja) → 5 (crítica/riesgo vital). D7 de Derecho.  │
│                                                                  │
│  Priorizador: cruza texto con catálogo D3. Flag si sujeto de    │
│     especial protección constitucional detectado.               │
│                                                                  │
│  ⚠️  DECISIÓN HUMANA: Profesional URAB valida/corrige antes     │
│     de que el caso avance a asignación.                          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│               M3 — ASIGNACIÓN Y ENRUTAMIENTO                     │
│                                                                  │
│  Matriz de competencia: (tipo, sub-tema) → entidad + datos      │
│     Alimentada por D4. Reglas declarativas actualizables.        │
│       ├── Otra entidad → Notificación de traslado automática    │
│       └── Defensoría → Recomendador de ruta interna              │
│                                                                  │
│  Recomendador híbrido: reglas base + scoring por historial      │
│  Bandejas con estados: pendiente → asignado → en_gestión →      │
│     escalado → cerrado. Colas por profesional y URAB.           │
│  Monitor SLA: alertas al 80% y 100% del plazo máximo.           │
│                                                                  │
│  ⚠️  DECISIÓN HUMANA: El profesional confirma la competencia    │
│     de la entidad. La IA sugiere, NUNCA decide competencia.     │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│            PROFESIONAL DEFENSORIAL GESTIONA EL CASO              │
│                                                                  │
│  M5 — Historial unificado (Elasticsearch):                       │
│     GET /ciudadano/{cc}/historial → <500ms. Filtros por fecha,  │
│     tipo, estado. Sugiere respuestas previas + templates D6.     │
│                                                                  │
│  M6 — Asistente generativo RAG (cloud corporativa):              │
│     ┌──────────────────────────────────────────┐                │
│     │ Consulta → Embedding → ChromaDB (top-5)  │                │
│     │    │                                      │                │
│     │    ▼                                      │                │
│     │ Prompt = instrucciones + documentos       │                │
│     │         + petición + historial             │                │
│     │    │                                      │                │
│     │    ▼                                      │                │
│     │ Mistral 7B (nube corporativa) → borrador │                │
│     │    │                                      │                │
│     │    ▼                                      │                │
│     │ Profesional: revisa / edita / rechaza     │                │
│     │ Todo en logs inmutables                   │                │
│     └──────────────────────────────────────────┘                │
│                                                                  │
│  ⚠️  DECISIÓN HUMANA: Respuesta automática SOLO para D5.        │
│     El profesional SIEMPRE revisa, edita y firma.               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                M7 — INTEROPERABILIDAD                            │
│                                                                  │
│  Message broker cloud: publica evento caso.{creado,             │
│     actualizado, cerrado}                                        │
│     ├── Consumer IRIS → IRIS API → OK/KO → Log                  │
│     └── Consumer VisionWeb → VisionWeb API → OK/KO → Log        │
│                                                                  │
│  Reintentos: backoff exponencial (1s, 2s, 4s, 8s, 16s, 32s)    │
│  Tras 6 fallos → alerta administrador.                           │
│  RPA como contingencia si no hay API de escritura.              │
│                                                                  │
│  Mapeo canónico de campos:                                       │
│     radicado ↔ numero_radicado (IRIS) ↔ codigo_expediente (VW) │
│     estado ↔ estado_tramite (IRIS) ↔ fase_procesal (VW)         │
│  Bitácora inmutable + conciliación diaria automática.           │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   M8 — ANALÍTICA                                 │
│                                                                  │
│  Dashboard 1: Carga temática (distribución, tendencias, top 10) │
│  Dashboard 2: Cuellos de botella (tiempos, demoras, carga)      │
│  Dashboard 3: Recurrencia y duplicidad                          │
│  Dashboard 4: Equidad (género, grupo, región, alertas)          │
│  Capa investigación: k-anonymity ≥5, rol "investigador"         │
└──────────────────────────────────────────────────────────────────┘
```

---

## A04.2 Flujo detallado por etapa (AS-IS → TO-BE)

| Etapa | AS-IS (hoy) | TO-BE (con IA + cloud) | Módulo | Punto de decisión humana |
|---|---|---|---|---|
| **A. Recepción** | Funcionario recibe, transcribe a mano, verifica legibilidad, crea radicado manual (~15 min). Errores de digitación frecuentes. | Sistema recibe por API/email/OCR. NER extrae datos automáticamente. Validador detecta faltantes y responde al ciudadano. Radicado semiautomático. | M1 | Profesional URAB valida datos extraídos y confirma radicado |
| **B. Triage** | Clasificación manual en 4 categorías, sin criterios uniformes, sin historial del peticionario. ~30 casos/día por funcionario. | IA sugiere tipo, sub-tema(s), urgencia (1–5) y flag de prioridad. M5 muestra historial unificado. Profesional valida o corrige. | M2, M5 | Profesional URAB valida/corrige clasificación y nivel de urgencia |
| **C. Reparto** | Asignación manual. Doble registro en IRIS y VisionWeb. Sin monitoreo de tiempos ni alertas de vencimiento. | M3 recomienda entidad y ruta. Un solo registro. M7 sincroniza simultáneamente. SLAs visibles con alertas. | M3, M7 | Profesional confirma competencia de la entidad y ruta de asignación |
| **D. Gestión** | Profesional investiga y redacta desde cero. Sin apoyo documental. Respuestas inconsistentes entre profesionales. | M6 (RAG) genera borrador basado en normativa real. M5 muestra historial y respuestas previas. Profesional edita y firma. | M6, M5 | Profesional revisa, edita y firma la respuesta. La IA solo redacta borrador |
| **E. Cierre** | Verificación manual. Archivo con riesgo de quedar en una sola plataforma. Sin trazabilidad. | M7 sincroniza cierre simultáneo en IRIS y VisionWeb. Bitácora inmutable. M8 actualiza dashboards. | M7, M8 | Profesional inicia el cierre tras verificar cumplimiento |

---

## A04.3 Mapeo problema → solución (ampliado)

| # | Problema crítico | Causa raíz | Módulo(s) | Mecanismo de solución | Impacto esperado |
|---|---|---|---|---|---|
| 1 | Volumen y saturación (~300/día) | Clasificación manual ~15 min/caso. Profesional procesa ~30/día. | M1, M2, M6 | Automatización de recepción, extracción de datos y clasificación. Profesional pasa de ejecutor a supervisor. | Reducción de tiempo de clasificación de ~15 min a <30 seg. Liberación de ~70% del tiempo del profesional para casos complejos. |
| 2 | Riesgo jurídico por represamiento | Sin sistema de priorización. Casos urgentes mezclados con rutinarios. | M2, M3 | Score de urgencia (1–5) con reglas auditables. Detección automática de sujetos de especial protección. SLAs con alertas graduadas. | Recall de urgencias ≥99%. Ningún caso de riesgo vital sin detectar. Reducción de acciones de tutela contra la Defensoría. |
| 3 | Doble registro IRIS/VisionWeb | Sistemas sin comunicación (§2.4.3). Profesional digita cada caso dos veces. | M7 | Capa de orquestación cloud con modelo canónico. Único punto de entrada. Sincronización bidireccional simultánea. Bitácora de cada operación. | Eliminación de doble digitación. Consistencia de estados garantizada. Auditoría completa de cada sincronización. |
| 4 | Duplicidad de peticiones | Sin sistema de detección. Ciudadano presenta misma queja hasta 10 veces. | M4 | Embeddings semánticos + cosine similarity. ≥85% similitud + mismo CC + misma pretensión = sugerencia de acumulación. | Recall de duplicados ≥90%. Reducción de reprocesos ≥50%. |
| 5 | Peticionarios sin historial | No existe historial unificado. Cada petición se trata como nueva. | M5 | Índice Elasticsearch. Historial completo por cédula en <500ms. Sugerencias de respuestas previas y templates. | Contexto completo del ciudadano disponible en segundos. Respuestas más coherentes entre interacciones. |

---

## A04.4 Decisiones que nunca se automatizan (supervisión humana §5.4)

| Decisión | Módulo | La IA solo... | El humano siempre... | Fundamento jurídico |
|---|---|---|---|---|
| Evaluación de competencia de la entidad | M3 | Sugiere direccionamiento según matriz D4 | Confirma o corrige la entidad competente | Debido proceso (CP art. 29). La competencia es decisión de fondo. |
| Priorización de casos de riesgo vital | M2, M6 | Asigna score de urgencia y flag de alerta | Determina la prioridad final del caso. El umbral asimétrico está calibrado para preferir falsos positivos sobre falsos negativos | Derecho a la vida e integridad (CP arts. 11–12). Prohibición de automatizar decisiones con impacto en derechos fundamentales. |
| Respuesta de fondo al peticionario | M6 | Redacta borrador basado en normativa real recuperada por RAG | Revisa, edita, corrige y firma la respuesta final | Debido proceso (CP art. 29). Derecho de petición (CP art. 23). La respuesta es un acto administrativo. |
| Corrección de errores de duplicación | M4 | Sugiere acumulación si supera el umbral de similitud | Decide si acumula, rechaza o marca como relacionado. Justifica por escrito. | Seguridad jurídica. Dos casos distintos acumulados erróneamente vulneran el derecho de acceso a la justicia. |
| Archivo y cierre del caso | M7, M8 | Sincroniza el cierre en IRIS y VisionWeb | Verifica que se cumplieron todos los pasos del proceso e inicia el cierre | Ley 594 de 2000 (gestión documental). La decisión de archivo tiene efectos jurídicos permanentes. |

> **Principio rector:** en cada interacción entre IA y humano, es este último quien tiene la potestad decisoria final. La IA asiste, sugiere y automatiza tareas repetitivas; el profesional defensorial conserva en todo momento el juicio, la responsabilidad y la firma.

# Modelo TO-BE — Proceso de la Defensoría del Pueblo con IA integrada

> **Para:** Equipo de Derecho. Este es el diseño del proceso futuro para que puedan referenciarlo en el documento y validar que cumple con los requisitos jurídicos (§5.4 del caso: supervisión humana, debido proceso, decisiones no automatizables).

---

## Flujo completo TO-BE (diagrama)

```
                          CIUDADANO
                    envía petición por
                web / email / físico / campo
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                     M1 — RECEPCIÓN INTELIGENTE                   │
│                                                                  │
│  ● OCR (Tesseract): convierte PDFs/fotos escaneadas en texto     │
│  ● NER (spaCy): extrae nombre, CC, dirección, pretensión        │
│  ● Validador: ¿faltan datos obligatorios?                        │
│       ├── SÍ → Respuesta automática: "Falta X, por favor..."     │
│       └── NO → Genera radicado URAB-YYYYMMDD-XXXXXX              │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   M4 — ANTI-DUPLICACIÓN                          │
│                                                                  │
│  ● Convierte el texto en embedding (vector de 768 números)       │
│  ● Compara con base de datos vía cosine similarity              │
│  ● Si ≥85% similitud + mismo CC + misma pretensión?              │
│       ├── SÍ → Sugiere acumulación al profesional                │
│       └── NO → Pasa a clasificación                              │
│                                                                  │
│  ⚠️  DECISIÓN HUMANA: El profesional acepta o rechaza           │
│     la acumulación con justificación escrita obligatoria        │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                  M2 — CLASIFICACIÓN Y TRIAJE                     │
│                                                                  │
│  ● BETO fine-tuned clasifica el TIPO entre 4 categorías:         │
│    Asesoría | Queja | Solicitud de Mediación | Conciliación     │
│  ● Sub-clasificador multi-etiqueta asigna SUB-TEMAS (~12)        │
│  ● Reglas de urgencia: score 1 (baja) → 5 (crítica)            │
│  ● Detector de sujetos de especial protección constitucional     │
│  ● Flag de prioridad si aplica                                   │
│                                                                  │
│  ⚠️  DECISIÓN HUMANA: El profesional de URAB valida o corrige   │
│     la clasificación antes de que continúe el flujo             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│               M3 — ASIGNACIÓN Y ENRUTAMIENTO                     │
│                                                                  │
│  ● Matriz de competencia (tipo + sub-tema → entidad)            │
│       ├── Otra entidad → Genera notificación de traslado         │
│       └── Defensoría → Recomienda ruta interna                   │
│  ● Bandejas de trabajo por profesional con SLA visible          │
│  ● Alertas: 80% y 100% del plazo máximo                         │
│                                                                  │
│  ⚠️  DECISIÓN HUMANA: El profesional confirma la entidad        │
│     competente. La IA solo sugiere, NUNCA decide competencia    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│               PROFESIONAL DEFENSORIAL                            │
│               Gestiona el caso, investiga, coordina              │
│                                                                  │
│  ● M5 (Historial): consulta historial unificado del ciudadano    │
│    en <500ms con todos sus casos previos                         │
│  ● M6 (Asistente RAG): la IA busca normativa aplicable en       │
│    ChromaDB y genera un borrador de respuesta                    │
│                                                                  │
│  ⚠️  DECISIÓN HUMANA: El profesional SIEMPRE revisa, edita y    │
│     firma la respuesta. La IA NUNCA responde sin supervisión.   │
│     Solo consultas del catálogo D5 son automáticas.             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                M7 — INTEROPERABILIDAD                            │
│                                                                  │
│  ● RabbitMQ publica evento "caso.cerrado"                       │
│  ● Dos consumidores sincronizan simultáneamente:                │
│       ├── IRIS (gestión documental)                              │
│       └── VisionWeb (sistema misional de estadísticas)          │
│  ● Si una API falla → reintentos automáticos (1s, 2s, 4s...)  │
│  ● Bitácora inmutable de cada sincronización                    │
│  ● RPA como contingencia si no hay APIs de escritura            │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   M8 — ANALÍTICA                                 │
│                                                                  │
│  ● Dashboard 1: Carga temática (distribución, tendencias)       │
│  ● Dashboard 2: Cuellos de botella (tiempos, demoras, carga)    │
│  ● Dashboard 3: Recurrencia y duplicidad                        │
│  ● Dashboard 4: Equidad (por género, grupo, región)             │
│  ● Capa de investigación: datos anonimizados (k-anonymity ≥5)   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Texto descriptivo para el documento

> *Copiar esto en la sección 4 del escrito.*

El modelo TO-BE propuesto inserta los ocho módulos de inteligencia artificial solicitados en el caso (§3, M1–M8) como una capa de asistencia integrada en el macroproceso actual. El principio rector del diseño es que **la IA automatiza tareas repetitivas y apoya —nunca reemplaza— la toma de decisiones del profesional defensorial**. En cada punto donde el sistema produce una clasificación, sugerencia o borrador, existe un mecanismo explícito de validación humana antes de que la decisión surta efectos jurídicos.

El flujo rediseñado opera de la siguiente manera:

1. **Recepción (M1).** La petición ingresa por cualquier canal (formulario web, correo electrónico, documento físico escaneado, jornada de campo) y es normalizada. El módulo M1 aplica reconocimiento óptico de caracteres (OCR) a documentos escaneados o fotografiados, extrae automáticamente los datos del ciudadano y el contenido de su solicitud mediante extracción de entidades (NER), verifica que no falte información crítica, y genera un número de radicado único. Si se detectan datos faltantes, el sistema responde automáticamente al ciudadano solicitando la información complementaria.

2. **Verificación de duplicidad (M4).** Antes de crear un nuevo caso, el sistema convierte el texto de la petición en una representación numérica (embedding) que captura su significado —no solo las palabras literales— y la compara contra la base de datos de peticiones existentes. Si detecta una similitud superior al 85% combinada con coincidencia de documento de identidad y pretensión, sugiere al profesional de URAB acumular la nueva petición al expediente existente. La decisión de acumular o no es siempre humana.

3. **Clasificación y triaje (M2).** El texto se procesa por un modelo de lenguaje entrenado específicamente para esta tarea (BETO con fine-tuning), que asigna automáticamente: (a) el tipo de caso según las cuatro categorías jurídicas, (b) los sub-temas aplicables (una petición puede versar sobre múltiples temas simultáneamente), (c) un nivel de urgencia en escala de 1 a 5 basado en reglas declarativas y auditables —no en caja negra—, y (d) un flag de prioridad si el peticionario pertenece a un grupo de especial protección constitucional. El profesional de URAB valida o corrige la clasificación antes de que el caso avance.

4. **Asignación y enrutamiento (M3).** La matriz de competencia determina la entidad responsable según el tipo y sub-tema del caso. Si la Defensoría no es competente, el sistema genera automáticamente la notificación de traslado. Si es competente, un recomendador interno sugiere la ruta de asignación óptima considerando la carga de trabajo y el perfil de los profesionales disponibles. La decisión final de competencia y asignación es humana.

5. **Gestión defensorial asistida (M5 + M6).** Durante la gestión del caso, el profesional cuenta con dos apoyos: M5 le muestra en menos de un segundo el historial completo de peticiones de ese ciudadano (todos los radicados previos, tipos, estados y respuestas emitidas), eliminando la ceguera contextual del proceso actual. M6, mediante arquitectura RAG (generación aumentada por recuperación), consulta una base de conocimiento con normativa, jurisprudencia y plantillas institucionales, y genera un borrador de respuesta que el profesional **siempre** revisa, edita y firma. La IA nunca emite una respuesta sin supervisión humana, con la única excepción de consultas puramente informativas previamente catalogadas por el equipo jurídico (catálogo D5: estado del radicado, profesional asignado, reenvío de constancia).

6. **Cierre sincronizado (M7).** Al cerrar el caso, el sistema publica un evento que sincroniza simultáneamente el estado final en IRIS y VisionWeb a través de una capa de orquestación con modelo canónico de datos, eliminando la doble digitación. Una bitácora inmutable registra cada sincronización para fines de auditoría.

7. **Analítica institucional (M8).** Todos los datos operativos alimentan dashboards en tiempo real que permiten a la Defensoría monitorear la carga temática, identificar cuellos de botella, medir la tasa de duplicidad y —fundamentalmente— evaluar la equidad del sistema desagregada por género, región y grupo poblacional.

---

## Tabla resumen: AS-IS → TO-BE por etapa

| Etapa | AS-IS (hoy) | TO-BE (con IA) | Módulo | ¿Quién decide? |
|---|---|---|---|---|
| **A. Recepción** | Funcionario recibe, transcribe datos a mano, verifica legibilidad, crea radicado manual | Sistema extrae datos automáticamente (OCR + NER), detecta faltantes, genera radicado semiautomático | M1 | Humano (validación de datos extraídos) |
| **B. Triage** | Clasificación manual, sin criterios uniformes, sin visibilidad del historial | IA sugiere tipo, sub-tema, urgencia (1–5) y prioridad. Profesional valida | M2, M5 | **Humano** (valida/corrige clasificación) |
| **C. Reparto** | Asignación manual, doble registro IRIS/VisionWeb, sin monitoreo de tiempos | Recomendación de entidad y ruta. Un solo registro, sincronización automática | M3, M7 | **Humano** (confirma competencia) |
| **D. Gestión** | Profesional investiga y redacta desde cero, sin apoyo documental | Asistente RAG genera borrador con base en normativa real. Profesional edita y firma | M6, M5 | **Humano** (revisa, edita, firma) |
| **E. Cierre** | Archivo manual, riesgo de quedar en una sola plataforma | Sincronización simultánea IRIS/VisionWeb con bitácora. Dashboards actualizados | M7, M8 | Humano (inicia el cierre) |

---

## Puntos donde el humano SIEMPRE tiene la última palabra

| Decisión | ¿Quién la toma? | La IA solo... |
|---|---|---|
| ¿Este caso es realmente una Queja o una Asesoría? | Profesional URAB | Sugiere la clasificación |
| ¿Este caso es urgente (nivel 5)? | Profesional URAB | Asigna un score, pero no decide |
| ¿Acumulo esta petición a un caso existente? | Profesional URAB | Sugiere la acumulación si supera el umbral |
| ¿Qué entidad es competente? | Profesional URAB | Recomienda según la matriz de competencia |
| ¿Qué dice la respuesta final al ciudadano? | Profesional defensorial | Genera un borrador que el profesional edita y firma |
| ¿Cierro el caso? | Profesional defensorial | Sincroniza el cierre en los sistemas |

---

## Lo que la IA NUNCA hace

- ❌ Decide la competencia de una entidad
- ❌ Determina la prioridad final de un caso de riesgo vital
- ❌ Envía una respuesta de fondo sin revisión y firma humana
- ❌ Corrige errores de deduplicación sin intervención del profesional
- ❌ Cierra un caso sin verificación humana
- ❌ Toma decisiones que afecten derechos fundamentales sin supervisión

> *Este diseño garantiza el cumplimiento del debido proceso (CP art. 29), el derecho de petición (CP art. 23), el principio de transparencia algorítmica (Directiva 007/2025) y los requisitos de supervisión humana significativa exigidos en §5.4 del caso.*

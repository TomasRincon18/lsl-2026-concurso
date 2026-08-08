# Borrador — Secciones técnicas del Escrito 1 (Equipo J)

> **Uso:** textos listos para copiar al escrito `CONCURSO_LEGALTECH_-_ESCRITO_INTENTO_1.docx` (sección de Especificaciones Técnicas). Las cifras marcadas `[validar]` son propuestas razonables que el equipo debe ajustar antes de entrega.
> Referencias a secciones (`§x`) remiten al **Caso oficial URAB (RFP)**. Referencias entre corchetes corresponden a los insumos del equipo (Matriz SGIA, SECOP, flujogramas).
> Se usará el formato Arial 12, interlineado 1, APA 7.ª en la redacción final.

---

## 1. Modelo TO-BE y alcance del piloto

### 1.1 Marco del rediseño

El objeto de la convocatoria es la solución integral de IA y gobernanza para el **Macroproceso de Atención y Trámite de Quejas**, con implementación **piloto** y escalamiento progresivo en la **URAB** e integración con **IRIS** y **VisionWeb** (§2.2). El proceso rediseñado inserta los módulos solicitados (§3, M1–M8) en los cuatro grandes bloques del macroproceso actual (§2.3 A–D):

| Etapa del macroproceso | Hoy (as-is) | Cambio esperado con la solución | Módulos |
|---|---|---|---|
| **A. Recepción** | Ingreso multicanal manual: web, correo en formato libre, correo físico (4-72), recepción en terreno. Se verifica legibilidad/completitud, se crea/confirma radicado a mano. | Ingesta multicanal normalizada, extracción de datos mínimos (relato, pretensión, entidad referida, anexos, canal, fecha), detección de faltantes y solicitud automática de información complementaria con plantillas. Radicado semiautomático con validación. | M1 |
| **B. Triage en URAB** | Clasificación manual en asesoría/queja/mediación/conciliación, evaluación de competencia y reparto discrecional sin visión integrada del historial. | Clasificación y subclasificación asistidas por IA con sugerencia de prioridad/riesgo y trazabilidad; validación humana previa a asignación. | M2, M5 |
| **C. Reparto y gestión** | Reparto manual con doble registro IRIS/VisionWeb; acompañamiento y seguimiento manual. | Bandejas de trabajo por rol, recomendación de entidad competente y ruta, indicadores de tiempo por segmento (ingreso→reparto→gestión→cierre). | M3, M7 |
| **D. Gestión defensorial** | Impulso/coordinación manual con la entidad competente; actualización de estado en dos plataformas. | Apoyo con borradores de respuesta (IA generativa con validación humana), alertas de riesgo para elevación a prioridad, historial unificado por ciudadano. | M6, M5 |
| **E. Cierre** | Verificación manual de respuesta, seguimiento interno y archivo; riesgo de archivo en una sola plataforma. | Consistencia de estados entre IRIS y VisionWeb con bitácora, indicios para el cierre y consolidación del expediente. | M7, M8 |

### 1.2 Alcance del piloto en URAB
- **Entra en el piloto funcional:** módulos **M1, M2, M3, M4, M5, M6** con validación humana (§5.4), módulo **M7** limitado a la integración mínima IRIS/VisionWeb requerida por §4.2, y módulo **M8** con tableros básicos de operación.
- **Se difiere al escalamiento progresivo:** otras Unidades de análisis de la Defensoría (fuera de Bogotá), integración con **Carpeta Ciudadana Digital (gov.co)** como componente opcional (módulo M7 — Banco de preguntas: "componente opcional… el proponente puede proponer un mecanismo de acuse de recibo y consulta de estado"), y foliación electrónica con firma de índice bajo estándares del **AGN** (Banco Q8: no es requisito mínimo; se ofrece como **diferenciador** a partir de §4.3 y gestión documental §5.1).
- **Decisión de alcance:** las métricas y obligaciones de la Fase 3 se comprometen en el piloto URAB; la analítica institucional (M8) se habilita sobre datos del piloto y se extiende con el escalamiento.

> **Referencia visual:** el flujograma as-is/to-be se incorpora como anexo (ver `FLUJOGRAMAS.pptx` → diagrama to-be).

---

## 2. Arquitectura técnica de la solución

### 2.1 Decisión de arquitectura: capa de orquestación con modelo canónico
Frente al "nudo" IRIS vs VisionWeb (no hay cruce entre ambas, §2.4.3, mientras §4.2 exige evitar dobles registros), el equipo opta por una **capa de orquestación con registro único y modelo canónico de datos, con sincronización bidireccional hacia IRIS y VisionWeb y resolución de conflictos**. Justificación:
- Cumple §4.2: evita doble registro cuando exista camino factible, mantiene **consistencia de estados** (radicado, asignación, gestión, cierre) y exige **bitácora y trazabilidad** de cada sincronización.
- Reduce el riesgo del §2.4.3 (archivo en una sola plataforma en el cierre) al centralizar el estado y reconciliar ambas plataformas.
- Alimenta la gobernanza §5.4 al dejar trazabilidad total (a quién y por qué) y la auditoría (posibilidad de explicar una decisión en el cierre).
- Es neutral tecnológicamente (§7.1) y compatible con que **IRIS** siga siendo la plataforma de gestión documental/reparto amigable y **VisionWeb** el sistema misional de estadísticas.

> La decisión se desarrolla junto con la estrategia jurídica para que no entre en conflicto con la cláusula de propiedad intelectual del anexo contractual (las notas del Escrito lo señalan).

### 2.2 Arquitectura lógica (capas)
```
[ Capas de acceso ]  Bandejas URAB · Bandejas profesionales · Tableros (M8)
-------------------------------------------
[Capa de orquestación]  API Gateway · colas · workflow (ingreso→cierre) · Bitácora
-------------------------------------------
[Motores de IA]
    · Motor M2 clasificación/triage
    · Motor M4 similitud/deduplicación
    · Motor M6 generativo (validación humana)
    · Motor M5 historial ciudadano
[Modelo canónico de datos]  (esquema unificado)
-------------------------------------------
[Integración]  conectores → IRIS · VisionWeb · gov.co (opcional)
[Seguridad transversal]  identidad · accesos · cifrado · logs
```

### 2.3 Arquitectura de datos
- **Ingesta:** multicanal normalizada (web, correo, escaneos, cargue manual) con OCR para PDFs/imágenes escaneadas; controles de error (§4.3).
- **Almacenamiento:** área cruda + capa canónica (modelo de datos único) + índices semánticos (embeddings) para clasificación, dedup y búsqueda de historial.
- **Indexación/recuperación:** búsqueda por cédula u otro identificador permitido, integrado con el historial por ciudadano (M5).
- **Gobernancia de datos:** perfilamiento de calidad, normalización de taxonomías (temáticas, entidades, tipos de trámite) y trazabilidad de origen (§4.3). `[detalle]` Según la Fase 0 (inventario de datos).

### 2.4 Arquitectura de integración (IRIS / VisionWeb)
- **Capa de integración:** APIs/ETL-ELT cuando existan caminos factibles; **RPA como capa de contingencia** solo para eliminar el doble registro manual si los sistemas legados no ofrecen escritura API (*Banco Q10*).
- **Modelo canónico:** mapea campos y estados entre ambas plataformas; la orquestación actualiza el dato único y replica a IRIS y VisionWeb.
- **Bitácora y trazabilidad:** cada sincronización registra *qué* se replicó, *cuándo*, *por quién* y *con qué resultado* (§4.2). Esto es también insumo de auditoría (§5.4 y matriz de riesgos).

### 2.5 Arquitectura de seguridad y continuidad (§4.5)
- Control de acceso por **roles**: URAB · profesional de trámite · auditoría · administración.
- **Logs con integridad** (registros de actividad, hash/inmutabilidad para evidencia).
- **Cifrado** en tránsito y en reposo; el incidente de ciberseguridad de nov-2025 [antecedente DOC_1] refuerza la necesidad.
- Planes de **contingencia** ante indisponibilidad de plataformas o conectividad (fallo crítico del §2.4.2): cola local/offline con acuse diferido.
- Esquema de **respaldo y recuperación** con objetivos de recupero `[validar]` (p.ej. RPO≤24 h, RTO≤4 h).

### 2.6 MLOps y operación (§4.6, si aplica)
- Versionamiento de modelos y datasets; monitoreo de deriva (drift) con alertas; canal de retroalimentación humana (correcciones que vuelven a training); política de actualización controlada con registro de cambios.

---

## 3. Matriz de riesgos (daño antijurídico) — §5.5

Tres familias: **T** falla técnica (caídas, errores de integración, falsos negativos), **O** operativa (uso indebido, dependencia excesiva, omisiones), **J** jurídica (términos, privacidad, trazabilidad). Cada riesgo incluye **mitigación, evidencia** y **frecuencia de monitoreo**. La matriz completa (con probabilidad/impacto inherente y residual por DAFP) se presenta en **anexo** (base: `Matriz_SGIA_ISO42001.xlsx`).

| ID | Familia | Riesgo | Mitigación / control | Evidencia | Monitoreo |
|---|---|---|---|---|---|
| R1 | T | Fallo de conectividad o caída IRIS/VisionWeb que genera represamiento (§2.4.2) | Colas resilientes, modo offline, acuse de ingreso, plan de contingencia (§4.5) | Logs de colas, bitácora de fallos | Semanal |
| R2 | T | Error de integración (doble registro o archivo en una sola plataforma) (§2.4.3) | Modelo canónico + sincronización y verificación de estados | Bitácora de sincronización §4.2 | Diaria |
| R3 | T | Falso negativo en clasificación de urgencias (no detección de riesgo vital, p.ej., desapariciones) | Umbral asimétrico (ver §6), supervisión humana, revisión de alto riesgo | Datasets gold + métricas recall urgencias | Diaria/por lote |
| R4 | T | Falso positivo en deduplicación (fragmentación/acumulación inadecuada) | Reglas configurables (umbral 85% + mismo ciudadano), justificación de acumulación (M4), revisión humana | Bitácora de acumulación M4 | Semanal |
| R5 | T/O | Sesgo algorítmico que amplifica exclusiones (género, discapacidad, juventud) | Pruebas de equidad §4, revisión por subgrupo, XAI | Resultado de pruebas §4.2 | Cada release |
| R6 | O | Dependencia excesiva / "automatizar de más" (falta de supervisión humana) | Human-in-the-loop §5.4; decisiones NO automatizadas (listado), límites M6 | Logs de revisión humana | Semanal |
| R7 | O | Omisiones/uso indebido por parte de los profesionales (cargue manual) | Capacitación §6.1/§6.3, roles y permisos, principio de menor privilegio | Plan de capacitación, registro de accesos | Mensual |
| R8 | J | Incumplimiento de términos (derecho de petición, req) por retraso | Tableros de tiempos M8, alertas M3, resp. en cadena | Indicadores M3/M8 | Diaria |
| R9 | J | Vulneración de privacidad/tratamiento de datos sensibles (salud, niñez) | Defensor como **responsable**, proveedor **encargado** (§5.1 y §5.4 + Ley 1581), cifrado, AIA | Registros de consentimiento/autorización | Trimestral |
| R10 | J | Falta de trazabilidad que impide explicar decisiones (transparencia algorítmica) | Ficha de Transparencia Algorítmica (Directiva 007/2025 + NIST), registro explicación | Fichas por sistema (SDA) | Trimestral |
| R11 | T/O | Falla de IA generativa (respuesta falsa / decisión de fondo errónea) | Solo consultas simples/no controversiales; autorización humana; reglas límites | Bitácora de respuestas automatizadas | Semanal |
| R12 | T | Incidente de seguridad (ciberseguridad) con manejo de datos sensibles | Controles de acceso, cifrado, monitoreo, equipo de respuesta a incidentes, pruebas de red teaming (cf. Matriz SGIA riesgos 4–7) | Reporte de incidentes/pentests | Mensual |

> **Garantía:** alineación de la propuesta con el régimen de responsabilidad por daño antijurídico (responsabilidad estatal y contractual), vínculo con el contrato anexo y con la gobernanza §5.4.

---

## 4. Enfoque diferencial • Pruebas de equidad • Cambio sociotécnico (§5.2, §5.3)

### 4.1 Pruebas de equidad (integradas al plan de pruebas de la Fase 2)
- **Principio:** se incorporan como *pruebas antes del despliegue* dentro del plan de pruebas de la Fase 2 (§6.3), no como apartado independiente. Qué se mide:
- Indicadores desagregados por población: **género, discapacidad, juventud** (+etnia y origen, según el enfoque institucional) para las tareas clave de M2 (clasificación/triage), M4 (deduplicación) y M6 (borradores).
- Métricas por subgrupo: precisión/exhaustividad, tasa de falsos positivos/negativos, tasa de elevación a prioridad, y equidad (por ejemplo, diferencia de precisión entre grupos como señal de desigualdad).
- **Umbrales de alerta:** si la diferencia de desempeño entre subgrupos excede un umbral `[validar]` (por ejemplo, diferencia de precisión > 5 puntos o cociente de falsos negativos > 1,5), la coordinación del proyecto detiene el despliegue de ese módulo y activa mitigación (refinamiento de datos, reentrenamiento, supervisión humana reforzada).
- **Salvaguardas institucionales:** validación manual de rechazos automáticos; revisión de casos de riesgo vital por un funcionario; formatos y lectura accesibles (documentos de lectura accesible, intérpretes) con enfoque de discapacidad; no automatizar decisiones de fondo (según §5.4).

### 4.2 Cambio sociotécnico: identificación de capacidades y conductas (§5.3)
Tabla que alimenta la sección correspondiente del modelo de gobernanza:

| (i) Capacidades nuevas | (ii) Conductas habilitadas / cambiadas | (iii) Impactos disruptivos a anticipar | (iv) Decisiones de gobernanza |
|---|---|---|---|
| Lectura y clasificación masiva (300/día) | Clasificar y priorizar en minutos en vez de días | Riesgo de automatizar más de lo permitido / perder juicio humano | Lista de decisiones NO automatizables; human-in-the-loop |
| Vista unificada del historial por ciudadano | Atender peticionarios recurrentes con contexto completo | Privacidad por concentración de historial | Minimización; consentimiento/autorización; roles |
| Borradores de respuesta (M6) | Redactar y responder consultas simples | Respuestas inaceptables que el profesional asume | Reglas de límite y bitácora; rechazo humano |
| Monitoreo y analítica (M8) | Evidenciar tiempos, cuellos, duplicidad | Datos agregados que amplifiquen barreras de grupos pobl. | Enfoque diferencial en analítica; controles de privacidad |
| Interop IRIS/Vision | Eliminar doble registro | Resistencia al cambio / redundancia | Gestión del cambio (MIPG) y comités §5.4 |

### 4.3 Gestión de cambio (MIPG – ISO 42001)
- La estrategia incluye gestión de cambio organizacional como parte de la Fase 0 (§6.0) y del plan de capacitación de al menos **20 profesionales** (§6.1).
- Sesiones de sensibilización, manuales de rol y mesa de ayuda (§6.4), con procesos de comunicación formal, siguiendo la MIPG (Modelo Integrado de Planeación y Gestión) y articulándolo a la ISO/IEC 42001:2023 para adaptar la cultura organizacional.

---

## 5. Plan de trabajo por fases y entregables (§6)

Plan propuesto (duración de hitos `[validar]` para ajustar al cronograma del caso):

| Fase | Entregables (del §6) | Criterio de aceptación | Duración propuesta |
|---|---|---|---|
| **Fase 0. Alistamiento y diagnóstico** | Flujograma as-is y to-be; inventario de datos/canales/puntos de falla; taxonomía propuesta; plan de gestión de cambio y capacitación (≥20 profesionales) | Diagnóstico aprobado por el comité del proyecto; taxonomía validada por la URAB; línea base de métricas levantada (§6.1) | 4 semanas |
| **Fase 1 . Diseño de arquitectura e integración** | Arquitectura objetivo + diagrama de integración con IRIS y Vision; diseño gov.co (opcional con decisión argumentada); seguridad, accesos, logs y continuidad | Arquitectura validada con sistemas legados; matriz de interoperabilidad firmada | 8 semanas |
| **Fase 2. Construcción de módulos IA** | Prototipos: clasificación/triage; similitud/deduplicación; historial por ciudadano; asistente generativo (si aplica); plan de pruebas (técnicas, sesgos, usabilidad, estrés) | Métricas de desempeño de M2/M4/M5 sobre el conjunto de prueba (gold); pruebas de equidad §4 superadas | 12 semanas |
| **Fase 3 . Implementación, capacitación, operación inicial** | Plan de despliegue y adopción; capacitación por roles; tableros de analítica (operación y derechos); protocolo de incidentes y mesa de ayuda | Piloto URAB desplegado en operación; 100% de los profesionales de la URAB capacitados; tableros operativos | 8 semanas |
| **Fase 4 . Gobernanza y mejora continua** | Modelo de gobierno (comités, rituales, métricas, auditoría); plan de actualización controlada; informes periódicos | Comité de IA operando; métricas estables sobre umbrales; auditoría interna sin hallazgos críticos | Continua (al menos 12 meses de garantía `[validar]`) |

Cronograma resumido de hitos `[validar]` → **Plan inicial: F0 (M1), F1 (M2–M3), F2 (M4–M6), F3 (M6–M7), F4 (M8+)** es una referencia; el cronograma final se debe armonizar con el calendario oficial del caso y el plazo límite de la Fase Escrita.

> El modelo de **costos de 3 años** (§7.1 – §7.2) se construye discriminando implementación (una vez), licencias, operación/soporte, infraestructura, capacitación/gestión de cambio y evolución (mejoras, retraining, auditorías), con supuestos unitarios explícitos (Banco Q7) y estudio de mercado en `SECOP IA.xlsx` como referencia de precios.

---

## 6. Métricas y línea base del piloto (§4.4)

### 6.1 Cuadro de indicadores
La línea base se levanta en la Fase 0 (no existen registros actuales automatizados; Banco Q18: el proceso tarda varios días). Valores propuestos `[validar]`.

| Indicador | Definición / Módulo | Línea base (estimada) | Meta piloto | Umbral de alerta | Frecuencia |
|---|---|---|---|---|---|
| Tiempo de clasificación sugerida | De radicado a sugerencia de clasificación M2 | manual varias horas-2 días (sin medir de forma formal) | ≤15 min en 90% de peticiones `[validar]` | p90 > 30 min | Diaria |
| Precisión de clasificación/triage | Acierto de la categoría (asesoría/queja/mediación/conciliación) | — | ≥90% global; ≥90% subclasificación por tarea | <85% o caída >3 pts vs línea | Semanal |
| Exhaustividad en urgencias/riesgo | recall en casos críticos (desaparición, amenaza, niñez, riesgo vital) | no medido | **≥99% de recall (falso negativo ≈ 0)** `[validar]` | Cualquier falso negativo real dispara | Diaria |
| Deduplicación: coincidencias útiles | Tasa de duplicados reales correctamente identificados M4 | no hay | **≥85% precisión de sugerencias y ≥90% recall de duplicados** `[validar]` | precisión <70% o recall <80% | Semanal |
| Falsos positivos/negativos en dedup | % de sugerencias incorrectas /no detectadas | no hay | FP ≤15%, FN ≤10% `[validar]` | FP>20% / FN>15% | Semanal |
| Reducción de reprocesos de reparto | % de reasignaciones por error/duplicación | línea base (F0) | ≥50% de reducción `[validar]` | <20% de reducción | Mensual |
| Cumplimiento de tiempos internos | % peticiones con gestión terminada antes del plazo | no robusto | ≥90% `[validar]` de peticiones en tiempo | <80% | Mensual |
| Tiempos intermedios de proceso | M3: ingreso→reparto, reparto→gestión, gestión→cierre | a medir (F0) | p.ej. ingreso→reparto ≤4 h; reparto→gestión ≤24 h `[validar]` | Desvío > +50% | Semanal |
| Precisión del asistente generativo | % de respuestas revisadas que no requirieron corrección M6 | no hay | ≥90% para consultas de trámite simples `[validar]` | alertas diarias por revisión conflictiva | Semanal |

### 6.2 Metodología para umbral asimétrico de riesgo vital
- El costo de un **falso negativo** en casos con riesgo vital (desaparecidos, amenaza, niñez) no es comparable al de un **falso positivo**: el primero involucra daño antijurídico y vulneración de derechos fundamentales (§2.4.2 + §5.5), mientras que el segundo es un costo operativo (revisión).
- **Método propuesto:** definir en la Fase 0 un *score de gravedad* de la petición; fijar para la clase "riesgo vital" un umbral de decisión **asimétrico** (p.ej. sensibilidad de 99–100% a costa de subir falsos positivos) y **calibrarlo** con un conjunto *gold* etiquetado por juristas de la URAB. Se monitorea el trade-off precisión/recall; cualquier falso negativo de esa clase activa revisión y reentrenamiento (ver §2.6 MLOps).
- En reporte del indicador se debe indicar (i) la línea base de clasificación (levantada en F0), (ii) la métrica de calidad por urgencia y por población de enfoque diferencial (§4.1), y (iii) el plan de reajuste cuando se active el umbral.

---

## Anexo a integrar
- **Anexo A — Matriz de riesgos completa (23+ riesgos graduados con DAFP)**: `Matriz_SGIA_ISO42001.xlsx` (hoja "2. Matriz SGIA").
- **Anexo B — Flujogramas as-is / to-be**: `FLUJOGRAMAS.pptx` (diapositivas del proceso, ver plantilla del diagrama en el escrito).
- **Anexo C — Estudio de mercado / referencias de precios**: `SECOP IA.xlsx` (insumo del modelo económico §7.2).

---

*Borrador generado a partir de las notas del Escrito-Intento 1 y el texto oficial §§2–7 del Caso. Las celdas [validar] deben confirmarse con la mentoría antes de la entrega.*
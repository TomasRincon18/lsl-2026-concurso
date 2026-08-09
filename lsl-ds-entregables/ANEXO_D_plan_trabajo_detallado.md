# Anexo D — Plan de trabajo detallado

> **Referenciado desde:** §10 del borrador principal.

---

## D.1 Actividades detalladas por fase

### Fase 0 — Alistamiento y diagnóstico (Semanas 1–4)

| Semana | Actividad | Responsable | Entregable |
|---|---|---|---|
| 1 | Kick-off del proyecto. Reunión con stakeholders URAB, IRIS, VisionWeb. Definición del comité de proyecto. | Conjunto | Acta de inicio, matriz de stakeholders |
| 1–2 | Levantamiento de datos AS-IS: extraer muestra anonimizada de IRIS y VisionWeb (últimos 12 meses). Analizar volúmenes, tipos, tiempos por etapa, patrones de duplicidad, recurrencia. | DS | Informe de diagnóstico con estadísticas descriptivas |
| 2–3 | Etiquetado del dataset gold: ~1000 peticiones etiquetadas manualmente por juristas URAB con tipo, sub-tema, nivel de urgencia y flag de riesgo vital. | DS + Derecho | Dataset etiquetado versionado (DVC) |
| 2–3 | Inventario de canales de ingreso, puntos de falla, taxonomía de tipos y sub-temas, catálogo de entidades referidas. | DS + Derecho | Documento de taxonomía validada |
| 3 | Auditoría de infraestructura existente: servidores, conectividad, capacidad de cómputo, versiones de IRIS y VisionWeb, disponibilidad de APIs. | DS | Informe de auditoría técnica |
| 3–4 | Configuración de ambiente de desarrollo: Docker, CI/CD (GitHub Actions), repositorios, herramientas MLOps. | DS | Ambiente de desarrollo operativo |
| 4 | Definición del modelo de datos canónico alineado con requisitos legales (Ley 1581, Ley 594). | DS + Derecho | Esquema de base de datos documentado |
| 4 | Plan de gestión de cambio y capacitación: cronograma, contenidos, responsables, métricas de efectividad. | Derecho + DS | Plan de gestión de cambio |
| 4 | Levantamiento de línea base de métricas (M1–M17 del §12). | DS | Documento de línea base |

**Criterio de aceptación F0:** diagnóstico aprobado por el comité del proyecto. Taxonomía validada por URAB. Dataset etiquetado con ≥200 ejemplos por categoría. Línea base documentada. Infraestructura validada como suficiente.

---

### Fase 1 — Diseño de arquitectura e integración (Semanas 5–12)

| Semana | Actividad | Responsable | Entregable |
|---|---|---|---|
| 5–6 | Diseño detallado de arquitectura de capas, componentes, flujos de datos. | DS | Documento de arquitectura |
| 6–7 | Diseño del modelo canónico de datos con mapeo de campos IRIS ↔ VisionWeb. Validación con equipos de sistemas legados. | DS | Modelo canónico documentado |
| 7–8 | Diseño de integración: contratos de API (OpenAPI 3.0), flujos RabbitMQ, estrategia de reintentos, plan de contingencia RPA. | DS | Documento de integración |
| 8–9 | Diseño de seguridad: modelo RBAC (4 roles), flujos OAuth2/JWT, política de cifrado, arquitectura de logs inmutables. | DS + Derecho | Documento de seguridad |
| 9–10 | Diseño de continuidad: plan de contingencia ante caída de IRIS/VisionWeb, RPO/RTO, estrategia de respaldo y recuperación. | DS | Plan de continuidad |
| 10–11 | Evaluación de integración con Carpeta Ciudadana Digital (gov.co). Decisión documentada: incluir como componente opcional o diferir. | DS + Derecho | Documento de decisión gov.co |
| 11–12 | Diseño de dashboards M8: mockups de los 4 dashboards, métricas, filtros, frecuencia de actualización. | DS | Mockups de dashboards |
| 12 | Revisión y aprobación de la arquitectura por el comité del proyecto. | Conjunto | Arquitectura firmada |

**Criterio de aceptación F1:** arquitectura validada con equipos de IRIS y VisionWeb. Matriz de interoperabilidad firmada. Documento de seguridad aprobado.

---

### Fase 2 — Construcción de módulos IA (Semanas 13–24)

| Semana | Actividad | Responsable | Entregable |
|---|---|---|---|
| 13–14 | Fine-tuning de BETO para M2 con el dataset etiquetado en F0. Experimentos con hiperparámetros (MLflow). Selección del mejor modelo. | DS | Modelo M2 v1 con métricas |
| 14–16 | Desarrollo de M1: pipeline OCR (Tesseract + OpenCV), NER (spaCy fine-tuned para dominio Defensoría), validador de completitud, generador de radicado. | DS | M1 funcional en staging |
| 16–17 | Desarrollo de M4: integración Sentence-Transformers, índice pgvector, cosine similarity, UI de acumulación. | DS | M4 funcional en staging |
| 17–18 | Desarrollo de M3: matriz de competencia, recomendador de ruta, bandejas de trabajo, monitor SLA. | DS + Derecho | M3 funcional en staging |
| 18–19 | Integración de módulos M1→M4→M2→M3. Pruebas de integración (pytest + docker-compose). | DS | Tests de integración pasando |
| 19–20 | Desarrollo de M5: índice Elasticsearch, API de historial, sugerencias de respuestas previas. | DS | M5 funcional en staging |
| 20–22 | Desarrollo de M6 v1: ingesta de base de conocimiento en ChromaDB, pipeline RAG con LangChain, integración con Mistral 7B, UI de revisión humana. | DS | M6 v1 funcional en staging |
| 22–23 | Plan de pruebas completo: unitarias, integración, aceptación, equidad, carga, seguridad. Ejecución de pruebas. | DS | Informe de pruebas |
| 23–24 | Pruebas de equidad: evaluación de M2, M4 y M6 con métricas de fairness segmentadas. | DS | Informe de equidad |
| 24 | Revisión de métricas de desempeño contra metas del §12. Ajustes finales. Aprobación para Fase 3. | Conjunto | Aprobación de pase a Fase 3 |

**Criterio de aceptación F2:** todas las métricas de desempeño ≥ metas del §12. Pruebas de equidad sin disparidad >5%. Tests de integración y carga pasando.

---

### Fase 3 — Implementación, capacitación y operación inicial (Semanas 25–32)

| Semana | Actividad | Responsable | Entregable |
|---|---|---|---|
| 25 | Plan de despliegue: infraestructura de producción, migración de datos inicial, configuración de monitoreo. | DS | Plan de despliegue ejecutado |
| 25–26 | Capacitación por roles: 3 sesiones (URAB, Profesionales, Administradores). Material: manuales de rol, ejercicios prácticos, evaluación de conocimientos. | DS + Derecho | 100% profesionales capacitados y certificados |
| 26–27 | Desarrollo de M7: RabbitMQ, conectores IRIS/VisionWeb, bitácora de sincronización, RPA de contingencia si aplica. | DS | M7 funcional en producción |
| 27–28 | Desarrollo de M8: implementación de los 4 dashboards (Streamlit), capa de investigación institucional. | DS | M8 funcional en producción |
| 28 | Pruebas pre-producción: carga (300 peticiones/día simuladas), seguridad (pentest), disponibilidad. | DS | Informe pre-producción |
| 29–32 | Operación controlada en modo supervisado: el sistema opera en producción pero en paralelo al proceso manual durante 4 semanas. Comparación diaria de métricas. Ajustes iterativos con feedback de profesionales. | DS + URAB | Informe comparativo sistema vs. manual |
| 29–32 | Mesa de ayuda operando: registro de incidencias, tiempos de resolución, escalamiento. | DS | Reporte semanal de mesa de ayuda |
| 32 | Evaluación del piloto: métricas contra metas del §12. Encuesta de satisfacción. Decisión de escalamiento. | Conjunto | Informe de cierre de piloto |

**Criterio de aceptación F3:** sistema piloto URAB en operación. Métricas dentro de umbrales (§12). Satisfacción de profesionales ≥80%. Sin incidentes de seguridad.

---

### Fase 4 — Gobernanza y mejora continua (Semanas 33–52 + continuación)

| Período | Actividad | Responsable | Entregable |
|---|---|---|---|
| Semanas 33–36 | Constitución formal del Comité de IA: propietario del sistema, dueño de datos, responsable misional. Rituales: sesión mensual, revisión trimestral de métricas. | Conjunto | Acta de constitución, reglamento del Comité |
| Continuo (mensual) | Monitoreo de drift: Evidently AI genera reporte automático. Si drift supera umbral → análisis de causas. | DS → Defensoría | Reporte mensual de drift |
| Continuo (trimestral) | Evaluación de equidad: reporte automático de Evidently AI segmentado por género, región, grupo. Presentación al Comité de IA. | DS → Defensoría | Reporte trimestral de equidad |
| Semanas 33–44 | Escalamiento progresivo a 5 regionales adicionales (1 regional cada 2–3 semanas). Ajustes por regional. | DS | Sistema en 6 regionales |
| Semanas 33–40 | Implementación de M6 en modo RAG completo (no solo templates D5). Expansión de la base de conocimiento en ChromaDB. | DS | M6 RAG completo |
| Semanas 45–52 | Primer reentrenamiento programado de M2 con datos acumulados del piloto y feedback humano. | DS | M2 v2 con métricas mejoradas |
| Meses 12–18 | Transferencia de conocimiento: train-the-trainer al equipo TI de la Defensoría. Documentación completa. | DS | Equipo interno capacitado |
| Meses 18–24 | Soporte decreciente: 6 meses full → 3 meses parcial (2 días/semana) → 3 meses bajo demanda. | DS | Acta de transferencia |
| Meses 24–36 | Garantía y evolución: actualizaciones de seguridad, reentrenamiento bajo demanda, soporte de segundo nivel. | DS | Reportes anuales |

**Criterio de aceptación F4:** Comité de IA operando. Métricas estables. Equipo interno autónomo ≥3 meses consecutivos. Auditoría de cierre: todos los SLA cumplidos.

---

## D.2 Carta Gantt

```
SEMANA:  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32
FASE 0   ████████████████
FASE 1                     ████████████████████████████████
FASE 2                                                       ████████████████████████████████████████████████
FASE 3                                                                                                         ████████████████████████████████
FASE 4                                                                                                             (continúa semana 33 en adelante)
```

---

## D.3 Presupuesto estimado por fase y rubro `[validar]`

| Fase | Implementación | Licencias | Infraestructura | Capacitación | Evolución | Total fase |
|---|---|---|---|---|---|---|
| F0. Alistamiento (4 sem) | $45 M | $0 | $10 M | $5 M | $0 | **$60 M** |
| F1. Diseño (8 sem) | $80 M | $0 | $10 M | $5 M | $0 | **$95 M** |
| F2. Construcción IA (12 sem) | $280 M | $0 | $25 M | $10 M | $0 | **$315 M** |
| F3. Implementación (8 sem) | $120 M | $0 | $35 M | $20 M | $0 | **$175 M** |
| F4. Gobernanza (año 1) | $50 M | $0 | $35 M | $15 M | $30 M | **$130 M** |
| **Total Año 1** | **$575 M** | **$0** | **$115 M** | **$55 M** | **$30 M** | **$775 M** |
| Año 2 (soporte + evolución) | $60 M | $0 | $50 M | $10 M | $50 M | **$170 M** |
| Año 3 (soporte + evolución) | $60 M | $0 | $50 M | $10 M | $60 M | **$180 M** |
| **Total 3 años** | **$695 M** | **$0** | **$215 M** | **$75 M** | **$140 M** | **$1.125 M** |

> **Notas:** (1) Licencias = $0 porque el 100% del stack es open-source. (2) Infraestructura asume GovCloud MinTIC u on-prem de la Defensoría. (3) El evento de cotización en Fase 0 validará los supuestos unitarios antes de la firma del contrato. (4) Valores en millones de pesos colombianos, basados en referencias de mercado del `SECOP IA.xlsx` `[validar]`.

---

## D.4 Hitos de pago `[validar]`

| Hito | Fase | Semana | % del contrato | Entregable que dispara el pago |
|---|---|---|---|---|
| Firma del contrato | F0 | 0 | 15% | Acta de inicio |
| Diagnóstico aprobado | F0 | 4 | 10% | Dataset etiquetado + línea base validada |
| Arquitectura validada | F1 | 12 | 15% | Documento de arquitectura firmado |
| Módulos IA aprobados | F2 | 24 | 25% | Pruebas de desempeño y equidad superadas |
| Piloto en operación | F3 | 32 | 20% | Sistema en producción con métricas en umbrales |
| Cobertura 6 regionales | F4 | 44 | 10% | Acta de aceptación de despliegue |
| Transferencia completada | F4 | Mes 24 | 5% | Acta de cierre y transferencia |

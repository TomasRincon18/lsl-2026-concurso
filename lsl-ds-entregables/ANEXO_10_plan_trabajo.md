# Anexo 10 — Plan de trabajo detallado

> Referenciado desde: seccion 10 del cuerpo del documento.

---

## 10.1 Actividades por fase

### Fase 0 — Alistamiento y diagnostico (Semanas 1-4)

| Sem | Actividad | Responsable | Entregable |
|---|---|---|---|
| 1 | Kick-off. Reunion con stakeholders URAB, IRIS, VisionWeb. Comite de proyecto. Configuracion tenant cloud. | Conjunto | Acta inicio, tenant cloud |
| 1-2 | Levantamiento AS-IS: muestra anonimizada IRIS/VisionWeb 12 meses. Analisis volumenes, tipos, tiempos, duplicidad. | DS | Informe diagnostico |
| 2-3 | Etiquetado dataset gold: 1000 peticiones (tipo, sub-tema, urgencia, riesgo vital). DVC. | DS + Derecho | Dataset versionado |
| 2-3 | Inventario canales, puntos falla, taxonomia, catalogo entidades. | DS + Derecho | Taxonomia validada |
| 3 | Auditoria infraestructura, versiones IRIS/VisionWeb, APIs disponibles. | DS | Informe auditoria |
| 3-4 | Configuracion entorno cloud desarrollo: CI/CD, MLOps, entornos dev/staging. | DS | Entorno operativo |
| 4 | Modelo datos canonico (Ley 1581, Ley 594). Plan gestion cambio. Linea base metricas. | DS + Derecho | Esquema BD + linea base |

**Criterio aceptacion:** diagnostico aprobado, dataset mayor o igual 200 ejemplos/categoria, linea base documentada, cloud operativo.

### Fase 1 — Diseno de arquitectura e integracion (Semanas 5-12)

| Sem | Actividad | Responsable | Entregable |
|---|---|---|---|
| 5-6 | Arquitectura cloud: capas, componentes, flujos, plataforma agentes IA. | DS | Documento arquitectura |
| 6-7 | Modelo canonico mapeo IRIS-VisionWeb. Validacion sistemas legados. | DS | Modelo canonico |
| 7-8 | Integracion: contratos API OpenAPI 3.0, mensajeria cloud, reintentos, RPA contingencia. | DS | Documento integracion |
| 8-9 | Seguridad cloud: RBAC, OAuth2/JWT, cifrado, WAF, logs inmutables, responsabilidad compartida. | DS + Derecho | Documento seguridad |
| 9-10 | Continuidad: plan contingencia, RPO/RTO, backup, DR. | DS | Plan continuidad |
| 10-11 | Evaluacion Carpeta Ciudadana Digital gov.co. Decision documentada. | DS + Derecho | Documento decision |
| 11-12 | Dashboards M8 mockups. Revision y aprobacion arquitectura. | Conjunto | Arquitectura firmada |

**Criterio aceptacion:** arquitectura validada con sistemas legados, matriz interoperabilidad firmada.

### Fase 2 — Construccion modulos IA (Semanas 13-24)

| Sem | Actividad | Responsable | Entregable |
|---|---|---|---|
| 13-14 | Fine-tuning BETO M2 con dataset F0. Experimentos MLflow. | DS | Modelo M2 v1 |
| 14-16 | Desarrollo M1: OCR, NER, validador, radicado en cloud. | DS | M1 en staging |
| 16-17 | Desarrollo M4: embeddings, pgvector, cosine similarity, UI acumulacion. | DS | M4 en staging |
| 17-18 | Desarrollo M3: matriz competencia, recomendador, bandejas, SLA. | DS + Derecho | M3 en staging |
| 18-19 | Integracion M1-M4-M2-M3. Pruebas integracion. | DS | Tests integracion |
| 19-20 | Desarrollo M5: Elasticsearch cloud, API historial, sugerencias. | DS | M5 en staging |
| 20-22 | Desarrollo M6 v1: ingesta ChromaDB, RAG LangChain, Mistral 7B cloud, UI revision. | DS | M6 v1 en staging |
| 22-23 | Plan pruebas completo: unitarias, integracion, aceptacion, carga, seguridad. | DS | Informe pruebas |
| 23-24 | Pruebas de equidad (Anexo 08). Ajustes. Aprobacion pase a F3. | DS + Conjunto | Aprobacion F3 |

**Criterio aceptacion:** metricas cumplen metas seccion 12, equidad sin disparidad mayor a 5 por ciento.

### Fase 3 — Implementacion, capacitacion y operacion (Semanas 25-32)

| Sem | Actividad | Responsable | Entregable |
|---|---|---|---|
| 25 | Despliegue produccion cloud, migracion datos, monitoreo. | DS | Plan ejecutado |
| 25-26 | Capacitacion por roles (URAB, Profesionales, Administradores). | DS + Derecho | 100% certificados |
| 26-27 | Desarrollo M7: message broker cloud, conectores IRIS/VisionWeb, bitacora. | DS | M7 en prod |
| 27-28 | Desarrollo M8: 4 dashboards + capa investigacion. | DS | M8 en prod |
| 28 | Pruebas pre-produccion: carga, seguridad, disponibilidad. | DS | Informe pre-prod |
| 29-32 | Operacion supervisada 4 semanas en paralelo al proceso manual. Mesa de ayuda. | DS + URAB | Informe comparativo |
| 32 | Evaluacion piloto: metricas vs metas, encuesta satisfaccion. Decision escalamiento. | Conjunto | Informe cierre piloto |

**Criterio aceptacion:** sistema en operacion, metricas en umbrales, satisfaccion mayor o igual 80 por ciento, sin incidentes seguridad.

### Fase 4 — Gobernanza y mejora continua (Semana 33 en adelante)

| Periodo | Actividad | Responsable | Entregable |
|---|---|---|---|
| Sem 33-36 | Constitucion Comite IA: propietario sistema, dueno datos, responsable misional. | Conjunto | Reglamento Comite |
| Continuo mensual | Monitoreo drift con Evidently AI. Reporte automatico. | DS hacia Defensoria | Reporte drift |
| Continuo trimestral | Evaluacion equidad (Anexo 08). Presentacion al Comite. | DS hacia Defensoria | Reporte equidad |
| Sem 33-44 | Escalamiento progresivo a 5 regionales adicionales. | DS | 6 regionales |
| Sem 33-40 | M6 RAG completo (no solo D5). Expansion ChromaDB. | DS | M6 full RAG |
| Sem 45-52 | Primer reentrenamiento programado M2 con datos piloto + feedback. | DS | M2 v2 |
| Meses 12-18 | Transferencia conocimiento: train-the-trainer equipo TI Defensoria. | DS | Equipo autonomo |
| Meses 18-24 | Soporte decreciente: 6m full, 3m parcial, 3m bajo demanda. | DS | Acta transferencia |
| Meses 24-36 | Garantia y evolucion: seguridad, reentrenamiento, soporte nivel 2. | DS | Reportes anuales |

**Criterio aceptacion F4:** Comite IA operando, metricas estables, equipo interno autonomo 3+ meses, auditoria sin hallazgos criticos.

---

## 10.2 Carta Gantt

```
SEMANA:  1-4   5-12   13-24   25-32   33-52   53+
FASE 0   [####]
FASE 1          [########]
FASE 2                   [############]
FASE 3                             [########]
FASE 4                                     [#################...]
```

---

## 10.3 Presupuesto estimado [validar]

| Fase | Implementacion | Licencias | Infraestructura cloud | Capacitacion | Evolucion | Total |
|---|---|---|---|---|---|---|
| F0 (4 sem) | $45 M | $0 | $10 M | $5 M | $0 | $60 M |
| F1 (8 sem) | $80 M | $0 | $10 M | $5 M | $0 | $95 M |
| F2 (12 sem) | $280 M | $0 | $30 M | $10 M | $0 | $320 M |
| F3 (8 sem) | $120 M | $0 | $40 M | $20 M | $0 | $180 M |
| F4 (ano 1) | $50 M | $0 | $35 M | $15 M | $30 M | $130 M |
| **Total Ano 1** | **$575 M** | **$0** | **$125 M** | **$55 M** | **$30 M** | **$785 M** |
| Ano 2 | $60 M | $0 | $50 M | $10 M | $50 M | $170 M |
| Ano 3 | $60 M | $0 | $50 M | $10 M | $60 M | $180 M |
| **Total 3 anos** | **$695 M** | **$0** | **$225 M** | **$75 M** | **$140 M** | **$1.135 M** |

Notas: (1) Licencias $0: 100% stack open-source. (2) Infraestructura cloud incluye computo, almacenamiento, red, seguridad gestionada. (3) Costo total aproximado $1.135 M COP a 3 anos. (4) Valores en millones COP, basados en referencias SECOP IA.xlsx [validar]. (5) Evento de cotizacion en Fase 0 valida supuestos unitarios antes de firma del contrato.

---

## 10.4 Hitos de pago [validar]

| Hito | Fase | Semana | Porcentaje | Entregable |
|---|---|---|---|---|
| Firma contrato | F0 | 0 | 15% | Acta de inicio |
| Diagnostico aprobado | F0 | 4 | 10% | Dataset + linea base |
| Arquitectura validada | F1 | 12 | 15% | Documento arquitectura firmado |
| Modulos IA aprobados | F2 | 24 | 25% | Pruebas desempeno y equidad |
| Piloto en operacion | F3 | 32 | 20% | Sistema en prod con metricas |
| 6 regionales operativas | F4 | 44 | 10% | Acta aceptacion despliegue |
| Transferencia completada | F4 | Mes 24 | 5% | Acta cierre |

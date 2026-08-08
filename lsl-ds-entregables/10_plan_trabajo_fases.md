# 10. Plan de trabajo por fases y entregables

## ¿Qué es esta sección?

El cronograma completo del proyecto dividido en fases, desde el diagnóstico inicial hasta la operación autónoma por parte de la Defensoría. Cada fase tiene objetivos, actividades, entregables y criterios de salida.

**Responsable:** Conjunto. DS define fases técnicas y entregables tecnológicos. Derecho define hitos contractuales, tiempos de SECOP y presupuesto.

**Extensión sugerida:** 2-3 páginas.

---

## ¿Qué necesitas del equipo de Derecho?

- **Tiempos estimados de contratación pública (SECOP):** ¿cuánto tarda una licitación de este tipo?
- **Validación de presupuesto:** ¿los costos estimados son realistas para el sector público colombiano?
- **Hitos contractuales:** ¿en qué momentos se hacen pagos? ¿qué entregables disparan cada pago?
- **Restricciones legales:** ¿hay plazos máximos que no se pueden exceder por normativa?

---

## Paso a paso para redactar esta sección

### Paso 1: Estructura de fases del proyecto

El proyecto se divide en 5 fases. Cada fase es un "escalón": no se avanza a la siguiente hasta cumplir los criterios de salida de la actual.

```
Fase 0: Diagnóstico (3 meses)
   |
Fase 1: Piloto (6 meses)
   |
Fase 2: Despliegue progresivo (6 meses)
   |
Fase 3: Maduración (12 meses)
   |
Fase 4: Sostenibilidad y transferencia (12 meses)
```

---

### Fase 0: Diagnóstico y preparación

**Duración:** 3 meses  
**Objetivo:** Entender el estado actual, preparar los datos y sentar las bases técnicas.

| Actividad | Responsable | Descripción |
|---|---|---|
| Levantamiento de datos AS-IS | DS | Recopilar y analizar peticiones históricas (anonimizadas) de IRIS/VisionWeb: tipos, volúmenes, tiempos, patrones |
| Etiquetado de dataset inicial | DS + Derecho | Etiquetar manualmente ~1000 peticiones con tipo, sub-tema y urgencia. Este dataset será la base del fine-tuning |
| Auditoría de infraestructura | DS | Evaluar servidores, conectividad, capacidad de cómputo de las regionales |
| Configuración de ambiente de desarrollo | DS | Instalar dependencias, contenedores Docker, CI/CD, repositorios |
| Definición de modelo de datos | DS + Derecho | Diseñar esquema de base de datos alineado con requisitos legales (Ley 1581, Ley 594) |
| Capacitación inicial | Derecho | Socializar el proyecto con profesionales de URAB, recoger feedback |
| Mapeo detallado de APIs IRIS/VisionWeb | DS | Documentar endpoints, formatos, limitaciones de las APIs existentes |

**Entregables de la Fase 0:**
- Informe de diagnóstico: volúmenes, patrones, cuellos de botella actuales
- Dataset etiquetado (~1000 casos, 4 tipos x ~12 sub-temas)
- Documento de especificación de requisitos técnicos
- Modelo de datos validado jurídicamente
- Ambiente de desarrollo funcionando
- Informe de auditoría de infraestructura

**Criterio de salida:** Dataset etiquetado con al menos 200 ejemplos por categoría. Infraestructura validada como suficiente para el piloto.

---

### Fase 1: Piloto

**Duración:** 6 meses  
**Objetivo:** Implementar una versión funcional del sistema en una regional, con los módulos core, y demostrar que las métricas objetivo son alcanzables.

**Regional piloto:** Una regional de alto volumen (Bogotá o similar).

**Módulos incluidos:** M1 (Recepción), M2 (Clasificación), M3 (Asignación), M4 (Anti-Duplicación), M7 (Interoperabilidad en modo lectura), M8 (Dashboard 1: carga temática).

| Mes | Actividad | Responsable |
|---|---|---|
| **Mes 1** | Fine-tuning de BETO para M2 con dataset etiquetado. Primera versión del clasificador | DS |
| **Mes 1-2** | Desarrollo de M1: OCR, NER, validador de completitud, generador de radicado | DS |
| **Mes 2** | Desarrollo de M4: vectorización, cosine similarity, umbral de duplicación | DS |
| **Mes 2-3** | Desarrollo de M3: matriz de competencia, bandejas de trabajo, monitor SLA | DS + Derecho |
| **Mes 3** | Integración de módulos M1→M4→M3. Pruebas de integración | DS |
| **Mes 4** | Desarrollo de M7: RabbitMQ, conectores IRIS/VisionWeb (solo lectura) | DS |
| **Mes 4** | Desarrollo de M8 Dashboard 1: carga temática | DS |
| **Mes 5** | Pruebas de aceptación con profesionales reales. Iteración sobre feedback | DS + Derecho |
| **Mes 5** | Evaluación de equidad sobre datos del piloto | DS |
| **Mes 6** | Capacitación de 5-8 profesionales de la regional piloto | DS + Derecho |
| **Mes 6** | Puesta en producción controlada (modo sombra: el sistema clasifica pero el profesional también lo hace manualmente para comparar) | DS |

**Entregables de la Fase 1:**
- Sistema piloto funcionando en 1 regional
- Modelo clasificador M2 fine-tuned con métricas documentadas
- Reporte de comparación: clasificación automática vs manual (accuracy, tiempo)
- Informe de evaluación de equidad (primera medición)
- 5-8 profesionales capacitados
- Documentación técnica y manual de usuario

**Criterios de salida:**
- Accuracy de clasificación >85%
- Tasa de duplicados detectados (recall) >85%
- Tiempo ingreso→asignación <4 horas (p95)
- Disponibilidad del sistema >99%
- Sin sesgo significativo detectado (>5%) en métricas de equidad
- Encuesta de satisfacción de profesionales >80%

---

### Fase 2: Despliegue progresivo

**Duración:** 6 meses  
**Objetivo:** Escalar el sistema a 5 regionales adicionales, activar M5 (historial unificado) y M6 en modo básico (respuestas del catálogo D5), y expandir M8 a todos los dashboards.

| Actividad | Responsable |
|---|---|
| Escalamiento progresivo a 5 regionales (1 regional por mes) | DS |
| Implementación de M5 (Elasticsearch + historial unificado) | DS |
| Implementación de M6 respuestas automáticas (catálogo D5 de Derecho) | DS + Derecho |
| Reentrenamiento de M2 con nuevos datos (enriquecimiento del dataset con casos de nuevas regionales) | DS |
| Desarrollo de M8 dashboards 2, 3 y 4 (cuellos de botella, recurrencia, equidad) | DS |
| Capacitación de ~20 profesionales adicionales | DS + Derecho |
| M7 en modo escritura: sincronización full con IRIS y VisionWeb | DS |

**Entregables de la Fase 2:**
- Sistema funcionando en 6 regionales (1 piloto + 5 nuevas)
- M5 (historial unificado) operativo
- M6 respuestas automáticas para catálogo D5
- M8 con los 4 dashboards completos
- M7 en modo escritura bidireccional
- 25+ profesionales capacitados

**Criterios de salida:**
- Accuracy >85% en TODAS las regionales (no solo la del piloto)
- Tasa de falsos positivos en M4 <5%
- Cobertura de respuestas automáticas >30%
- Sincronización IRIS/VisionWeb exitosa >99.5%
- Cero incidentes de seguridad

---

### Fase 3: Maduración

**Duración:** 12 meses  
**Objetivo:** Completar todas las funcionalidades, escalar a cobertura nacional, y madurar el sistema con mejora continua basada en datos reales.

| Actividad | Responsable |
|---|---|
| Escalamiento a cobertura nacional (todas las regionales) | DS |
| Implementación de M6 RAG completo (no solo templates): ChromaDB con normativa, jurisprudencia, respuestas previas | DS + Derecho |
| Automatización de respuestas repetitivas con revisión humana | DS + Derecho |
| Monitoreo de drift con Evidently AI (primeros reportes trimestrales) | DS |
| Primer reentrenamiento programado de M2 (con feedback de 18 meses de operación) | DS |
| Integración de analítica avanzada: predicción de carga, detección temprana de crisis humanitarias por patrones de quejas | DS |
| Auditoría externa de seguridad y equidad | DS + Auditor externo |

**Entregables de la Fase 3:**
- Sistema con cobertura nacional
- M6 RAG completo: borradores de respuesta con base en normativa real
- 3 ciclos de reentrenamiento y evaluación de equidad documentados
- Reportes trimestrales de monitoreo de drift
- Auditoría externa de seguridad superada
- Modelo operativo maduro: procedimientos, roles, protocolos documentados

**Criterios de salida:**
- Accuracy >88% a nivel nacional
- Tasa de aceptación de borradores M6 >70%
- Drift de datos y predicciones dentro de umbrales aceptables
- Cobertura >95% de regionales
- Sin incidentes de seguridad en 6 meses

---

### Fase 4: Sostenibilidad y transferencia

**Duración:** 12 meses  
**Objetivo:** Transferir el conocimiento y la operación a la Defensoría para que sea autónoma. El contratista sale progresivamente.

| Actividad | Responsable |
|---|---|
| Capacitación del equipo interno de TI de la Defensoría (train-the-trainer) | DS |
| Documentación completa: código, modelos, procedimientos, guías de troubleshooting | DS |
| Transferencia de repositorios, modelos, datasets y pipelines | DS |
| Soporte decreciente: 6 meses full → 3 meses parcial (2 días/semana) → 3 meses bajo demanda | DS |
| Entrega de manual de operación y plan de continuidad | DS + Derecho |
| Cierre contractual: verificación de todos los entregables y SLAs | Derecho |

**Entregables de la Fase 4:**
- Equipo interno de la Defensoría capacitado y autónomo
- Documentación completa transferida
- Modelo de gobernanza de IA operado internamente
- Manual de operación y plan de continuidad
- Acta de cierre contractual

**Criterios de salida:**
- Equipo interno opera el sistema sin asistencia del contratista durante 3 meses consecutivos
- Reentrenamiento de modelos realizado por equipo interno
- Auditoría de cierre: todos los SLAs cumplidos

---

### Paso 2: Carta Gantt resumen

```
FASE       M1  M2  M3  M4  M5  M6  M7  M8  M9  M10 M11 M12 ... M36 M37 M38 M39
Fase 0     ██████
Fase 1              ██████████████████
Fase 2                                  ██████████████████
Fase 3                                                      ████████████████████████████████████████
Fase 4                                                                                              ████████████████████████████████████████
```

---

### Paso 3: Presupuesto estimado (a completar con Derecho)

| Fase | Duración | Costo estimado | Principales rubros |
|---|---|---|---|
| Fase 0: Diagnóstico | 3 meses | $XX COP | Personal técnico, servidores de desarrollo |
| Fase 1: Piloto | 6 meses | $XX COP | Desarrollo, infraestructura piloto, capacitación |
| Fase 2: Despliegue | 6 meses | $XX COP | Escalamiento, hardware adicional, capacitación masiva |
| Fase 3: Maduración | 12 meses | $XX COP | Mantenimiento, reentrenamiento, auditorías, soporte |
| Fase 4: Sostenibilidad | 12 meses | $XX COP | Transferencia, soporte decreciente, documentación |
| **TOTAL** | **39 meses** | **$XX COP** | |

> NOTA: Los costos deben ser estimados por el equipo de Derecho con base en precios de mercado de contratación pública colombiana y los rubros del SECOP IA.

---

### Paso 4: Hitos de pago (a definir con Derecho)

| Hito | Fase | % del contrato | Entregable que dispara el pago |
|---|---|---|---|
| Firma del contrato | Fase 0 | 15% | Acta de inicio |
| Aprobación de especificaciones | Fase 0 | 10% | Documento de requisitos aprobado |
| Piloto funcionando | Fase 1 | 25% | Sistema piloto en producción con métricas cumplidas |
| 6 regionales operativas | Fase 2 | 25% | Acta de aceptación de despliegue |
| Cobertura nacional | Fase 3 | 15% | Acta de aceptación de cobertura total |
| Transferencia completada | Fase 4 | 10% | Acta de cierre y transferencia |

---

## Glosario de términos técnicos usados en esta sección

| Término | Explicación |
|---|---|
| **Fine-tuning** | Tomar un modelo de IA que ya sabe español y enseñarle a clasificar peticiones de la Defensoría con ejemplos etiquetados. |
| **Dataset etiquetado** | Conjunto de ejemplos donde un humano ya dijo "esta petición es una Queja sobre salud". El modelo aprende de estos ejemplos. |
| **Drift** | Cuando el rendimiento del modelo empeora con el tiempo porque el mundo cambió (nuevo gobierno, nueva normativa, nuevo lenguaje en las peticiones). |
| **Modo sombra** | El sistema nuevo funciona en paralelo al proceso manual, pero sus resultados no se usan aún. Sirve para comparar y validar sin riesgo. |
| **CI/CD** | Continuous Integration / Continuous Deployment. Práctica de desarrollo donde el código se prueba y despliega automáticamente. |
| **SLA** | Service Level Agreement. Compromiso medible de calidad del servicio (ej: "disponibilidad 99.5%"). |
| **p95** | Percentil 95. El 95% de los casos cumple la métrica. Más realista que el promedio. |
| **RAG** | Retrieval-Augmented Generation. Técnica que hace que la IA busque en documentos reales antes de responder. |
| **API** | Interfaz para que dos sistemas se comuniquen. Define cómo pedir y recibir datos. |

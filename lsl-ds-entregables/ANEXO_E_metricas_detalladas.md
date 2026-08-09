# Anexo E — Métricas detalladas y metodología de umbral asimétrico

> **Referenciado desde:** §12 del borrador principal.

---

## E.1 Definición operativa de cada indicador

| # | Indicador | Definición operativa | Fórmula | Unidad | Dirección deseada |
|---|---|---|---|---|---|
| M1 | Tiempo de clasificación sugerida | Tiempo transcurrido entre la generación del radicado (M1) y la disponibilidad de la sugerencia de clasificación en la bandeja del profesional URAB (M2) | `timestamp_sugerencia_M2 - timestamp_radicado_M1` | Minutos | ↓ Menor es mejor |
| M2 | Precisión de clasificación (accuracy) | Proporción de peticiones donde el tipo asignado por M2 coincide con la etiqueta gold del dataset de validación | `(VP + VN) / Total` (suma de aciertos sobre total de predicciones) | % | ↑ Mayor es mejor |
| M3 | Recall de urgencias / riesgo vital | Proporción de casos de riesgo vital real (gold) que M2 clasificó correctamente como urgentes | `VP_urgentes / (VP_urgentes + FN_urgentes)` | % | ↑ Mayor es mejor (objetivo ≥99%) |
| M4 | Precisión de sugerencias de duplicados | Proporción de sugerencias de duplicado de M4 que realmente son duplicados (confirmado por profesional) | `VP_dup / (VP_dup + FP_dup)` | % | ↑ Mayor es mejor |
| M5 | Recall de duplicados | Proporción de duplicados reales en el conjunto de prueba que M4 detectó correctamente | `VP_dup / (VP_dup + FN_dup)` | % | ↑ Mayor es mejor |
| M6 | Reducción de reprocesos de reparto | Diferencia porcentual en el número de reasignaciones por error o duplicación entre la línea base (F0) y el período de medición | `(Reasig_F0 - Reasig_actual) / Reasig_F0 * 100` | % | ↑ Mayor es mejor |
| M7 | Cumplimiento de tiempos internos | Proporción de peticiones cuya gestión completa se realizó dentro de los plazos establecidos por tipo de caso | `Casos_en_plazo / Total_casos_cerrados * 100` | % | ↑ Mayor es mejor |
| M8 | Tiempo ingreso→asignación | Tiempo desde radicado hasta que el caso aparece en la bandeja del profesional asignado (M3) | `timestamp_asignacion - timestamp_radicado` | Horas | ↓ Menor es mejor |
| M9 | Tiempo ingreso→primera respuesta | Días hábiles desde radicado hasta que se envía la primera respuesta al ciudadano (M6) | `días_hábiles(timestamp_respuesta - timestamp_radicado)` | Días hábiles | ↓ Menor es mejor |
| M10 | Tasa de extracción correcta de entidades | Proporción de campos obligatorios (nombre, CC, pretensión) extraídos correctamente por el NER de M1 sobre un conjunto gold de 200 documentos | `Campos_correctos / Total_campos_obligatorios * 100` | % | ↑ Mayor es mejor |
| M11 | Tasa de borradores M6 aceptados sin corrección mayor | Proporción de borradores generados por M6 que el profesional aprueba sin editar o con ediciones menores (<20% del texto modificado) | `Borradores_aprobados_sin_corrección / Total_borradores_generados * 100` | % | ↑ Mayor es mejor |
| M12 | Disponibilidad del sistema | Porcentaje del tiempo en que el sistema responde a peticiones HTTP con código 2xx/3xx sobre el tiempo total del período | `(Tiempo_total - Tiempo_caída) / Tiempo_total * 100` | % | ↑ Mayor es mejor |
| M13 | Tasa de sincronización IRIS/VisionWeb | Proporción de eventos de sincronización que se completan exitosamente en el primer intento (sin reintentos) | `Eventos_exitosos_primer_intento / Total_eventos * 100` | % | ↑ Mayor es mejor |
| M14 | Tasa de error en OCR (CER) | Proporción de caracteres incorrectamente reconocidos por Tesseract sobre un conjunto gold de 100 documentos escaneados | `(Inserciones + Sustituciones + Eliminaciones) / Total_caracteres_reales * 100` | % | ↓ Menor es mejor |
| M15 | Equal Opportunity por género | Diferencia absoluta en True Positive Rate (recall) entre grupos de género para la clasificación M2 | `|TPR_grupo_A - TPR_grupo_B|` | Puntos porcentuales | ↓ Menor es mejor |
| M16 | Disparate Impact Ratio | Cociente entre el F1 score del grupo con peor rendimiento y el F1 del grupo con mejor rendimiento | `min(F1_grupos) / max(F1_grupos)` | Ratio (0–1) | ↑ Mayor es mejor (>0.80) |
| M17 | Satisfacción del profesional URAB | Puntuación promedio en encuesta trimestral estructurada (escala Likert 1–5, 10 preguntas) | `Suma_puntuaciones / (N_encuestados * 10)` | Escala 1–5 | ↑ Mayor es mejor |

---

## E.2 Plan de medición con herramientas, responsables y dashboards

| Grupo | Indicadores | Herramienta de medición | Fuente de datos | Frecuencia | Responsable | Visualización |
|---|---|---|---|---|---|---|
| Operativas | M1, M8, M9 | Logs del sistema (JSON estructurado) → ELK stack → PostgreSQL | Timestamps en tabla `casos` y `eventos` | Tiempo real | Equipo MLOps | M8 — Dashboard 2 (cuellos de botella) |
| Calidad IA | M2, M3, M4, M5, M6, M10, M11 | MLflow (métricas de evaluación) + Evidently AI (reportes) + PostgreSQL (feedback humano) | Dataset gold (validación) + tabla `feedback` (profesionales) | Semanal automático | Equipo MLOps | M8 — Reporte de calidad + MLflow UI |
| Infraestructura | M12, M13, M14 | Prometheus + Grafana (métricas de sistema) + Healthcheck endpoints | Métricas de Docker, RabbitMQ, PostgreSQL, Elasticsearch | Tiempo real | Equipo de Infraestructura | Dashboard de operaciones (Grafana) |
| Equidad | M15, M16 | Evidently AI (reportes de equidad) | Dataset gold segmentado + predicciones en producción | Trimestral automático | MLOps + Comité de IA | M8 — Dashboard 4 (equidad) |
| Satisfacción | M17 | Formulario integrado en Streamlit (post-cierre de caso) → PostgreSQL | Tabla `encuestas_satisfaccion` | Trimestral | URAB / Defensoría | Reporte manual al Comité de IA |

---

## E.3 Metodología de umbral asimétrico para riesgo vital

### E.3.1 Fundamento

En un sistema de clasificación estándar, los errores de tipo I (falso positivo: decir que algo es urgente cuando no lo es) y tipo II (falso negativo: decir que algo NO es urgente cuando SÍ lo es) se tratan como simétricos. Esto es inadecuado para el contexto de la Defensoría del Pueblo. Un falso negativo en un caso de riesgo vital —una desaparición forzada no detectada, una amenaza de muerte clasificada como rutinaria, un menor en peligro sin alerta— tiene consecuencias catastróficas e irreversibles: daño antijurídico, vulneración de derechos fundamentales y posible pérdida de vidas humanas. Un falso positivo, en cambio, genera un costo operativo manejable: un profesional revisa un caso que no era urgente, invirtiendo entre 5 y 15 minutos adicionales.

El principio rector es: **es preferible generar 100 falsas alarmas que omitir 1 riesgo real.** El sistema se calibra deliberadamente para ser "hipersensible" a indicadores de riesgo vital, aceptando un incremento controlado de falsos positivos como costo de la cobertura casi total de los verdaderos positivos.

### E.3.2 Procedimiento de calibración

1. **Fase 0 — Construcción del conjunto gold de riesgo vital.** Los juristas de la URAB, con supervisión del equipo de Derecho del proyecto, etiquetan un subconjunto de al menos 200 peticiones del dataset de entrenamiento que contengan indicadores reales de riesgo vital (amenazas explícitas, desapariciones forzadas, menores en situación de peligro, violencia basada en género activa, riesgo inminente contra la vida o integridad). Cada caso se etiqueta binariamente: `riesgo_vital = true/false`.

2. **Fase 2 — Calibración del umbral.** Durante el fine-tuning de BETO para M2, se entrena un clasificador binario adicional específico para la clase "riesgo vital". Sobre el conjunto gold, se ajusta el umbral de decisión (threshold) del clasificador para alcanzar una sensibilidad (recall) ≥99%. Esto implica mover el threshold hacia abajo: el modelo requerirá menos "confianza" para marcar un caso como riesgo vital, lo que inevitablemente aumentará los falsos positivos.

3. **Validación del trade-off.** Se mide el costo operativo del incremento de falsos positivos: ¿cuántos casos adicionales por día deberá revisar un profesional? Si el volumen de falsos positivos generados por el umbral asimétrico supera la capacidad de revisión humana (estimada en ~20 revisiones adicionales/día por profesional), se ajusta el threshold al punto de equilibrio más cercano a recall 99% que sea operativamente viable.

### E.3.3 Ejemplo numérico

| Escenario | Threshold | Recall riesgo vital | Falsos positivos/día (estimado) | Costo operativo diario |
|---|---|---|---|---|
| Umbral simétrico (estándar) | 0.50 | 92% | ~5 casos/día | ~25 min de revisión extra |
| Umbral asimétrico (propuesto) | 0.15 | **99.5%** | ~18 casos/día | ~90 min de revisión extra |
| Umbral extremo | 0.05 | 99.9% | ~45 casos/día | ~225 min (inviable para 1 profesional) |

El punto óptimo propuesto es el umbral asimétrico con recall 99.5% y ~18 falsos positivos/día, que representa aproximadamente 90 minutos adicionales de revisión diaria —un costo operativo aceptable frente al beneficio de detectar prácticamente todos los casos de riesgo vital—.

### E.3.4 Monitoreo y ajuste continuo

- **Diario:** se monitorea el recall sobre los casos etiquetados como riesgo vital por los profesionales (feedback humano). Cualquier falso negativo real (caso de riesgo vital que el sistema no marcó) activa una revisión inmediata: análisis de causa raíz, verificación de si el caso estaba en el conjunto gold, y decisión sobre reentrenamiento.
- **Mensual:** se recalcula el trade-off precisión/recall con los datos acumulados. Si el recall cae por debajo de 99%, se reajusta el threshold.
- **Trimestral:** el Comité de IA revisa el informe de umbral asimétrico, que incluye: (i) recall mensual de riesgo vital, (ii) volumen de falsos positivos y su impacto operativo, (iii) número de falsos negativos reales detectados (debería tender a cero), y (iv) recomendación de ajuste si aplica.

# Anexo 12 — Metricas detalladas y metodologia de umbral asimetrico

> Referenciado desde: seccion 12 del cuerpo del documento.

---

## 12.1 Definicion operativa de cada indicador

| Num | Indicador | Formula | Unidad | Direccion |
|---|---|---|---|---|
| M1 | Tiempo clasificacion sugerida (M2) | timestamp_sugerencia_M2 - timestamp_radicado_M1 | Minutos | Menor mejor |
| M2 | Accuracy clasificacion (M2) | (VP + VN) / Total predicciones | Porcentaje | Mayor mejor |
| M3 | Recall urgencias / riesgo vital (M2) | VP_urgentes / (VP_urgentes + FN_urgentes) | Porcentaje | Mayor mejor (objetivo mayor o igual 99%) |
| M4 | Precision sugerencias duplicados (M4) | VP_dup / (VP_dup + FP_dup) | Porcentaje | Mayor mejor |
| M5 | Recall duplicados (M4) | VP_dup / (VP_dup + FN_dup) | Porcentaje | Mayor mejor |
| M6 | Reduccion reprocesos reparto | (Reasig_F0 - Reasig_actual) / Reasig_F0 x 100 | Porcentaje | Mayor mejor |
| M7 | Cumplimiento tiempos internos | Casos_en_plazo / Total_casos_cerrados x 100 | Porcentaje | Mayor mejor |
| M8 | Tiempo ingreso a asignacion (M3) | timestamp_asignacion - timestamp_radicado | Horas | Menor mejor |
| M9 | Tiempo ingreso a primera respuesta | dias_habiles(timestamp_respuesta - timestamp_radicado) | Dias habiles | Menor mejor |
| M10 | Extraccion correcta entidades (M1) | Campos_correctos / Total_campos_obligatorios x 100 | Porcentaje | Mayor mejor |
| M11 | Borradores M6 sin correccion mayor | Borradores_aprobados / Total_borradores x 100 | Porcentaje | Mayor mejor |
| M12 | Disponibilidad del sistema | (Tiempo_total - Tiempo_caida) / Tiempo_total x 100 | Porcentaje | Mayor mejor |
| M13 | Sincronizacion IRIS/VisionWeb (M7) | Eventos_exito_primer_intento / Total_eventos x 100 | Porcentaje | Mayor mejor |
| M14 | Tasa error OCR (M1) | (Inserciones + Sustituciones + Eliminaciones) / Total_caracteres x 100 | Porcentaje | Menor mejor |
| M15 | Equal Opportunity por genero (M2) | ValorAbsoluto(TPR_grupo_A - TPR_grupo_B) | Puntos porcentuales | Menor mejor |
| M16 | Disparate Impact Ratio | min(F1_grupos) / max(F1_grupos) | Ratio (0-1) | Mayor mejor (mayor a 0.80) |
| M17 | Satisfaccion profesional URAB | Suma_puntuaciones / (N_encuestados x 10) | Escala 1-5 | Mayor mejor |

---

## 12.2 Plan de medicion

| Grupo | Indicadores | Herramienta | Fuente | Frecuencia | Responsable | Visualizacion |
|---|---|---|---|---|---|---|
| Operativas | M1, M8, M9 | Logs JSON + PostgreSQL | Tablas casos y eventos | Tiempo real | MLOps | M8 Dashboard 2 |
| Calidad IA | M2-M5, M10, M11 | MLflow + Evidently AI | Dataset gold + tabla feedback | Semanal | MLOps | M8 Reporte calidad |
| Infraestructura | M12-M14 | Prometheus + Grafana cloud | Metricas contenedores, APIs, OCR | Tiempo real | Infraestructura | Dashboard operaciones |
| Equidad | M15, M16 | Evidently AI | Dataset gold segmentado + predicciones prod | Trimestral | MLOps + Comite IA | M8 Dashboard 4 |
| Satisfaccion | M17 | Formulario integrado | Tabla encuestas_satisfaccion | Trimestral | URAB | Reporte al Comite IA |

---

## 12.3 Metodologia de umbral asimetrico para riesgo vital

### Fundamento

En el contexto de la Defensoria del Pueblo, un falso negativo en un caso de riesgo vital (desaparicion forzada no detectada, amenaza de muerte clasificada como rutinaria, menor en peligro sin alerta) tiene consecuencias catastroficas e irreversibles: dano antijuridico, vulneracion de derechos fundamentales y posible perdida de vidas humanas. Un falso positivo, en cambio, genera un costo operativo manejable: un profesional revisa un caso que no era urgente, invirtiendo entre 5 y 15 minutos adicionales.

El principio rector es: **es preferible generar 100 falsas alarmas que omitir 1 riesgo real.** El sistema se calibra deliberadamente para ser hipersensible a indicadores de riesgo vital, aceptando un incremento controlado de falsos positivos como costo de la cobertura casi total de los verdaderos positivos.

### Procedimiento de calibracion

1. **Fase 0 — Construccion del conjunto gold.** Los juristas de la URAB etiquetan al menos 200 peticiones con indicadores reales de riesgo vital (amenazas explicitas, desapariciones forzadas, menores en peligro, VBG activa, riesgo inminente contra la vida o integridad). Etiqueta binaria: `riesgo_vital = true/false`.

2. **Fase 2 — Calibracion del umbral.** Durante el fine-tuning de BETO para M2, se entrena un clasificador binario adicional para la clase riesgo vital. Sobre el conjunto gold, se ajusta el umbral de decision (threshold) para alcanzar una sensibilidad (recall) mayor o igual a 99%. Esto implica mover el threshold hacia abajo: el modelo requerira menos confianza para marcar un caso como riesgo vital, lo que aumentara los falsos positivos.

3. **Validacion del trade-off.** Se mide el costo operativo del incremento de falsos positivos. Si el volumen supera la capacidad de revision humana (estimada en aproximadamente 20 revisiones adicionales por dia por profesional), se ajusta al punto de equilibrio mas cercano a recall 99% que sea operativamente viable.

### Ejemplo numerico

| Escenario | Threshold | Recall riesgo vital | Falsos positivos/dia | Costo operativo diario |
|---|---|---|---|---|
| Simetrico (estandar) | 0.50 | 92% | ~5 casos | ~25 min extra |
| **Asimetrico (propuesto)** | **0.15** | **99.5%** | **~18 casos** | **~90 min extra** |
| Extremo | 0.05 | 99.9% | ~45 casos | ~225 min (inviable) |

El punto optimo propuesto es el umbral asimetrico con recall 99.5% y aproximadamente 18 falsos positivos/dia (90 minutos adicionales de revision), un costo operativo aceptable frente al beneficio de detectar practicamente todos los casos de riesgo vital.

### Monitoreo y ajuste continuo

- **Diario:** monitoreo de recall sobre casos etiquetados por profesionales (feedback humano). Cualquier falso negativo real activa revision inmediata: analisis de causa raiz y decision sobre reentrenamiento.
- **Mensual:** recalculo del trade-off precision/recall con datos acumulados. Si recall cae por debajo de 99%, reajuste del threshold.
- **Trimestral:** el Comite de IA revisa el informe de umbral asimetrico con: (i) recall mensual, (ii) volumen de falsos positivos, (iii) falsos negativos reales (debe tender a cero), (iv) recomendacion de ajuste.

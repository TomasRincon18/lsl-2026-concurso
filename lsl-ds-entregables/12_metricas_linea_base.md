# 12. Métricas y línea base del piloto

## ¿Qué es esta sección?

Defines indicadores cuantitativos para medir el éxito del sistema. Para cada métrica debes establecer:

1. **Línea base (AS-IS):** el valor actual, sin IA. Se estima a partir de lo descrito en el caso y supuestos razonables.
2. **Meta del piloto (TO-BE):** el valor que esperas alcanzar con el sistema funcionando.
3. **Módulo responsable:** qué módulo(s) impactan esa métrica.
4. **Forma de medición:** cómo y con qué frecuencia se medirá.

**Extensión sugerida:** 1-2 páginas.

---

## ¿Qué necesitas del equipo de Derecho?

- **Validación de que las metas no violan plazos legales.** El CPACA (Ley 1437/2011) establece términos máximos de respuesta a peticiones. Tus metas deben cumplirlos.
- **Confirmación de los tiempos legales:** ¿cuántos días hábiles máximo para responder cada tipo de petición?
- **Cualquier otra métrica que Derecho considere obligatoria** desde el punto de vista jurídico o de gobernanza.

---

## Paso a paso para redactar esta sección

### Paso 1: Métricas operativas (eficiencia del proceso)

Estas métricas miden qué tan rápido y eficiente es el proceso comparado con el manual.

| # | Métrica | Descripción | Línea base (AS-IS) | Meta piloto | Módulo |
|---|---|---|---|---|---|
| M1 | **Tiempo de procesamiento por caso** | Minutos desde que la petición llega hasta que está lista para asignación (recepción + clasificación) | ~15 minutos/caso (manual). Un funcionario clasifica ~30 casos/día. | <30 segundos/caso (automático) | M1, M2 |
| M2 | **Tiempo ingreso → asignación** | Horas desde que se recibe la petición hasta que se asigna a un profesional | ~2 días hábiles (basado en la saturación operativa de ~300 casos/día descrita en el caso) | <4 horas para el 95% de los casos | M2, M3 |
| M3 | **Tiempo ingreso → primera respuesta** | Días hábiles desde la recepción hasta que el ciudadano recibe una primera respuesta | ~15-20 días hábiles (estimado por represamiento) | <10 días hábiles para el 90% de los casos | M2, M3, M6 |
| M4 | **Capacidad de procesamiento diario** | Número máximo de peticiones que el sistema puede procesar en un día | ~30 por funcionario. Con 10 funcionarios = ~300/día (punto de saturación) | Sin límite teórico relevante para el piloto. Cuello de botella pasa a ser la gestión humana, no la clasificación | M1, M2 |
| M5 | **Tasa de automatización de clasificación** | Porcentaje de peticiones clasificadas sin intervención humana | 0% (todo es manual) | >90% (solo escapan casos que el modelo clasifica con baja confianza) | M2 |

**Nota sobre la línea base:** Los datos AS-IS se estiman a partir de lo que el caso describe. El caso menciona ~300 peticiones/día, saturación operativa, duplicidad y represamiento. De ahí derivamos estas estimaciones. Si el equipo de Derecho tiene datos más precisos de la Defensoría, deben ajustarse.

---

### Paso 2: Métricas de calidad (precisión de la IA)

Estas métricas miden qué tan bien funciona la inteligencia artificial, independientemente de la velocidad.

| # | Métrica | Descripción | Línea base (AS-IS) | Meta piloto | Módulo |
|---|---|---|---|---|---|
| M6 | **Precisión de clasificación (Accuracy)** | Porcentaje de peticiones donde el tipo asignado (Asesoría/Queja/Mediación/Conciliación) es correcto | ~80% (humano). Se asume que un profesional entrenado acierta ~8 de cada 10, pero con fatiga y volumen el error aumenta | >85% (modelo). Consistente, sin fatiga | M2 |
| M7 | **F1 score por categoría** | Media armónica entre precisión (de lo que dijo "Queja", ¿cuántas realmente lo eran?) y recall (de todas las quejas reales, ¿cuántas detectó?) | No medido actualmente. Se estima similar al accuracy (~0.80) | >0.80 para cada una de las 4 categorías. Ninguna categoría por debajo de 0.75 | M2 |
| M8 | **Tasa de falsos negativos en urgencia** | Porcentaje de casos urgentes que el sistema NO detectó como urgentes (el error más grave) | Desconocido. Sin sistema automático, la urgencia la determina el profesional al leer. Estimado ~5-10% de omisiones por fatiga/volumen | <1%. Este es el error que MENOS se puede tolerar | M2 |
| M9 | **Tasa de extracción correcta de entidades** | Porcentaje de campos (nombre, CC, dirección, pretensión) extraídos correctamente por el NER | ~70-80% (digitación manual con errores de tipeo, campos omitidos) | >90% para campos obligatorios | M1 |
| M10 | **Precisión en detección de duplicados** | De cada 100 casos que el sistema marca como duplicados, ¿cuántos realmente lo son? | ~30% (muestreo manual aleatorio. Sin sistema, la mayoría de duplicados pasan desapercibidos) | >90% (precision). Que el sistema no moleste al profesional con falsos duplicados | M4 |
| M11 | **Recall en detección de duplicados** | De cada 100 duplicados reales que existen, ¿cuántos detecta el sistema? | <30% (manual, aleatorio) | >85% (recall). Que el sistema detecte la gran mayoría | M4 |
| M12 | **Tasa de aceptación de borradores M6** | Porcentaje de borradores generados por el LLM que el profesional aprueba sin edición mayor | No aplica (no existe el sistema) | >70% (el borrador es útil y requiere solo ajustes menores) | M6 |

**Sobre el F1 score:** Es una métrica que combina dos cosas en un solo número (de 0 a 1). Imagina que el modelo busca "Quejas" entre 100 peticiones:
- **Precision:** De 50 que dijo "Queja", ¿40 realmente lo eran? Precision = 40/50 = 0.80. Mide que no "invente" quejas donde no las hay.
- **Recall:** Había 60 quejas reales. ¿Cuántas encontró? Si encontró 40, recall = 40/60 = 0.67. Mide que no se le escapen quejas reales.
- **F1:** Combina ambas. F1 = 2 * (0.80 * 0.67) / (0.80 + 0.67) = 0.73. Un modelo perfecto tiene F1 = 1.0.

---

### Paso 3: Métricas de sistema (infraestructura)

| # | Métrica | Descripción | Meta piloto |
|---|---|---|---|
| M13 | **Disponibilidad del sistema** | Porcentaje del tiempo que el sistema está operativo y responde | >99.5% (máximo ~43 horas de caída al año) |
| M14 | **Tiempo de respuesta de la API** | Latencia desde que el frontend hace una petición hasta que recibe respuesta | <500ms para el 95% de las peticiones (p95) |
| M15 | **Tasa de sincronización IRIS/VisionWeb** | Porcentaje de eventos de sincronización exitosos (sin reintentos) | >99.5% |
| M16 | **Tasa de error en OCR** | Character Error Rate: porcentaje de caracteres mal reconocidos en documentos escaneados | <5% en documentos limpios, <10% en documentos con baja calidad |

---

### Paso 4: Métricas de equidad

| # | Métrica | Descripción | Meta piloto |
|---|---|---|---|
| M17 | **Equal Opportunity por género** | Diferencia en True Positive Rate entre grupos de género | <5% de diferencia |
| M18 | **Equal Opportunity por regional** | Diferencia en TPR entre regionales | <5% de diferencia entre la mejor y la peor regional |
| M19 | **Disparate Impact Ratio** | Ratio entre el grupo con peor F1 y el grupo con mejor F1 | >0.80 (no menos del 80% del rendimiento del mejor grupo) |

---

### Paso 5: Métricas de satisfacción

| # | Métrica | Descripción | Meta piloto |
|---|---|---|---|
| M20 | **Satisfacción del profesional URAB** | Encuesta trimestral a profesionales que usan el sistema | >80% de satisfacción |
| M21 | **Satisfacción del ciudadano** | Encuesta opcional al cerrar el caso (breve: 1-3 preguntas) | >70% de satisfacción |
| M22 | **Tasa de quejas sobre el sistema** | Porcentaje de ciudadanos que presentan una queja específica sobre el uso de IA en su caso | <2% |

---

### Paso 6: Mecanismo de medición

Para cada grupo de métricas, describe cómo se medirán:

| Grupo | Herramienta de medición | Frecuencia | Responsable | Dashboard |
|---|---|---|---|---|
| Operativas (M1-M5) | Logs del sistema + PostgreSQL queries | Tiempo real | MLOps | M8 - Dashboard 2 |
| Calidad IA (M6-M12) | MLflow + Evidently AI | Semanal (automático) | MLOps | M8 - Reporte específico |
| Sistema (M13-M16) | Prometheus + Grafana (monitoreo de infraestructura) | Tiempo real | Infraestructura | Dashboard de operaciones |
| Equidad (M17-M19) | Evidently AI | Trimestral (automático) | MLOps + Comité IA | M8 - Dashboard 4 |
| Satisfacción (M20-M22) | Formulario Google Forms / integrado en el sistema | Trimestral | URAB / Defensoría | Reporte manual al Comité IA |

---

### Paso 7: Estructura de la sección en el documento

```
12. Métricas y línea base del piloto

12.1 Metodología de medición
     [Explicar que las métricas AS-IS se estiman a partir del caso y
      que las metas TO-BE son conservadoras pero ambiciosas]

12.2 Métricas operativas (eficiencia)
     [Insertar tabla del Paso 1]

12.3 Métricas de calidad de IA
     [Insertar tabla del Paso 2]

12.4 Métricas de infraestructura
     [Insertar tabla del Paso 3]

12.5 Métricas de equidad
     [Insertar tabla del Paso 4]

12.6 Métricas de satisfacción
     [Insertar tabla del Paso 5]

12.7 Mecanismo de medición y reporte
     [Insertar tabla del Paso 6]
```

---

## Glosario de términos técnicos usados en esta sección

| Término | Explicación |
|---|---|
| **Línea base (AS-IS)** | El valor actual de una métrica, antes de implementar la mejora. Sirve para saber si la solución realmente mejoró algo. |
| **Accuracy** | Porcentaje de aciertos del modelo. Si clasificó 100 peticiones y acertó en 85, accuracy = 85%. |
| **F1 Score** | Métrica que combina precision y recall en un solo número de 0 a 1. Útil cuando hay desbalance entre categorías (muchas más Asesorías que Quejas, por ejemplo). |
| **Precision** | Del total de casos que el modelo clasificó como "X", qué porcentaje realmente eran "X". Mide que el modelo no "invente" clasificaciones. |
| **Recall** | Del total de casos que realmente son "X", qué porcentaje detectó el modelo. Mide que no se le escapen casos. |
| **Falso Negativo** | El modelo dice "NO es urgente" pero SÍ lo es. El error más peligroso. |
| **True Positive Rate (TPR)** | Sinónimo de Recall. Porcentaje de casos positivos reales que el modelo detectó correctamente. |
| **Disparate Impact Ratio** | Medida de equidad: el rendimiento del peor grupo dividido por el del mejor grupo. Debe ser >0.80. |
| **Equal Opportunity** | Métrica de equidad: el TPR debe ser similar entre grupos. |
| **p95 (Percentil 95)** | El 95% de las peticiones se procesan en menos de X tiempo. Más realista que el promedio. |
| **Latencia** | Tiempo que tarda el sistema en responder desde que recibe una petición. |
| **CER (Character Error Rate)** | Tasa de error del OCR: porcentaje de caracteres mal reconocidos. |
| **SLA** | Service Level Agreement. Compromiso formal de nivel de servicio. |
| **NER** | Named Entity Recognition. Técnica que extrae automáticamente nombres, cédulas, etc. de un texto. |

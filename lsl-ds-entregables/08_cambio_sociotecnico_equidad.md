# 8. Análisis de cambio sociotécnico, enfoque diferencial y pruebas de equidad

## ¿Qué es esta sección?

Esta sección tiene 3 partes. Dos las escribe el equipo de Derecho y una la escribes tú (Ciencia de Datos).

| Sub-sección | Quién la escribe | Contenido |
|---|---|---|
| **8.1 Cambio sociotécnico** | Derecho | Cómo cambia el trabajo de los funcionarios al introducir IA |
| **8.2 Enfoque diferencial** | Derecho | Cómo se protege a poblaciones vulnerables (género, discapacidad, juventud, etc.) |
| **8.3 Pruebas de equidad** | **DS (tú)** | Cómo se garantiza que la IA no discrimine a ningún grupo |

**Extensión sugerida:** ~3 páginas en total. Tu parte (8.3) ocupa ~1 página.

---

## ¿Qué necesitas del equipo de Derecho?

- **Su borrador de 8.1 (Cambio sociotécnico):** para que tus pruebas de equidad estén alineadas con los impactos que ellos identifican.
- **Su borrador de 8.2 (Enfoque diferencial):** para saber qué grupos vulnerables priorizan y qué criterios legales usan.
- **D3 (Sujetos de especial protección):** para cruzar con las métricas de equidad.
- **D1 y D2:** para saber sobre qué categorías y sub-temas medir equidad.

---

## Paso a paso para redactar tu parte (8.3 - Pruebas de equidad)

### Paso 1: Explica por qué importa la equidad algorítmica

> "Los sistemas de inteligencia artificial, si no se diseñan y monitorean cuidadosamente, pueden reproducir e incluso amplificar sesgos presentes en los datos de entrenamiento o en la sociedad. En el contexto de la Defensoría del Pueblo —cuya misión constitucional es proteger los derechos humanos de toda la población, con énfasis en los grupos más vulnerables— un sesgo algorítmico no es solo un error técnico: es una vulneración de derechos fundamentales. Por ello, la solución incorpora desde su diseño un marco de pruebas de equidad algorítmica con monitoreo continuo."

### Paso 2: Define las métricas de equidad que usarás

| Métrica | ¿Qué mide? | Ejemplo de problema que detecta |
|---|---|---|
| **Equal Opportunity** (Igualdad de Oportunidad) | ¿El modelo clasifica con la misma precisión a todos los grupos? | Si el modelo acierta el 90% de las quejas de hombres pero solo el 70% de las de mujeres, hay un sesgo. |
| **Demographic Parity** (Paridad Demográfica) | ¿El modelo asigna cada categoría en proporciones similares entre grupos? | Si al 40% de los hombres se les clasifica como "Queja" pero solo al 15% de las mujeres, puede haber un sesgo (si la realidad no justifica esa diferencia). |
| **Disparate Impact Ratio** (Ratio de Impacto Dispar) | ¿Hay diferencias grandes en resultados entre grupos? | Si el ratio entre el grupo con mejor tasa de clasificación correcta y el peor es menor a 0.8, se considera impacto desproporcionado. |
| **False Negative Rate por grupo** (Tasa de Falsos Negativos) | ¿El modelo deja pasar casos urgentes sin marcar más en unos grupos que en otros? | Si al 5% de los desplazados no se les detecta urgencia pero al 0.5% del resto sí, hay un riesgo grave. |

**Glosario rápido de métricas:**
- **Verdadero Positivo:** El modelo dijo "Queja" y realmente era una queja. Acertó.
- **Falso Positivo:** El modelo dijo "Queja" pero no lo era. Se equivocó por exceso.
- **Falso Negativo:** El modelo dijo "NO es queja" pero sí lo era. Se equivocó por omisión (el error más peligroso en este contexto).
- **Equal Opportunity:** El porcentaje de verdaderos positivos debe ser similar entre grupos. Mide que el modelo no "favorezca" a unos sobre otros.

### Paso 3: Describe el plan de evaluación

> **¿Cuándo se mide la equidad?**
>
> 1. **Antes del despliegue:** sobre el dataset de entrenamiento y validación, segmentando por las variables disponibles.
> 2. **Trimestralmente en producción:** usando Evidently AI para generar reportes automáticos de equidad.
> 3. **Ante cualquier cambio:** si se reentrena el modelo o se modifican las reglas de clasificación, se repite la evaluación completa.

> **¿Sobre qué variables se segmenta?**
>
> - Género (si el dato está disponible en la petición, respetando la autodeterminación)
> - Regional / departamento
> - Grupo de especial protección (cuando sea detectable por el texto: NNA, adulto mayor, desplazado, etc.)
> - Canal de ingreso (web, email, físico, campo)

> **¿Cómo se segmenta si el dato de género no siempre está disponible?**
>
> Se usa solo cuando el ciudadano lo proporciona voluntariamente en el formulario. Nunca se infiere. Si la muestra de un grupo es muy pequeña (menos de 30 casos), no se reporta esa segmentación para evitar conclusiones no estadísticamente significativas.

### Paso 4: Describe qué se hace si se detecta sesgo

| Nivel de disparidad | Acción |
|---|---|
| **<3% de diferencia entre grupos** | Aceptable. Solo monitoreo continuo. |
| **3-5% de diferencia** | Alerta amarilla. Revisión por el equipo técnico. Análisis de causas. |
| **5-10% de diferencia** | Alerta naranja. Se escala al Comité de IA. Se inicia protocolo de mitigación. |
| **>10% de diferencia** | Alerta roja. Se suspende el uso del modelo para decisiones que afecten a ese grupo específico. Investigación inmediata. |

**Estrategias de mitigación (si se detecta sesgo):**

1. **Rebalanceo del dataset de entrenamiento:** añadir más ejemplos del grupo subrepresentado. Si el modelo falla con peticiones de población desplazada, buscar y etiquetar más ejemplos de ese grupo.

2. **Threshold tuning por grupo:** ajustar el umbral de decisión del modelo para igualar las tasas de error entre grupos. Ej: si el modelo es más conservador con cierto grupo, bajar ligeramente el umbral de confianza requerido para ese grupo.

3. **Adversarial debiasing:** técnica avanzada donde se entrena simultáneamente al modelo para que clasifique bien PERO sin poder distinguir a qué grupo pertenece la persona. Como enseñarle a un evaluador a calificar exámenes sin saber el nombre del estudiante.

4. **Revisión humana obligatoria:** para los grupos donde se detectó sesgo, toda clasificación automática pasa por revisión humana adicional hasta que se resuelva el sesgo.

### Paso 5: Tabla de monitoreo (ejemplo para incluir en el documento)

| Variable de segmentación | Métrica | Frecuencia | Responsable | Herramienta |
|---|---|---|---|---|
| Género | Equal Opportunity, Demographic Parity | Trimestral | Equipo MLOps | Evidently AI |
| Regional | Accuracy por departamento | Trimestral | Equipo MLOps | Evidently AI |
| Grupo de especial protección | False Negative Rate | Mensual | Comité de IA | Evidently AI + reporte manual |
| Canal de ingreso | Accuracy por canal | Trimestral | Equipo MLOps | Evidently AI |
| Sub-tema | F1 score por sub-tema | Trimestral | Equipo MLOps | Evidently AI |

---

## Glosario de términos técnicos usados en esta sección

| Término | Explicación |
|---|---|
| **Sesgo algorítmico** | Cuando un modelo de IA comete errores de forma sistemática contra un grupo específico (mujeres, desplazados, ciertas regiones). No es intencional: es un patrón en los datos de entrenamiento que el modelo aprende y reproduce. |
| **Equidad algorítmica (Fairness)** | Conjunto de métricas y prácticas para garantizar que la IA no discrimine. No es que el modelo sea perfecto, sino que sus errores se distribuyan de forma pareja entre grupos. |
| **Equal Opportunity** | "Igualdad de Oportunidad". Mide que la tasa de aciertos positivos sea similar entre grupos. |
| **Demographic Parity** | "Paridad Demográfica". Mide que las predicciones se distribuyan en proporciones similares entre grupos. |
| **Disparate Impact Ratio** | Ratio que compara el resultado del grupo menos favorecido con el más favorecido. Menos de 0.8 se considera impacto desproporcionado. |
| **False Negative (Falso Negativo)** | El error más grave en este contexto: el modelo dice que NO hay problema cuando SÍ lo hay. Ej: clasificar una amenaza de muerte como "consulta rutinaria". |
| **Threshold** | Umbral. El punto de corte que decide la clasificación. Si el modelo tiene 60% de confianza en que es "Queja", ¿lo clasifica como Queja o no? Depende del threshold. |
| **Adversarial debiasing** | Técnica de entrenamiento donde se obliga al modelo a ignorar la información de grupo (género, origen) mientras aprende a clasificar. |
| **Dataset** | Conjunto de datos etiquetados usados para entrenar o evaluar un modelo. |
| **k-anonymity** | Técnica de anonimización: agrupar datos para que nadie pueda ser identificado individualmente. |
